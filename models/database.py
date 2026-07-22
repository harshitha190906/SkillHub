class Database:
    """
    Helper class for common database operations.
    """

    @staticmethod
    def execute_query(mysql, query, params=None):
        cursor = mysql.connection.cursor()

        cursor.execute(query, params or ())

        mysql.connection.commit()

        cursor.close()

    @staticmethod
    def fetch_one(mysql, query, params=None):
        cursor = mysql.connection.cursor()

        cursor.execute(query, params or ())

        result = cursor.fetchone()

        cursor.close()

        return result

    @staticmethod
    def fetch_all(mysql, query, params=None):
        cursor = mysql.connection.cursor()

        cursor.execute(query, params or ())

        result = cursor.fetchall()

        cursor.close()

        return result