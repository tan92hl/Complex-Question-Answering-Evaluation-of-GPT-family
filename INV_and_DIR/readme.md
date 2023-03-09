
# Introduction

This repository serves as a record of the results generated during the invariance test and directional expectation test experiments we conducted on the KQApro dataset. We chose to primarily focus our experiments on the KQApro dataset because it contains all the necessary types of data we required.  

We hope that these experimental results will be useful for researchers and developers working on open-domain complex question answering models, and that this repository will provide a valuable resource for evaluating and improving those models.  

Please feel free to use the data contained in this repository for your own experiments and research purposes. If you have any questions or feedback, please do not hesitate to reach out to us.  

## Invariance test (INV)


This repository contains the results of our invariance test experiments on the KQApro dataset. We primarily used methods such as changing sentence expressions and modifying words (through letter repetition and omission) for this test. We sampled 100 pieces of data on the answer type and question type for the experiment.  

The "word_change.json" file located under the INV folder contains the results of our word-changing experiments. It includes the "original_question," which is the original question, "question," which is the question after changing the word, "answer," which is the ChatGPT-generated answer, and "ground_truth," which is the actual answer to the question.  

The "sentences_paraphrase.json" file, also located under the INV folder, contains the results of our sentence paraphrasing experiments. It includes the "question," which is the original question, "new_question," which is the paraphrased question, "new_answer," which is the ChatGPT-generated answer, and "ground_truth," which is the actual answer to the question.  


## Directional Expectation test (DIR)

In the Directional Expectation test, we employ several methods to evaluate the SPARQL language, including prompting the answer type, step-by-step guidance, and changing the syntax of the reasoning type. For the answer type prompt method, we extract 70 data for each answer type and conduct experiments with step-by-step guidance. We also sample 100 pieces of data for experiments with the answer type and question type method, and experiment with the set, count, comparison (most value and sorting), and condition types by changing the syntax of reasoning type.  

Under the DIR folder, the "prompt_answer_type.json" file contains the results of prompting the answer type, with the "original_answer" field indicating the original answer, "new_answer" field indicating the result of the prompt answer type, "ground_truth" field indicating the real answer to the question, and "new_answer_type" field indicating the type of ChatGPT answer after the prompt answer type. The "step_by_step.json" file under the DIR folder records the results of ChatGPT for each noun question.  

The Inference_type folder contains the sampling data for the collection, counting, comparison (most value and sorting), and condition types, which are used to create the original data of the inference type.  


