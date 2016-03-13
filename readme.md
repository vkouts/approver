Система согласования и одобрения кредитных заявок
=================================================

 Роли пользователей
 ------------------

В системе заведены следующие группы пользователей:
- кредитчик
- согласователь
- группы согласователей ДБ
- ДСКП выдача

В зависимости от прав пользователя, ему доступны те или иные элементы интерфейса.

**Кредитчику** доступны инструменты для заведения заявок (первый и второй пакет документов), передачи ее на рассмотрение согласователям, а также для общения с согласователями. При этом от кредитчика скрывается личность конкретного согласователя, с которым он ведет переписку по кредитной заявке.

**Согласователь** согласовывает заявки, и передает их на рассмотрение другим группам пользователей (ДБ, ДСКП)

**Сотрудник ДБ** выносит решения по заявкам переданным в соотвествующее подразделение ДБ

**Сотрудник ДСКП**- как правило выносит окончательное решение по заявке

Общая схема логики работы системы
=================================
![alt tag](https://www.gliffy.com/go/publish/image/9866817/L.png)

Краткие характеристики системы:
 -----------------------------
 - прозрачная авторизация через Active directory (необходима поддержка со стороны модулей веб-сервера)
 - разграничение доступа по ролям. Соответствующие сотрудники имеют права просмотра только соотсветстьующих ихним правам заявок.
 - быстрый поиск по заявкам
 - логирование всех действий
 - "защита от дурака" там где это возможно
 - дублирование сообщений посредством email соотвествующим группам получателей рассылки
 - модуль статистики
 - возможность подключения модулей кредитного калькулятора
 
Примеры интерфейса кредитчика  
![Imgur](http://i.imgur.com/DPYhyNt.png)

Пример интерфейса согласователя:  
![Imgur](http://i.imgur.com/kNOgPeg.png)