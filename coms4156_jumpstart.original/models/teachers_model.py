from model import Model
from datetime import datetime, date
from google.cloud import datastore

class Teachers(Model):

    def __init__(self, tid):
        self.tid = tid
        self.now = datetime.now()
        self.today = datetime.today()
        self.ds = self.get_client()

    def get_courses(self):
        query = self.ds.query(kind='teaches')
        query.add_filter('tid', '=', self.tid)
        teaches = list(query.fetch())
        results = list()
        for teach in teaches:
            query = self.ds.query(kind='courses')
            query.add_filter('cid', '=', teach['cid'])
            results = results + list(query.fetch())
        return results

    def get_courses_with_session(self):
        query = self.ds.query(kind='teaches')
        query.add_filter('tid', '=', self.tid)
        teaches = list(query.fetch())
        courses = list()
        for teach in teaches:
            query = self.ds.query(kind='courses')
            query.add_filter('cid', '=', teach['cid'])
            courses = courses + list(query.fetch())
        results = list()
        for course in courses:
            query = self.ds.query(kind='sessions')
            query.add_filter('cid', '=', course['cid'])
            sessions = list(query.fetch())
            for session in sessions:
                if session['expires'].replace(tzinfo=None) > datetime.now():
                    results.append(session)
            if len(results) == 1:
                course['secret'] = sessions[0]['secret']

        # result = courses + sessions
        return courses


    def add_course(self, course_name):
        key = self.ds.key('courses')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'name': course_name,
            'active': 0
        })
        self.ds.put(entity)
        cid = entity.key.id
        entity.update({
            'cid': cid
        })
        self.ds.put(entity)

        key = self.ds.key('teaches')
        entity = datastore.Entity(
            key=key)
        entity.update({
            'tid': self.tid,
            'cid': cid
        })
        self.ds.put(entity)
        return cid

    def remove_course(self, cid):
        key = self.ds.key('courses', int(cid))
        self.ds.delete(key)

        # remove course from students' enrolled list
        query = self.ds.query(kind='enrolled_in')
        query.add_filter('cid', '=', int(cid))
        results = list(query.fetch())
        for result in results:
            self.ds.delete(result.key)
