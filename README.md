# Парсер рецензий на ivi.ru

## /ivi_parser

Начиная с какого-нибудь айди открывает страницы с рецензиями по фильмам и записывает рейтинг из рецензии и текст в ```/ivi_parser/reviews/movie_<айди фильма>.csv```

Запуск: ```python ./parser.py```  
Остановка: ```Ctrl + C```

Во время работы на стандартный выход пишется некоторая информация: "." - пустая страница, цифра - айди существующей страницы. В конце работы в файл ```last_number.txt``` пишется номер последней необработанной страницы.
