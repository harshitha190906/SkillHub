class Skill:
    """Handles all skill-related database operations."""

    @staticmethod
    def add_skill(mysql, user_id, skill_name, skill_level, description):
        """
        Add a new skill for a user.
        """

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            INSERT INTO skills (user_id, skill_name, skill_level, description)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, skill_name, skill_level, description)
        )

        mysql.connection.commit()
        cursor.close()

        return True

    @staticmethod
    def get_all_skills(mysql, user_id):
        """
        Retrieve all skills of a user.
        """

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM skills
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        skills = cursor.fetchall()

        cursor.close()

        return skills

    @staticmethod
    def get_skill_by_id(mysql, skill_id, user_id):
        """
        Retrieve a single skill belonging to the logged-in user.
        """

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM skills
            WHERE id = %s AND user_id = %s
            """,
            (skill_id, user_id)
        )

        skill = cursor.fetchone()

        cursor.close()

        return skill

    @staticmethod
    def update_skill(mysql, skill_id, user_id, skill_name, skill_level, description):
        """
        Update an existing skill.
        """

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            UPDATE skills
            SET skill_name = %s,
                skill_level = %s,
                description = %s
            WHERE id = %s
            AND user_id = %s
            """,
            (skill_name, skill_level, description, skill_id, user_id)
        )

        mysql.connection.commit()
        cursor.close()

        return True

    @staticmethod
    def delete_skill(mysql, skill_id, user_id):
        """
        Delete a skill belonging to the logged-in user.
        """

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            DELETE FROM skills
            WHERE id = %s
            AND user_id = %s
            """,
            (skill_id, user_id)
        )

        mysql.connection.commit()
        cursor.close()

        return True