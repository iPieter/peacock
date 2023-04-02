#!/usr/bin/env python
from ast import arguments
import sys, argparse, logging
import time
import pystache
import json
import os
import http.server
import socketserver
import functools
import pathlib
import shutil
import datetime
import sass
import pandoc
from feedgen.feed import FeedGenerator
from watchdog.observers import Observer
from filesystem_event_handler import FilesystemEventHandler
import re
from pybtex import database
from pybtex.style.names.plain import NameStyle

plain = NameStyle().format

PORT = 8000


def find_index_posts(path, drafts=False):
    tree = list(os.walk(os.path.join(path, "posts")))

    blog_posts = []

    for node, folders, files in tree:
        if "config.json" in files:
            with open(os.path.join(node, "config.json")) as f:
                post_data = json.load(f)
                if drafts or not "draft" in post_data or not post_data["draft"]:
                    post_data["path"] = node
                    post_data["files"] = files
                    # blog posts have a separate url scheme
                    if "blog" in post_data and post_data["blog"]:
                        year = datetime.datetime.strptime(post_data["date"], "%Y-%m-%d").strftime("%Y")
                        post_data["url"] = "blog/" + year + "/" + post_data["post_title"].lower().replace(" ", "-").replace("?", "").replace("(", "").replace(")", "")
                    else:
                        post_data["url"] = post_data["post_title"].lower().replace(" ", "-").replace("(", "").replace("?", "").replace(")", "")
                            
                    logging.debug("Added post: {}".format(post_data["post_title"]))

                    # reset unused fields
                    if "pdf" not in post_data:
                        post_data["pdf"] = False
                    if "bibtex" not in post_data:
                        post_data["bibtex"] = False
                    if "code" not in post_data:
                        post_data["code"] = False
                    if "resource" not in post_data:
                        post_data["resource"] = False
                    if "absoluteresource" not in post_data:
                        post_data["absoluteresource"] = False
                    if "video" not in post_data:
                        post_data["video"] = False

                    bib_files = []
                    for file in files:
                        match = re.search(r".*\.bib", file)
                        if match:
                            file = os.path.join(node, match.group())
                            bib_data = database.parse_file(file)
                            
                            with open(file) as fp:
                                biblio = fp.read()

                            if len(bib_data.entries) > 1:
                                logging.warn(f"Multiple bib entries in {file}, this is not properly supported.")

                            for item in bib_data.entries:
                                bib_files.append(
                                    {
                                        "title": bib_data.entries[item]
                                        .fields["title"]
                                        .replace("{", "")
                                        .replace("}", ""),
                                        "venue": bib_data.entries[item].fields["venue"]
                                        if "venue" in bib_data.entries[item].fields
                                        else bib_data.entries[item].fields[
                                            "archivePrefix"
                                        ]
                                        if "archivePrefix"
                                        in bib_data.entries[item].fields
                                        else bib_data.entries[item].fields["booktitle"]
                                        if "booktitle" in bib_data.entries[item].fields
                                        else bib_data.entries[item].fields["journal"]
                                        if "journal" in bib_data.entries[item].fields
                                        else None,
                                        "authors": ", ".join(
                                            [
                                                plain(p).format().render_as("text")
                                                for p in bib_data.entries[item].persons[
                                                    "author"
                                                ]
                                            ]
                                        ),
                                        "key": item,
                                        "year": bib_data.entries[item].fields["year"],
                                        "url": bib_data.entries[item].fields["url"],
                                        "bibtex": biblio,
                                    }
                                )

                    print(bib_files)
                    post_data["papers"] = bib_files
                    blog_posts.append(post_data)
                post_data = {}

    return sorted(blog_posts, key=lambda post: post["date"], reverse=True)


def serve_build(path):
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=path)

    with socketserver.TCPServer(("", PORT), Handler, bind_and_activate=False) as httpd:
        logging.info(
            "Serving build at http://127.0.0.1:{}, stop with CRL+C.".format(PORT)
        )
        httpd.allow_reuse_address = True
        httpd.server_bind()
        httpd.server_activate()
        httpd.serve_forever()


