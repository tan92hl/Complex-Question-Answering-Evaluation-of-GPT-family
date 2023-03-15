# Complex-Question-Answering-Evaluation-of-ChatGPT
Evaluation of ChatGPT as a Question Answering System for Answering Complex Questions

A framework for detailed evaluation of the ability of ChatGPT and similar large-scale language models to answer complex questions.

This repository is a subproject of [KSESEU](https://github.com/KSESEU).  

If you use the code, please cite the following paper:   

**Evaluation of ChatGPT as a Question Answering System for Answering Complex Questions**  [[Arxiv]](https://arxiv.org/abs/2303.07992)

---

This repository is mainly contributed  by [Yiming Tan](https://github.com/tan92hl), [Dehai Min](https://github.com/ZhishanQ), [Yu Li](https://github.com/liyu19980601), [Wenbo Li](https://github.com/zhexuezhujiu), [Nan Hu](https://github.com/HuuuNan), Guilin Qi.

:fire::tada: We have released the answers of chatgpt and other models to a total of 194,782 questions across 8 datasets, including multiple languages in [Datasets we publish](#Datasets-we-publish).

To our knowledge(2023-3-9), this is the first public release of a large-scale Q&A dataset for chatgpt.

#  Overview

To evaluate ChatGPT's ability to answer complex knowledge, we propose an evaluation framework:
First, we classify the latent features that constitute complex questions, and describe each question under test with multi-labels for identifying combinatorial reasoning.
Secondly, following the black-box test specification of [CheckList](https://arxiv.org/abs/2005.04118) proposed by Microsoft, we design an evaluation method that introduces [CoT](https://arxiv.org/abs/2201.11903) hints to measure the reasoning function and reliability of large language models in answering complex questions.
Our evaluation uses 8 real complex question answering datasets, including six English datasets and two multilingual datasets, to further analyze the potential impact of language bias.
We compared the evaluation results of ChatGPT, GPT3.5, GPT3, and FLAN-T5 to identify persistent historical issues in LLMs. All data and results are available for further analysis.  

# Datasets we publish

We classify the answers of these models for the KBQA dataset according to dataset and model, and release them in this folder.

[answers_from_models](answers_from_models) : The response(answers) of these models(Chatgpt, Gpt3/Gpt3.5, FLAN-T5) to the KBQA datasets mentioned in [Datasets we use](#Datasets-we-use). 
<table>
  <tr>
    <th>Datasets</th>
    <th>Size</th>
    <th>Col.Size</th>
    <th>Lang</th>
  </tr>
  <tr>
    <td>KQAPro</td>
    <td style="text-align: center">117970</td>
    <td style="text-align: center">106173</td>
    <td>EN</td>
  </tr>
  <tr>
    <td>LC-quad2.0</td>
    <td style="text-align: center">26975</td>
    <td style="text-align: center">26975</td>
    <td>EN</td>
  </tr>
  <tr>
    <td>WQSP</td>
    <td style="text-align: center">4737</td>
    <td style="text-align: center">4700</td>
    <td>EN</td>
  </tr>
  <tr>
    <td>CWQ</td>
    <td style="text-align: center">31158</td>
    <td style="text-align: center">31158</td>
    <td>EN</td>
  </tr>
  <tr>
    <td>GrailQA</td>
    <td style="text-align: center">64331</td>
    <td style="text-align: center">6763</td>
    <td>EN</td>
  </tr>
  <tr>
    <td>GraphQuestions</td>
    <td style="text-align: center">4776</td>
    <td style="text-align: center">4776</td>
    <td>EN</td>
  </tr>
  <tr>
    <td>QALD-9</td>
    <td style="text-align: center">6045</td>
    <td style="text-align: center">6045</td>
    <td>Mul</td>
  </tr>
  <tr>
    <td>MKQA</td>
    <td style="text-align: center">260000</td>
    <td style="text-align: center">6144</td>
    <td>Mul</td>
  </tr>
  <tr>
    <td  style="text-align: center">Total Collected</td>
    <td colspan="3" style="text-align: center">194782</td>
  </tr>
</table>






[datasets](datasets) : 
We have processed the 8 datasets mentioned in [Datasets we use](#Datasets-we-use)  into a unified format and released them in this folder. The datasets in the unified format include the following items: question_id, question, ground_truth, SPARQL, and our added labels. Additionally, we have generated alias dictionaries from Wikipedia for the ground truth, which we can use during the evaluation.

# Datasets we use 

Given that the training data of the Language Model (LLM) covers Wikipedia extensively, we have opted to evaluate our model using open-domain complex question-answering datasets related to Wikipedia. Specifically, we have curated a set of 8 distinct datasets for this purpose, as follows:

:collision: Please note : The links in the `Source` section below refer to the original datasets as published by their respective authors. For our experiments in this paper, we have processed these datasets accordingly, including random sampling and formatting. Please download the datasets used in our experiments from this folder: [datasets](datasets).


| Monolingual datasets      | Source     | Paper     |
| ---------- | :-----------:  | :-----------: |
| WebQuestionSP(WQSP) | [Download_url](https://www.microsoft.com/en-us/download/details.aspx?id=52763)| [Paper_url](https://arxiv.org/pdf/2210.00063.pdf)|
| ComplexWebQuestion(CWQ)     | [Download_url](https://allenai.org/data/complexwebquestions)|[Paper_url](https://aclanthology.org/2022.coling-1.145.pdf)|
| GraphQuestions    | [Download_url](https://github.com/ysu1989/GraphQuestions)     | [Paper_url](https://openreview.net/pdf?id=HyxgBerKwB)     |
| GrailQA     | [Download_url](https://dki-lab.github.io/GrailQA/)     | [Paper_url](https://arxiv.org/pdf/2011.07743v6.pdf)     |
| KQApro     | [Download_url](http://thukeg.gitee.io/kqa-pro/leaderboard.html)     | [Paper_url](https://arxiv.org/abs/2007.03875)     |
| LC-quad2.0     | [Download_url](http://lc-quad.sda.tech/)     | [Paper_url](http://jens-lehmann.org/files/2019/iswc_lcquad2.pdf)     |

Multilingual dataset

| Multilingual datasets      | Source     | Paper     |
| ---------- | :-----------:  | :-----------: |
| QALD-9             | [Download_url](https://github.com/ag-sc/QALD)| [Paper_url](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9815253)|
| MKQA               | [Download_url](https://github.com/apple/ml-mkqa)|[Paper_url](https://arxiv.org/pdf/2007.15207v2.pdf)|



# CheckList Model

## Minimum Functionality Test (MFT)

We assess the LLM's ability to handle each feature in the CQA scenario through the Minimal Functional Test (MFT); we classify the answer types into 9 categories, respectively Mixed fact (MISC);Reason (WHY);Location (LOC);Time (DATE/TIME);Character (PER);Yes or no (Boolean);Number (NUM);Organization (ORG);Unable to answer (UNA)  

At the same time, we divide the labels of "reasoning type" into eight categories, which are: SetOperation; Filtering; Counting; The most valuable; Sort;  Single-hop; Multi-hop; Star-shape  

We also take into account the "language type" label that may have an impact on model performance: de; ru; pt; hi_IN; en; Fa; it; fr; ro; es; nl; pt_BR; zh cn 

We adopted a simple idea of expanding the matching range to strengthen the generalization of answer matching, including the following two operations:  

1. Subtree marking method provided by constituent tree.  

2. A strategy of exact matching between the noun phrase list and the answer list is employed.  

For the samples that did not complete the matching, we set a threshold based on the cosine similarity between phrase vectors to obtain potential correct matches. The parts above the threshold are manually judged whether the answer is right or wrong.  

## Invariance test (INV)

Invariance test means adding perturbations to the original sentence that should not change the output of the model. The main purpose of this test is to verify that ChatGPT maintains the invariance of the answer in the case of increasing disturbance. We mainly use two methods to perform the invariance test:
1. To change the spelling of words in a sentence, we imitate the habit of humans when typing sentences, and perform random letter repetition and random letter omission and stemming methods on words.  
2. Rewrite the sentence, paraphrasing the sentence without changing the original meaning of the sentence, and evaluate whether the result has changed.  


## Directional Expectation test (DIR)

Directional Expectation test refers to perturbing the input with known expected results to evaluate whether the final result is developing in the direction we expect. We mainly conduct directional expectation tests from three aspects:
1. Conduct experiments on "reasoning types", mainly on SetOperation types, Filtering types, counting types, and comparison (most value and sorting) types.   
2. Use the type of answer to guide, what type of answer we prompt to the question, and then evaluate whether the type of answer matches the type we prompt.  
3. Using a step-by-step guidance method, ask each noun or noun phrase in the sentence again, and finally ask the question again to evaluate whether the accuracy of the answer has improved. 


