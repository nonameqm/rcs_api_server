from dataclasses import dataclass
from os import path, environ
import logging



base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@dataclass
class Config:
    BASE_DIR = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True

@dataclass
class LocalConfig(Config):
    PROJ_RELOAD : bool = True
    DB_URL : str = "mysql+pymysql://rcs_admin:%s@db-90ndo.cdb.ntruss.com/rcs_db?charset=utf8mb4"

@dataclass
class ProdConfig(Config):
    PROJ_RELOAD : bool = False

def conf():
    """
        set environment
    """
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))
    