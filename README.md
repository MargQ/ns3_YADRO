
# Тестовое задание для AME (Инженер-исследователь по разработке алгоритмов)
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

<details><summary> Пример использование своего скрипта</summary>

* Создаем свой файл в папке scratch. Запускаем командой:

```
./ns3 run lte_example
```
</details>

## Описание кода
<details><summary>Описание минимального LTE сценария</summary>

### Начальный шаблон
Основа кода взята из [документации](https://www.nsnam.org/docs/models/html/lte.html)
```
#include <ns3/core-module.h>
#include <ns3/network-module.h>
#include <ns3/mobility-module.h>
#include <ns3/lte-module.h>
#include <ns3/applications-module.h>
#include <ns3/config-store-module.h>
#include <ns3/internet-module.h>
#include <ns3/point-to-point-module.h>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("lte_example");

int main(int argc, char *argv[])
{
```
Определяем компонент логирования, в данном случае это `lte_example`
```
NS_LOG_COMPONENT_DEFINE ("lte_example");
```


### Конфигурация модели
```
Time simTime = Seconds(10.0);
bool epc = true;
bool disableDl = false;
bool disableUl = false;
```
Этот код устанавливает параметры модели, такие как количество пар узлов, время симуляции, наличие EPC и возможность отключения передачи данных в направлении DL и UL.

### Настройка атрибутов по умолчанию
Атрибуты взяты из файла [lena-x2-handover-measures.cc](https://www.nsnam.org/docs/release/3.18/doxygen-3.18/lena-x2-handover-measures_8cc_source.html) (72-74 строки)
```
Config::SetDefault("ns3::UdpClient::Interval", TimeValue(MilliSeconds(1)));
Config::SetDefault("ns3::UdpClient::MaxPackets", UintegerValue(1000000));
Config::SetDefault("ns3::LteRlcUm::MaxTxBufferSize", UintegerValue(10 * 1024));
```
Устанавливаем некоторые атрибуты по умолчанию для компонентов, таких как UdpClient и LteRlcUm.

### Создание сети LTE
Создаем объекты LteHelper и PointToPointEpcHelper для управления LTE сетью и эмуляции EPC:
```
Ptr<LteHelper> lteHelper = CreateObject<LteHelper>();
Ptr<PointToPointEpcHelper> epcHelper = CreateObject<PointToPointEpcHelper>();
lteHelper->SetEpcHelper(epcHelper);
lteHelper->SetSchedulerType("ns3::PfFfMacScheduler");
```

Настраиваем тип планировщика пакетов `pf-ff-mac-scheduler`:
```
lteHelper->SetSchedulerType("ns3::PfFfMacScheduler");
```

### Создание узлов и установка соединений
Создаем контейнеры узлов для удаленного хоста, eNB и UE:
```
NodeContainer remoteHostContainer;
remoteHostContainer.Create(1);
NodeContainer enbNodes;
NodeContainer ueNodes;
```

### Установка мобильности и сетевых устройств
Устанавливаем модель мобильности и сетевые устройства для узлов eNB и UE:
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

### Настройка IP адресов и маршрутизации
Этот код назначает IP адреса и устанавливает маршруты для узлов:
```
Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign(internetDevices);
Ipv4InterfaceContainer ueIpIface = epcHelper->AssignUeIpv4Address(NetDeviceContainer(ueDevs));
```

Выполняем назначение IP-адресов пользовательским устройствам (UE, User Equipment) и устанавливаем приложения на этих устройствах:
```
// Назначение IP-адресов для UE и установка приложений
for (uint32_t u = 0; u < ueNodes.GetN(); ++u)
    {
        Ptr<Node> ueNode = ueNodes.Get(u);
        // Устанавливаем шлюз по умолчанию для UE
        Ptr<Ipv4StaticRouting> ueStaticRouting =
            ipv4RoutingHelper.GetStaticRouting(ueNode->GetObject<Ipv4>());
        ueStaticRouting->SetDefaultRoute(epcHelper->GetUeDefaultGatewayAddress(), 1);
    }
```

### Установка приложений
Этот код создает контейнеры для клиентских и серверных приложений:
```
ApplicationContainer clientApps;
ApplicationContainer serverApps;
```
### Запуск приложений
Старт приложений через 1 секунду после начала симуляции:
```
serverApps.Start(Seconds(1.0));
clientApps.Start(Seconds(1.0));
```
Включаем запись трассировок (log traces) для уровней MAC и RLC соответственно:
```
lteHelper->EnableMacTraces();
lteHelper->EnableRlcTraces();
```

### Запуск симуляции
Этот код запускает симуляцию, останавливает ее по истечении времени и завершает работу симулятора:
```
Simulator::Stop(simTime);
Simulator::Run();
Simulator::Destroy();
```

</details>

## Результат
<details><summary>Полученный результат</summary>
   
- Полученные данные (ключевые характеристики с RLC и MAC уровня):
* [MAC для DL](https://github.com/MargQ/ns3_YADRO/blob/master/src/DlMacStats.txt)
* [RLC для DL](https://github.com/MargQ/ns3_YADRO/blob/master/src/DlRlcStats.txt)
* [RLC для Ul](https://github.com/MargQ/ns3_YADRO/blob/master/src/UlRlcStats.txt)
* [MAC для Ul](https://github.com/MargQ/ns3_YADRO/blob/master/src/UlMacStats.txt)

- Посчитанный [Throughput](https://github.com/MargQ/ns3_YADRO/blob/master/src/thrpt.png) для каждого пользователя
</details>

## Список литературы
<details><summary>Список использованной литературы</summary>
   
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
</details>
