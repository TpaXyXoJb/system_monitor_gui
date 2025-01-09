import psutil


def get_system_metrics():
    """
    Функция получающая данные метрик из системы
    :return:
    """
    cpu_load = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')

    return {
        'cpu_load': cpu_load,
        'ram_free': memory_usage.available,
        'ram_total': memory_usage.total,
        'disk_free': disk_usage.free,
        'disk_total': disk_usage.total,
    }
