# TODO: use a dict for show. (here, and in db_helper)


class User:
    def __init__(self, user_id, db):
        self.user_id = user_id
        self.db = db

    def exists(self):
        return self.db.user_exists(self.user_id)

    def create(self):
        self.db.add_user(self.user_id)

    def get_shows(self):
        shows = self.db.user_get_shows(self.user_id)
        for show in shows:
            yield show

    def has_show(self, show_id):
        return self.db.user_has_show(self.user_id, show_id)

    def add_show(self, show_id, show_name):
        # add show to db if show doesn't exist in db
        if not self.db.show_exists(show_id):
            self.db.add_show(show_id, show_name)

        # if user doesn't have the show already
        if not self.has_show(show_id):
            self.db.user_add_show(self.user_id, show_id)

    def remove_show(self, show_id):
        if self.has_show(show_id):
            self.db.user_delete_show(self.user_id, show_id)
