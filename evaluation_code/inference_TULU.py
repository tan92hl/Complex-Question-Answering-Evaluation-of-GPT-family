from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed,T5Tokenizer,T5ForConditionalGeneration
import torch
import deepspeed
import json
import random 
import time
from tqdm import *
import os
import argparse 
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('--model',type=str)
parser.add_argument('--dataset',type=str)
parser=parser.parse_args()

logging.info(f"inference using model: {parser.model} and dataset: {parser.dataset}")

#读取数据
f =open(os.path.join("Complex-Question-Answering-Evaluation-of-GPT-family-main","datasets",parser.dataset,f"{parser.dataset}_all_question_with_label.json"),'r',encoding='utf-8')
dataset = json.load(f)


tokenizer = AutoTokenizer.from_pretrained(parser.model)
model = AutoModelForCausalLM.from_pretrained(parser.model,device_map="auto")


#推理
time1=time.time()
n=len(dataset)
for i in tqdm(range(n)):
    prompt = '''<|user|>
            {input}
            <|assistant|>
            '''
    prompt = prompt.format(input=dataset[i]['question'])
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    generated_ids =model.generate(input_ids, do_sample=True,max_length=512)
    ans = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    dataset[i][parser.model]=ans
    
        
time2=time.time()

#if rank=="0":
data=json.dumps(dataset,indent=1)
with open(os.path.join("answer",f"{parser.model}_answer_{parser.dataset}.json"),"w",newline='\n') as f:
    f.write(data)
    logging.info(f"加载入answer/{parser.model}_answer_{parser.dataset}.json完成...")

# if rank=="0":
#     logging.info(f"总共用时:{str(time2-time1)},平均用时:{str((time2-time1)/n)}",)




