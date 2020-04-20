import math
import nltk
import pandas as pd
import numpy as np
from tqdm import tqdm
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import List

tokenizer = nltk.tokenize.WordPunctTokenizer()
stop_words = set(stopwords.words('russian'))

all_texts = pd.read_csv("./all.csv", encoding="utf-8")["text"]
words = [w.lower() for text in tqdm(all_texts) for sent in nltk.sent_tokenize(text, language='russian') for w in tokenizer.tokenize(sent)]
freq = nltk.FreqDist(words)

print("Top 10:")
for i, (w, f) in enumerate(freq.most_common(10)):
    print("  %d. %s (%d)" % (i, w, f))

print("Distribution without stop-words")
filtered_freq = nltk.FreqDist((w.lower() for w in words if len(w) > 2 and w.lower() not in stop_words))
print("Filtered top 10:")
for i, (w, f) in enumerate(filtered_freq.most_common(10)):
    print("  %d. %s (%d)" % (i, w, f))

# approximation
y = [f for _, f in freq.most_common(100)]
x = np.arange(len(y))
A = np.vstack([np.log(x + 1, dtype="float"), np.ones(len(x))]).T
m, c = np.linalg.lstsq(A, y, rcond=None)[0]

yf = [f for _, f in filtered_freq.most_common(100)]
xf = np.arange(len(yf))
A = np.vstack([np.log(xf + 1, dtype="float"), np.ones(len(xf))]).T
mf, cf = np.linalg.lstsq(A, yf, rcond=None)[0]

print("Making plot")
fig: Figure = plt.figure(figsize=(8, 6))
ax: List[Axes] = fig.subplots(1, 2)

ax[0].set(xlabel="Word rank", ylabel="Occurrences count", title="Without stop-words filtration")
ax[0].plot(list(f for w, f in freq.most_common(100)), 'o')
ax[0].plot(x, m * np.log(x + 1, dtype="float") + c, 'r')
ax[1].set(xlabel="Word rank", title="After filtration")
ax[1].plot(list(f for w, f in filtered_freq.most_common(100)), 'o')
ax[1].plot(xf, mf * np.log(xf + 1, dtype="float") + cf, 'r')

fig.savefig("./zipf.png")
print("Plot in zipf.png")
plt.show()