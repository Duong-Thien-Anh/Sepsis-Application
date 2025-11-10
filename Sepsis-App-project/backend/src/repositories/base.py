from os import environ
from peewee import MySQLDatabase, Model


db = MySQLDatabase(
    database=environ.get("MYSQL_DB"),
    user=environ.get("MYSQL_USER"),
    password=environ.get("MYSQL_PWD"),
    host=environ.get("MYSQL_HOST"),
    port=environ.get("PORT", 3306),
    charset="utf8mb4",
    use_unicode=True,
    init_command="SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;",
    sql_mode="TRADITIONAL,STRICT_ALL_TABLES,NO_AUTO_VALUE_ON_ZERO",
)


class BaseModel(Model):
    class Meta:
        database: MySQLDatabase = db
