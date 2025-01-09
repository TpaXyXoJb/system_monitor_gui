from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///database.sqlite')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class LoadMetrics(Base):
    """
    Описание модели таблицы для хранения метрик загрузки системы
    """
    __tablename__ = 'load_metrics'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cpu_load = Column(Float)
    ram_free = Column(Float)
    ram_total = Column(Float)
    disk_free = Column(Float)
    disk_total = Column(Float)


Base.metadata.create_all(engine)


def insert_metrics(cpu_load, ram_free, ram_total, disk_free, disk_total):
    """
    Функция вставляет данные метрик в БД
    """
    metrics = LoadMetrics(
        cpu_load=cpu_load,
        ram_free=ram_free,
        ram_total=ram_total,
        disk_free=disk_free,
        disk_total=disk_total,
    )
    session.add(metrics)
    session.commit()
