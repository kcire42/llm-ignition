# import logging
# import os
# import sys

# # 1. Leer el nivel de log desde las variables de entorno (por defecto INFO)
# # En desarrollo lo cambiarás a DEBUG en tu archivo .env o docker-compose
# LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO").upper()

# # Mapeo de strings a los niveles reales de la librería logging
# LOG_LEVELS = {
#     "DEBUG": logging.DEBUG,
#     "INFO": logging.INFO,
#     "WARNING": logging.WARNING,
#     "ERROR": logging.ERROR,
#     "CRITICAL": logging.CRITICAL
# }
# current_level = LOG_LEVELS.get(LOG_LEVEL_STR, logging.INFO)

# def setup_logger(name: str) -> logging.Logger:
#     """
#     Configura un logger con formato estandarizado para Saphira.
#     """
#     logger = logging.getLogger(name)
    
#     # Evitar duplicidad de logs si el logger ya fue configurado
#     if logger.hasHandlers():
#         return logger

#     logger.setLevel(current_level)

#     # 2. Definir un formato limpio y profesional
#     # Incluye: Tiempo, Nombre del Componente/Servicio, Nivel del Log y el Mensaje
#     formatter = logging.Formatter(
#         fmt="%(asctime)s | %(levelname)-8s | [%(name)s] -> %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S"
#     )

#     # 3. Handler para enviar los logs a la salida estándar (consola/Docker logs)
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setFormatter(formatter)
#     logger.addHandler(console_handler)

#     return logger