import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASS")
mysql_host = os.environ.get("MYSQL_HOST")
mysql_port = os.environ.get("MYSQL_PORT")
mysql_db_name = os.environ.get("MYSQL_DB_NAME")

print(mysql_user, mysql_password, mysql_host, mysql_port, mysql_db_name)

MYSQL_DATABASE_URL = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db_name}"

print(MYSQL_DATABASE_URL)

engine: Engine = create_engine(MYSQL_DATABASE_URL, isolation_level="SERIALIZABLE")
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
