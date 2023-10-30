I took a week of holidays, so naturally I needed a small project.
I have been thinking a while about gluing together Text-To-Speech (TTS), Speech-To-Text (STT) and some transformers models for some small dialogue app, but that's not too exciting in itself ([Duolingo Max](https://blog.duolingo.com/duolingo-max/) is doing that).
On the other hand, I actually had three master's thesis projects where students were investigating how to automatically construct skill trees with sentences from [Tatoeba](https://tatoeba.org/) and how to predict CEFR levels. These things worked reasonably well.

So lot's of interesting stuff that we can combine into a cool language learning app where users can pick a topic—I really started to get annoyed how half of the lessons from Duolingo were about Octoberfest—and then have a conversation with some language model about it.

# Speech
After a certain point, actually being able to speak and hold a conversation is the best way to actually learn a language, at least for me. 
Some vocabulary is definitely necessary, which apps like Duolingo help a lot with. Other methods do focus more on thinking how to actually say a full sentence, like [Language Transfer](https://www.languagetransfer.org/free-courses-1).
Now imagine, how cool would it be to actually do this for every language and topic you want? And what if you could get feedback on what you said?


There is even [an implementation with React Native bindings](https://github.com/mybigday/whisper.rn). Perfect.

# Topics and skill trees
One aspect that makes learning a language interesting is that it allows you to say stuff. Of course, what you want to say is different than what I want to say (most likely I would talk about giraffes). If you go on holiday to Berlin, getting some basic knowledge on ordering a Pretzel is fine, but getting an employment contract requires some other vocabulary.

One aspect that I always found missing in current language learning apps is the ability to customize what you want to learn. Sure, you have to start with the basics, but nothing is as demotivating as learning vocabulary you just don't care about.

So let's do better. What if we could construct a tree based on how many times certain words occur and how difficult we estimate those words to be?

The idea would be to cluster words (i.e. topic modeling with some BERT model) and then try to find an iteratively larger set of words to cover most of the text of a topic. Some of this has already been experimented with for a master's thesis, but that thesis mostly went into the topic of CEFR classification instead of skill tree construction.

That's for later this week.

# Automatic corrections
Let's make it easy for ourselves and just use GPT-4 for this. The results are pretty good:

```json
{
"correct": false,
"corrected": "Ich möchte eine Brezel.",
"mistake on verb conjugations": true,
"needs table with all verb conjugations": true,
"explanation": "The verb 'möchten' (would like) is a modal verb and it should be conjugated as 'möchte' in the first person singular (Ich). You used 'möchtest' which is used for second person singular (Du).",
"conjugation": "
| Person  | Conjugation |
|---------|-------------|
| Ich     | möchte      |
| Du      | möchtest    |
| Er/Sie/Es | möchte    |
| Wir     | möchten     |
| Ihr     | möchtet     |
| Sie/sie | möchten     |"
}
```
