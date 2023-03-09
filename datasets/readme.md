# Introduction

We choose to evaluate our model using an open-domain complex question answering dataset related to Wikipedia. Specifically, we curated a set of 7 different datasets for this purpose: WebQuestionSP, ComplexWebQuestion, GraphQA, GrailQA, KQApro, QALD-9, MKQA.

This file contains all the dataset files we have compiled, including two files in the CWQ, GrailQA, GraphQuestions, KQApro, QALD-9 and WQSP dataset files. 

The file ending with the "aliase_data.json" file name is the list of aliases in various languages that we obtained on the wikidata website according to groun_truth for answer matching.  

The data in the file ending with "_all_question_with_label.json" contains "ID", the question "question" of the dataset, the sparql query of the question, the answer "ans" of the question, and the labels "type_label" and "type_label" for the question and answer The first dimension represents the answer type 0-7, and each dimension of the 1-8 latitudes of "type_label" represents a question type, and the number is 1 means that the question belongs to this latitude, and a question may belong to different types at the same time.
