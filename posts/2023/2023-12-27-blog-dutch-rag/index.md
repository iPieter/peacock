Let's build a chatbot with some domain knowledge about one topic. 
For this demo, I chose to focus on the town where I grew up in: Oudenaarde. I know some die-hard fans of this town, so that's gonna be fun to test!

The knowledge base is basically news articles, wikipedia pages about all _deelgemeenten_ and some facts from [Le Petit Bruges](https://www.le-petit-bruges.be).

# The benefits of retrieval-augmented generation
Language models are good at generating text, but the often don't know a lot of facts and thus start hallucinating. The easiest way to make a model that knows stuff about your domain is to include those facts in the prompt. Since a language model can _'look back'_ to the prompt, it is way more likely to return actual correct information if that was in the prompt.

However, our prompt and the output can only be a few thousand tokens long, so it is quite valuable real estate. Every token we use for some facts can't be used for outputs. This is especially important for conversational models, since we want to include as much as we can from the actual conversation.

So we have to choose which facts we include, which we can do by querying a database. A typical way is to use embeddings of our collection of facts, which we do by a Sentence Embedding variant of our RobBERT-2022 model, which was converted by the Dutch Forensics Institute. Cool!

Let's start with a simple comparison when we ask it what it knows about Oudenaarde ("Wat weet je over Oudenaarde?"):

</div>
</div>
<div class="row">
    <div class="col-md-12 mx-auto">


<table>
<thead>
<tr class="header">
<th>Default</th>
<th style="width: 33%;">RAG</th>
</tr>
</thead>
<tbody>
<tr class="demo smaller">
<td>Oudenaarde is een historisch stadje in de provincie
<span class="wrong">West-Vlaanderen</span> in België. Het ligt in het oosten van
de Vlaanderen, aan de <span class="wrong">Zenne</span>. De stad is gelegen op een
strategische locatie <span class="wrong">tussen</span> Brussel en Gent.<br>De geschiedenis van
Oudenaarde ontwikkelde zich vanwege haar strategische ligging als een
vestingplaats. Al in de  <span class="wrong">9e eeuw was de stad de zetel van de Vikingen in
Zeeland. In detweede helft van de 10e eeuw wordt het opgericht als de
zetel van de Grieken en later van de Normannen</span>. In de 14e eeuw komt de
stad <span class="wrong">onder de Zuidelijke Nederlanden, toen wordt het stadsrecht het
bestuur over de stad verlenen</span>.<br>De stad heeft veel historische
bouwwerken, zoals het stadhuis, de <span class="wrong">Korenlei en het Klokhuis</span>. Het
<span class="wrong">historisch centrum</span> wordt beschermd als UNESCO
Werelderfgoed.<br><span class="wrong">Ouidenaarde</span> is tevens de
<span class="wrong">hoofdplaats van de provincie Oost-Vlaanderen</span>. Het
stadje is bekend om zijn laken, de traditionele wederzijdsstrijd tussen
Oudenaarde en Gent, en de traditionele feestdag van <span class="wrong">6
augustus</span>, toen de <span class="wrong">Slag van de Drie Heeren
gelegen</span> is.</td>
<td>Oudenaarde is een stad in de provincie
Oost-Vlaanderen in België. Het is de tweede cultuurstad van de provincie
na Gent en telt veel historische gebouwen. De stad is bekend om haar
bruine bieren, zoals Cnudde, Ename, Felix, Liefmans en Roman. Oudenaarde
heeft een rijk cultureel erfgoed en is bekend om haar landelijke
omgeving in de Vlaamse Ardennen. De stad heeft een belangrijke
toeristische industrie. Oudenaarde is ook bekend om haar
textielnijverheid, zoals de textielfabriek Saffre Frères.</div></td>
</tr>
<tr class="even">
<td><div></div></td>
<td></td>
</tr>
</tbody>
</table>

</div>
</div>
<div class="row">
    <div class="col-md-8 mx-auto">

Well, the default model is not great. There are a lot of hallucinations, so is Oudenaarde not in West Flanders, but in East Flanders. Some things seem plausible, but we don't have a Korenlei (that's in Ghent). The last paragraph might spark some debate as well. And we certainly didn't have Vikings and Greeks founding our city.

The RAG version is not only way shorter, which I like, but it also is basically correct. The only debate could be about the list of beers, since some are not of the Flemish _Oud Bruin_ variety (but they are from Oudenaarde).

# Design decisions

## Inference performance
We want to have a chatbot, so we need quick responses. There are two elements that are a bottleneck for our usecase:
- Running the LLM
- Obtaining vectors for our RAG

The LLM itself is the biggest bottleneck, since the default gives not even a single token per second (on a A50000 GPU with 24 GB of VRAM).

<center>

| Setting | Inference  | Total runtime |
|---------|------------|---------------|
| float32 | 0.36 t/s   | 13m54s        |
| bfloat16| 0.53 t/s   | 15m12s        |
| int8    | 15.0 t/s   | 1m30s        |

</center>

The performance of the quantized model with 15 tokens per second is acceptable, especially if we can stream that and not have someone wait 1+ minute.

## Prompts
The Mistral model we use is by default not exactly a Dutch model, so how can we make it one? Prompting is the easiest way and that does seem to work pretty well. I tried to keep all of the prompt in Dutch, since introducing some English seems to make the model more likely to switch to English. 

```text
[INST] Je bent een expert in {topic}. Antwoord enkel in het Nederlands. Gebruik de volgende context voor vragen te beantwoorden:

{context}

[/INST]
{chat_history}

[INST]
{question} 
[/INST]
```

Mistral's separation of instructions and user input is a bit weird, so we do have to open and close the instruction tags (which are both the system prompt and the user input) by fiddling a bit with LangChain's prompt processing functions. Ah well, as long as it works.

## Future work
There are some things left to improve the usefulness of this toolkit. The biggest ones are (i) to swap the model for a Dutch one and (ii) improve the scraping.
One cool feature would be to use our LLM to remove junk and irrelevant artifacts before adding them to the vector store.