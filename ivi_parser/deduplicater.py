#!.env/Scripts/python.exe

__doc__ = '''Скрипт для удаления дубликатов.'''

import re
from pathlib import Path
from typing import List
from datasketch import MinHash, MinHashLSH
import pandas as pd


HASH_PERMUTATIONS_COUNT = 64


def normalize(text: str) -> List[str]:
    """Приводим строчки к детерминированному виду."""
    return re.sub(r'[^\w\s]', '', text).lower().split()


def to_minhash(words: List[str]) -> MinHash:
    """Сворачиваем текст в набор шинглов"""
    hasher = MinHash(num_perm=HASH_PERMUTATIONS_COUNT)
    for w in words:
        hasher.update(w.encode('utf-8'))
    return hasher


def main():
    print('Загружаем корпус')
    all_csv = pd.read_csv("./all.csv", encoding="utf-8")
    raw_corpus = all_csv["text"]

    print('Приводим его к стандартному виду')
    normalized_copus: List[List[str]] = [normalize(proverb) for proverb in raw_corpus]

    print('Составляем индекс для поиска дублей')
    lsh = MinHashLSH(num_perm=HASH_PERMUTATIONS_COUNT)
    deduplicated_corpus = []
    for i, words in enumerate(normalized_copus):
        words_hash = to_minhash(words)
        duplicates = lsh.query(words_hash)
        if duplicates:
            print(f'Найдены совпадения для ({i}): {raw_corpus[i]}')
            all_csv.drop(duplicates)
            for idx in duplicates:
                print(f'\t{idx:>5d}. {raw_corpus[idx]}')
        else:
            lsh.insert(i, words_hash)
            deduplicated_corpus.append(raw_corpus[i])
    print('Удалено дублей:', len(raw_corpus) - len(deduplicated_corpus))

    print(f'Сохраняем дедуплицированный корпус ({len(deduplicated_corpus)} рецензий)')
    all_csv.to_csv("./all_deduplicated.csv", encoding="utf-8", index=False)


if __name__ == "__main__":
    main()
