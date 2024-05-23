
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
```
 git clone https://gitlab.com/nsnam/ns-3-dev.git
 ```

* Перемещаемся в папку с ns-3:
```
cd ns-3-dev
```

</details>

<details><summary>Компиляция NS-3</summary>
  
* Необходимо ввести следующую команду в корневом каталоге для того, чтобы настроить сборку ns-3 с включением примеров  и тестов
```
./ns3 configure --enable-examples --enable-tests
```
* Затем собираем проект ns-3:
```
./ns3 build
```
* После завершения запускаем тесты, чтобы проверить свой билд:
```
 ./test.py
```

</details>

## Создание своего скрипта
<details><summary> Пример использование своего скрипта</summary>

* Создаем свой файл в папке scratch. Запускаем командой:

```
./ns3 run lte_example
```
</details>

## Описание кода

### Конфигурация модели
```
uint16_t numNodePairs = 2;
Time simTime = Seconds(10.0);
bool epc = true;
bool disableDl = false;
bool disableUl = false;
```
Этот код устанавливает параметры модели, такие как количество пар узлов, время симуляции, наличие EPC и возможность отключения передачи данных в направлении DL и UL.

### Настройка атрибутов по умолчанию
```
Config::SetDefault("ns3::UdpClient::Interval", TimeValue(MilliSeconds(1)));
Config::SetDefault("ns3::UdpClient::MaxPackets", UintegerValue(1000000));
Config::SetDefault("ns3::LteRlcUm::MaxTxBufferSize", UintegerValue(10 * 1024));
```
Этот код устанавливает некоторые атрибуты по умолчанию для компонентов, таких как UdpClient и LteRlcUm.

### Создание сети LTE
```
Ptr<LteHelper> lteHelper = CreateObject<LteHelper>();
Ptr<PointToPointEpcHelper> epcHelper = CreateObject<PointToPointEpcHelper>();
lteHelper->SetEpcHelper(epcHelper);
lteHelper->SetSchedulerType("ns3::PfFfMacScheduler");
```
Этот код создает объекты LteHelper и PointToPointEpcHelper для управления LTE сетью и эмуляции EPC.

### Создание узлов и установка соединений
```
NodeContainer remoteHostContainer;
remoteHostContainer.Create(1);
NodeContainer enbNodes;
NodeContainer ueNodes;
```
Этот код создает контейнеры узлов для удаленного хоста, eNB и UE.

### Установка мобильности и сетевых устройств
```
MobilityHelper mobility;
mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
mobility.Install(enbNodes);
mobility.Install(ueNodes);
NetDeviceContainer enbDevs;
NetDeviceContainer ueDevs;
enbDevs = lteHelper->InstallEnbDevice(enbNodes);
ueDevs = lteHelper->InstallUeDevice(ueNodes);
```
Этот код устанавливает модель мобильности и сетевые устройства для узлов eNB и UE.

### Настройка IP адресов и маршрутизации
```
Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign(internetDevices);
Ipv4InterfaceContainer ueIpIface = epcHelper->AssignUeIpv4Address(NetDeviceContainer(ueDevs));
```
Этот код назначает IP адреса и устанавливает маршруты для узлов.

### Установка приложений
```
ApplicationContainer clientApps;
ApplicationContainer serverApps;
```
Этот код создает контейнеры для клиентских и серверных приложений.

### Запуск симуляции
```
serverApps.Start(Seconds(1.0));
clientApps.Start(Seconds(1.0));
Simulator::Stop(simTime);
Simulator::Run();
Simulator::Destroy();
```
Этот код запускает приложения и симуляцию, останавливает ее по истечении времени и завершает работу симулятора.

## Результат

Полученные данные(ключевые характеристики с RLC и MAC уровня):
* [MAC для DL](https://github.com/MargQ/ns3_YADRO/blob/master/src/DlMacStats.txt)
* [RLC для DL](https://github.com/MargQ/ns3_YADRO/blob/master/src/DlRlcStats.txt)
* [Rlc для Ul](https://github.com/MargQ/ns3_YADRO/blob/master/src/UlRlcStats.txt)
* [MAC для Ul](https://github.com/MargQ/ns3_YADRO/blob/master/src/UlMacStats.txt)

* [Посчитанный Throughput для каждого пользователя](https://github.com/MargQ/ns3_YADRO/blob/master/src/thrpt.png)


## Список литературы

- Установка и сборка ns-3

[Документация](https://www.nsnam.org/docs/release/3.41/tutorial/ns-3-tutorial.pdf) по установке и сборке ns-3 находится в ns-3 Tutorial. 

- Документация по модулю LTE

Полная [документация](https://www.nsnam.org/docs/models/html/lte.html) по модулю LTE для ns-3.

- Файл "основа" (п. 19.2.3)

В разделе 19.2.3 документации по LTE содержится [информация о создании и использовании стандартной программы](https://www.nsnam.org/docs/models/html/lte.html) для сценариев LTE в ns-3.

- Описание параметров таблицы (п. 19.2.6)

В разделе 19.2.6 [документации по LTE](https://www.nsnam.org/docs/models/html/lte-user.html) приводится описание параметров, используемых в таблицах для анализа результатов симуляции LTE.

- Реализация режима full buffer

Пример кода для [реализации режима full buffer](https://www.nsnam.org/docs/models/html/lte-user.html) в LTE сценариях ns-3 можно найти в файле lena-epc-dual-stripe, описанном в данной документации. Этот файл предоставляет необходимые настройки и параметры для симуляции с использованием режима full buffer.
