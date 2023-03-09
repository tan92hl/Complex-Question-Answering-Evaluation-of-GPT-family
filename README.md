# Complex-Question-Answering-Evaluation-of-ChatGPT
A large-scale complex question answering evaluation of ChatGPT and similar large-language models

A framework for detailed evaluation of the ability of ChatGPT and similar large-scale language models to answer complex questions.

This repository is a subproject of [KSESEU](https://github.com/KSESEU).  

If you use the code, please cite the following paper:  


This repository is mainly contributed  by [Yiming Tan](https://github.com/tan92hl), [Dehai Min](https://github.com/ZhishanQ), [Yu Li](https://github.com/liyu19980601), [Wenbo Li](https://github.com/zhexuezhujiu), [Nan Hu](https://github.com/HuuuNan) Guilin Qi.



# Overview

To evaluate ChatGPT's ability to answer complex knowledge, we propose an evaluation framework:
First, we classify the latent features that constitute complex questions, and describe each question under test with multi-labels for identifying combinatorial reasoning.
Secondly, following the black-box test specification of [CheckList](https://arxiv.org/abs/2005.04118) proposed by Microsoft, we design an evaluation method that introduces [CoT](https://arxiv.org/abs/2201.11903) hints to measure the reasoning function and reliability of large language models in answering complex questions.
Our evaluation uses 8 real complex question answering datasets, including six English datasets and two multilingual datasets, to further analyze the potential impact of language bias.
We compared the evaluation results of ChatGPT, GPT3.5, GPT3, and T5 to identify persistent historical issues in LLMs. All data and results are available for further analysis.  

# Datasets

Given that the training data for language models (LLMs) extensively covers Wikipedia, we choose to evaluate our model using an open-domain complex question answering dataset related to Wikipedia. Specifically, we curated a set of 7 different datasets for this purpose: WebQuestionSP, ComplexWebQuestion, GraphQA, GrailQA, KQApro, QALD-9, MKQA, and the comparison models used include: GPT3 davinci-1, GPT3.5 davinci-2/davinci-3, T5.

| Monolingual datasets      | Source     | Paper     |
| ---------- | :-----------:  | :-----------: |
| WebQuestionSP(WQSP) | [download_url](https://www.microsoft.com/en-us/download/details.aspx?id=52763)| [paper_url](https://arxiv.org/pdf/2210.00063.pdf)|
| ComplexWebQuestion(CWQ)     | [download_url](https://allenai.org/data/complexwebquestions)|[paper_url](https://aclanthology.org/2022.coling-1.145.pdf)|
| GraphQA    | [download_url](https://github.com/ysu1989/GraphQuestions)     | [paper_url](https://openreview.net/pdf?id=HyxgBerKwB)     |
| GrailQA     | [download_url](https://dki-lab.github.io/GrailQA/)     | [paper_url](https://arxiv.org/pdf/2011.07743v6.pdf)     |
| KQApro     | [download_url](http://thukeg.gitee.io/kqa-pro/leaderboard.html)     | [paper_url](https://arxiv.org/abs/2007.03875)     |

Multilingual dataset

| Multilingual datasets      | Source     | Paper     |
| ---------- | :-----------:  | :-----------: |
| QALD-9             | [download_url](https://github.com/ag-sc/QALD)| [paper_url](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9815253)|
| MKQA               | [download_url](https://github.com/apple/ml-mkqa)|[paper_url](https://arxiv.org/pdf/2007.15207v2.pdf)|

We make the resources of datasets public and classify them according to dataset type and model type.  
Please visit this [folder]() for specific information classified by dataset and this [folder]() for specific information classified by model.The folder contains the detailed structure and organization of our dataset.


# CheckList Model

## Minimum Functionality Test (MFT)

We assess the LLM's ability to handle each feature in the CQA scenario through the Minimal Functional Test (MFT); we classify the answer types into 9 categories, respectively Mixed fact (MISC);Reason (WHY);Location (LOC);Time (DATE/TIME);Character (PER);Yes or no (Boolean);Number (NUM);Organization (ORG);Unable to answer (UNA)  

At the same time, we divide the labels of "reasoning type" into eight categories, which are: SetOperation;Filtering;Counting;The most valuable;Sort  ;Single-hop;Multi-hop;Star-shape  

We also take into account the "language type" label that may have an impact on model performance: de;ru;pt;hi_IN;en;Fa;it;fr;ro;es;nl;pt_BR  

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


