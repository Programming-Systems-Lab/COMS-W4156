from model import Model


class User(Model):
    def __init__(self, **kwargs):
        self.datastore = self.get_client()

        self.fetched = False

        # try to fetch by id
        if 'id' in kwargs:
            key = self.datastore.key('user', kwargs['id'])
            self.model = self.datastore.get(key)
            self.fetched = bool(self.model)

        # try to fetch by uni
        if not self.fetched and 'uni' in kwargs:
            model_query = self.datastore.query(kind='user')
            model_query.add_filter('uni', '=', kwargs['uni'])
            users = list(model_query.fetch())
            if len(users) > 0:
                self.model = users[0]
                self.fetched = True

        # try to fetch by email
        if not self.fetched and 'email' in kwargs:
            model_query = self.datastore.query(kind='user')
            model_query.add_filter('email', '=', kwargs['email'])
            users = list(model_query.fetch())
            if len(users) == 0:
                self.fetched = False
                self.model = kwargs
            else:
                self.fetched = True
                self.model = users[0]

        # no other unique fields
        if not self.fetched:
            self.fetched = False
            self.model = kwargs

    def is_teacher(self):
        return self.get('teacher', False)

    def is_student(self):
        return self.get('uni') is not None

    def get_or_create(self):
        if not self.fetched:
            key = self.create_entity(
                kind='user',
                **self.model
            )
            self.model = self.datastore.get(key)
            self.fetched = True

        return self
