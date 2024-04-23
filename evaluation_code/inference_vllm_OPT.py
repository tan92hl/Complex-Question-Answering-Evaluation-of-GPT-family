from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
from vllm import LLM,SamplingParams
import torch
import deepspeed
import json
import random 
import time
from tqdm import *
import os
import argparse 
import re
import logging 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('--model',type=str,default="opt-iml-max-30b")
parser.add_argument('--dataset',type=str,default="WQSP")
parser.add_argument('--COT',type=str)
parser=parser.parse_args()

logging.info(f"inference using model: {parser.model} and dataset: {parser.dataset}")


if parser.COT == "COT_naive":
    COT = """You are a knowledge base AI. You need to help me solve a problem: 
<Instruction> Answer the input question. You can generate any intermedate lists and states, but the final output should only contain the exact answer(s):
{{
    answer 1,
    answer 2,
    ...,
    answer n.
}}
</Instruction>

<Approach>
To answer the input question follow these steps:
1. Generate 5 sub-questions based on the input question.
2. Answer the generated sub-questions.
3. Answer the input question.
</Approach>

<Examples>
<Example1>
Input: For what was John Houseman (who is in the Jewish ethnic group) nominated for an Academy Award for Best Picture ?
Sub-questions:
{{
  1.Who is John Houseman?
  2.What is the Jewish ethnic group?
  3.Was John Houseman nominated for an Academy Award?
  4.In which category was John Houseman nominated?
  5.What was the film John Houseman was nominated for in the category of Best Picture at the Academy Awards? 
}}
Answers of Sub-questions:
{{
  1.John Houseman (September 22, 1902 - October 31, 1988) was a highly acclaimed American actor known for his work in both film and theater. In addition to acting, he was also involved in writing, directing, and producing..
  2.Jewish ethnic divisions refer to many distinctive communities within the world's ethnically Jewish population. Although considered a self-identifying ethnicity, there are distinct ethnic subdivisions among Jews, most of which are primarily the result of geographic branching from an originating Israelite population, mixing with local communities, and subsequent independent evolutions..
  3.Yes.
  4.Golden Globe Award for Best Supporting Actor.
  5.Julius Caesar.
}}
Output: 
{{
    'John Houseman, being a prominent figure in the film industry, was nominated for an Academy Award for Best Picture as a producer. His nomination was for the film “Julius Caesar.,” which was released in 1973.'
}}
</Example1>

<Example2>
Input: Is coffee originally from Brazil?
Sub-questions:
{{
  1.What is coffee?
  2.Where was coffee originally discovered?
  3.When was coffee discovered?
  4.How did coffee spread around the world?
  5.When did coffee first arrive in Brazil?
}}
Answers to Sub-questions:
{{
  1.Coffee is a brewed drink prepared from roasted coffee beans, the seeds of berries from certain Coffea species.
  2.Coffee was originally discovered in Ethiopia, in East Africa.
  3.Coffee was discovered in the 9th century.
  4.Coffee spread around the world through trade, first reaching the Arabian Peninsula, and then Europe in the 17th century.
  5.Coffee first arrived in Brazil in the 18th century.
}}
Output: 
{{
    'No, coffee is not originally from Brazil. The coffee plant, Coffea, is native to the region of Ethiopia in East Africa. It is believed that coffee was first discovered and consumed in Ethiopia in the 9th century. From there, it spread to other parts of Africa, the Arabian Peninsula, and eventually to Europe and the Americas through trade and colonization. Brazil, however, became the largest coffee producer in the world during the 19th century and has played a significant role in the global coffee industry ever since.'
}}
</Example2>

<Example3>
Input: Who is the reviewer of the Georgia national football team, which is ranked 78th by FIFA?
Sub-questions:
{{
  1.What is the Georgia national football team?
  2.What is the role of a reviewer in football?
  3.What is FIFA?
  4.What does it mean for a team to be ranked 78th by FIFA?
  5.Who has reviewed the Georgia national football team recently?
}}
Answers of Sub-questions:
{{
  1.The Georgia national football team represents Georgia in international football and is governed by the Georgian Football Federation. It competes in matches and tournaments sanctioned by FIFA and UEFA.
  2.A reviewer in football typically refers to a sports analyst or commentator who evaluates and discusses the performance of football teams and players.
  3.FIFA (Fédération Internationale de Football Association) is the international governing body of association football, futsal, and beach soccer. It is responsible for organizing major international tournaments, including the FIFA World Cup.
  4.Being ranked 78th by FIFA indicates that the Georgia national football team is positioned at number 78 in FIFA's global ranking system, which ranks men's national teams based on their game results.
  5.The reviewer of the Georgia national football team could vary depending on the context. It could be a sports journalist, a football analyst, or a commentator known for analyzing international football teams.
}}
Output:
{{
    'The reviewer of the Georgia national football team may vary depending on the source. As of my last update, the team was managed by Willy Sagnol, a former French international footballer, from 2020 until 2021. However, please note that managerial positions can change over time, so it is always a good idea to check the current information from reliable sources.'
}}
</Example3>

<Example4>
Input: {input}
"""
elif parser.COT =="COT_sp":
    COT="""<Instruction> Answer the input question. You can generate any intermedate lists and states, but the final output should only contain the exact answer(s):
    {{
        'Answer(s) to the input question...'
    }}
    </Instruction>

    <Approach>
    To answer the input question follow these steps:
    1. Determine the topic entity type of the input question.
    2. Determine the reasoning operation in the input question.
    3. Determine the conditional constraints in the input question.
    4. Generate the SPARQL query for input question.
    5. Answer the input question based on the SPARQL query.
    </Approach>

    <Examples>
    <Example1>
    Input: how many major cities are there ? 
    From_QA:('Question: "how many major cities are there? ", what is the sentence talks about?','Answer: city')
    SELECT_QA:('Question: "how many major cities are there? " from city, what is the sentence asks to select?','Answer: count(*)')
    WHERE_QA:('Question: "how many major cities are there? " from city select count(*), what is the sentence requires ?','Answer: city.population > 150,000')
    SPARQL: SELECT count(*) FROM city WHERE city.population > 150,000
    Output:
    {{
        The number of major cities can vary depending on the criteria used to define a “major” city. Generally, major cities are often determined based on factors such as population, economic significance, cultural importance, infrastructure, and political influence. Different sources may provide different lists of major cities. For example, some common lists include the Global Cities Index, Megacity classification, or simply cities with high population numbers. According to the United Nations, as of 2021, there are more than 30 megacities (cities with a population of over 10 million) worldwide, and numerous other cities with populations ranging from millions to several hundred thousand.It’s important to note that the exact number of major cities can change over time due to urbanization, population growth, and other factors.
    }}
    </Example1>

    <Example2>
    Input: which state is the second most populous state in the United States ?
    From_QA:('Question: "Which state is the second most populous state in the United States ?", what is the sentence talks about?','Answer: state')
    SELECT_QA:('Question: "Which state is the second most populous state in the United States ?" from state, what is the sentence asks to select?','Answer: state.state_name')
    WHERE_QA:('Question: "Which state is the second most populous state in the United States ?" from state select state.state_name, what is the sentence requires ?','Answer: {{state:isPartOf :US}} ORDER BY DESC(state.polulation) LIMIT 2 OFFSET 1')
    SPARQL: SELECT state.state_name FROM state WHERE {{state :isPartOf UnitedStates}} ORDER BY DESC(state.polulation) LIMIT 2 OFFSET 1
    Output:
    {{
        As of the most recent data, the second most populous state in the United States is Texas. California is the most populous state, followed by Texas.
    }}
    </Example2>

    <Example3>
    Input: Who is the author of The Old Man and the Sea ?
    From_QA:('Question: "Who is the author of The Old Man and the Sea ?", what is the sentence talks about?','Answer: literature')
    SELECT_QA:('Question: "Who is the author of The Old Man and the Sea ?" from literature, what is the sentence asks to select?','Answer: author')
    WHERE_QA:('Question: "Who is the author of The Old Man and the Sea ?" from literature select author what is the sentence requires ?,'Answer: author:Write TheOldManAndTheSea')
    SPARQL: SELECT author FROM literature WHERE author :Write TheOldManAndTheSea
    Output:
    {{
        The author of “The Old Man and the Sea” is Ernest Hemingway.
    }}
    </Example3>

    <Example4>
    Input: {input}
    """
