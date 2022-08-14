# The need for a new RobBERT model
2020 happened. RobBERT was trained in 2019, so some terms have since then changed meaning—corona is no longer just a beer—and new words are now in common use. RobBERT doesn't know about all of this.

# The new dataset
The OSCAR corpus has a new 2022 version, which we can use for our project.
However, the data is packed a bit differently. 
The version of OSCAR that we used previously was "shuffled", meaning that only a few sentences of a document were kept together instead of the entire document.
This worked pretty well to train RobBERT on, but might not really learn longer-ranging dependencies because of this.

We previously looked into the shuffled and non-shuffled variants of the corpus when we trained our distilled RobBERTje models, and we found that only some tasks benefit from longer training inputs. But more importantly, merging different training examples also reduced the training time, since we make more optimal use of the 512 tokens we _can_ provide to the model compared to using only single lines (typically 1 or 2 sentences, but can also be one word).

The new corpus uses a slightly different format and provides the entire documents, leaving the shuffling to us if we want it. 
This is pretty nice, because that means we can train on entire documents, as long as they are below the 512 token limit.

To get a better understanding of our dataset, I've plotted the distribution of the document length. With single lines, the inputs are really short, 80% is shorter than 35 tokens. For entire documents, we need 315 tokens to cover 80% of the documents. That's a big difference... 

<div class="row">
        <figure>
    <div class="col-md-10 col-sm-12 col-12 mx-auto"> 
        <img src="cdf.png" width="100%" alt="Cumulative distribution function of our dataset"/>
        </div>
        <div class="col">
    <figcaption>Cumulative distribution function of the Dutch section of OSCAR 2022. </figcaption>
    </div>
        </figure>
    </div>

I've also included the merging algorithm that we used for our distilled RobBERTje models. 
This is a bit more spaced out, but not a lot.

The benefits of training on the entire documents are (i) more examples long-ranging dependencies, (ii) better use of the maximum number of tokens and (iii) the model actually learns to use line breaks as well.

Training on entire documents it is!

# Updating the tokenizer
Retraining our model on a new dataset is all fine and well, but a few things happened since 2019 that also affect which words we use. Words like `corona` or `COVID` were not in the original tokenizer for obvious reasons. But we started using those words quite a lot.

So we also want to add some tokens to our vocabulary. For this, we can create another BPE tokenizer and look at which tokens are new ([notebook <i class="fab fa-python"></i>]()). This is pretty cool, since it also gives us some more insights in what words society started using, for example:

- coronamaatregelen
- coronaregels
- coronacrisis
- coronat
- coronab
- coronabesmettingen
- corona
- Bitcoin
- Biden
- omikronvariant
- TikTok

Since we use merges of two different tokens, like `coronab` with something else`, we do also want to add those to our tokenizer. 
This is a bit trickier.
Each token namely has a "_dependency tree_" of other tokens and each time they are merged. 
As an illustration, these are the final merges of three tokens. 

<div class="row">
    <figure>
<div class="col-md-10 col-sm-12 col-12 mx-auto"> 
    <img src="corona.png" width="100%" alt="Merges of words related to corona."/>
    </div>
    <div class="col">
<figcaption>Merges of the words `coronamaatregelen`, `coronab` and `corona`. Notice how `coron` gets used, instead of `corona`.</figcaption>
</div>
    </figure>
</div>

Because this is a statistical process, some merges make little sense, especially in Dutch where we have compound words. We had a thesis student working on improving these merges, but that is quite tricky to automate.

To extend our RobBERT vocab, we can add all the new tokens. Since we can view both vocabularies as sets, the difference `New - Old` will have all the tokens and by definition also the dependencies that were not in the old tokenizer to begin with.

But we still need to figure out how to find the merges. We only need the merges that result in a token that is in the difference `New - Old`, since all others should be covered by the original RobBERT (v2) tokenizer. This means we can easily iterate over all merges, perform the merger and check if it is one that we need. 

So that gives us a new vocabulary size of 42750, meaning we added 2750 tokens. The actual difference was a bit larger, but I removed some completely meaningless ascii sequences. If we are performing tokenizer surgery anyways, why not do it right?

# The actual training: where do we start?

RQs