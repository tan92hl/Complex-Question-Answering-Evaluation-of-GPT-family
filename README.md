# Complex-Question-Answering-Evaluation-of-ChatGPT
A large-scale complex question answering evaluation of ChatGPT and similar large-language models

A framework for detailed evaluation of the ability of ChatGPT and similar large-scale language models to answer complex questions.

# Overview

To evaluate ChatGPT's ability to answer complex knowledge, we propose an evaluation framework:
First, we classify the latent features that constitute complex questions, and describe each question under test with multi-labels for identifying combinatorial reasoning.
Secondly, following the black-box test specification of CheckList proposed by Microsoft, we design an evaluation method that introduces CoT hints to measure the reasoning function and reliability of large language models in answering complex questions.
Our evaluation uses 8 real complex question answering datasets, including six English datasets and two multilingual datasets, to further analyze the potential impact of language bias.
We compared the evaluation results of ChatGPT, GPT3.5, GPT3, and T5 to identify persistent historical issues in LLMs. All data and results are available for further analysis.  

# Datasets

Given that the training data for language models (LLMs) extensively covers Wikipedia, we choose to evaluate our model using an open-domain complex question answering dataset related to Wikipedia. Specifically, we curated a set of 7 different datasets for this purpose: WebQuestionSP, ComplexWebQuestion, GraphQA, GrailQA, KQApro, QALD-9, MKQA, and the comparison models used include: GPT3 davinci-1, GPT3.5 davinci-2/davinci-3, T5.

| Monolingual datasets      | Source     | Paper     |
| ---------- | :-----------:  | :-----------: |
| WebQuestionSP(WQSP) | [download_url](https://www.microsoft.com/en-us/download/details.aspx?id=52763)| [paper_url](https://arxiv.org/pdf/2210.00063.pdf)|
| ComplexWebQuestion(CWQ)     | [download_url](https://allenai.org/data/complexwebquestions)|[paper_url](https://aclanthology.org/2022.coling-1.145.pdf)|
| GraphQA    | [download_url]     | [paper_url](https://openreview.net/pdf?id=HyxgBerKwB)     |
| GrailQA     | [download_url](https://dki-lab.github.io/GrailQA/)     | [paper_url](https://arxiv.org/pdf/2011.07743v6.pdf)     |
| KQApro     | [download_url](http://thukeg.gitee.io/kqa-pro/leaderboard.html)     | [paper_url](https://arxiv.org/abs/2007.03875)     |


| Multilingual datasets      | Source     | Paper     |
| ---------- | :-----------:  | :-----------: |
| QALD-9 | [download_url]((https://github.com/ag-sc/QALD))| [paper_url](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9815253)|
| MKQA     | [download_url](https://github.com/apple/ml-mkqa)|[paper_url](https://arxiv.org/pdf/2007.15207v2.pdf)|
