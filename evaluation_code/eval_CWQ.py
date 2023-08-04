from nltk.corpus import wordnet
import json,nltk
from nltk.stem import PorterStemmer
import time
import pandas as pd
import re,torch
from transformers import BertTokenizer, BertModel
from scipy.spatial.distance import cosine
from torch.utils.data import DataLoader
import hanlp


Ground_truth_dataset_dir = 'completed/CWQ/CWQ_all_question_with_label.json'
Models_output_dir = 'completed/CWQ/chatgpt_answers.txt'
Dataset_aliases_dir = 'completed/CWQ/aliase_data31158.json'

debug_flag = 0
questions_and_answers = []
models_answers = []
aliases_dict = []

# Read the ground truth of the dataset
with open(Ground_truth_dataset_dir, "r", encoding='utf-8') as file:
    _data = json.load(file)
    questions_and_answers = [{'question': line['question'], 'answer': line['ans'], 'type_label': line['type_label']} for line in _data]

# Read the model's response (the answer given by the model)
with open(Models_output_dir, "r",encoding='utf-8') as file:
    num = 0
    for line in file:
        parts = line.split("\t")
        ans = parts[2].rstrip().lstrip()
        if parts[1].rstrip().lstrip()!=questions_and_answers[num]['question'].rstrip().lstrip():
            print("An anomaly occurred when verifying the consistency of the question.")
            print("Question id: {}:\nQuestion input to the model:{}\nOriginal problem:{}".format(num,parts[1].rstrip().lstrip(),questions_and_answers[num]['question']))
            time.sleep(5)
        assert parts[1].rstrip().lstrip() == questions_and_answers[num]['question'].rstrip().lstrip()
        num += 1
        models_answers.append(ans)

# Read the alias dictionary of the dataset
with open(Dataset_aliases_dir, "r",encoding='utf-8') as file:
    aliases_dict = json.load(file)

# Judge if the data lengths are equal (to verify the correctness of the data).
print(len(questions_and_answers))
print(len(models_answers))
assert len(models_answers) == len(questions_and_answers)


# Obtain synonyms of the vocabulary in WordNet.
def get_synonyms(word: str):
    word = word[:-2] if word.endswith("'s") else word
    return list(set(lm.name().lower().replace('_', ' ') for syn in wordnet.synsets(word) for lm in syn.lemmas()))


# Judge if a synonym of a word appears in the answer given by the model.
# Create a stemmer
stemmer = PorterStemmer()
def synonyms_judge(item: str, models_answer: str) -> int:
    synonyms = [syn.lower() for syn in get_synonyms(item)]
    return any(syn in models_answer or stemmer.stem(syn) in models_answer for syn in synonyms)


# Judge if an alias of the standard answer appears in the answer provided by the model.
def aliases_judge(models_answer, ans_aliase: dict):
    return any(i.lower() in models_answer or stemmer.stem(i.lower()) in models_answer for i in ans_aliase)


# Using Syntactic Parsing Tree to Extract Noun Phrases from Text
HanLP = hanlp.load('CTB9_CON_FULL_TAG_ELECTRA_SMALL')
def keywords_extraction_hanlp(context_seq):
    def preprocess_seq(seq):
        new_seq = []
        seq = seq.split(' ')
        for s in seq:
            punctuation = re.findall(r'[,\.\?!;:]', s)
            if punctuation:
                try:
                    float(s)
                    new_seq.append(s)
                except:
                    s = s.replace(punctuation[0], ' ' + punctuation[0])
                    for subs in s.split(' '):
                        new_seq.append(subs)
            else:
                new_seq.append(s)
        return new_seq

    def list2phrase(alist):
        phrase = ''
        for p in alist:
            phrase += p + ' '
        return phrase[:-1]

    phraselist = []
    result = HanLP(preprocess_seq(context_seq))
    tree = result[0]
    for subtree in tree.subtrees(lambda t: 'NP' in t.label()):
        phrase = subtree.leaves()
        phrase = list2phrase(phrase)
        phraselist.append(phrase.lower())

    filter_words = ['the', 'a', 'an', "what", "which", "who"]
    result = [word for word in phraselist if word.lower() not in filter_words]
    phraselist = list(set(result))
    phraselist = list(phraselist)
    # print(len(phraselist))
    if len(phraselist) == 0:
        phraselist.append(context_seq)
    return phraselist


# Calculate the cosine similarity between these two vectors.
def cosine_similarity(a, b):
    return 1 - cosine(a, b)

# Load the bert-base-multilingual model;
# choose between using GPU or CPU depending on your device.
device = torch.device('cuda:2' if torch.cuda.is_available() else 'cpu')
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained('bert-base-multilingual-cased')
model = model.to(device)
model.eval()

# Choose the batch_size according to your GPU.
batch_size = 16


# Obtain the embedding vector of the text in mBERT.
def get_mbert_embeddings(text_list):
    data_loader = DataLoader(text_list, batch_size=batch_size)
    embeddings_list = []
    for batch in data_loader:
        inputs = tokenizer(batch, return_tensors='pt', padding=True, truncation=True)
        inputs = {key: value.to(device) for key, value in inputs.items()}
        with torch.cuda.amp.autocast():
            outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().cpu().numpy()
        embeddings_list += [ item for item in embeddings]
        # print(embeddings)
    return embeddings_list


