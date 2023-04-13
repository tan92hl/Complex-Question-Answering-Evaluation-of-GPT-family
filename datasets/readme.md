# Introduction

This repository contains a set of eight open-domain complex question answering datasets related to Wikipedia, which were curated for the purpose of evaluating the ChatGPT model. The datasets included are WebQuestionSP, ComplexWebQuestion, GraphQuestions, GrailQA, KQApro, QALD-9, LC-quad2.0 and MKQA.

For each dataset, there are two files ending with "_all_question_with_label.json" that contain the question ID, the question text, the SPARQL query corresponding to the question, the answer to the question, and labels for the question and answer. Labels include "type_label" for questions and "type_label" for answers.The first dimension of "type_label" represents the answer type of 0-7. Specifically, the meaning of each number is:   
0: mixed fact (MISC); 1: reason (Why); 2: location (LOC); 3: Time (DATE/TIME); 4: Character (PER); 5: Right and wrong (Boolean); 6: Number (NUM); 7: Organization (ORG).  
The second dimension of "type_label" represents the type of the question. There are 1-8 categories, and a value of 1 indicates that the question belongs to this category. A question may belong to multiple categories at the same time. Specifically, the meaning of each dimension is:   
1: Collection; 2: Condition; 3: Count; 4: Most Value; 5: Sorting; 6: Single Hop; 7: Multi Hop, 8: Star.

Example：
<pre><code>
{
        "ID": 0,
        "question": "what does jamaican people speak",
        "sparql": "PREFIX ns: <http://rdf.freebase.com/ns/>\nSELECT DISTINCT ?x\nWHERE {\nFILTER (?x != ns:m.03_r3)\nFILTER (!isLiteral(?x) OR lang(?x) = '' OR langMatches(lang(?x), 'en'))\nns:m.03_r3 ns:location.country.languages_spoken ?x .\n}\n",
        "ans": [
            "Jamaican English",
            "Jamaican Creole English Language"
        ],
        "type_label": [
            0,
            0,
            1,
            0,
            0,
            0,
            1,
            0,
            0
        ]
    },
</code></pre>

Additionally, the file ending with "alias_data.json" contains a list of aliases in various languages that were obtained from the Wikidata website for answer matching according to the ground truth.

Within the LC-Quad2.0 dataset, there is an "Other_materials" folder containing two subfolders: "question_with_ground_truth_raw" and "question_with_ground_truth_processed." The former likely includes the original training and test data, while the latter may contain processed versions of this data.

We hope that this repository will be useful for researchers and developers working on open-domain complex question answering. Please feel free to use these datasets for evaluation and improvement of your models.

Thank you for visiting this repository and please let us know if you have any questions or feedback.
