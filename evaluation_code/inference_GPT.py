import requests
import openai
import os
import torch
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

logging.info(f"inference using model: {parser.model} and dataset: {parser.dataset} ")

openai.api_key = os.getenv('OPENAI_KEY', default="sk-4Hs3Kpr8oEKdyQqH0cB7B712937648638714757e3212D3A6")
openai.api_base = "https://api.rcouyi.com/v1"


#读取数据
f =open(os.path.join("Complex-Question-Answering-Evaluation-of-GPT-family-main","datasets",parser.dataset,f"{parser.dataset}_all_question_with_label.json"),'r',encoding='utf-8')
dataset = json.load(f)


#推理
time1=time.time()
n=len(dataset)

MAX_TOKEN_LEN = 1024    # The maximum number of tokens (words or symbols) allowed in a single response from the chatbot
TIME_OUT = 3            # The number of seconds to wait for a response from the chatbot API before timing out
ROLE = 'assistant'
USER_ROLE = 'user'
PROMPT = f'you are {ROLE}.'

for i in tqdm(range(n)):
    prompt = dataset[i]['question']
    if parser.model=="gpt-3.5-turbo-instruct":
        response = openai.Completion.create(
                    model=parser.model,
                    prompt=prompt,
                    temperature=0,
                    max_tokens=512, # 限定模型的回答最多有多少个token
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
        ans = response.choices[0].text.strip()
    else:
        message=[
            {"role": "system", "content":"you are assistant"},
            {"role": "user", "content": f"{prompt}"}
        ]
        response = openai.ChatCompletion.create(
            model=parser.model,   # The name of the OpenAI language model to use
            messages=message,       # The conversation history so far
            temperature=0,              # Controls the creativity of the chatbot's responses
            max_tokens=512,     # The maximum number of tokens (words or symbols) allowed in a single response from the chatbot
            top_p=1,                    # Controls the diversity of the chatbot's responses
            frequency_penalty=0,        # Penalizes the chatbot for using frequently occurring words
            presence_penalty=0,         # Penalizes the chatbot for using words that don't occur very often
            timeout=TIME_OUT,             # The number of seconds to wait for a response from the chatbot API before timing out
        )
        ans = response.choices[0].message.content.strip()
    dataset[i][parser.model]=ans.replace("</s>","")
time2=time.time()

data=json.dumps(dataset,indent=1)
with open(os.path.join("answer_GPT",f"{parser.model}_answer_{parser.dataset}.json"),"w",newline='\n') as f:
    f.write(data)
    logging.info(f"加载入answer/{parser.model}_answer_{parser.dataset}.json完成...")


logging.info(f"总共用时:{str(time2-time1)},平均用时:{str((time2-time1)/n)}",)