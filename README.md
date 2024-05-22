
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

## Описание кода

### Конфигурация модели
```cpp
uint16_t numNodePairs = 2;
Time simTime = Seconds(10.0);
bool epc = true;
bool disableDl = false;
bool disableUl = false;
```
Этот код устанавливает параметры модели, такие как количество пар узлов, время симуляции, наличие EPC и возможность отключения передачи данных в направлении DL и UL.

### Настройка атрибутов по умолчанию
```cpp
Config::SetDefault("ns3::UdpClient::Interval", TimeValue(MilliSeconds(1)));
Config::SetDefault("ns3::UdpClient::MaxPackets", UintegerValue(1000000));
Config::SetDefault("ns3::LteRlcUm::MaxTxBufferSize", UintegerValue(10 * 1024));
```
Этот код устанавливает некоторые атрибуты по умолчанию для компонентов, таких как UdpClient и LteRlcUm.

### Создание сети LTE
```cpp
Ptr<LteHelper> lteHelper = CreateObject<LteHelper>();
Ptr<PointToPointEpcHelper> epcHelper = CreateObject<PointToPointEpcHelper>();
lteHelper->SetEpcHelper(epcHelper);
lteHelper->SetSchedulerType("ns3::PfFfMacScheduler");
```
Этот код создает объекты LteHelper и PointToPointEpcHelper для управления LTE сетью и эмуляции EPC.

### Создание узлов и установка соединений
```cpp
NodeContainer remoteHostContainer;
remoteHostContainer.Create(1);
NodeContainer enbNodes;
NodeContainer ueNodes;
```
Этот код создает контейнеры узлов для удаленного хоста, eNB и UE.

### Установка мобильности и сетевых устройств
```cpp
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
```cpp
Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign(internetDevices);
Ipv4InterfaceContainer ueIpIface = epcHelper->AssignUeIpv4Address(NetDeviceContainer(ueDevs));
```
Этот код назначает IP адреса и устанавливает маршруты для узлов.

### Установка приложений
```cpp
ApplicationContainer clientApps;
ApplicationContainer serverApps;
```
Этот код создает контейнеры для клиентских и серверных приложений.

### Запуск симуляции
```cpp
serverApps.Start(Seconds(1.0));
clientApps.Start(Seconds(1.0));
Simulator::Stop(simTime);
Simulator::Run();
Simulator::Destroy();
```
Этот код запускает приложения и симуляцию, останавливает ее по истечении времени и завершает работу симулятора.

## Результат

Полученные данные(ключевые характеристики с RLC и MAC уровня):
* [MAC для DL](https://github.com/MargQ/ns3_YADRO/blob/master/DlMacStats.txt)
* [RLC для DL](https://github.com/MargQ/ns3_YADRO/blob/master/DlRlcStats.txt)
* [Rlc для Ul](https://github.com/MargQ/ns3_YADRO/blob/master/UlRlcStats.txt)
* [MAC для Ul](https://github.com/MargQ/ns3_YADRO/blob/master/UlMacStats.txt)

* [Посчитанный Throughput для каждого пользователя](https://github.com/MargQ/ns3_YADRO/blob/master/thrpt.png)
