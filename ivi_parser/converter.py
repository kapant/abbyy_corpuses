from os import walk
import pandas as pd
import nltk
tokenizer = nltk.tokenize.WordPunctTokenizer()

csvs = []
for (dirpath, dirnames, filenames) in walk("./reviews"):
    csvs.extend(filenames)
    break

stat = {
    "reviews": 0,
    "films": len(csvs),
    "words": 0
}

vocab = {}

def proc(text):
    tokens = tokenizer.tokenize(text.lower())
    stat["words"] += len(tokens)
    for token in tokens:
        if token in vocab:
            vocab[token] += 1
        else:
            vocab[token] = 1
    return " ".join(tokens)

data = pd.DataFrame(columns=["rating", "title", "text"])

for fname in csvs:
    cur_data = pd.read_csv("./reviews/" + fname)
    cur_data["text"] = cur_data["text"].apply(proc)
    stat["reviews"] += len(cur_data["text"])
    data = pd.concat([data, cur_data])

data.to_csv("./all.csv", encoding="utf-8", index=False)

with open("./stat.txt", "w") as f:
    f.write("num of reviews: " + str(stat["reviews"]) + "\n")
    f.write("num of films: " + str(stat["films"]) + "\n")
    f.write("num of words: " + str(stat["words"]) + "\n")
    f.close()

with open("./vocab.txt", "w") as f:
    for (key, item) in vocab.items():
        f.write(key + ": " + str(item) + "\n")
    f.close()
