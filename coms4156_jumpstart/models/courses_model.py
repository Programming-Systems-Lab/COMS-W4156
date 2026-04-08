from model import Model
import models
from datetime import datetime
from random import randint


class CourseNotTakingAttendance(Exception):
    pass


class Course(Model):
    def __init__(self, **kwargs):
        self.datastore = self.get_client()
        self.fetched = False
        if 'id' in kwargs:
            key = self.datastore.key('course', kwargs['id'])
            self.model = self.datastore.get(key)
            self.fetched = bool(self.model)

        if not self.fetched:
            self.model = kwargs

    def get_or_create(self):
        if not self.fetched:
            key = self.create_entity(
                kind='course',
                **self.model
            )
            self.model = self.datastore.get(key)
            self.fetched = True

        return self

    def has_student(self, student):
        if not self.fetched or not student.fetched:
            return False

        query = self.datastore.query(kind='takes')
        query.add_filter('course_id', '=', self.get_id())
        query.add_filter('student_id', '=', student.get_id())
        return len(list(query.fetch())) > 0

    def get_students(self):
        if not self.fetched:
            return list()

        query = self.datastore.query(kind='takes')
        query.add_filter('course_id', '=', self.get_id())
        takes = list(query.fetch())

        return [models.students_model.Student(id=take['student_id']) for take in takes]

    def add_student(self, student):
        if not student.fetched:
            raise ValueError('Student does not exist')

        if not student.is_student():
            raise ValueError('Must add a registered student to course')

        if self.has_student(student):
            return

        self.create_entity(
            kind='takes',
            course_id=self.get_id(),
            student_id=student.get_id()
        )

        while not self.has_student(student):
            pass

        assert self.has_student(student), (
            'Adding student didn\'t work. Must be something wrong with datastore.')

    def remove_student(self, student):
        if not student.fetched:
            raise ValueError('Student must be saved to remove from course')

        if not self.has_student(student):
            print 'skippideedooda'
            return

        query = self.datastore.query(kind='takes')
        query.add_filter('course_id', '=', self.get_id())
        query.add_filter('student_id', '=', student.get_id())

        keys = [take.key for take in list(query.fetch())]

        # clean up attendance records
        if not self.has_TA(student):
            query = self.datastore.query(kind='attendance_record')
            query.add_filter('course_id', '=', self.get_id())
            query.add_filter('user_id', '=', student.get_id())

            keys = keys + [take.key for take in list(query.fetch())]

        self.datastore.delete_multi(keys)

        while self.has_student(student):
            pass

        assert not self.has_student(student), (
            'Removing student didn\'t work. Must be something wrong with datastore.')

    def get_TAs(self):
        if not self.fetched:
            return list()

        query = self.datastore.query(kind='tas')
        query.add_filter('course_id', '=', self.get_id())
        tas = list(query.fetch())

        return [models.users_model.User(id=ta['ta_id']) for ta in tas]

    def has_TA(self, ta):
        if not self.fetched or not ta.fetched:
            return False

        query = self.datastore.query(kind='tas')
        query.add_filter('course_id', '=', self.get_id())
        query.add_filter('ta_id', '=', ta.get_id())
        query.keys_only()
        return len(list(query.fetch())) > 0

    def add_TA(self, ta):
        if not ta.fetched:
            raise ValueError('TA must be saved to add to course')

        if self.has_TA(ta):
            return

        self.create_entity(
            kind='tas',
            course_id=self.get_id(),
            ta_id=ta.get_id()
        )

        while not self.has_TA(ta):
            pass

        assert self.has_TA(ta), 'Adding TA didn\'t work. Must be something wrong with datastore'

    def remove_TA(self, ta):
        if not ta.fetched:
            raise ValueError('TA must be saved to remove from course')

        if not self.has_TA(ta):
            return

        query = self.datastore.query(kind='tas')
        query.add_filter('course_id', '=', self.get_id())
        query.add_filter('ta_id', '=', ta.get_id())

        keys = [t.key for t in list(query.fetch())]

        # clean up attendance records
        if not self.has_student(ta):
            query = self.datastore.query(kind='attendance_record')
            query.add_filter('course_id', '=', self.get_id())
            query.add_filter('user_id', '=', ta.get_id())

            keys = keys + [take.key for take in list(query.fetch())]

        self.datastore.delete_multi(keys)

        while self.has_TA(ta):
            pass

        assert not self.has_TA(ta), (
            'Removing TA didn\'t work. Must be something wrong with datastore')

    def get_open_session(self):
        if not self.fetched:
            return None

        query = self.datastore.query(kind='attendance_window')
        query.add_filter('course_id', '=', self.get_id())
        query.add_filter('closed_at', '=', None)
        sessions = list(query.fetch())
        if len(sessions) == 0:
            return None

        return sessions[0]

    def open_session(self):
        if not self.fetched:
            raise ValueError('Course must be saved to open its session')

        session = self.get_open_session()

        if session is None:
            key = self.create_entity(
                kind='attendance_window',
                course_id=self.get_id(),
                opened_at=datetime.now(),
                closed_at=None,
                secret=randint(1000, 9999)
            )

            while session is None:
                session = self.datastore.get(key)
                pass

        return session['secret']

    def close_session(self):
        session = self.get_open_session()
        if session is None:
            return

        session.update({
            'closed_at': datetime.now()
        })

        self.datastore.put(session)

        while self.get_open_session() is not None:
            pass

    def session_count(self):
        if not self.fetched:
            return None

        query = self.datastore.query(kind='attendance_window')
        query.add_filter('course_id', '=', self.get_id())
        query.keys_only()
        return len(list(query.fetch()))

    def sign_student_in(self, student, secret=None):
        if not self.fetched:
            raise ValueError('Course must be saved to sign in to')

        if not student.fetched:
            raise ValueError('Student must be saved to sign in')

        if not self.has_student(student) and not self.has_TA(student):
            raise ValueError('Student must be in course to sign in')

        session = self.get_open_session()

        if session is None:
            raise CourseNotTakingAttendance('Course\'s attendance window is not open')

        if str(secret) != str(session['secret']) and not (secret is None and self.has_TA(student)):
            return False

        query = self.datastore.query(kind='attendance_record')
        query.add_filter('attendance_window_id', '=', session.key.id)
        query.add_filter('user_id', '=', student.get_id())
        query.keys_only()
        signed_in = len(list(query.fetch())) > 0

        if signed_in:
            raise ValueError('Student already signed into session')

        self.create_entity(
            kind='attendance_record',
            attendance_window_id=session.key.id,
            user_id=student.get_id(),
            # not strictly necessary, but good for performance in get_attendance_records
            course_id=self.get_id()
        )

        while not self.currently_signed_in(student):
            pass

        return True

    def currently_signed_in(self, student):
        if not student.fetched:
            raise ValueError('Unsaved user cannot be signed into a course')

        if not self.fetched:
            raise ValueError('Cannot be signed into an unsaved course')

        session = self.get_open_session()

        if session is None:
            return False

        query = self.datastore.query(kind='attendance_record')
        query.add_filter('user_id', '=', student.get_id())
        query.add_filter('attendance_window_id', '=', session.key.id)
        query.keys_only()
        return len(list(query.fetch())) > 0

    def get_attendance_records(self, student=None, ta=None):
        query = self.datastore.query(kind='attendance_record')
        query.add_filter('course_id', '=', self.get_id())

        user = student or ta

        if user is not None:
            if not user.fetched:
                return list()
            query.add_filter('user_id', '=', user.get_id())
        return list(query.fetch())

    def get_attendance_details(self, student):
        if not self.fetched:
            raise ValueError('Can\'t get attendance details of an unsaved course')

        if not self.has_student(student) and not self.has_TA(student):
            return []

        query = self.datastore.query(kind='attendance_window')
        query.add_filter('course_id', '=', self.get_id())
        windows = list(query.fetch())

        query = self.datastore.query(kind='attendance_record')
        query.add_filter('user_id', '=', student.get_id())
        query.add_filter('course_id', '=', self.get_id())
        records = list(query.fetch())

        details = list()
        for window in windows:
            relevant_records = [record for record in records
                                if record['attendance_window_id'] == window.key.id]
            details.append({
                'opened_at': window['opened_at'],
                'closed_at': window['closed_at'],
                'user_id': student.get_id(),
                'session_id': window.key.id,
                'attended': len(relevant_records) > 0
            })
        details.sort(key=lambda record: [record['opened_at'], record['closed_at']])

        return details

    def edit_attendance_history(self, **kwargs):
        if not self.fetched:
            raise ValueError('Can\'t change attendance of an unsaved course')

        if 'student' not in kwargs and 'ta' not in kwargs:
            raise ValueError('No student or TA specified')

        if 'attended' not in kwargs:
            raise ValueError('`attended` not specified')

        if 'session_id' not in kwargs or kwargs['session_id'] is None:
            raise ValueError('`session_id` not specified')

        user = None
        if 'student' in kwargs:
            user = kwargs['student']
            if not user.takes_course(self):
                raise ValueError('Student does not take course')
        else:
            user = kwargs['ta']
            if not user.tas_course(self):
                raise ValueError('TA does not TA course')

        query = self.datastore.query(kind='attendance_record')
        query.add_filter('user_id', '=', user.get_id())
        query.add_filter('course_id', '=', self.get_id())
        query.add_filter('attendance_window_id', '=', kwargs['session_id'])
        query.keys_only()
        records = list(query.fetch())
        record = records[0] if len(records) > 0 else None

        if kwargs['attended'] == (record is not None):
            return

        if kwargs['attended']:
            self.create_entity(
                kind='attendance_record',
                user_id=user.get_id(),
                course_id=self.get_id(),
                attendance_window_id=kwargs['session_id']
            )
        else:
            self.datastore.delete_multi([r.key for r in records])

    def destroy(self):
        super(self.__class__, self).destroy()

        # clean up attendance windows, records, and join table entities
        keys = list()
        for kind in ['attendance_record', 'attendance_window', 'tas', 'takes', 'teaches']:
            query = self.datastore.query(kind=kind)
            query.add_filter('course_id', '=', self.get_id())
            query.keys_only()
            keys = keys + [e.key for e in list(query.fetch())]

        self.datastore.delete_multi(keys)
