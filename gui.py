import tkinter as tk
import time
import threading
from datetime import timedelta
from system_monitor import get_system_metrics
from database import insert_metrics
from humanfriendly import format_size

# время обновления
UPDATE_INTERVAL_SEC = 10


class App:
    """
    Описание объекта окна
    """

    def __init__(self, root):
        self.root = root
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.root.title("System monitor")

        label_font = ("Arial", 12, "bold")
        button_font = ("Arial", 10, "bold")

        self.cpu_label = tk.Label(self.root, text="CPU load: ", font=label_font)
        self.cpu_label.pack(pady=10)

        self.ram_label = tk.Label(self.root, text="RAM: ", font=label_font)
        self.ram_label.pack(pady=10)

        self.disk_label = tk.Label(self.root, text="Disk: ", font=label_font)
        self.disk_label.pack(pady=10)

        self.timer_label = tk.Label(root, text="Recording Time: 00:00:00", font=label_font)
        self.timer_label.pack(pady=10)
        self.timer_label.pack_forget()

        self.start_btn = tk.Button(self.root, text="Start recording", font=button_font, command=self.start_recording)
        self.start_btn.pack(pady=20)

        self.stop_btn = None
        self.recording = False
        self.start_time = None
        self.timer_thread = None

        self.update()

    def update(self):
        """
        Этот метод обновляет системные метрики, отображаемые в графическом интерфейсе (GUI).
        Она получает информацию о загрузке процессора (CPU), доступной и общей оперативной памяти (RAM),
        а также о дисковом пространстве.
        Функция вызывается периодически в соответствии с интервалом обновления, заданным пользователем.
        """
        metrics = get_system_metrics()
        self.cpu_label.config(text=f"CPU load: {metrics['cpu_load']}%")
        self.ram_label.config(
            text=f"RAM free: {format_size(metrics['ram_free'])} / {format_size(metrics['ram_total'])}")
        self.disk_label.config(
            text=f"Disk free: {format_size(metrics['disk_free'])} / {format_size(metrics['disk_total'])}")

        if self.recording:
            insert_metrics(
                metrics['cpu_load'],
                metrics['ram_free'],
                metrics['ram_total'],
                metrics['disk_free'],
                metrics['disk_total']
            )
        self.root.after(UPDATE_INTERVAL_SEC * 1000, self.update)

    def start_recording(self):
        """
        Метод, запускающий запись данных в БД. Заменяет кнопку старта на кнопку остановки. Показывает и
        запускает отсчет таймера
        :return:
        """
        self.recording = True
        self.start_time = time.time()
        self.start_btn.pack_forget()
        self.stop_btn = tk.Button(self.root, text="Stop recording", command=self.stop_recording)
        self.stop_btn.pack(pady=20)
        self.timer_label.pack(pady=10)
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()

    def stop_recording(self):
        """
        Метод, останавливающий запись данных в БД. Заменяет кнопку остановки на кнопку старта
        """
        self.recording = False
        self.stop_btn.pack_forget()
        self.start_btn.pack(pady=20)
        self.timer_label.pack_forget()
        self.timer_label.config(text="Recording Time: 00:00:00")

    def update_timer(self):
        """
        Этот метод обновляет отображение таймера каждую секунду во время записи.
О       на вычисляет время, прошедшее с момента начала записи, и обновляет метку с таймером.
        """
        while self.recording:
            duration = timedelta(seconds=time.time() - self.start_time)
            minutes, seconds = divmod(duration.seconds, 60)
            formatted_time = f"{minutes:02}:{seconds:02}"
            self.timer_label.config(text=f"Recording time {formatted_time}")
            time.sleep(1)


def run_app():
    """
    Функция создания и запуска окна
    """
    root = tk.Tk()
    app = App(root)
    root.mainloop()
