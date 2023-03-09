# Introduction

This repository contains a set of eight open-domain complex question answering datasets related to Wikipedia, which were curated for the purpose of evaluating the ChatGPT model. The datasets included are WebQuestionSP, ComplexWebQuestion, GraphQA, GrailQA, KQApro, QALD-9, and MKQA.

For each dataset, there are two files ending with "_all_question_with_label.json" that contain the question ID, the question text, the SPARQL query corresponding to the question, the answer to the question, and labels for the question and answer. The labels include "type_label" and "type_label" which represent the answer type and question type, respectively. The first dimension of "type_label" represents the answer type from 0-7, while the second dimension of "type_label" represents the question type with each of the 1-8 categories, and a value of 1 indicating that the question belongs to that category. A question may belong to multiple categories at the same time.

Additionally, the file ending with "alias_data.json" contains a list of aliases in various languages that were obtained from the Wikidata website for answer matching according to the ground truth.

We hope that this repository will be useful for researchers and developers working on open-domain complex question answering. Please feel free to use these datasets for evaluation and improvement of your models.

Thank you for visiting this repository and please let us know if you have any questions or feedback.
