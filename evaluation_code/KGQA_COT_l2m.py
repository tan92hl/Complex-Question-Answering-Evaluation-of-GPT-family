import requests
import openai
import os
import time
import json

Cot_L2M = """<Instruction> Answer the input question. You can generate any intermedate lists and states, but the final output should only contain the exact answer(s):
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
Input: what is the role of opera designer gig who designed the telephone / the medium?
Iteration question and answering:
{{
    Iteration 1
    Q1: To solve "What is the role of the opera designer Gig who designed The Telephone/The Medium?", what do we need to solve first?
    A1: Identify who Gig, the opera designer, is.
    Q2: Who is Gig, the opera designer?
    A2: Gig is an opera designer known for their work on operas such as The Telephone/The Medium.

    Iteration 2
    Q1: To solve "What is the role of the opera designer Gig who designed The Telephone/The Medium?", knowing that Gig is an opera designer who worked on The Telephone/The Medium, what do we need to solve next?
    A1: Define the specific role or responsibilities of an opera designer in a production.
    Q2: What are the specific roles or responsibilities of an opera designer in a production?
    A2: The role of an opera designer includes creating the visual aspects of the production, such as set design, costumes, and sometimes lighting.

    Iteration 3
    Q1: To solve "What is the role of the opera designer Gig who designed The Telephone/The Medium?", knowing the specific roles of an opera designer, what do we need to solve next?
    A1: Determine Gig's specific contributions to The Telephone/The Medium.
    Q2: What were Gig's specific contributions to The Telephone/The Medium as an opera designer?
    A2: Gig was responsible for designing the set and costumes for The Telephone/The Medium.

    Iteration End
    Q: We know Gig is an opera designer who worked on The Telephone/The Medium and that the role of an opera designer includes designing sets and costumes. What is the role of opera designer Gig who designed The Telephone/The Medium?
    A: Gig's role was to design the set and costumes for The Telephone/The Medium.
}}
Output:
{{
    Gig's role was to design the set and costumes for The Telephone/The Medium.
}}
</Examples4>
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
    prompt_cot = Cot_L2M.format(
                    input = content
                )
    # print(f"prompt_cot:{prompt_cot}\n")
    generate_text(prompt_cot)


f = json.load(open('GrailQA_all_question_with_label.json'))
for line in f[:5]:
    content = line['question']
    get_LLM_output(content)
    time.sleep(1.5)