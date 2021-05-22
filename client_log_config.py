import logging

logging.basicConfig(  # настройки
    filename="app.main",
    format=" %(asctime)s %(levelname)-10s %(module)s %(message)s",
    level=logging.INFO
)

logger = logging.getLogger('client_log')  # создаем объект класса логгер
