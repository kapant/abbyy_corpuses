import pyphen
import nltk
import collections
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords

tokenizer = nltk.tokenize.WordPunctTokenizer()
syllab_tok = pyphen.Pyphen(lang="ru_RU")
stop_words = set(stopwords.words('russian'))
vowels = "уеыаоэяию"

def syllabs_proc(syllabs, filtered=False):
    stat = {
            0: {
                "words": 0,
                "syllabs": 0,
                "tot_len": 0
            }
        }
    for word in syllabs:
        if not any(vowel in "".join(word) for vowel in vowels):
            stat[0]["words"] += 1
            stat[0]["syllabs"] += 1
            stat[0]["tot_len"] += len("".join(word))
        else:
            if len(word) not in stat:
                stat[len(word)] = {}
                stat[len(word)]["words"] = 0
                stat[len(word)]["syllabs"] = 0
                stat[len(word)]["tot_len"] = 0
            stat[len(word)]["words"] += 1
            stat[len(word)]["syllabs"] += len(word)
            stat[len(word)]["tot_len"] += len("".join(word))

    stat_arr = [{}] * (max(list(stat.keys())) + 1)
    for key, val in stat.items():
        stat_arr[key] = val

    data = pd.DataFrame(columns=["syllabs per word", "words count", "letters in syllab"])

    data["syllabs per word"] = list(range(len(stat_arr)))
    data["words count"] = list(map(lambda e: e.get("words", 0), stat_arr))
    data["letters in syllab"] = list(map(lambda e: e.get("tot_len", 0) / float(e.get("syllabs", 1)), stat_arr))

    if filtered:
        data.to_csv("./filtered_menzerath.csv", index=False)
    else:
        data.to_csv("./menzerath.csv", index=False)



all_texts = pd.read_csv("./all.csv", encoding="utf-8")["text"]
syllabs = []
filtered_syllabs = []
words = set([])
filtered_words = set([])
for text in tqdm(all_texts):
    for sent in nltk.sent_tokenize(text, language='russian'):
        for w in tokenizer.tokenize(sent):
            if w == "томсамомсайтепрокинопрокоторыйстолькописалиосенью":
                print(text)
            words.add(w)
            if w not in stop_words:
                filtered_words.add(w)

for w in tqdm(words):
    arr = syllab_tok.inserted(w.lower(), hyphen="|").split("|")
    syllabs.append(arr)

for w in tqdm(filtered_words):
    arr = syllab_tok.inserted(w.lower(), hyphen="|").split("|")
    if len(arr) > 15:
        # longest word "томсамомсайтепрокинопрокоторыйстолькописалиосенью"
        print(w)
    filtered_syllabs.append(arr)

syllabs_proc(syllabs)
syllabs_proc(filtered_syllabs, True)