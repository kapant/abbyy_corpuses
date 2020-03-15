from pathlib import Path

import whoosh.index
import whoosh.qparser
import whoosh.highlight

import pandas as pd


def main() -> None:
    # Подгружаем корпус (не храним тексты в индексе)
    print('Подгружаем корпус из ./all_deduplicated.csv')
    all_csv = pd.read_csv("./all_deduplicated.csv", encoding="utf-8")
    proverbs = []
    for _, row in all_csv.iterrows():
        row["rating"] = float(row["rating"].replace(",", "."))
        proverbs.append(row)
    
    # Подгружаем индекс
    print('Загружаем индекс из ./index')
    idx = whoosh.index.open_dir("./index")
    
    # Парсер для запроса
    parser = whoosh.qparser.QueryParser('review', idx.schema)

    # Ввод самого запроса
    print('См. синтаксис запроса: https://whoosh.readthedocs.io/en/latest/querylang.html')
    print("""Описание полей:
    movie - название фильма
    rating - рейтинг
    review - ревью, поле поиска по умолчанию
    """)
    query = parser.parse(input('Введите запрос:\n'))
    
    out = pd.DataFrame(columns=["movie", "rating", "context"])

    # Поиск
    with idx.searcher() as searcher:
        result = searcher.search(query, limit=None, terms=True)
    
        # Показываем результаты поиска
        hlt = whoosh.highlight.Highlighter(
            fragmenter=whoosh.highlight.ContextFragmenter(),
            formatter=whoosh.highlight.UppercaseFormatter())
        for hit in result:
            elem = proverbs[hit["review_id"]]
            print(elem["title"], "\t", elem["rating"], "\t", hlt.highlight_hit(hit, 'review', text=elem["text"]))
            # out = out.append({
            #     "movie": elem["title"],
            #     "rating": elem["rating"],
            #     "context": hlt.highlight_hit(hit, 'review', text=elem["text"])
            # }, ignore_index=True)
        
        print('Всего:', len(result))
        # print(out)


if __name__ == "__main__":
    main()