from google.cloud import datastore



class Model(object):
    def get_client(self):
        return datastore.Client('coms4156-168718')

    def get(self, key, fallback=None):
        return self.model.get(key, fallback)

    def get_id(self):
        return self.get_key().id

    def get_key(self):
        return self.model.key

    def destroy(self):
        if not self.fetched:
            return

        self.datastore.delete(self.get_key())

        while self.datastore.get(self.get_key()):
            pass

    def update(self, **kwargs):
        self.model.update(kwargs)
        self.datastore.put(self.model)

    def create_entity(self, **kwargs):
        key = self.datastore.key(kwargs['kind'])
        entity = datastore.Entity(key=key)
        kwargs.pop('kind')
        entity.update(kwargs)
        self.datastore.put(entity)

        # datastore is really annoying and it seems it doesn't always update
        # immediately, so if we don't do this then sometimes querying the key
        # immediately after calling this function won't work
        while not self.datastore.get(entity.key):
            pass

        return entity.key
