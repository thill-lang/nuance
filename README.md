# nuance

## Motivation

Nuance is intended to be a tiny app and webapp that does the opposite of what most translation apps do - emphasising the **different** meanings a translated word has between two languages, despite their shared sense across them.

For example, any translation engine will translate the English word 'cockroach' into French as __cafard__. But in fact __cafard__ has many meanings in French, including a bad mood, a hypocrite, etc. Similarly, translating __cafard__ back again into English might result in the word 'roach', which has a range of other meanings beyond the creepy-crawly insect. In addition, cognate forms such as __cafardeux__ shade the meaning of __cafard__, whereas in English it is not really possible to say someone is 'cockroachy'

Examples like this are easy to multiply - anyone who has ever learned (or attempted to learn) another language will have run into them frequently. The intention behind __nuance__ is to help language learners with this aspect of language-learning - partly by making language exploration more fun and interesting (discovering associated meanings that don't exist in your primary language is an imaginative exercise!), and partly just by making it easier through interlinkage.

## Implementation

### Overview

In the first instance __nuance__ will be little more than a set visualiser built on top of [BabelNet](http://babelnet.org/). 

1.  The user enters a word, indicating the native and target languages
2.  __nuance__ queries BabelNet appropriately in each language
3.  The application then plots out the intersection and disjunct of the synsets found in each language

Subsequent iterations can explore the best way of picking out the intersecting terms and whether navigating along more complex relations (hyponyms, hypernyms) is valuable.

### Framework

Try Flask for this, rather than Django

TODO: Visualisation library? Need good Venn diagram and tree layout libraries.

