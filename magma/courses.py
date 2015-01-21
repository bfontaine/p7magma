# -*- coding: UTF-8 -*-

from magma.souputils import text, coursecode, parseint, parsefloat, parsebool

import platform
if platform.python_version() >= '3.0':
    unicode = str


class Course(dict):
    """
    A course, which is a dict with at least the following attributes:
        - title
        - code
        - semester (1 or 2)
        - statut (REC or OPT)
        - ects
    and possibly the following one:
        - result
        - session
    """

    def desc(self):
        """
        A textual description of this course
        """
        s = '%s (%s, S%d) [%s, %.2f ECTS]' % (
            self['title'], self['code'], self['semester'], self['status'],
            self['ects'])
        if self['followed'] and self['session']:
            s += ' --> %.2f/20 (%s)' % (self['result'], self['session'])

        return s


class CoursesList(list):
    """
    A list of ``Course``s
    """

    def __init__(self, lst=None):
        """
        Create a new courses list, either empty, from another courses list, or
        from a ``BeautifulSoup`` object.
        """
        super(list, self).__init__()
        if lst is None:
            return
        if hasattr(lst, 'HTML_FORMATTERS'):  # is a soup
            self._populate(lst)
        else:
            for c in lst:
                self.append(c)

    def _populate(self, soup):
        """
        Populate the list, assuming ``soup`` is a ``BeautifulSoup`` object.
        """
        tables = soup.select('table[rules=all]')
        if not tables:
            return
        table = tables[0]
        for tr in table.select('tr')[1:]:
            tds = tr.select('td')
            cs = Course(
                code=coursecode(tds[0]),
                title=text(tds[1]),
                semester=parseint(tds[2]),
                status=text(tds[3]),
                ects=parsefloat(tds[4]),
                followed=parsebool(tds[5]),
            )

            followed = cs['followed']
            cs['result'] = parsefloat(tds[6]) if followed else None
            cs['session'] = text(tds[7]) if followed else None

            self.append(cs)

    def desc(self):
        """
        Return a textual representation of this list
        """
        return "\n".join([c.desc() for c in self])

    # filters

    def filter(self, criteria):
        """
        Return a filtered version of this list following the given criteria,
        which can be a string (take only courses where this attribute is
        truthy) or a function which takes a course and return a boolean.
        """
        if isinstance(criteria, str) or isinstance(criteria, unicode):
            _criteria = criteria
            criteria = lambda x: x.get(_criteria)

        return CoursesList(filter(criteria, self))

    def followed(self):
        """
        Return a filtered version of this list where all courses have their
        ``followed`` attribute set to ``True``.
        """
        return self.filter('followed')

    def with_results(self):
        """
        Return a filtered version of this list where all courses have their
        ``session`` attribute set.
        """
        return self.filter('session')
