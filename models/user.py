from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """Handles all user-related database operations."""

    @staticmethod
    def create_user(mysql, fullname, email, password):
        """Create a new user account."""

        cursor = mysql.connection.cursor()

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users (fullname, email, password)
            VALUES (%s, %s, %s)
            """,
            (fullname, email.lower(), hashed_password)
        )

        mysql.connection.commit()
        cursor.close()

        return True

    @staticmethod
    def get_user_by_email(mysql, email):
        """Retrieve a user by email."""

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email=%s
            """,
            (email.lower(),)
        )

        user = cursor.fetchone()

        cursor.close()

        return user

    @staticmethod
    def get_user_by_fullname(mysql, fullname):
        """Retrieve a user by fullname."""

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE fullname=%s
            """,
            (fullname,)
        )

        user = cursor.fetchone()

        cursor.close()

        return user

    @staticmethod
    def verify_password(user, password):
        """Verify password."""

        if not user:
            return False

        return check_password_hash(user[3], password)