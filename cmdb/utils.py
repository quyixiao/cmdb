import logging


def getlogger(mod_name: str, filepath: str):
    FORMAT = '%(asctime)s 【%(levelname)s】 [%(filename)s:%(lineno)d] %(message)s'
    logger = logging.getLogger(mod_name)
    logger.setLevel(logging.INFO)  # 单独设置
    logger.propagate = False  # 阻止传送给父logger
    handler = logging.FileHandler(filepath)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt=FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
