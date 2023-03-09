# Introduction

Below this folder are answers to questions classified according to models. 

Our comparison models include Chatgpt, davinci1, davinci2, davinci3 (from [OpenAI Models](https://platform.openai.com/docs/models/overview)) 
and T5 models (From [google/flan-t5-xxl](https://huggingface.co/google/flan-t5-xxl)). 

Each model folder contains answers(responses) to 8 datasets under this model. 

# Format Description

If model's answers file is a txt file, the format of file is :  index '\t' question '\t' answer  

For example:

If model's answers file is a json file, the format of file is :  

For example:


# About Some Answers From Questions With Prompt

For the davinci3, davinci2 and T5 models, we made an English prompt on the QALD-9 dataset for comparison, and the file name ends with "QALD-9_en_prompt.json".  

On the davinci1 model, we did not handle the English prompt.  

For the ChatGPT model, we have done multiple comparison experiments. On the WQSP, QALD-9 and GraphQuestions data sets, we compared the data of February and March, and ended with "_March.txt" and "_February.txt" respectively .  

Additionally, for the QALD-9 and GraphQuestions datasets, we used Chinese prompts and English prompts for comparison, ending with "zh_cn_prompt.txt" and "en_prompt.txt" respectively.  
