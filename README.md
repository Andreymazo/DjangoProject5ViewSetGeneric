# Это проект студента скайпро (Бэк). Наш учитель Олег Маслов. Модели - Пользователи: КастомЮзер от Абстактюзера (Суперпользователь и Стафф) и Профайл(УанТуУан к КастомЮзеру). Курсы(ФК к КастомЮзеру), Уроки (ФК к Курсам и ФК к КастомЮзеру), Платежи(ФК к КастомЮзеру и ФК к Курсам)б Подписка (ФК к КастомЮзеру, Курсам и Урокам). Сериализаторы: выводим сразу уроки, курсы и подписки.  Формсет: Через этот инструмент можно создавть(апдейт тоже) подписку (можно что угодно сделать). Наполнять базу можно командными файлами (в конце файла номер запуска), через админку и частично формсетом, то есть через реквест. В проекте реализована регистрация, авторизация, токены выдают после регистрации, документация. Эндпоинты в spa/urls.py ('api/token/', 'api/token/refresh/'). Упаковка в контейнер и деплой, тоже все есть. После наполненния базы лучше тестировать в Постмэне или аналогичном приложении, например свагер (докумнетация), если освоили)