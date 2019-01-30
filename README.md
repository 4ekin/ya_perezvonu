## What is it?

This script allows to get information about phone number from GetContact servers.
Information about API was received by reverse engineering `app.source.getcontact` Android application 


## How to use 

```
➜ python getcontact.py -h
usage: getcontact.py [-h] [-p PHONENUMBER] [-t TOKEN] [-d DEVICEID]
                     [-c COUNTRYCODE] [-a] [-D DECRYPT] [-E ENCRYPT]
                     [-P PROXY] [-v]

This script allows to get information about phone number from GetContact servers.
Information about API was received by revers engineering Android app "app.source.getcontact"
--- chipik

optional arguments:
  -h, --help            show this help message and exit
  -p PHONENUMBER, --phoneNumber PHONENUMBER
                        Phone number (example: +79217XXX514)
  -t TOKEN, --token TOKEN
                        Token for request (Ex:: AxPA568b72d9c908520b95407e6e95b5482c7995fd98b1e794a2e516a3d1)
  -d DEVICEID, --deviceID DEVICEID
                        DeviceID (default: 27b6dc0c3cb18681)
  -c COUNTRYCODE, --countryCode COUNTRYCODE
                        Country code (default: US)
  -a, --all             Print all possible info
  -D DECRYPT, --decrypt DECRYPT
                        Decrypt data
  -E ENCRYPT, --encrypt ENCRYPT
                        Encrypt data
  -P PROXY, --proxy PROXY
                        Use proxy (ex: 127.0.0.1:8080)
  -v, --debug           Show debug info
```



* Get basic information


```
➜ python getcontact.py -p +79217XXX514
Мария Стадник
Мария Стадник
Маша Стадник
Маша Тренер
Мария Стадник Фуд Парк
Маша Кассир
Мария Фитнесфэмили
Стадник Маша
Маша Касса
Маша Кассир 🌳 Food Park
Мария Стадник Касир Гинза
Маша Касса Гастро Стадник
Мария Олимп На Оптиков
Мария Стадник Европлан
Мария Тренер Олимпик
Мария Большой Орех
Мария Фитнес Бар/2
Маша Стадник Сиаб
Маша Тренер Олимп
Маша Сиаб Личный
Маша Стадник Зал
Хс Мария Стадник
Мария Кассир Фп
Си Стадник Маша
Фитнес Бар Маша
Маша 💪 Стадник
Mary Big Ass
Маша New Бар
Мария Тренер🏋🏼‍♀️
Машулька Стадник
Машка Фитоняшка
Маша Начальник
Машуля Стадник
Мария Фудпарк
Машуля Касир)
Стадник Мария
Мария Тиндер
Маша Качалка
Маша Стандик
Стадник Маня
Мари Кассир
Маша Соляра
Маша Царева
Маша Артур
Маша Ванек
Маша Олимп
Моя Сестра
М Стадник
Мария Фит
Маша Босс
Макс Зал
Мария Фф
Махыч 👸🏽
Маша Бар
Маша Ст
Марина...
Стадник💃🏽
Маша💪🏻❤️
Стадник
Маняша
Зёбра
Мария
```

* Get full information

```
➜  getcontact python getcontact.py -p +79217XXX514 -a
We found:
displayName: Мария Стадник
countryCode: RU
tags
    Мария Стадник
    Маша Стадник
    Маша Тренер
    Мария Стадник Фуд Парк
    Маша Кассир
    Мария Фитнесфэмили
    Стадник Маша
    Маша Касса
    Маша Кассир 🌳 Food Park
    Мария Стадник Касир Гинза
    Маша Касса Гастро Стадник
    Мария Олимп На Оптиков
    Мария Стадник Европлан
    Мария Тренер Олимпик
    Мария Большой Орех
    Мария Фитнес Бар/2
    Маша Стадник Сиаб
    Маша Тренер Олимп
    Маша Сиаб Личный
    Маша Стадник Зал
    Хс Мария Стадник
    Мария Кассир Фп
    Си Стадник Маша
    Фитнес Бар Маша
    Маша 💪 Стадник
    Mary Big Ass
    Маша New Бар
    Мария Тренер🏋🏼‍♀️
    Машулька Стадник
    Машка Фитоняшка
    Маша Начальник
    Машуля Стадник
    Мария Фудпарк
    Машуля Касир)
    Стадник Мария
    Мария Тиндер
    Маша Качалка
    Маша Стандик
    Стадник Маня
    Мари Кассир
    Маша Соляра
    Маша Царева
    Маша Артур
    Маша Ванек
    Маша Олимп
    Моя Сестра
    М Стадник
    Мария Фит
    Маша Босс
    Макс Зал
    Мария Фф
    Махыч 👸🏽
    Маша Бар
    Маша Ст
    Марина...
    Стадник💃🏽
    Маша💪🏻❤️
    Стадник
    Маняша
    Зёбра
    Мария
phoneNumber: +79217XXX514
tagCount: 61
Left 122 requests
```

## How does it work?

* check sources (if you able to read shitty python code :) )
* check details in the [reverse engineering](rev/README.md) part

