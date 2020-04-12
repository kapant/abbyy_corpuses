import math
import nltk
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from nltk.corpus import stopwords
from tqdm import tqdm
import pandas as pd

def t_score(n_ii, n_ind, n_xx) -> float:
    n_ix, n_xi = n_ind
    p0N = n_ix * n_xi / n_xx
    return (n_ii - p0N) / math.sqrt(n_ii)


def print_samples(bigram_finder: BigramCollocationFinder, f) -> None:
    print("count metrics")
    # Bigram metrics
    bigram_measures = BigramAssocMeasures()

    # Finding best words by metrics
    f.write("Best by PMI\n")
    for i, collocation in enumerate(bigram_finder.nbest(bigram_measures.pmi, 10)):
        f.write('\t%02d. %s (%d)\n' % (i, collocation, bigram_finder.ngram_fd[collocation]))

    f.write("Best by t-score:\n")
    for i, collocation in enumerate(bigram_finder.nbest(t_score, 10)):
        f.write('\t%02d. %s (%d)\n' % (i, collocation, bigram_finder.ngram_fd[collocation]))

    f.write("Best by Dice:\n")
    for i, collocation in enumerate(bigram_finder.nbest(bigram_measures.dice, 10)):
        f.write('\t%02d. %s (%d)\n' % (i, collocation, bigram_finder.ngram_fd[collocation]))


tokenizer = nltk.tokenize.WordPunctTokenizer()
stop_words = set(stopwords.words('russian'))

all_texts = pd.read_csv("./all.csv", encoding="utf-8")["text"]

print("make finder")
bigram_finder = BigramCollocationFinder.from_documents(
        [w.lower() for w in tokenizer.tokenize(sent)] for text in tqdm(all_texts) for sent in nltk.sent_tokenize(text, language='russian'))

with open("./bigrams.txt", "w", encoding="utf-8") as f:
    f.write("all bigrams: %d\n" % bigram_finder.N)
    print_samples(bigram_finder, f)

    f.write("\nFiltrate words by punctuation, stop words and frequency\n")
    bigram_finder.apply_freq_filter(5)
    bigram_finder.apply_word_filter(lambda w: len(w) < 3 or w in stop_words)
    f.write("All bigrams after filtration: %d\n" % bigram_finder.N)
    print_samples(bigram_finder, f)