elif parser.COT == "COT_L2M":
    COT = """<Instruction> Answer the input question. You can generate any intermedate lists and states, but the final output should only contain the exact answer(s):
    {{
        'Answer to input question...'
    }}
    </Instruction>

    <Approach>
    To answer the input question follow these steps:
    1. Find the current first sub-question need to solve.
    2. Answer the generated sub-question, and find the current first sub-question need to solve.
    3. Answer the input question.
    </Approach>

    <Examples>
    <Example1>
    Input: For what was John Houseman (who is in the Jewish ethnic group) nominated for an Academy Award for Best Picture?
    Iteration question and answering:
    {{
        Iteration 1 
        Q1: To solve "For what was John Houseman (who is in the Jewish ethnic group) nominated for an Academy Award for Best Picture ?", what we need to solve first?
        A1: Has John Houseman ever been nominated for an Academy Award for Best Picture?
        Q2: Has John Houseman ever been nominated for an Academy Award for Best Picture?
        A2: Yes

        Iteration 2
        Q1: To solve "For what was John Houseman (who is in the Jewish ethnic group) nominated for an Academy Award for Best Picture ?", we know that John Houseman have been nominated for an Academy Award for Best Picture.Then, what we need to solve next?
        A1: Which specific movie was John Houseman nominated for Best Picture ?
        Q2: Which specific movie was John Houseman nominated for Best Picture ?
        A2: Julius Caesar

        Iteration End
        Q: We know that John Houseman have been nominated for an Academy Award for Best Picture. we know that the John Houseman's movie Julius Caesar win an Academy Award for Best Picture. So,  For what was John Houseman (who is in the Jewish ethnic group) nominated for an Academy Award for Best Picture ?
        A: Julius Caesar
    }}
    Output: 
    {{
    'John Houseman, being a prominent figure in the film industry, was nominated for an Academy Award for Best Picture as a producer. His nomination was for the film “Julius Caesar.,” which was released in 1973.'
    }}
    </Example1>

    <Example2>
    Input: What is the mascot of the team that has Nicholas S. Zeppos as its leader?
    Iteration question and answering:
    {{
        Iteration 1
        Q1: To solve "What is the mascot of the team that has Nicholas S. Zeppos as its leader?", what do we need to solve first?
        A1: Identify the team led by Nicholas S. Zeppos.
        Q2: What team is led by Nicholas S. Zeppos?
        A2: Vanderbilt University

        Iteration 2
        Q1: To solve "What is the mascot of the team that has Nicholas S. Zeppos as its leader?", knowing that Nicholas S. Zeppos leads Vanderbilt University, what do we need to solve next?
        A1: Find out the mascot of Vanderbilt University's team.
        Q2: What is the mascot of Vanderbilt University's team?
        A2: Commodore

        Iteration End
        Q: Knowing that Nicholas S. Zeppos leads Vanderbilt University, and Vanderbilt University's team mascot is the Commodore, what is the mascot of the team that has Nicholas S. Zeppos as its leader?
        A: Commodore
    }}
    Output:
    {{
        Nicholas S. Zeppos served as the Chancellor of Vanderbilt University from 2008 to 2019. The Vanderbilt University athletic teams are known as the Vanderbilt Commodores, and their mascot is a personification of a naval officer Commodore named Mr. C or "Mr. Commodore".
    }}
    </Example2>

    <Example3>
    Input: What US state has a capital named Springfield and also the Illinois River?
    Iteration question and answering:
    {{
        Iteration 1
        Q1: To solve "What US state has a capital named Springfield and also the Illinois River?", what do we need to solve first?
        A1: Identify which US states have a capital named Springfield.
        Q2: Which US states have a capital named Springfield?
        A2: Illinois

        Iteration 2
        Q1: To solve "What US state has a capital named Springfield and also the Illinois River?", we know that Illinois has a capital named Springfield. Then, what do we need to solve next?
        A1: Determine if the Illinois River is in the state with Springfield as its capital.
        Q2: Is the Illinois River in the state of Illinois?
        A2: Yes

        Iteration End
        Q: We know that Illinois has a capital named Springfield and also has the Illinois River. So, what US state has a capital named Springfield and also the Illinois River?
        A: Illinois
    }}
    Output:
    {{
        The US state that has a capital named Springfield and is also home to the Illinois River is the state of Illinois.
    }}
    </Example3>

    <Example4>
    Input: {input}
    """
