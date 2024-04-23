from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
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
parser.add_argument('--local_rank',type=str)
parser=parser.parse_args()

logging.info(f"inference using model: {parser.model} and dataset: {parser.dataset}")


#读取数据
f =open(os.path.join("Complex-Question-Answering-Evaluation-of-GPT-family-main","datasets",parser.dataset,f"{parser.dataset}_all_question_with_label.json"),'r',encoding='utf-8')
dataset = json.load(f)
rank = os.environ['LOCAL_RANK']

#加载模型
if rank=='0':
    print('Begin load model...')
model = AutoModelForCausalLM.from_pretrained(parser.model, torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained(parser.model, use_fast=False)

ds_model = deepspeed.init_inference(
    model=model,      # Transformers模型
    mp_size=4,        # GPU数量
    dtype=torch.float16, # 权重类型(fp16)
    replace_method="auto", # 让DS自动替换层
    replace_with_kernel_inject=True, # 使用kernel injector替换
)

#推理
time1=time.time()
n=len(dataset)


for i in tqdm(range(n)):
    prompt = dataset[i]['question']
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    logits = ds_model.generate(input_ids, do_sample=False,max_new_tokens=500)
    ans=tokenizer.decode(logits[0].tolist())
    if rank=="0":
        ans = ans.split('<Example4>')[1]
        dataset[i][parser.model]=ans.replace("</s>","")
        
time2=time.time()

if rank=="0":
    data=json.dumps(dataset,indent=1)
    with open(os.path.join("answer_COT","COT",f"{parser.model}_answer_{parser.dataset}.json"),"w",newline='\n') as f:
        f.write(data)
        logging.info(f"加载入answer/{parser.model}_answer_{parser.dataset}.json完成...")

if rank=="0":
    logging.info(f"总共用时:{str(time2-time1)},平均用时:{str((time2-time1)/n)}",)




