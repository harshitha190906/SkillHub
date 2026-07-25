class Certificate:
    """Handles all certificate-related database operations."""

    @staticmethod
    def add_certificate(mysql, user_id, title, file_name):
        """Add a new certificate."""

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            INSERT INTO certificates (user_id, title, file_name)
            VALUES (%s, %s, %s)
            """,
            (
                user_id,
                title.strip(),
                file_name
            )
        )

        mysql.connection.commit()
        cursor.close()

        return True

    @staticmethod
    def get_certificates(mysql, user_id):
        """Return all certificates of the logged-in user."""

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM certificates
            WHERE user_id=%s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        certificates = cursor.fetchall()

        cursor.close()

        return certificates

    @staticmethod
    def delete_certificate(mysql, certificate_id, user_id):
        """Delete a certificate belonging to the logged-in user."""

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            DELETE FROM certificates
            WHERE id=%s
            AND user_id=%s
            """,
            (
                certificate_id,
                user_id
            )
        )

        mysql.connection.commit()
        cursor.close()

        return True