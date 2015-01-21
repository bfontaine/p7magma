# -*- coding: UTF-8 -*-

import platform

if platform.python_version() < '2.7':
    import unittest2 as unittest
else:
    import unittest

from magma.courses import Course, CoursesList


class TestCourses(unittest.TestCase):

    def setUp(self):
        # without results
        self.course1 = Course(code="AB", title="Alpha Beta", semester=2,
                status="REC", ects=42.0, followed=True, result=0, session="")
        # with results
        self.course2 = Course(code="AB", title="Alpha Beta", semester=2,
                status="REC", ects=42.0, followed=True, result=13.21,
                session="XX")

    # Course
    # Course#__str__

    def test_course_str_no_results(self):
        self.assertEquals("Alpha Beta (AB, S2) [REC, 42.00 ECTS]",
                str(self.course1))

    def test_course_str_results(self):
        expected = "Alpha Beta (AB, S2) [REC, 42.00 ECTS] --> 13.21/20 (XX)"
        self.assertEquals(expected, str(self.course2))

    # CoursesList

    def test_courseslist_init_with_list(self):
        cs = CoursesList([self.course1, self.course2])
        self.assertIs(cs[0], self.course1)
        self.assertIs(cs[1], self.course2)

    # TODO CoursesList#_populate

    # CoursesList#filter

    def test_courses_filter_str(self):
        self.course1["foo"] = 42
        cs = CoursesList([self.course1, self.course2])
        self.assertEquals([self.course1], cs.filter("foo"))

    def test_courses_filter_fn(self):
        cs = CoursesList([self.course1, self.course2])
        self.assertEquals([], cs.filter(lambda e: False))

    # CoursesList#followed

    def test_courseslist_followed(self):
        self.course2["followed"] = False
        cs = CoursesList([self.course1, self.course2])
        self.assertEquals([self.course1], cs.followed())

    # CoursesList#with_results

    def test_courseslist_with_results(self):
        cs = CoursesList([self.course1, self.course2])
        self.assertEquals([self.course2], cs.with_results())
