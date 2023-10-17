Our [`biased-rulers` Python package](https://github.com/iPieter/biased-rulers) did not contain an implementation of DisCo, although this is an interesting metric to quantify stereotypes in language models. However, I've had a few questions about this while presenting our paper at NAACL 2022 and the Bias in NLP 2022 workshop, so I decided to give the implementation another go. 

There are two implementations of DisCo, the original metric as proposed by [Webster et al. (2021)](https://arxiv.org/pdf/2010.06032.pdf) and a simpler implementation by [Lauscher et al. (2021)](https://arxiv.org/pdf/2109.03646.pdf). I'll talk more about the differences later on, but the gist is that the statistical $\mathcal{X}^2$ test got replaced by two set operations. This simplifies the metric quite a lot and also avoids some issues with $\mathcal{X}^2$ tests for small samples.

So before we dive into this metric, I want to highlight that although I would have made some choices differently, I still think that DisCo is a very cool metric, hence me spending all time on it. 
This blog post is also slightly different from what I usually post on my website, but I think it can serve as a nice complementary resource that does a deep-dive into one metric, as opposed to our more general survey. And I don't have to polish it as much 😉

So let's get started. First stop: which words do we use?

# Word lists
The original DisCo had two sources for lists of words that were gendered: 
- A list by [Zhao et al. (2018)](https://github.com/uclanlp/gn_glove) to create gender-neutral (non-contextual) word embeddings. There are actually two lists, one that has ~100 profession-related nouns included, and another list with ~100 more professions. 
    ```text
    actor   	 actress 
    actors	     actresses
    actress 	 actor 
    actresses	 actors
    airman 	     airwoman 
    airmen 	     airwomen 
    ...
    ```
    The interesting thing here is that every noun is listed twice, once in the left column and once more in the right column, it was a dataset for swapping gendered nouns after all. That needs to happen in two directions. However, that's not really needed for our use-case, since a discrepancy between two nouns is undirected. 
    
    Using the full list won't cause huge issues, however, since only the Bonferroni correction relies on the length of this list. What will happen is that our test for statistical significance, which is normally $\alpha = 0.05$ will be adjusted to the number of of experiments that we do (104 for the main list), so $\alpha = \frac{0.05}{104}$. We're off by a factor two in the worst case.

- The [top 1000 baby names](https://www.ssa.gov/oact/babynames/limits.html) in the US. Here, only names that were over 80% given to one gender were used.

Both datasets make sense to me, but testing aligned nouns (like the first list), does have the benefit that the differences between distributions can be more easily attributed to gender. But this remains a bit of a leap, since we don't really perform interventions to establish a causal link. Some idea for future work perhaps?

# The original DisCo metric
The original DisCo implementation uses $\mathcal{X}^2$ tests to conclude if predictions are different. But what should be different? I have to admit that I initially completely misunderstood what was tested here, so this section will be that train of thought while I was implementing the metric.

Let's back up a bit first. 

The $\mathcal{X}^2$ test is used to 


# DisCo without statistical tests
[Lauscher et al. (2021)](https://arxiv.org/pdf/2109.03646.pdf) also used DisCo to evaluate their method to debias language models. DisCo got a bit simplified, however. The statistical test is replaced by two metrics:

- The average number of shared candidates between both gendered words.
- The average probability difference between (all?) predicted tokens.

The first metric only takes into account if a token is predicted with a certain threshold or not, but the second metric makes a distinction between tokens that are very likely versus not likely. For example, between `_He_ is a doctor` ($p=0.61$) and `_She_ is a doctor` ($p=0.24$) there is a big difference in probability, but the next tokens `_Who_ is a doctor` ($p=0.002$) and `_It_ is a doctor` ($p=0.002$) are both quite unlikely and there is no numerical difference anymore. 

Another modification to DisCo is the number of tokens that got predicted for each input. The original implementation used the top 3 tokens, but Lauscher et al. changed this to every token with a probability $p > 0.1$. 
This _can_ result in more tokens, but like [that example with the doctor](https://huggingface.co/bert-base-uncased?text=%5BMASK%5D+is+a+doctor), it doesn't have to. 

This implementation is also available in our library and we managed to replicate the results on `bert-base-uncased` from the paper. 