# -*- coding: UTF-8 -*-

class Course(object):

    def __init__(self, code, name):
        self.code = code
        self.name = name
        # TODO


class CoursesList(list):

    def __init__(self, soup):
        super(list, self).__init__()

        self.soup = soup  # TEST
        tables = soup.select('table[rules=all]')
        # TODO
