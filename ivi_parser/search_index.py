import os
from pathlib import Path
from typing import Iterable

import whoosh
import whoosh.writing
from whoosh.fields import TEXT, NUMERIC

from tqdm import tqdm
import pandas as pd


def add_to_index(proverbs: Iterable,
                 idx_writer: whoosh.writing.IndexWriter) -> None:
    """Функция добавления в индекс"""
    for i, row in enumerate(proverbs):
        idx_writer.add_document(review_id=i,
                                review=row["text"],
                                movie=row["title"],
                                rating=row["rating"])


def main() -> None:
    """Точка входа в приложение"""
    # Создаём папку с индексом
    print('Создаём папки...')
    root = Path('.')
    idx_dir = root / 'index'
    idx_dir.mkdir(parents=True, exist_ok=True)

    # Открываем корпус
    print('Открываем корпус')
    all_csv = pd.read_csv("./all_deduplicated.csv", encoding="utf-8")
    proverbs = []
    for _, row in all_csv.iterrows():
        row["rating"] = float(row["rating"].replace(",", "."))
        proverbs.append(row)
    
    # Открываем и заполняем индекс
    print('Заполняем индекс')
    text_analyser = whoosh.analysis.StandardAnalyzer(stoplist=None, minsize=None) \
        | whoosh.analysis.StemFilter(lang='ru')
    schema = whoosh.fields.Schema(review_id=NUMERIC(unique=True, stored=True),
                                  review=TEXT(analyzer=text_analyser),
                                  movie=TEXT(analyzer=text_analyser),
                                  rating=NUMERIC(numtype=float, unique=False))
    idx = whoosh.index.create_in(idx_dir, schema)
    with idx.writer(procs=os.cpu_count()) as idx_writer:
        add_to_index(tqdm(proverbs), idx_writer)
    
    print('Готово.')


if __name__ == "__main__":
    main()
