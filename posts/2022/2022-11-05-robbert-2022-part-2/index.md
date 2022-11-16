In [part 1](updating-robbbert), I explained how we created a new tokenizer for RobBERT and how we prepared the data.
These were the first steps to update our language model to 2022. 
Since that blogpost, we ran a training script for some time and we now have a model that we're quite proud of.
Let's take a look!

# Training
To pretrain the first versions of RobBERT, we used Meta's FairSeq library. 
This worked pretty well, especially because, back then, the HuggingFace library was not really so popular and we would have needed to implement the pretraining from scratch.
So we trained in FairSeq and later converted the model to HuggingFace.
There even was a script to do this, although we had to add an extra translation step for the tokens.

However, we  had some occasional issues with our converted model.
For instance, our model worked perfectly well for some time, but when the HuggingFace library moved to a faster implementation of the tokenizers, our model broke.
It wasn't a big issue and we managed to fix it, but, in hindsight, those translations cost us a lot of time.
So now we wanted to train with the HuggingFace library. 

We used a training script that uses the HuggingFace models combined with [PyTorch Lightning](https://www.pytorchlightning.ai).
This worked pretty well.
The benefit of this library is that we get checkpointing, distributed training, data loading, etc. for free.
We definitely needed the checkpoints, since our process got terminated a few times, as you can see in the validation chart.

<div class="row">
    <figure>
<div class="col-md-12 col-sm-12 col-12 mx-auto"> 
    <img src="training.png" width="100%" alt="Graph of the pseudo-perplexity on the validation set."/>
    </div>
    <div class="col">
<figcaption>Graph of the pseudo-perplexity (PPPL) on the validation set. The spikes with PPPL=100 are when a training run was interrupted, the last checkpoint was then loaded again and training was resumed.</figcaption>
</div>
    </figure>
</div>

The interesting thing is that our model is now still getting lower and lower validation scores, so no reason to stop just yet. 
So we are still letting the training run, but we've been spending a lot of compute and we don't know yet if our model is any good.

# Can RobBERT-2022 replace the original?
One of the first requirements is that any new model that we release must be at least as "good" as the old RobBERT model.
Otherwise it is just confusing to have a new model that performs worse and which we would discourage people to use.
This was actually the case when we were first evaluating a very early checkpoint of the model and we were hoping to catch a conference deadline. 
The model performed worse that RobBERT on the old benchmark tasks and on new tasks, so it made no sense to submit this model.

Luckily, the training continued and our new model does perform well on these benchmarks. 
We'll do a detailed writeup (or a paper directly) on these evaluations, but the gist is that most benchmark scores were pretty good and surpassed RobBERT.

Aside from getting high benchmark scores, the embeddings also have to be suitable as a replacement for RobBERT.
People have been building applications with the embeddings directly, without finetuning, so if we now mess those up, those applications break as well.

Although it is a bit more difficult to analyze those embeddings directly, we can visualize them and see if there are any big differences in quality. 
I would hope to see the same kinds of clusters in both embeddings, which is indeed the case, as you can see in the following chart.

<script src="https://cdn.jsdelivr.net/npm/vega@5.22.1"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@5.6.0"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@6.21.0"></script>
<div id="vis"></div>

<script type="text/javascript">
    var yourVlSpec = {"config": {"view": {"continuousWidth": 500, "continuousHeight": 300}}, "data": {"url": "data.json"}, "mark": {"type": "circle", "size": 60}, "encoding": {"color": {"field": "hue", "type": "nominal"}, "tooltip": [{"field": "hue", "type": "nominal"}, {"field": "sentences", "type": "nominal"}], "x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}}, "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json", "title": "T-SNE visualization of 1000 embeddings from both RobBERT and RobBERT-2022"};
    vegaEmbed('#vis', yourVlSpec, {actions: {
    export: true,
    source: false,
    compiled: false,
    editor: false
  }});
</script>

Since the training did not constrain the model to stay close to the original embeddings, there is some drift. 
Most clusters are present in both models, but they are mirrored in our visualization.
This mirroring is mostly an artifact of the t-SNE dimensionality reduction, but it does show that the embeddings shifted enough to affect the t-SNE visualization.

# Does RobBERT-2022 model language shifts?
Our previous model is from 2019, so over the last 3 years, the language has shifted a bit.
I already discussed how we tested if the model is better or at least as good on _old_ tasks, but how about new ones?

We've chosen two tasks about the COVID-19 pandemic, as this is one of the most telling events that happened since 2019 and many people created new datasets.
At our lab, [Kristen Scott, Bettina Berendt and I created a dataset](/attitudes-towards-covid-19-measures/) and [a few models](https://huggingface.co/DTAI-KULeuven/mbert-corona-tweets-belgium-curfew-support) to analyze sentiment for COVID-19 measures, like the curfew.
Walter Daelemans' lab at UAntwerpen also created [a cool dataset for a chatbot](https://vaccinchat.be) with frequently asked questions about the vaccination policy in Flanders, called VaccinChat.

<div class="row">
<div class="col-md-8 col-sm-12 col-6 mx-auto">
<figcaption>Results on the <a href="https://vaccinchat.be">VaccinChat</a> dataset. Results without $F_1$ score are reported by <a href="https://aclanthology.org/2022.coling-1.312.pdf">Buhmann et al.</a> and are a nice illustration that it certainly helps to adapt the model to the domain, which is what happened with BERTje+ and CoNTACT+.</figcaption>

<style type="text/css">
.tg td{padding:3px 10px;word-break:normal;}
.tg th{font-weight:normal; overflow:hidden;padding:10px 10px;word-break:normal;}
.tg .tg-fymr{border-color:inherit;font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
.tg .tg-dvpl{border-color:inherit;text-align:right;vertical-align:top}
.tg {width: auto !important;}.
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-fymr">Model</th>
    <th class="tg-fymr">ACC</th>
    <th class="tg-fymr">$F_1$</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-fymr"><span style="font-style:normal;text-decoration:none">Domain-adapted models</span></td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-dvpl">BERTje+</td>
    <td class="tg-0pky">77.7%</td>
    <td class="tg-0pky"><span style="font-weight:normal;font-style:normal;text-decoration:none">—</span></td>
  </tr>
  <tr>
    <td class="tg-dvpl">CoNTACT+</td>
    <td class="tg-fymr">77.9%</td>
    <td class="tg-0pky"><span style="font-weight:normal;font-style:normal;text-decoration:none">—</span></td>
  </tr>
  <tr>
    <td class="tg-fymr">General-purpose models</td>
    <td class="tg-0pky"></td>
    <td class="tg-0pky"></td>
  </tr>
  <tr>
    <td class="tg-dvpl">BERTje</td>
    <td class="tg-0pky">74.7%</td>
    <td class="tg-0pky">—</td>
  </tr>
  <tr>
    <td class="tg-dvpl">RobBERT v2</td>
    <td class="tg-0pky">74.9%</td>
    <td class="tg-0pky">77.2%</td>
  </tr>
  <tr>
    <td class="tg-dvpl">RobBERT-2022</td>
    <td class="tg-fymr">76.3%</td>
    <td class="tg-fymr">79.3%</td>
  </tr>
</tbody>
</table>
</div>
</div>

RobBERT-2022 performs pretty well on both sentence classification tasks, surpassing the original RobBERT model with a few percentage points.
The VaccinChat results are also pretty interesting, since the original paper also included experiments with domain-adapted models that we can compare with.
There, the results of RobBERT-2022 are a bit lower than the domain-adapted models, which makes sense: RobBERT-2022 is still a general-purpose model and Corona-related text was only a small part of the training data.