import os
import pandas as pd
import nltk
from deeppavlov import build_model, configs

os.environ["KERAS_BACKEND"] = "tensorflow"
model = build_model(configs.morpho_tagger.UD2_0.morpho_ru_syntagrus_pymorphy, download=True)

csvs = []
for (dirpath, dirnames, filenames) in os.walk("./reviews"):
    csvs.extend(filenames)
    break

tag_stat = {}

for file in csvs:
    data = pd.read_csv("./reviews/" + file)
    for i, text in enumerate(data["text"]):
        sents = nltk.sent_tokenize(text, language='russian')
        # writing to file for each review
        with open(f'./tags/{file.split(".")[0]}_{i}.tags', "w", encoding="utf-8") as f:
            for parse in model(sents):
                f.write(parse + "\n")
                # tag stats
                rows = parse.split("\n")
                for row in rows:
                    try:
                        tag = row.split("\t")[2]
                        if tag in tag_stat:
                            tag_stat[tag] += 1
                        else:
                            tag_stat[tag] = 1
                    except IndexError:
                        continue

# writing stat file
with open("./tag_stat.txt", "w") as f:
    amount = sum(tag_stat.values())
    print(f'tags statistic for {amount} tags')
    print("tag\tfreq\tcount")
    f.write(f'tags statistic for {amount} tags\n')
    f.write("tag\tfreq\tcount\n")
    for tag, count in tag_stat.items():
        print(f'{tag}\t{count / amount:.4f}\t{count}')
        f.write(f'{tag}\t{count / amount:.4f}\t{count}\n')