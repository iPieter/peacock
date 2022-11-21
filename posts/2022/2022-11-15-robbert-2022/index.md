RobBERT-2022 is the newest release of the [Dutch RobBERT model](/robbert/). Since the original release in January 2020, some things happened and our language evolved. For instance, the COVID-19 pandemic introduced a wide range of new words that were suddenly used daily. To account for this and other changes in language use, we release a new Dutch BERT model trained on data from 2022.

Thanks to this more recent dataset, this model shows increased performance on several tasks related to recent events, e.g. COVID-19-related tasks. We also found that for some tasks that do not contain more recent information than 2019, the original RobBERT model can still outperform this newer one.

# Creating RobBERT-2022
I've detailed the development of RobBERT-2022 in two blogposts: [part one](/blog/2022/updating-robbert/) and [part two](/blog/2022/updating-robbert-part-2/),
but the gist is that we added almost 3k new tokens to our vocabulary and then pre-trained our model based on the old weights.

We evaluated RobBERT-2022 on the same benchmark tasks as RobBERT and on two COVID-19-related tasks and the model performs very well on most tasks.

# Usage
RobBERT-2022 is a plug-in replacement for the original RobBERT model, so you can just update your code to use the new identifier in the HuggingFace Transformers library.

</div>
</div>
<div class=row>
<div class="col-12">
<pre class="small pl-0" style="margin: 0px; line-height: 125%">
<span style="color: rgb(249, 38, 114);">from</span> <span style="color: rgb(30, 30, 38);">transformers</span> <span style="color: rgb(249, 38, 114);">import</span> <span style="color: rgb(30, 30, 38);">AutoTokenizer,</span> <span style="color: rgb(30, 30, 38);">AutoModelForSequenceClassification</span>
<span style="color: rgb(30, 30, 38);">tokenizer</span> <span style="color: rgb(249, 38, 114);">=</span> <span style="color: rgb(30, 30, 38);">AutoTokenizer</span><span style="color: rgb(249, 38, 114);">.</span><span style="color: rgb(30, 30, 38);">from_pretrained(</span><span style="color: #2980b9;">"DTAI-KULeuven/robbert-2022-dutch-base"</span><span style="color: rgb(30, 30, 38);">)</span>
<span style="color: rgb(30, 30, 38);">model</span> <span style="color: rgb(249, 38, 114);">=</span> <span style="color: rgb(30, 30, 38);">AutoModelForSequenceClassification</span><span style="color: rgb(249, 38, 114);">.</span><span style="color: rgb(30, 30, 38);">from_pretrained(</span><span style="color: #2980b9;">"DTAI-KULeuven/robbert-2022-dutch-base"</span><span style="color: rgb(30, 30, 38);">)</span>
</pre>
</div>
</div>