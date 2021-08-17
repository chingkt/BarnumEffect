import pymysql
import os

username = os.environ["username"]
pw = os.environ["pw"]
host = os.environ["host"]
port = int(os.environ["Port"])

db = pymysql.connect(
    host=host,
    user=username,
    password=pw,
    port=port,
    database=os.environ["database"]
)
cursor = db.cursor()


def add_entry(info: dict):
    sql = """INSERT INTO user_info (tg_name, tg_id, nickname, star, gender, age, occupation, score) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (info["tg_name"], info["tg_id"], info["nickname"], info["star"], info["gender"]
           , info["age"], info["occupation"], info["score"])
    cursor.execute(sql, val)
    db.commit()
