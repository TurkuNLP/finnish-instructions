# finnish-instructions
Centralized repo for Finnish instruction data. License? 

## Format

`instruction`: mandatory. May include all the required context.

`input`: optional. Used as an optional context for instructions.

`output`: Generated response.


Examples:
```
Instruction: "Laadi kysymys annetusta tekstistä."
Input: "Teksti: Sandra siirtyi toimistoon. Sandra meni kylpyhuoneeseen. Mary meni makuuhuoneeseen. Daniel siirtyi eteiseen."
Output: "Missä on Daniel?"
```
or 
```
Instruction: "Kumpi on parempaa suomenkieltä, vaihtoehto a) {a} vai b) {b}"
Input: ""
Output: "a"
```

## Datasets:

TODOs
* [Anthropic HH-RLHF](https://huggingface.co/datasets/Anthropic/hh-rlhf)

Ready / contains already usable material
1) Machine translated from the original English using [DeepL](<https://www.deepl.com/>)
* [dolly-fi](https://github.com/turkunlp/dolly-fi): Finnish version of the [databricks-dolly-15k instruction dataset](<https://github.com/databrickslabs/dolly/tree/master/data>)
* [oasst-fi](<https://github.com/turkunlp/oasst-fi>) Finnish version of
[OpenAssistant dataset v1](https://huggingface.co/datasets/OpenAssistant/oasst1)
* [natural-instructions-fi](https://github.com/luukkonenr/natural-instructions-fi) is an on-going process of machine translating manually selected tasks.

2) Synthetic datasets

TODOs
* OCR-correction
* Masked word prediction
* Recognize text from space-separated characters
* Recognize text from characters without space

Ready


3) Native Finnish datasets:

Ready

* Paraphrase 
* Question Answering 



## Processing 

