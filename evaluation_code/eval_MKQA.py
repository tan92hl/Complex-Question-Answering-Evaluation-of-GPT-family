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


stemmer = PorterStemmer()
Ground_truth_dataset_dir = 'completed/MKQA/mkqa_sample_label_id_final_processed.json'
Models_output_dir = 'completed/MKQA/chatgpt_answers_final.json'

debug_flag = 0
labels = []
ground_truth = {}
questions = {}
chatgpt_answers = []
num = 0

with open(Ground_truth_dataset_dir, "r", encoding='utf-8') as file:
    _data = json.load(file)
    for line in _data:
        for each_la in line["answers"]:
            ground_truth[(each_la,line["id"])] = line["answers"][each_la]
        for each_la in line["queries"]:
            questions[(each_la, line["id"])] = line["queries"][each_la]
        labels .append(line["type_label"])



with open(Models_output_dir, "r",encoding='utf-8') as file:
    _data = json.load(file)
    for line in _data:
        chatgpt_answers.append(line)
        if not line["question"] == questions[(line["language"],int(line["id"]))]:
            print(line["question"])
            print(questions[(line["language"],int(line["id"]))])

        assert line["question"] == questions[(line["language"],int(line["id"]))]


def get_synonyms(word: str):
    if word.endswith("'s"):
        word = word[:-2]
    synonyms = []
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            synonyms.append(lm.name().lower().replace('_', ' '))
    return list(set(synonyms))

def synonyms_judge(item :str,chatgpt_answer):
    res = get_synonyms(item)
    flag = 0
    for i in res :
        i = i.lower()
        if (i in chatgpt_answer) or (stemmer.stem(i) in chatgpt_answer):
            flag = 1
            break
    return flag


def aliases_judge(chatgpt_answer, ans_aliase:dict):
    if debug_flag:
        print("aliases len : {}".format(len(ans_aliase)))
    flag = 0
    for i in ans_aliase :
        i = i.lower()
        if (i in chatgpt_answer) or (stemmer.stem(i) in chatgpt_answer):
            flag = 1
            break
    return flag


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
device1 = torch.device('cuda:2' if torch.cuda.is_available() else 'cpu')
device2 = torch.device('cuda:3' if torch.cuda.is_available() else 'cpu')
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained('bert-base-multilingual-cased')
model = torch.nn.DataParallel(model, device_ids=[device1, device2])
model = model.to(device1)
model.eval()
batch_size = 64

def get_mbert_embeddings(text_list):
    data_loader = DataLoader(text_list, batch_size=batch_size)
    embeddings_list = []
    for batch in data_loader:
        inputs = tokenizer(batch, return_tensors='pt', padding=True, truncation=True)
        inputs = {key: value.to(device1) for key, value in inputs.items()}
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


def check_right(answer:dict, chatgpt_answer:str, label:list):
    if "aliases" in answer:
        ans_aliase = answer["aliases"]
    else:
        ans_aliase = []

    answer["text"] = answer["text"].lower()
    parts = answer["text"].split(' ')
    if label[0]==6:
        parts = parts[:1]
        parts[0] = parts[0].replace(',','').replace('.','')
        chatgpt_answer = chatgpt_answer.replace(',', '').replace('.', '')

    flag = 1
    for item in parts:
        if (item not in chatgpt_answer) \
                and (stemmer.stem(item) not in chatgpt_answer) \
                and (not synonyms_judge(item, chatgpt_answer)) \
                and (not aliases_judge(chatgpt_answer,ans_aliase) ) :
            flag = 0

    if (not flag) and (not has_digits_and_dashes_over_80_percent(answer)):
        flag = cos_similarity(answer["text"], chatgpt_answer)

    return flag


def check_time(answer:str, chatgpt_answer:str):
    answer = answer["text"]
    match = re.search('\d{4}', answer)
    if match:
        if debug_flag:
            print("The year number is extracted. ==== "+match.group(0)+" ==== ")
        match = str(match.group(0))
    else:
        match = "Warnging : No match"
    return match in chatgpt_answer


count = 0

ans_type_count = [0, 0, 0, 0, 0, 0, 0, 0]
ans_type_right = [0, 0, 0, 0, 0, 0, 0, 0]

