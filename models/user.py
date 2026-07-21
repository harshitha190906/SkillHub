from werkzeug.security import generate_password_hash, check_password_hash

class User:

    @staticmethod
    def create_user(mysql, fullname, email, password):

        cursor = mysql.connection.cursor()

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users(fullname,email,password)
            VALUES(%s,%s,%s)
            """,
            (fullname, email, hashed_password)
        )

        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_user_by_email(mysql, email):

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()

        return user