from model import Model
from google.cloud import datastore

class Users(Model):

    def __init__(self):
        self.ds = self.get_client()

    def get_or_create_user(self, user):
        query = self.ds.query(kind='user')
        query.add_filter('email', '=', user['email'])
        result = list(query.fetch())
        if result:
            print result
        else:
            try:
                key = self.ds.key('user')
                entity = datastore.Entity(
                    key=key)
                entity.update(user)
                self.ds.put(entity)
            except:  # TODO
                pass
        result = list(query.fetch())
        return result[0]['id']


    def is_valid_uni(self, uni):
        query = self.ds.query(kind='student')
        query.add_filter('uni', '=', uni)
        result = list(query.fetch())
        return True if len(result) == 1 else False
