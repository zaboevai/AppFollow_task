# Readme

Задание от AppFolow.

Более подробно в "Тестовое задание для Python разработчика.pdf"

### Getting Started

Run api server: 

>python api.py

Run news parser: 

>python hacker_news.py


### API 

Приложение доступно по ссылке:  

[https://appfollow-hacker-news.herokuapp.com/posts]()


Возможные запросы:
1) По умолчанию выводит 5 последних записей:

    [http://127.0.0.1:8000/posts/]()
2) Вывести 10 последних записей:
    
    [http://127.0.0.1:8000/posts/?limit=10]()    
3) Вывести 5 последних записей со сдвигом 2:

    [http://127.0.0.1:8000/posts/?offset=2]()
4) Вывести 5 последних записей отсортированных по "title":

    [http://127.0.0.1:8000/posts/?order=title]()

5) Вывести 5 последних записей отсортированных с конца по "title":

    [http://127.0.0.1:8000/posts/?order_desc=title]()

Запросы можно смешивать. Например:

1) Вывести 10 последних записей со сдвигом на 2 записи:

    [http://127.0.0.1:8000/posts/?limit=10&offset=2]()


### Installing

Для старта потребуется:

1) склонировать проект с GitHub
>   https://github.com/zaboevai/AppFollow_task.git

2) установить зависимости 

>requirements.txt

3) создать базу данных
 

>flask db init 

>flask db migrate 

>flask db upgrade
        