# Judge if the cosine similarity of the two texts is greater than the empirical threshold.
def cos_similarity(answer:str, models_answer):
    reference_embeddings = get_mbert_embeddings([answer])
    # Check if models_answer is a list
    if isinstance(models_answer, list):
        candidate_embeddings = get_mbert_embeddings(models_answer)
    else:
        candidate_embeddings = get_mbert_embeddings(keywords_extraction_hanlp(models_answer))

    max_similarity = max(cosine_similarity(ref_emb, cand_emb) for ref_emb in reference_embeddings for cand_emb in
                         candidate_embeddings)
    similarity_threshold = 0.78  # empirical threshold
    return bool(max_similarity >= similarity_threshold)


# Judge if the number of digits and hyphens in the text is greater than 80%.
# If it's greater than 80%, then it's not suitable to use cosine similarity to calculate QA correctness.
def has_digits_and_dashes_over_80_percent(string):
    total_chars = len(string)
    if total_chars == 0:
        return False
    num_digits_and_dashes = sum(c.isdigit() or c == '-' for c in string)
    percentage = (num_digits_and_dashes / total_chars) * 100
    return percentage >= 80


# Evaluate the correctness of the model's answer to the question.
def check_right(answer:str, models_answer:str, label:list):
    if answer.isdigit():
        models_answer = models_answer.replace(',', '').replace('.', '').lower()
        models_answer = models_answer.split()  # Split the sentence into words.

    ans_aliase = aliases_dict.get(answer, []) + [answer]
    answer = answer.lower()
    parts = answer.split(' ')
    flag = 1

    for item in parts:
        if (item not in models_answer) \
                and (stemmer.stem(item) not in models_answer) \
                and (not synonyms_judge(item, models_answer)) \
                and (not aliases_judge(models_answer, ans_aliase)) :
            flag = 0

    if (not flag) and (not has_digits_and_dashes_over_80_percent(answer)):
        flag = cos_similarity(answer, models_answer)

    return flag


#  Use this function for special judgment on ground truth answers that are dates (such as those containing only the year).
def check_date(answer:str, models_answer:str):
    answer = answer.lower()
    match = re.search('\d{4}', answer)
    if match:
        if debug_flag:
            print("The year number is extracted. ==== "+match.group(0)+" ==== ")
        match = str(match.group(0))
    else:
        match = "Warnging : No match"
    return match in models_answer


# Displaying the results from a unified labeling perspective
def display_labeled_results(ans_type_count, ans_type_right, que_type_count, que_type_right):
    id2ans_type = ['Mixed Fact (MISC)', 'Reason (Why)', 'Location (LOC)', 'Date/Time (DATE/TIME)', 'Person (PER)',
                   'Yes/No (Boolean)', 'Number (NUM)', 'Organization (ORG)']
    id2que_type = ['Set', 'Condition', 'Counting', 'Extreme Value', 'Sorting', 'Single Hop', 'Multi Hop', 'Star-shaped']

    ans_type_acc = []
    for i in range(0, 8):
        if ans_type_count[i] == 0:
            result = 0
        else:
            result = ans_type_right[i] * 1.0 / ans_type_count[i]
        ans_type_acc.append(result)

    que_type_acc = []
    for i in range(0,8):
        if que_type_count[i] == 0:
            result = 0
        else:
            result = que_type_right[i]*1.0/que_type_count[i]
        que_type_acc.append(result)

    ans_data = {
        "answer type": [id2ans_type[i] for i in range(0, 8)],
        "EM Score": ans_type_acc,
        "num": ["{}/{}".format(ans_type_right[i], ans_type_count[i]) for i in range(0, 8)]
    }
    ans_df = pd.DataFrame(ans_data)

    que_data = {
        "question type": [id2que_type[i] for i in range(0, 8)],
        "EM Score": que_type_acc,
        "num": ["{}/{}".format(que_type_right[i], que_type_count[i]) for i in range(0, 8)]
    }
    que_df = pd.DataFrame(que_data)
    print(ans_df)
    print()
    print(que_df)
    print()


def evaluation():
    count = 0
    ans_type_count = [0, 0, 0, 0, 0, 0, 0, 0]
    ans_type_right = [0, 0, 0, 0, 0, 0, 0, 0]
    que_type_count = [0, 0, 0, 0, 0, 0, 0, 0]
    que_type_right = [0, 0, 0, 0, 0, 0, 0, 0]
    flag_list = []

    for i in range(len(models_answers)):
        question = questions_and_answers[i]['question']
        answer = questions_and_answers[i]['answer']
        models_answer = models_answers[i].lower()
        label = questions_and_answers[i]['type_label']
        flag = 0

        time_ans_flag = 1 if label[0] == 3 else 0

        for _item in answer:
            if check_right(_item, models_answer,label):
                flag = 1
                break

        if time_ans_flag and flag == 0 :
            # ans is the time format , we need to rejudge .
            for _item in answer:
                if check_date(_item, models_answer):
                    flag = 1
                    break

        if flag:
            count += 1
            ans_type_right[label[0]] += 1
            for j in range(1, 9):
                if label[j]:
                    que_type_right[j-1] += 1

        ans_type_count[label[0]] += 1
        for j in range(1, 9):
            if label[j]:
                que_type_count[j - 1] += 1

        if i % 100 == 0:
            print("EM Score : {}, rate: {}/{}".format(count*1.0/(i+1), count, i+1))

        flag_list.append(flag)


    num = len(models_answers)
    print()
    print("EM Score:{:.4f} and specific num:{}/{}".format(count*1.0/num, count, num))
    print()
    display_labeled_results(ans_type_count, ans_type_right, que_type_count, que_type_right)


def main():
    evaluation()


if __name__ == '__main__':
    main()