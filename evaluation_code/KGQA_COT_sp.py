import requests
import openai
import os
import json
import time

COT_SP="""<Instruction> Answer the input question. You can generate any intermedate lists and states, but the final output should only contain the exact answer(s):
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
Input: how many major cities are there ? 
From_QA:('Question: "how many major cities are there? ", what is the sentence talks about?','Answer: city')
SELECT_QA:('Question: "how many major cities are there? " from city, what is the sentence asks to select?','Answer: count(*)')
WHERE_QA:('Question: "how many major cities are there? " from city select count(*), what is the sentence requires ?','Answer: city.population > 150,000')
SPARQL: SELECT count(*) FROM city WHERE city.population > 150,000
Output:
{{
    The number of major cities can vary depending on the criteria used to define a “major” city. Generally, major cities are often determined based on factors such as population, economic significance, cultural importance, infrastructure, and political influence. Different sources may provide different lists of major cities. For example, some common lists include the Global Cities Index, Megacity classification, or simply cities with high population numbers. According to the United Nations, as of 2021, there are more than 30 megacities (cities with a population of over 10 million) worldwide, and numerous other cities with populations ranging from millions to several hundred thousand.It’s important to note that the exact number of major cities can change over time due to urbanization, population growth, and other factors.
}}

Input: which state is the second most populous state in the United States ?
From_QA:('Question: "Which state is the second most populous state in the United States ?", what is the sentence talks about?','Answer: state')
SELECT_QA:('Question: "Which state is the second most populous state in the United States ?" from state, what is the sentence asks to select?','Answer: state.state_name')
WHERE_QA:('Question: "Which state is the second most populous state in the United States ?" from state select state.state_name, what is the sentence requires ?','Answer: {{state:isPartOf :US}} ORDER BY DESC(state.polulation) LIMIT 2 OFFSET 1')
SPARQL: SELECT state.state_name FROM state WHERE {{state :isPartOf UnitedStates}} ORDER BY DESC(state.polulation) LIMIT 2 OFFSET 1
Output:
{{
    As of the most recent data, the second most populous state in the United States is Texas. California is the most populous state, followed by Texas.
}}

Input: Who is the author of The Old Man and the Sea ?
From_QA:('Question: "Who is the author of The Old Man and the Sea ?", what is the sentence talks about?','Answer: literature')
SELECT_QA:('Question: "Who is the author of The Old Man and the Sea ?" from literature, what is the sentence asks to select?','Answer: author')
WHERE_QA:('Question: "Who is the author of The Old Man and the Sea ?" from literature select author what is the sentence requires ?,'Answer: author:Write TheOldManAndTheSea')
SPARQL: SELECT author FROM literature WHERE author :Write TheOldManAndTheSea
Output:
{{
    The author of “The Old Man and the Sea” is Ernest Hemingway.
}}
</Examples>

Input: {input}
"""


def generate_text(message):
    openai.api_key = os.getenv('OPENAI_KEY', default="sk-zi9fiEnbkYRXKY0KC6C74c04272e4a7aA4B8359239637dAf")
    openai.api_base = "https://ai-yyds.com/v1"
    
    messages = [
        {"role": "system", "content": "You are a knowledge base AI."},
        {"role": "user", "content": message},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.0,
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content

    print("summary_result:\n", result)


def get_LLM_output(content):
    # prompt_cot = Cot_naive.format(
    #                 input = content
    #             )
    # prompt_cot = Cot_SP.format(
    #                 input = content
    #             )
    prompt_cot = COT_SP.format(
                    input = content
                )
    # print(f"prompt_cot:{prompt_cot}\n")
    generate_text(prompt_cot)


f = json.load(open('GrailQA_all_question_with_label.json'))
for line in f[:5]:
    content = line['question']
    get_LLM_output(content)
    time.sleep(1.5)