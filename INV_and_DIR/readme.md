
# Introduction

This repository serves as a record of the results generated during the invariance test and directional expectation test experiments we conducted on the KQApro dataset. We chose to primarily focus our experiments on the KQApro dataset because it contains all the necessary types of data we required.  

We hope that these experimental results will be useful for researchers and developers working on open-domain complex question answering models, and that this repository will provide a valuable resource for evaluating and improving those models.  

Please feel free to use the data contained in this repository for your own experiments and research purposes. If you have any questions or feedback, please do not hesitate to reach out to us.  

## Invariance test (INV)


This repository contains the results of our invariance test experiments on the KQApro dataset. We primarily used methods such as changing sentence expressions and modifying words (through letter repetition and omission) for this test. We sampled 100 pieces of data on the answer type and question type for the experiment.  

The "word_change.json" file located under the INV folder contains the results of our word-changing experiments. It includes the "original_question," which is the original question, "question," which is the question after changing the word, "answer," which is the ChatGPT-generated answer, and "ground_truth," which is the actual answer to the question.  
Example：
<pre><code>
{
    "ID": 3710,
    "oreginal_question": "Which movie is shorter, Godzilla (the one whose production company is Tōhō) or Natural Born Killers?",
    "question": "Which movie s shorter, Godzilla (the one whos production company is Tōhō) or Natural Born Killers?",
    "answer": "Godzilla (the one produced by Tōhō) is shorter than Natural Born Killers. The 1954 original Japanese version of Godzilla has a runtime of 96 minutes, while Natural Born Killers has a runtime of 118 minutes.",
    "ground_truth": [
      "Godzilla"
    ],
    "label_type": [
      0,
      1,
      1,
      0,
      1,
      1,
      0,
      0,
      0
    ]
  },

</code></pre>

The "sentences_paraphrase.json" file, also located under the INV folder, contains the results of our sentence paraphrasing experiments. It includes the "question," which is the original question, "new_question," which is the paraphrased question, "new_answer," which is the ChatGPT-generated answer, and "ground_truth," which is the actual answer to the question.  
Example：
<pre><code>
{
        "ID": 3710,
        "question": "Which movie is shorter, Godzilla (the one whose production company is Tōhō) or Natural Born Killers?",
        "new_question": "Is Natural Born Killers longer than Godzilla (the one produced by Tōhō)?",
        "new_answer": "\n\nNo, Natural Born Killers is shorter than Godzilla (the one produced by Tōhō). Natural Born Killers has a runtime of 1 hour and 59 minutes, while Godzilla (the one produced by Tōhō) has a runtime of 1 hour and 36 minutes.",
        "ground_truth": [
            "Godzilla"
        ],
        "label_type": [
            0,
            1,
            1,
            0,
            1,
            1,
            0,
            0,
            0
        ]
    },

</code></pre>

## Directional Expectation test (DIR)

In the Directional Expectation test, we employ several methods to evaluate the SPARQL language, including prompting the answer type, step-by-step guidance, and changing the syntax of the reasoning type.  For the answer type prompt method, we extract 70 data for each answer type and conduct experiments with step-by-step guidance. We also sample 100 pieces of data for experiments with the answer type and question type method, and experiment with the set, count, comparison (most value and sorting), and condition types by changing the syntax of reasoning type.  

Under the DIR folder, the "prompt_answer_type.json" file contains the results of prompting the answer type, with the "original_answer" field indicating the original answer, "new_answer" field indicating the result of the prompt answer type, "ground_truth" field indicating the real answer to the question, and "new_answer_type" field indicating the type of ChatGPT answer after the prompt answer type.  

Example：
<pre><code>
{
    "ID": 35343,
    "question": "What is the connection between John Davis (the one whose date of birth is 1787-01-13) to Governor of Massachusetts? (Limit the length of the answer to 5 words or less.) ",
    "original_answer": "Unclear or no connection.",
    "new_answer": "John Davis was a Governor.",
    "ground_truth": "['position held']",
    "label_type": [
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      1,
      1
    ],
    "original_answer_type": "MISC",
    "new_answer_type": "PER",
    "ground_truth_type": "MISC",
    "whether_change": "True"
  },

</code></pre>

The "step_by_step.json" file under the DIR folder records the results of ChatGPT for each noun question.  
Example：
<pre><code>
{
    "ID": 41991,
    "question": "How is Andy Williams that is 173 centimeters tall related to the New England Revolution?",
    "step 0 question": "what does 'williams' mean?",
    "step 0 answer": "Williams is a surname of English origin, derived from the given name William, which means \"resolute protector\" or \"willful protector\".",
    "step 1 question": "what does 'andy' mean?",
    "step 1 answer": "Andy is a shortened form of the name Andrew, which is of Greek origin and means \"manly\" or \"warrior\".",
    "step 2 question": "what does 'andy williams' mean?",
    "step 2 answer": "Andy Williams is a proper noun and refers to a famous American singer and television personality who was active from the 1950s to the 1980s. He was known for his smooth baritone voice and popular hits such as \"Moon River\" and \"Can't Get Used to Losing You\".",
    "step 3 question": "what does 'centimeters' mean?",
    "step 3 answer": "Centimeters (cm) is a unit of measurement in the metric system. It is used to measure length or distance and is equal to one hundredth of a meter. One centimeter is approximately 0.39 inches.",
    "step 4 question": "what does '173 centimeters' mean?",
    "step 4 answer": "173 centimeters is a measurement of length or height in the metric system. It is equal to 1.73 meters or approximately 5 feet 8 inches in the imperial system.",
    "step 5 question": "what does 'the new england revolution' mean?",
    "step 5 answer": "The New England Revolution is a professional soccer team based in Foxborough, Massachusetts, United States. The team competes in Major League Soccer (MLS) and was founded in 1995 as one of the league's original ten teams. The team plays its home games at Gillette Stadium, which is also the home of the New England Patriots of the National Football League (NFL).",
    "step 6 question": "what does 'revolution' mean?",
    "step 6 answer": "Revolution is a noun that refers to a sudden, radical, or complete change in something. It can also refer to a political uprising or rebellion against a government or authority, often resulting in a change of leadership or system of government. In the context of technology, revolution can refer to a major breakthrough or innovation that fundamentally changes the way things are done.",
    "final answer": "There is no known direct relationship between Andy Williams, who is 173 centimeters tall, and the New England Revolution soccer team. They are two separate entities with no apparent connection.",
    "ground_truth": [
      "member of sports team"
    ],
    "type_label": [
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      1,
      1
    ]
  },

</code></pre>
The Inference_type folder contains the sampling data for the collection, counting, comparison (most value and sorting), and condition types, which are used to create the original data of the inference type.  


