from models import courses_model, users_model


class Teacher(users_model.User):
    def register_as_teacher(self):
        self.update(teacher=True)
        return self

    def add_course(self, name):
        if not self.fetched:
            raise ValueError('Unsaved teacher cannot create a course')

        if not self.is_teacher():
            raise ValueError('Must be a registered teacher to create a course')

        if not name:
            raise ValueError('Course must have a name')

        course = courses_model.Course(name=name).get_or_create()
        self.create_entity(
            kind='teaches',
            teacher_id=self.get_id(),
            course_id=course.get_id()
        )

        while not self.teaches_course(course):
            pass

        return course

    def remove_course(self, course):
        if not self.fetched:
            raise ValueError('Unsaved teacher cannot remove a course')

        if not self.is_teacher():
            raise ValueError('Must be a registered teacher to remove a course')

        if not course.fetched:
            raise ValueError('Course must be saved to be removed.')

        if not self.teaches_course(course):
            return

        course.destroy()

    def teaches_course(self, course):
        if not self.fetched or not course.fetched:
            return False

        query = self.datastore.query(kind='teaches')
        query.add_filter('teacher_id', '=', self.get_id())
        query.add_filter('course_id', '=', course.get_id())
        query.keys_only()
        return len(list(query.fetch())) > 0

    def get_courses(self):
        if not self.fetched or not self.is_teacher():
            return list()

        query = self.datastore.query(kind='teaches')
        query.add_filter('teacher_id', '=', self.get_id())
        joins = query.fetch()
        return [courses_model.Course(id=join['course_id']) for join in joins]
