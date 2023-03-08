# Complex-Question-Answering-Evaluation-of-ChatGPT
A large-scale complex question answering evaluation of ChatGPT and similar large-language models

A framework for detailed evaluation of the ability of ChatGPT and similar large-scale language models to answer complex questions.

# Overview

To evaluate ChatGPT's ability to answer complex knowledge, we propose an evaluation framework:
First, we classify the latent features that constitute complex questions, and describe each question under test with multi-labels for identifying combinatorial reasoning.
Secondly, following the black-box test specification of CheckList proposed by Microsoft, we design an evaluation method that introduces CoT hints to measure the reasoning function and reliability of large language models in answering complex questions.
Our evaluation uses 8 real complex question answering datasets, including six English datasets and two multilingual datasets, to further analyze the potential impact of language bias.
At the same time, we also compared the performance capabilities of other large models such as ChatGPT, GPT3.5, GPT3 and T5 on similar problems, and found some remaining problems of these models.

# CheckList Model

## Minimum Functionality Test (MFT)

We assess the LLM's ability to handle each feature in the CQA scenario through the Minimal Functional Test (MFT); we classify the answer types into 9 categories, respectively  
0: Mixed fact (MISC);  
1: Reason (WHY);  
2: Location (LOC);  
3: Time (DATE/TIME);  
4: Character (PER);  
5: Yes or no (Boolean);  
6: Number (NUM);  
7: Organization (ORG);  
8: Unable to answer (UNA)  

At the same time, we divide the labels of "reasoning type" into eight categories, which are:  
0 : SetOperation  
1 : Filtering  
2 : Counting  
3: The most valuable  
4: Sort  
5: Single-hop  
6: Multi-hop  
7: Star-shape  

We also take into account the "language type" label that may have an impact on model performance:  
1: de  
2: ru  
3: pt  
4: hi_IN  
5: en  
6: Fa  
7: it  
8: fr  
9: ro  
10: es  
11: nl  
12: pt_BR  

We adopted a simple idea of expanding the matching range to strengthen the generalization of answer matching, including the following two operations:  

Subtree marking method provided by constituent tree.  

A strategy of exact matching between the noun phrase list and the answer list is employed.  

For the samples that did not complete the matching, we set a threshold based on the cosine similarity between phrase vectors to obtain potential correct matches. The parts above the threshold are manually judged whether the answer is right or wrong.  

## Invariance test (INV)

Invariance test means adding perturbations to the original sentence that should not change the output of the model. The main purpose of this test is to verify that ChatGPT maintains the invariance of the answer in the case of increasing disturbance, so as to prove the robustness of the model. We mainly use two methods to perform the invariance test. This test is mainly on the type of answer conduct:
1. To change the spelling of words in a sentence, we imitate the habit of humans when typing sentences, and perform random letter repetition and random letter omission and stemming methods on words.  
2. Rewrite the sentence, paraphrasing the sentence without changing the original meaning of the sentence, and evaluate whether the result has changed.  


## Directional Expectation test (DIR)

Directional Expectation test refers to perturbing the input with known expected results to evaluate whether the final result is developing in the direction we expect. We mainly conduct directional expectation tests from three aspects:
1. Conduct experiments on "reasoning types", mainly on SetOperation types, Filtering types, counting types, and comparison (most value and sorting) types. Definitely; on the comparison type, it is mainly to modify the qualifier, change the highest level to the second level, and consider changing it to the Boolean type on the counting type. These changes are all observed through sparql to change in the direction we expected.  
2. Use the type of answer to guide, what type of answer we prompt to the question, and then evaluate whether the type of answer matches the type we prompt.  
3. Using a step-by-step guidance method, ask each noun or noun phrase in the sentence again, and finally ask the question again to evaluate whether the accuracy of the answer has improved.  

# Experiments

Given that the training data of the Language Model (LLM) covers Wikipedia extensively, we have opted to evaluate our model using open-domain complex question-answering datasets related to Wikipedia. Specifically, we have curated a set of 7 distinct datasets for this purpose.  

Given that the training data for language models (LLMs) extensively covers Wikipedia, we choose to evaluate our model using an open-domain complex question answering dataset related to Wikipedia. Specifically, we curated a set of 7 different datasets for this purpose: WebQuestionSP, ComplexWebQuestion, GraphQA, GrailQA, KQApro, QALD-9, MKQA, with moral comparison models including: GPT3 davinci-1, GPT3.5 davinci -2/davinci-3, T5.  




