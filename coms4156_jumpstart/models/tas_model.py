from models import students_model, courses_model


class TA(students_model.Student):
    def tas_course(self, course):
        if not self.fetched:
            raise ValueError('TA must be saved to TA a course')

        return course.has_TA(self)

    def get_taed_courses(self):
        if not self.fetched:
            raise ValueError('TA must be saved to TA a course')

        query = self.datastore.query(kind='tas')
        query.add_filter('ta_id', '=', self.get_id())
        tas = list(query.fetch())
        return [courses_model.Course(id=ta['course_id']) for ta in tas]

    def as_TA(self):
        return self
