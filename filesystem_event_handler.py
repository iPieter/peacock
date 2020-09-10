import typing

from watchdog.events import FileSystemEventHandler
import os, logging


class FilesystemEventHandler(FileSystemEventHandler):
    """Calls a callback to rebuild the site when changes have been detected."""

    def __init__(self, base_path:str, callback: typing.Callable = None, args=None, loglevel=None ):
        if os.path.exists(".gitignore"):
            self.ignored_paths = ['build']
            with open(os.path.join(base_path, ".gitignore")) as fp:
                self.ignored_paths.extend([x for x in fp.read().splitlines()])

            print(self.ignored_paths)

        self.callback = callback
        self.args = args
        self.loglevel = loglevel


    def on_moved(self, event):
        super(FilesystemEventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        if os.path.realpath(event.src_path) not in (os.path.realpath(p) for p in self.ignored_paths):
            logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

    def on_created(self, event):
        super(FilesystemEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        if os.path.realpath(event.src_path) not in (os.path.realpath(p) for p in self.ignored_paths):
            logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(FilesystemEventHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        if os.path.realpath(event.src_path) not in (os.path.realpath(p) for p in self.ignored_paths):
            logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super(FilesystemEventHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        if True not in (self._in_directory(event.src_path, p) for p in self.ignored_paths) and event.src_path != '.':
            logging.info("Modified %s: %s", what, event.src_path)
            self.callback(self.args, self.loglevel)

    @staticmethod
    def _in_directory(path, root):
        # make both absolute
        root = os.path.realpath(root)
        path = os.path.realpath(path)

        # return true, if the common prefix of both is equal to directory
        # e.g. /a/b/c/d.rst and directory is /a/b, the common prefix is /a/b
        return os.path.commonprefix([path, root]) == root
