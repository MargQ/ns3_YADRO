import os

def calculate_throughput(file_path):
    tx_1 = 0
    tx_2 = 0
    rx_1 = 0
    rx_2 = 0

    time = 0 

    # Проверяем существует ли файл
    if not os.path.exists(file_path):
        print("Не удалось открыть входной файл")
        return

    # Обработка статистика RLC
    with open(file_path, 'r') as rlc:
        next(rlc)  # Пропускаем первую строку
        for line in rlc:
            tokens = line.strip().split('\t')
            start_time = float(tokens[0])
            end_time = float(tokens[1])
            imsi = int(tokens[3])
            tx_bytes = int(tokens[7])
            rx_bytes = int(tokens[9])

	    # Считаем количество переданных и принятых байтов для каждого пользователя
            if imsi == 2:
                time += (end_time - start_time)
                tx_2 += tx_bytes
                rx_2 += rx_bytes
            else:
                tx_1 += tx_bytes
                rx_1 += rx_bytes

    # Рассчитываем и выводим пропускную способность
    if time > 0:
        print(f"User_1: Throughput_Tx: {round(tx_1 / time, 2)} Bytes per second")
        print(f"User_1: Throughput_Rx: {round(rx_1 / time, 2)} Bytes per second")
        print(f"User_2: Throughput_Tx: {round(tx_2 / time, 2)} Bytes per second")
        print(f"User_2: Throughput_Rx: {round(rx_2 / time, 2)} Bytes per second")
   

print("Посчитанный Throughput для DL")
calculate_throughput('DlRlcStats.txt')
print()
print("Посчитанный Throughput для UL")
calculate_throughput('UlRlcStats.txt')



