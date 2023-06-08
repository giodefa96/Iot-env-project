import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class Database():
    def __init__(self, host, user, password, db) -> None:
        self._conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            db = db
        )
        self._cursor = self._conn.cursor()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._cursor.close()
        self._conn.close()
    
    @property
    def cursor(self):
        return self._cursor
    
    @property
    def connection(self):
        return self._conn
    
    def commit(self):
        return self._conn.commit()
    
    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()
    
    def execute(self, sql: str, params=None) -> None:
        self.cursor.execute(sql, params or ())
    
    def execute_many(self, sql: str, params=None) -> None:
        self.cursor.executemany(sql, params or ())
    
    def fetchall(self) -> list:
        return self.cursor.fetchall()
    
    def fetchone(self) -> tuple:
        return self.cursor.fetchone()
    
    def query(self, sql: str, params=None) -> list:
        self.execute(sql, params)
        return self.fetchall()



if __name__ == '__main__':
    with Database(**user_dict) as db:
        
        try:
            db.execute("CREATE TABLE iot_devices (ip VARCHAR(255), type VARCHAR(255))")
        except Exception as e:
            print(e)
            
        sql = "INSERT INTO iot_devices (ip, type) VALUES (%s, %s)"
        val = [
            ("123", "sensor"),
            ("456", "sensor"),
            ("789", "sensor"),
            ("101", "sensor"),
            ("102", "sensor"),
            ("103", "sensor"),
            ("104", "sensor"),
            ("105", "sensor")
        ]
        
        db.execute_many(sql, val)
        
        comments = db.query('SELECT * FROM iot_devices')
        print(comments)
        
        db.commit()
        print(db.cursor.rowcount, "was inserted.") 