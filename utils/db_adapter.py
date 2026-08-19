import os
import sqlite3
import pymysql

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class SQLiteCursorWrapper:
    def __init__(self, conn):
        self.cursor = conn.cursor()

    def execute(self, sql, params=None):
        sql_trans = sql.replace("INT AUTO_INCREMENT PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        sql_trans = sql_trans.replace("AUTO_INCREMENT", "AUTOINCREMENT")
        sql_trans = sql_trans.replace("%s", "?")
        if params is None:
            return self.cursor.execute(sql_trans)
        return self.cursor.execute(sql_trans, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()


class SQLiteConnWrapper:
    def __init__(self, db_path=None):
        if not db_path:
            db_path = os.path.join(BASE_DIR, "skillhub.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def cursor(self):
        return SQLiteCursorWrapper(self.conn)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


class SmartMySQL:
    """
    A pure-Python database connector for Flask that attempts to connect to MySQL using PyMySQL.
    If MySQL server is unavailable or connection fails, it seamlessly falls back
    to a local SQLite database (skillhub.db or /tmp/skillhub.db on Vercel).
    """

    def __init__(self, app=None):
        self.app = app
        self._mysql_conn = None
        self._sqlite_wrapper = None
        self._using_sqlite = False
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    @property
    def connection(self):
        if self._using_sqlite and self._sqlite_wrapper:
            return self._sqlite_wrapper

        if self.app and not self._using_sqlite:
            try:
                host = self.app.config.get("MYSQL_HOST")
                port = int(self.app.config.get("MYSQL_PORT") or 3306)
                user = self.app.config.get("MYSQL_USER")
                password = self.app.config.get("MYSQL_PASSWORD") or ""
                db = self.app.config.get("MYSQL_DB")

                if host and user and db:
                    if self._mysql_conn is None:
                        self._mysql_conn = pymysql.connect(
                            host=host,
                            port=port,
                            user=user,
                            password=password,
                            database=db,
                            connect_timeout=5
                        )
                    cur = self._mysql_conn.cursor()
                    cur.execute("SELECT 1")
                    cur.close()
                    return self._mysql_conn
            except Exception as e:
                print(f"[INFO] MySQL connection unavailable ({e}). Falling back to local SQLite database.")
                self._using_sqlite = True
                self._mysql_conn = None

        if self._sqlite_wrapper is None:
            if os.getenv("VERCEL"):
                db_file = "/tmp/skillhub.db"
            else:
                db_file = os.path.join(BASE_DIR, "skillhub.db")
            self._sqlite_wrapper = SQLiteConnWrapper(db_file)
            self._using_sqlite = True

        return self._sqlite_wrapper
