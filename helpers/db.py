# postgres database helper

import psycopg2


class DB:
    def __init__(self, database_url, sslmode="prefer"):
        self.conn = psycopg2.connect(
                database_url,
                sslmode=sslmode
                )
        self.cur = self.conn.cursor()

    def execute(self, query, data=None):
        try:
            self.cur.execute(query, data)
        except Exception:
            self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()

    def user_exists(self, user_id):
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s);"
        data = (user_id,)
        self.execute(query, data)
        return self.cur.fetchone()[0]

    def add_user(self, user_id):
        query = "INSERT INTO users (user_id) values(%s);"
        data = (user_id,)
        self.execute(query, data)
        self.conn.commit()

    def delete_user(self, user_id):
        query = "DELETE FROM users where user_id = %s;"
        data = (user_id,)
        self.execute(query, data)
        self.conn.commit()

    def show_exists(self, show_id):
        query = "SELECT EXISTS(SELECT 1 FROM shows WHERE show_id = %s);"
        data = (show_id,)
        self.execute(query, data)
        return self.cur.fetchone()[0]

    def add_show(self, show_id, show_name):
        query = "INSERT INTO shows (show_id, show_name) values(%s, %s);"
        data = (show_id, show_name)
        self.execute(query, data)
        self.conn.commit()

    def get_show(self, show_id):
        query = "SELECT (show_id, show_name) FROM shows \
                WHERE show_id = %s;"
        data = (show_id,)
        self.execute(query, data)

    def delete_show(self, show_id):
        query = "DELETE FROM shows where show_id = %s;"
        data = (show_id,)
        self.execute(query, data)
        self.conn.commit()

    def user_has_show(self, user_id, show_id):
        query = "SELECT EXISTS(SELECT 1 FROM users_shows \
                WHERE (user_id, show_id) = (%s, %s));"
        data = (user_id, show_id)
        self.execute(query, data)
        return self.cur.fetchone()[0]

    def user_add_show(self, user_id, show_id):
        query = "INSERT INTO users_shows (user_id, show_id) VALUES(%s, %s);"
        data = (user_id, show_id)
        self.execute(query, data)
        self.conn.commit()

    def user_get_shows(self, user_id):
        query = "SELECT show_id, show_name FROM shows \
                WHERE show_id IN \
                (SELECT show_id from users_shows WHERE user_id = %s)"
        data = (user_id,)
        self.execute(query, data)
        yield from self.cur.fetchall()

    def user_delete_show(self, user_id, show_id):
        query = "DELETE FROM users_shows WHERE (user_id, show_id) = (%s, %s);"
        data = (user_id, show_id)
        self.execute(query, data)
        self.conn.commit()

    def get_all_users(self):
        query = "SELECT user_id FROM users;"
        self.execute(query)
        yield from self.cur.fetchall()

    def get_all_shows(self):
        query = "SELECT show_id FROM shows;"
        self.execute(query)
        yield from self.cur.fetchall()
