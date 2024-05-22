
# Тестовое задание для AME
#### Версия NS: ns-3-dev
#### Используемые языки: C++, Python

## Тестовое задание
<details><summary>Задание</summary>

**Основное задание**
* Установить NS-3 и скомпилировать.
* С помощью документации NS-3 сделать минимальный LTE сценарий:

    * Есть eNB и два абонента.
    * Траффик Full Buffer (пакеты идут в обе стороны бесконечно).
    * В LTE модуле сконфигурирован планировщик пакетов pf-ff-mac-scheduler.
    * В LTE модуле сконфигурирован вывод ключевых характеристик с Rlc и MAC уровня.
  
* Запустить сценарий и получить вывод ключевых характеристик.

**Основное задание**
Написать скрипт, который по полученному выводу ключевых характеристик с Rlc уровня 
посчитает Throughput в DL и в UL для каждого пользователя отдельно и выведет его на экран.

</details>

## Начало работы с ns-3
<details><summary> Установка NS-3</summary>
  
* Нужно склонировать репозиторй из Github:
```Shell
 git clone https://gitlab.com/nsnam/ns-3-dev.git
 ```

* Перемещаемся в папку с ns-3:
```Shell
cd ns-3-dev
```

</details>

<details><summary>Компиляция NS-3</summary>
  
* Необходимо ввести следующую команду в корневом каталоге для того, чтобы настроить сборку ns-3 с включением примеров  и тестов
```Shell
./ns3 configure --enable-examples --enable-tests
```
* Затем собираем проект ns-3:
```Shell
./ns3 build
```
* После завершения запускаем тесты, чтобы проверить свой билд:
```Shell
 ./test.py
```

</details>

## Создание своего скрипта
<details><summary> Пример использование своего скрипта</summary>

* Создаем свой файл в папке scratch. Запускаем командой:

```Shell
./ns3 run lte_scenario.cc
```
</details>

## Результат

Полученные данные(ключевые характеристики с RLC и MAC уровня):
* [MAC для DL](https://github.com/MargQ/ns3_YADRO/blob/master/DlMacStats.txt)
* [RLC для DL](https://github.com/MargQ/ns3_YADRO/blob/master/DlRlcStats.txt)
* [Rlc для Ul](https://github.com/MargQ/ns3_YADRO/blob/master/UlRlcStats.txt)
* [MAC для Ul](https://github.com/MargQ/ns3_YADRO/blob/master/UlMacStats.txt)

* [Посчитанный Throughput для каждого пользователя:](https://github.com/MargQ/ns3_YADRO/blob/master/thrpt.png)