def parse_file(template_file, config_data) -> str:
    with open(os.path.join(template_file)) as f:

        rendered = pystache.render(f.read(), config_data, escape=lambda u: u)
        return rendered


def build_file(template_file, destination_file, config_data):
    logging.info("Exporting {} to {}".format(template_file, destination_file))
    rendered = parse_file(template_file, config_data)
    with open(os.path.join(destination_file), mode="w") as fout:
        fout.write(rendered)


def build_post(path, post, destination_file, config_data):

    post_config = config_data
    post_config.update(post)

    if "index.md" in post["files"]:
        logging.debug("Rendering markdown file for this post.")
        with open(os.path.join(post["path"], "index.md"), mode="r") as f:
            doc = pandoc.Document()
            doc.add_argument("katex")
            doc.add_argument("highlight-style=pygments")
            doc.gfm = f.read().encode("utf-8")
            post_config["text"] = doc.html.decode()
            post_config["html"] = ""
    elif "index.html" in post["files"]:
        logging.debug("Using html file for this post.")
        with open(os.path.join(post["path"], "index.html"), mode="r") as f:
            post_config["html"] = f.read()
            post_config["text"] = ""

    rendered = parse_file(os.path.join(path, "_post.html"), config_data)

    with open(os.path.join(destination_file), mode="w") as fout:
        fout.write(rendered)


def process_news(data):
    today = datetime.datetime.now()
    d = datetime.timedelta(days=180)
    for item in data["news"]:
        item["date"] = datetime.datetime.strptime(item["date"], "%d/%m/%Y").strftime(
            "%B %d, %Y"
        )
    data["news_recent"] = [
        item
        for item in data["news"]
        if datetime.datetime.strptime(item["date"], "%B %d, %Y") > today - d
    ]

    data["talks"] = [
        item
        for item in data["news"]
        if item["type"] == "talk"
    ]

    data["press"] = [
        item
        for item in data["news"]
        if item["type"] == "press"
    ]

def generate_feeds(config_data, output_path, drafts=False):
    fg = FeedGenerator()
    fg.id("1234")
    fg.title(config_data["RSS_title"])
    fg.author(
        {
            "name": config_data["RSS_author_name"],
            "email": config_data["RSS_author_email"],
        }
    )
    fg.link(href=config_data["RSS_link"], rel="alternate")
    fg.logo(config_data["RSS_logo"])
    fg.description(config_data["RSS_subtitle"])
    fg.link(href=config_data["RSS_link"] + "/test.atom", rel="self")
    fg.language(config_data["RSS_language"])

    for post in config_data["featured_posts"]:
        fe = fg.add_entry()
        fe.id(config_data["RSS_link"] + post["url"] + "/")
        fe.title(post["post_title"])
        fe.summary(post["abstract"])
        fe.published(
            datetime.datetime.strptime(post["date"], "%Y-%m-%d").isoformat() + "+00:00"
        )
        fe.link(href=config_data["RSS_link"] + post["url"] + "/")

    fg.atom_file(os.path.join(output_path, "atom.xml"))
    fg.rss_file(os.path.join(output_path, "rss.xml"))


