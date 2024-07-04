import threading
import time
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.queue = Queue()
        self.tables = tables

    def customer_arrival(self):
        for i in range(1, 21):  # Ограничение в 20 посетителей
            customer = f'Посетитель номер {i}'
            print(f'{customer} прибыл')
            self.serve_customer(customer)
            time.sleep(1)  # Приход посетителя каждую секунду

    def serve_customer(self, customer):
        free_table = next((table for table in self.tables if not table.is_busy), None)
        if free_table:
            free_table.is_busy = True
            print(f'{customer} сел за стол {free_table.number}. (начало обслуживания)')
            customer_thread = threading.Thread(target=self.customer_dining, args=(customer, free_table))
            customer_thread.start()
        else:
            print(f'{customer} ожидает свободный стол. (помещение в очередь)')
            self.queue.put(customer)

    def customer_dining(self, customer, table):
        time.sleep(5)  # Время обслуживания 5 секунд
        print(f'{customer} покушал и ушёл. (конец обслуживания)')
        table.is_busy = False
        if not self.queue.empty():
            next_customer = self.queue.get()
            self.serve_customer(next_customer)

class Customer(threading.Thread):
    def __init__(self, cafe, name):
        super().__init__()
        self.cafe = cafe
        self.name = name

    def run(self):
        while True:
            self.cafe.customer_arrival()

# Создаем столики в кафе
tables = [Table(i) for i in range(1, 4)]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()