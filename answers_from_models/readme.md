# Introduction

Below this folder are answers to questions classified according to models. 

Our comparison models include Chatgpt, davinci1, davinci2, davinci3 (from [OpenAI Models](https://platform.openai.com/docs/models/overview)) 
, FLAN-T5 (From [google/flan-t5-xxl](https://huggingface.co/google/flan-t5-xxl)) and GPT-4 models. 

Each model folder contains answers(responses) to 8 datasets under this model. 

# Format Description

If model's answers file is a txt file, the format of file is :  index '\t' question '\t' answer  

For example:  
<pre><code>
8	What has alternative rock in common with Greg Graffin?	Greg Graffin is a musician who is often associated with the alternative rock genre, specifically as the lead singer and songwriter of the punk rock band Bad Religion.
</code></pre>

If the file is a json file, an example of the format of the file is as follows:  

<pre><code>
{
        "id": "0",  
        "language": "fr",  
        "question": "Quel est le fuseau horaire de Salt Lake City?",  
        "answer": "Le fuseau horaire de Salt Lake City est Mountain Time Zone (MT)."  
}
</code></pre>

# About Some Answers From Questions With Prompt

For the davinci3, davinci2 and FLAN-T5 models, we made an English prompt on the QALD-9 dataset for comparison, and the file name ends with "QALD-9_en_prompt.json".  

On the davinci1 model, we did not handle the English prompt.  

For the ChatGPT model, we have done multiple comparison experiments. On the WQSP, QALD-9 and GraphQuestions data sets, we compared the data of February and March, and ended with "_March.txt" and "_February.txt" respectively .  

Additionally, for the QALD-9 and GraphQuestions datasets, we used Chinese prompts and English prompts for comparison, ending with "zh_cn_prompt.txt" and "en_prompt.txt" respectively.  

:fire:At the same time, we also tested on the newly released GPT-4. Due to the limitation of OpenAI, we extracted 500 data from each data set for testing. The format of the test data results is the same as that of ChatGPT.
