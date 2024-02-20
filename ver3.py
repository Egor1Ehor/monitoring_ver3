import os
import psutil
import sys
import time

def wrapper_decorator(func):
    def wrapper(*args, **kwargs):
        with open('Moni.txt', 'a') as file:  # Открываем файл в режиме дописывания
            func(file, *args, **kwargs)  # Передаём файловый объект в функцию
    return wrapper

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_progress_bar(percentage, length=100):
    filled_length = int(length * percentage // 100)
    bar = "|" * filled_length + "-" * (length - filled_length)
    return bar

def print_cpu_status(file, cpu_loads):
    file.write("Загрузка ядер CPU:\n")  # Запись в файл
    print("Загрузка ядер CPU:")
    for i, load in enumerate(cpu_loads):
        bar = get_progress_bar(load)
        cpu_label = f"Ядро {i + 1}:".rjust(8)
        line = f"{cpu_label} [{bar}] {load:5.1f}%\n"
        file.write(line)  # Запись в файл
        print(line, end='')

def move_cursor_up(lines):
    sys.stdout.write(f"\033[{lines}A")

@wrapper_decorator
def main(file):
    cpu_count = psutil.cpu_count(logical=True)
    try:
        while True:
            cpu_loads = psutil.cpu_percent(interval=1, percpu=True)
            move_cursor_up(cpu_count + 1)
            print_cpu_status(file, cpu_loads)
            time.sleep(1)  # Добавлен интервал для замедления обновления
    except KeyboardInterrupt:
        clear_console()

if __name__ == '__main__':
    main()