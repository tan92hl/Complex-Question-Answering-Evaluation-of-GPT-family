import requests
import openai
import os
import json
import time
#CoT
Cot_naive = """<Instruction> Answer the input question. You can generate any intermedate lists and states, but the final output should only contain the exact answer(s):
{{
    Answer to input question...
}}
</Instruction>

<Approach>
To answer the input question follow these steps:
1. Generate 5 sub-questions based on the input question.
2. Answer the generated sub-questions.
3. Answer the input question.
</Approach>

<Examples>
Input: For what was John Houseman (who is in the Jewish ethnic group) nominated for an Academy Award for Best Picture ?
Sub_questions:['Who is John Houseman?','What is the Jewish ethnic group?','Was John Houseman nominated for an Academy Award','In which category was John Houseman nominated?','What was the film John Houseman was nominated for in the category of Best Picture at the Academy Awards?']
Answers_to_Sub-questions:['John Houseman (September 22, 1902 - October 31, 1988) was a highly acclaimed American actor known for his work in both film and theater. In addition to acting, he was also involved in writing, directing, and producing..','Jewish ethnic divisions refer to many distinctive communities within the world's ethnically Jewish population. Although considered a self-identifying ethnicity, there are distinct ethnic subdivisions among Jews, most of which are primarily the result of geographic branching from an originating Israelite population, mixing with local communities, and subsequent independent evolutions..','Yes.','Golden Globe Award for Best Supporting Actor.','Julius Caesar.']
Output: 
{{
    'John Houseman, being a prominent figure in the film industry, was nominated for an Academy Award for Best Picture as a producer. His nomination was for the film “Julius Caesar.,” which was released in 1973.'
}}

Input: Is coffee originally from Brazil?
Sub_questions:['What is coffee?','2.Where was coffee originally discovered?','When was coffee discovered?','How did coffee spread around the world?','When did coffee first arrive in Brazil?']
Answers_to_Sub-questions:['Coffee is a brewed drink prepared from roasted coffee beans, the seeds of berries from certain Coffea species.','Coffee was originally discovered in Ethiopia, in East Africa.','Coffee was discovered in the 9th century.','Coffee spread around the world through trade, first reaching the Arabian Peninsula, and then Europe in the 17th century.','Coffee first arrived in Brazil in the 18th century.']
Output: 
{{
    'No, coffee is not originally from Brazil. The coffee plant, Coffea, is native to the region of Ethiopia in East Africa. It is believed that coffee was first discovered and consumed in Ethiopia in the 9th century. From there, it spread to other parts of Africa, the Arabian Peninsula, and eventually to Europe and the Americas through trade and colonization. Brazil, however, became the largest coffee producer in the world during the 19th century and has played a significant role in the global coffee industry ever since.'
}}

Input: Who is the reviewer of the Georgia national football team, which is ranked 78th by FIFA?
Sub_questions:['What is the Georgia national football team?','What is the role of a reviewer in football?','What is FIFA?','What does it mean for a team to be ranked 78th by FIFA?','Who has reviewed the Georgia national football team recently?']
Answers_to_Sub-questions:['The Georgia national football team represents Georgia in international football and is governed by the Georgian Football Federation. It competes in matches and tournaments sanctioned by FIFA and UEFA.','A reviewer in football typically refers to a sports analyst or commentator who evaluates and discusses the performance of football teams and players.','FIFA (Fédération Internationale de Football Association) is the international governing body of association football, futsal, and beach soccer. It is responsible for organizing major international tournaments, including the FIFA World Cup.','Being ranked 78th by FIFA indicates that the Georgia national football team is positioned at number 78 in FIFA's global ranking system, which ranks men's national teams based on their game results.','The reviewer of the Georgia national football team could vary depending on the context. It could be a sports journalist, a football analyst, or a commentator known for analyzing international football teams.']
Output:
{{
    'The reviewer of the Georgia national football team may vary depending on the source. As of my last update, the team was managed by Willy Sagnol, a former French international footballer, from 2020 until 2021. However, please note that managerial positions can change over time, so it is always a good idea to check the current information from reliable sources.'
}}
</Examples>

Input: {input}
"""


def generate_text(message):
    openai.api_key = os.getenv('OPENAI_KEY', default="sk-kZ4KkN0y29WRqX1n8172897fF1D3451eA51fDa3bC5Bc6aD6")
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
    prompt_cot = Cot_naive.format(
                    input = content
                )
    # prompt_cot = Cot_SP.format(
    #                 input = content
    #             )
    # prompt_cot = Cot_L2M.format(
    #                 input = content
    #             )
    generate_text(prompt_cot)
    # generate_text(content)


f = json.load(open('GrailQA_all_question_with_label.json'))
for line in f[:5]:
    content = line['question']
    get_LLM_output(content)
    time.sleep(1.5)