# Complex-question-answering-evaluation-of-GPT-family

Can ChatGPT Replace Traditional KBQA Models? An In-depth Analysis of the Question Answering Performance of the GPT LLM Family

## Citation

If you find our code, data and paper useful, please kindly cite:
```bash
@inproceedings{TanMLLHCQ23,
  title={Can ChatGPT Replace Traditional {KBQA} Models? An In-Depth Analysis of the Question Answering Performance of the {GPT} {LLM} Family},
  author={Tan, Yiming and Min, Dehai and Li, Yu and Li, Wenbo and Hu, Nan and Chen, Yongrui and Qi, Guilin},
  journal={The Semantic Web - {ISWC} 2023 - 22nd International Semantic Web Conference, Athens, Greece, November 6-10, 2023, Proceedings, Part {I}},
  volume={14265},
  pages ={348--367},
  publisher={Springer},
  year={2023}
}
```

A framework for detailed evaluation of the ability of ChatGPT and similar large language models to answer complex questions.

We have released the answers of chatgpt and other models to a total of 194,782 questions across 8 datasets, including multiple languages in [Datasets we publish](answers_from_LLMs).

This repository is mainly contributed  by [Yiming Tan](https://github.com/tan92hl), [Dehai Min](https://github.com/ZhishanQ), [Yu Li](https://github.com/liyu19980601), [Wenbo Li](https://github.com/zhexuezhujiu), [Nan Hu](https://github.com/HuuuNan), Guilin Qi.

:fire::tada: We have released the answers of chatgpt and other models to a total of 194,782 questions across 8 datasets, including multiple languages in [Datasets we publish](#Datasets-we-publish).


#  Overview
![Framework_simple](https://user-images.githubusercontent.com/97523884/236836915-3e7042fb-b445-42be-b907-da0afe4b338b.png)

To evaluate the ability of large language models such as ChatGPT to answer KB-based complex question answering (KB-based CQA), we proposed an evaluation framework:

First, we designed multiple labels to describe the answer type, reasoning operations required to answer the question, and language type of each test question.

Second, based on the black-box testing specifications proposed by Microsoft's [CheckList](https://arxiv.org/abs/2005.04118), we designed an evaluation method that introduces [CoT](https://arxiv.org/abs/2201.11903) prompts to measure the reasoning capability and reliability of large language models when answering complex questions.

Our evaluation used eight real and complex QA datasets, including six English datasets and two multilingual datasets, to further analyze the potential impact of language type on the performance of large language models.

We compared the evaluation results of FLAN-T5, ChatGPT, GPT3, GPT3.5 series, and GPT-4 to determine the iterative benefits of different models within the GPT family and some commonalities between GPT family models and other LLMs.

## Overall results

The following table shows the performance of evaluated models on different datasets, and we also compared them with the current SOTA traditional KBQA models (fine-tuned (FT) and zero-shot (ZS)).

(When evaluating answers, we only consider two situations: answering correctly or answering incorrectly. Therefore, our Acc score is the same as our F1 score.)

<img width="549" alt="overall result" src="https://github.com/tan92hl/Complex-Question-Answering-Evaluation-of-GPT-family/assets/47051778/32b20566-0ce3-4792-97dd-5f24e8ad03d7">

# Datasets we publish
<img width="1450" alt="label_statistic" src="https://user-images.githubusercontent.com/97523884/236836031-932a9180-3c12-4f65-8b47-854fd356d2d3.png">

We classify the answers of these models for the KBQA dataset according to dataset and model, and release them in this folder.

[answers_from_LLMs](answers_from_LLMs) : The response(answers) of these models(Chatgpt, Gpt3/Gpt3.5, FLAN-T5, GPT-4) to the KBQA datasets mentioned in [Datasets we use](datasets). 
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
We have processed the 8 datasets mentioned in [Datasets we use](datasets)  into a unified format and released them in this folder. The datasets in the unified format include the following items: question_id, question, ground_truth, SPARQL, and our added labels. Additionally, we have generated alias dictionaries from Wikipedia for the ground truth, which we can use during the evaluation.

# Datasets we use 

To highlight the complexity of the testing questions and the breadth of the testing dataset, after careful consideration, we selected six representative English monolingual KBQA datasets and two multilingual KBQA datasets for evaluation.

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


# Code for ChatGPT API
We have uploaded our [code](ChatGPT_API.py) for using ChatGPT to collect answers to questions in datasets. The code uses the official OpenAI's API. If you want to learn more about APl, see OpenAI's official website for more information: https://platform.openai.com/docs/guides/chat.

# Code for evaluating model performance

We have released the code for evaluating the EM score（model performance） of the model's answers in our paper, located in the [evaluation_code](evaluation_code).
We believe it is a good reference for evaluating the correctness of generative language models in question-answering tasks.

# CheckList Model

The data for Invariance test (INV) and Directional Expectation test (DIR) are published at: [INV_and_DIR](#INV_and_DIR)

![INV_DIR](https://user-images.githubusercontent.com/97523884/236835552-62c8b615-a3c2-4b72-83ab-cf8e23d4b9f7.png)


## Minimum Functionality Test (MFT)

We assess the LLM's ability to handle each feature in the KB-based CQA scenario through the Minimal Functional Test (MFT); we classify the answer types into 9 categories, respectively Mixed fact (MISC);Reason (WHY);Location (LOC);Time (DATE/TIME);Character (PER);Yes or no (Boolean);Number (NUM);Organization (ORG);Unable to answer (UNA)  

At the same time, we divide the labels of "reasoning type" into eight categories, which are: SetOperation; Filtering; Counting; The most valuable; Sort;  Single-hop; Multi-hop; Star-shape.

We also take into account the "language type" label that may have an impact on model performance: de; ru; pt; hi_IN; en; Fa; it; fr; ro; es; nl; pt_BR; zh cn.


## Invariance test (INV)

We have designed 2 methods to generate test cases for INV:

1. Randomly introducing spelling errors into the original problem sentence.
2. Generating a question that is semantically equivalent (paraphrased) to the original problem sentence.

Then, we evaluate the invariance of the LLMs by checking the consistency of their correctness in the outputs generated from 3 inputs (The above two methods generate the question sentence and the original question).

## Directional Expectation test (DIR)

We created three modes to generate DIR test cases: 
1. replacing reasoning operation-related phrases in questions to observe LLMs' output. 
2. adding prompts for answer types to test LLMs' control over output.
3. using multi-round questioning inspired by CoT to observe LLMs' sensitivity and effectiveness with CoT prompts for different question types.