multilan_counter = {}
time_ans_flag = 0
count_flag = 0
flag_list = []
for i in range(len(chatgpt_answers)):

    q_id = int(chatgpt_answers[i]['id'])
    question = chatgpt_answers[i]['question']
    chatgpt_answer = chatgpt_answers[i]['answer'].lower()
    q_la = chatgpt_answers[i]['language']
    answer = ground_truth[(q_la,q_id)]
    label = labels[q_id]

    if label[0] == 5 and q_la != "en":
        chatgpt_answer = chatgpt_answers[i]['en_answer'].lower()

    if label[0] == 3:
        time_ans_flag = 1
    else:
        time_ans_flag = 0

    if q_la not in multilan_counter:
        multilan_counter[q_la] = {'ans_type_count':[0] * 8, 'ans_type_right':[0]*8,
                                  'count':0,'sum':0 }

    flag = 0
    for _item in answer:
        if check_right(_item, chatgpt_answer, label):
            flag = 1
            break

    if time_ans_flag and flag == 0 :
        # ans is the time format , we need to rejudge .
        for _item in answer:
            if check_time(_item, chatgpt_answer):
                flag = 1
                break

    multilan_counter[q_la]['sum'] += 1
    count_flag += flag
    if flag:
        multilan_counter[q_la]['count'] += 1
        try:
            multilan_counter[q_la]['ans_type_right'][label[0]] += 1
        except TypeError as e:
            print("Error occurred with parameters: multilan_counter[{}]['ans_type_right'][{}]".format(q_la, label[0]))
            print("Error message:", e)

        for j in range(1, 9):
            if label[j]:
                multilan_counter[q_la]['que_type_right'][j-1] += 1

    multilan_counter[q_la]['ans_type_count'][label[0]] += 1


    if i % 100 == 0:
        print("EM : {}, rate: {}/{}".format(count_flag*1.0/(i+1), count_flag, i+1))

    flag_list.append(flag)


id2ans_type = ['Mixed Fact (MISC)', 'Reason (Why)', 'Location (LOC)', 'Date/Time (DATE/TIME)', 'Person (PER)',
               'Yes/No (Boolean)', 'Number (NUM)', 'Organization (ORG)']

la_acc_list = []

overall = {'ans_type_count':[0] * 8, 'ans_type_right':[0]*8,
                                  'count':0,'sum':0 }

for each_la in multilan_counter :
    la_info = multilan_counter[each_la]
    # to do : overall += la_info
    for key in la_info.keys():
        # overall[key] = overall[key] + la_info[key]
        if key == 'count' or key == 'sum':
            overall[key] += la_info[key]
            continue
        for j in range(len(overall[key])):
            overall[key][j] += la_info[key][j]

    count = la_info['count']
    num = la_info['sum']
    print("========== {} ========".format(each_la))
    print("EM:{:.4f} and specific num:{}/{}".format(count*1.0/num, count, num))
    la_acc_list.append((each_la, count*1.0/num))

    ans_type_acc = []
    ans_type_count = multilan_counter[each_la]['ans_type_count']
    ans_type_right = multilan_counter[each_la]['ans_type_right']

    for i in range(0,8):
        if ans_type_count[i] == 0:
            result = 0
        else:
            result = ans_type_right[i] * 1.0 / ans_type_count[i]
        ans_type_acc.append(result)


    ans_data = {
        "answer type": [id2ans_type[i] for i in range(0,8)],
        "EM": ans_type_acc,
        "num": ["{}/{}".format(ans_type_right[i], ans_type_count[i]) for i in range(0, 8)]
    }
    ans_df = pd.DataFrame(ans_data)

    print(ans_df)
    print()



def get_score(t):
    return t[1]


la_acc_list.sort(key=get_score, reverse=True)

print("Overall EM:{:.4f} and specific num:{}/{}".format(count_flag * 1.0 / len(chatgpt_answers), count_flag, len(chatgpt_answers)))
print("EM rank: ", la_acc_list)
print("="*20)
print(overall)

ans_type_acc = []
ans_type_count = overall['ans_type_count']
ans_type_right = overall['ans_type_right']

for i in range(0, 8):
    if ans_type_count[i] == 0:
        result = 0
    else:
        result = ans_type_right[i] * 1.0 / ans_type_count[i]
    ans_type_acc.append(result)


ans_data = {
    "answer type": [id2ans_type[i] for i in range(0, 8)],
    "EM": ans_type_acc,
    "num": ["{}/{}".format(ans_type_right[i], ans_type_count[i]) for i in range(0, 8)]
}
ans_df = pd.DataFrame(ans_data)


print(ans_df)
print()