def build_site(config_data, path, output_path, drafts=False):
    logging.info("Exporting site to folder {}/".format(output_path))

    config_data["PHEASANT_VERSION"] = "0.5"
    config_data["last_updated"] = datetime.datetime.now().strftime("%B %d, %Y")

    # First render the nav bar and footer components
    config_data["navbar"] = parse_file(os.path.join(path, "_navbar.html"), config_data)
    config_data["footer"] = parse_file(os.path.join(path, "_footer.html"), config_data)

    posts = find_index_posts(path, drafts)

    # add the blog posts
    config_data["featured_posts"] = list(filter(lambda post: post["featured"], posts))
    config_data["project_posts"] = list(filter(lambda post: post["project"], posts))
    config_data["blog_posts"] = list(filter(lambda post: "blog" in post and post["blog"], posts))

    for page in posts:
        page["date_formatted"] = datetime.datetime.strptime(
            page["date"], "%Y-%m-%d"
        ).strftime("%B %d, %Y")

    for page in config_data["static_pages"]:
        build_file(
            os.path.join(path, page["url"]),
            os.path.join(output_path, page["url"]),
            config_data,
        )

    # seperately run build_file for 404 page, we do not want to list it
    build_file(
            os.path.join(path, "404.html"),
            os.path.join(output_path, "404.html"),
            config_data,
        )
    
    for page in posts:
        # os.mkdir(os.path.join(output_path, page["url"]))
        logging.debug(
            "Copying resources to {}".format(os.path.join(output_path, page["url"]))
        )
        shutil.copytree(
            os.path.join(page["path"], "resources"),
            os.path.join(output_path, page["url"]),
        )
        build_post(
            path,
            page,
            os.path.join(output_path, page["url"], "index.html"),
            config_data,
        )

    logging.info("Copying resources to folder {}/resources".format(output_path))
    shutil.copytree(
        os.path.join(path, "resources"), os.path.join(output_path, "resources")
    )

    logging.info("Copying js to folder {}/js".format(output_path))
    shutil.copytree(os.path.join(path, "js"), os.path.join(output_path, "js"))

    logging.info("Copying css to folder {}/css".format(output_path))
    shutil.copytree(os.path.join(path, "css"), os.path.join(output_path, "css"))

    logging.info("Copying webfonts to folder {}/webfonts".format(output_path))
    shutil.copytree(
        os.path.join(path, "webfonts"), os.path.join(output_path, "webfonts")
    )

    logging.info("Building additional scss to folder {}/css".format(output_path))

    sass.compile(
        dirname=(os.path.join(path, "scss"), os.path.join(output_path, "css")),
        output_style="compressed",
    )

    logging.debug("Generation atom and rss files.")
    generate_feeds(config_data, output_path)

    # print(scss_parser.load())


def main(args, loglevel):
    logging.basicConfig(format="| %(levelname)s: %(message)s", level=loglevel)
    logging.debug("Passed path: %s" % args.path)

    try:
        logging.debug("Reading file config.json.")
        with open(os.path.join(args.path, "config.json")) as f:
            data = json.load(f)

        logging.debug("Reading file news.json.")
        with open(os.path.join(args.path, "news.json")) as f:
            data["news"] = json.load(f)

            process_news(data)

            logging.debug("Correctly read in all data, building the site")

            output_path = os.path.join(args.path, "build")

            if args.base:
                data["base"] = args.base[0]

            if args.clean:
                logging.info("Cleaning flag present. Removing build folder.")
                try:
                    shutil.rmtree(
                        output_path,
                    )
                except FileNotFoundError as e:
                    logging.warn("Some error during build removal.")
                    print(e)
                finally:
                    os.mkdir(output_path)

            build_site(data, args.path, output_path, drafts=args.draft)

        return output_path

    except FileNotFoundError as e:
        logging.error(
            "File config.json or news.json not found or not readable. Check if it exists. Stacktrace:"
        )
        print(e)
    except json.decoder.JSONDecodeError as e:
        logging.error(
            "File config.json or news.json was unreadable by the JSON parser. Stacktrace:"
        )
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build a site.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars="@",
    )
    # TODO Specify your real parameters here.
    parser.add_argument("path", help="pass path to the program", metavar="path")
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    parser.add_argument(
        "-s",
        "--serve",
        help="Serve the HTML with a web server on port 8000",
        action="store_true",
    )

    parser.add_argument(
        "-c",
        "--clean",
        help="Clean up the build folder before creating a new build. Note that certain folders, like .git/ don't get recreated.",
        action="store_true",
    )

    parser.add_argument(
        "--base",
        nargs=1,
        default="",
        help="Overwrite base url from the config file.",
    )

    parser.add_argument(
        "-d",
        "--draft",
        help="Show draft posts with a 'draft': true flag in their config.json.",
        action="store_true",
    )
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    output_path = main(args, loglevel)

    if args.serve:
        event_handler = FilesystemEventHandler(
            args.path, callback=main, args=args, loglevel=loglevel
        )
        observer = Observer()
        observer.schedule(event_handler, args.path, recursive=True)
        observer.start()

        serve_build(output_path)
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
