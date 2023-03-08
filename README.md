# Complex-Question-Answering-Evaluation-of-ChatGPT
A large-scale complex question answering evaluation of ChatGPT and similar large-language models

A framework for detailed evaluation of the ability of ChatGPT and similar large-scale language models to answer complex questions.

# Overview

To evaluate ChatGPT's ability to answer complex knowledge, we propose an evaluation framework:
First, we classify the latent features that constitute complex questions, and describe each question under test with multi-labels for identifying combinatorial reasoning.
Secondly, following the black-box test specification of CheckList proposed by Microsoft, we design an evaluation method that introduces CoT hints to measure the reasoning function and reliability of large language models in answering complex questions.
Our evaluation uses 8 real complex question answering datasets, including six English datasets and two multilingual datasets, to further analyze the potential impact of language bias.
At the same time, we also compared the performance capabilities of other large models such as ChatGPT, GPT3.5, GPT3 and T5 on similar problems, and found some remaining problems of these models.

# Minimum Functionality Test (MFT)

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
2:ru
3: pt
4: hi_IN
5:en
6: Fa
7: it
8:fr
9: ro
10:es
11:nl
12: pt_BR