else:
    COT = """Question: What timezone is Phoenix, AZ in right now?
        Answer:Mountain Standard Time Zone.
        Question: Is coffee originally from Brazil?
        Answer: True.
        Question: 1000.0 is the number of joules per mole for what unit of energy?
        Answer: Kilojoule per mole.
        Question: {input}
        Answer:"""

#读取数据
# f =open(os.path.join("Complex-Question-Answering-Evaluation-of-GPT-family-main","datasets",parser.dataset,f"{parser.dataset}_all_question_with_label.json"),'r',encoding='utf-8')
if os.path.exists(os.path.join("answer_COT","COT",f"{parser.model}_temp_answer_{parser.COT}_{parser.dataset}.json")):
    f = open(os.path.join("answer_COT","COT",f"{parser.model}_temp_answer_{parser.COT}_{parser.dataset}.json"),'r',encoding='utf-8')
else:
    f =open(os.path.join("dataset_sampled",f"{parser.dataset}_sampled_question_1060.json"),'r',encoding='utf-8')
dataset = json.load(f)
llm = LLM("opt-30b", tensor_parallel_size=4)


#推理
time1=time.time()
n=len(dataset)


for i in tqdm(range(n)):
    if parser.model not in dataset[i]:
        prompt = dataset[i]['question']
        sampling_params = SamplingParams(temperature=0, top_p=1,max_tokens=1024)
        prompt = COT.format(input=prompt)
        ans =  llm.generate(prompt,sampling_params)
        ans = ans[0].outputs[0].text
        dataset[i][parser.model] = ans
    else:
        pass
    if i%100==0:
        data=json.dumps(dataset,indent=1)
        with open(os.path.join("answer_COT","COT",f"{parser.model}_temp_answer_{parser.COT}_{parser.dataset}.json"),"w",newline='\n') as f:
            f.write(data)
    
time2=time.time()


data=json.dumps(dataset,indent=1)
with open(os.path.join("answer_COT","COT",f"{parser.model}_answer_{parser.COT}_{parser.dataset}.json"),"w",newline='\n') as f:
    f.write(data)


logging.info(f"总共用时:{str(time2-time1)},平均用时:{str((time2-time1)/n)}",)



