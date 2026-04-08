from model import Model


class Index(Model):

    def __init__(self, uid):
        self.uid = uid

    def is_student(self):
        ds = self.get_client()
        query = ds.query(kind='student')
        query.add_filter('sid', '=', self.uid)
        result = list(query.fetch())
        return True if len(result) == 1 else False

    def is_teacher(self):
        ds = self.get_client()
        query = ds.query(kind='teacher')
        query.add_filter('tid', '=', self.uid)
        result = list(query.fetch())
        return True if len(result) == 1 else False