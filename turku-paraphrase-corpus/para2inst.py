import os
import json
import tqdm
import datasets
import random

def read_instructions(fname):
    patterns={}
    with open(fname) as f:

        cat=None   #  # -line
        field=None #  ##-line
        lines=[]   #  accumulated lines
        ex={} 
        
        for line in f:
            line=line.rstrip("\n")
            if line.startswith("##"):
                #new field!
                if lines: #did I have something for the previous field?
                    ex.setdefault(field,[]).append("\n".join(lines).strip())
                    lines=[]
                field=line[2:]
            elif line.startswith("#"):
                #new example pattern!
                if ex:
                    if lines: #did I have something for the previous field?
                        ex.setdefault(field,[]).append("\n".join(lines).strip())
                        lines=[]
                    patterns.setdefault(cat,[]).append(ex)
                    ex={}
                cat=line[1:]
            else:
                lines.append(line)
        else:
            if ex:
                patterns.setdefault(cat,[]).append(ex)
    return patterns

def draw(patterns,cat):
    ex_pattern=random.choice(patterns[cat])
    ex={}
    for key,list_of_options in ex_pattern.items():
        ex[key]=random.choice(list_of_options)
    return ex

def format_p(ex_pattern,**kwargs):
    ex={}
    for k,v in ex_pattern.items():
        ex[k]=v.format(**kwargs)
    return ex

def enrich_rewrites(examples):
    """
    Finds the original for every rewrite, since these are not explicitly bound
    but the rewrite always refers to the previous non-rewrite example
    but some examples have several rewrites
    """
    last_real_example=None #holds the last seen non-rewrite example
    for ex in examples:
        if not ex["is_rewrite"]:
            last_real_example=ex
            yield ex
        else:
            assert ex["goeswith"]==last_real_example["goeswith"]
            ex["original"]=last_real_example
            yield ex

def general_special_prompt(ex):
    res=[]
    #arrow points towards more general
    prompt=draw(patterns,"PARAPHRASE-ONE-DIR")
    if ex["label"]=="4>":
        res.append(format_p(prompt,txt_special=ex["text1"],txt_general=ex["text2"]))
    elif ex["label"]=="4<":
        res.append(format_p(prompt,txt_special=ex["text2"],txt_general=ex["text1"]))
    return res
    

def paraphrase_me_prompt(ex):
    res=[]
    if ex["label"]=="4":
        prompt=draw(patterns,"PARAPHRASE")
        res.append(format_p(prompt,txt1=ex["text1"],txt2=ex["text2"]))
        res.append(format_p(prompt,txt2=ex["text1"],txt1=ex["text2"]))
    return res

def rewrite_me_prompt(ex):
    res=[]
    if ex["is_rewrite"]:
        if ex["text1"].strip()==ex["original"]["text1"].strip():
            prompt=draw(patterns,"REW-ONE-UNCHANGED")
            res.append(format_p(prompt,txt_fixed=ex["text1"],txt_change=ex["original"]["text2"],rew_txt=ex["text2"]))
        elif ex["text2"].strip()==ex["original"]["text2"].strip():
            prompt=draw(patterns,"REW-ONE-UNCHANGED")
            res.append(format_p(prompt,txt_fixed=ex["text2"],txt_change=ex["original"]["text1"],rew_txt=ex["text1"]))
        else:
            prompt=draw(patterns,"REW-BOTH-CHANGED")
            res.append(format_p(prompt,txt1=ex["original"]["text1"],txt2=ex["original"]["text2"],rewtxt1=ex["text1"],rewtxt2=ex["text2"]))
    return res
              

def prompt3(ex):
    res=[]
    if ex["label"]=="3":
        prompt=draw(patterns,"PARAPHRASE-3-Y")
        res.append(format_p(prompt,txt1=ex["text1"],txt2=ex["text2"]))
    elif ex["label"]=="4":
        prompt=draw(patterns,"PARAPHRASE-3-N")
        res.append(format_p(prompt,txt1=ex["text1"],txt2=ex["text2"]))
    return res

if __name__=="__main__":
    dataset = datasets.load_dataset('TurkuNLP/turku_paraphrase_corpus', name="plain")
    inst_file=os.path.join(os.path.dirname(__file__),"instructions.txt")
    
    #for ex in enrich_rewrites(dataset["train"]):
    #    if ex["label"]=="4>":
    #        print(ex["text1"],"  >  ",ex["text2"])

    patterns = read_instructions(inst_file)
    for ex in tqdm.tqdm(enrich_rewrites(dataset["train"])):
        res=[]
        res.extend(paraphrase_me_prompt(ex))
        res.extend(rewrite_me_prompt(ex))
        res.extend(prompt3(ex))
        res.extend(general_special_prompt(ex))
        for inst in res:
            print(json.dumps(inst,ensure_ascii=False,sort_keys=True))

  
