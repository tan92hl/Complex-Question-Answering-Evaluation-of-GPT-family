## Introduction
The code here is used to evaluate the correctness of Chatgpt and other models' answers to KB-CQA questions. As introduced in the paper, we used an enhanced exact match algorithm, and its algorithm framework diagram is as follows:

![image](https://github.com/AnonymousgitT/complex-question-answering-evaluation-of-GPT-family/assets/97523884/1303b81a-b7ef-41c1-9809-b0b13497d3a5)

## Install required packages

the following Python packages need to be installed.

```
nltk==3.7
pandas== 1.3.5
torch==1.9.0
transformers==4.30.2
scipy==1.7.3
hanlp==2.1.0
num2words==0.5.12
```

## Preparation of datasets

Before using the code, we need to have the following 3 files and set their directories correctly in the code. They are the ground truth of the dataset, the textual answers of the model to the questions, and the alias table of entities in this dataset.

The textual answers of the model to the questions can be found in the [answers_from_LLMs](answers_from_LLMs). The ground truth of the dataset and the alias table of entities can be found in the [datasets](datasets). 

Here is an example of my settings for evaluating Chatgpt's answers to the CWQ dataset:

``` python
Ground_truth_dataset_dir = 'datasets/CWQ/CWQ_all_question_with_label.json'
Models_output_dir = 'answers_from_LLMs/chatgpt/CWQ_chatgpt_answers.txt'
Dataset_aliases_dir = 'datasets/CWQ/aliase_data31158.json'
```

## Code for Evaluating Model QA Performance

The code uses mBERT for similarity matching calculations, which requires a high-performance computer and is very **time-consuming**. By **commenting out** the similarity matching calculation code and only performing Exact Match, you can still achieve very close results to the original article data.

For monolingual dataset, we recommend referring to the code in `eval_CWQ.py`, which has detailed comments. 

For multilingual datasets, please refer to the code in `eval_MKQA.py`. Since the structure of the **QALD-9 dataset** is similar to **MKQA**, you can simply modify the `eval_MKQA.py` code to use it for the **QALD-9** dataset.

## Usage of the code: 

Run the following command in a Python environment with the required packages installed:

``` python
python eval_{dataset_name}.py
```
