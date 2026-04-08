from models import courses_model, users_model


class DuplicateUNIException(Exception):
    pass


class Student(users_model.User):
    def register_as_student(self, uni=None):
        if uni is None or len(uni) == 0:
            raise ValueError('Students must have UNIs')

        query = self.datastore.query(kind='user')
        query.add_filter('uni', '=', uni)
        conflicting_students = list(query.fetch())
        if len(conflicting_students) > 0:
            raise DuplicateUNIException('Student with UNI ' + uni + ' already exists.')

        self.update(uni=uni)

        return self

    def sign_in(self, course, secret=None):
        if not self.fetched:
            raise ValueError('User must be saved to sign in')

        return course.sign_student_in(self, secret)

    def is_signed_into(self, course):
        return course.currently_signed_in(self)

    def takes_course(self, course):
        if not self.fetched or not self.is_student():
            raise ValueError('User must be a registered student to take a course')

        return course.has_student(self)

    def get_courses(self):
        if not self.fetched or not self.is_student():
            raise ValueError('User must be saved to have a course')

        query = self.datastore.query(kind='takes')
        query.add_filter('student_id', '=', self.get_id())
        takes = list(query.fetch())
        return [courses_model.Course(id=take['course_id']) for take in takes]

    def as_TA(self):
        from models import tas_model
        if not self.fetched:
            return tas_model.TA(**self.model)

        return tas_model.TA(id=self.get_id())
