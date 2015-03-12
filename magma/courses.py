# -*- coding: UTF-8 -*-

from magma.souputils import text, coursecode, parseint, parsefloat, parsebool
from magma.souputils import parseresult

import platform
if platform.python_version() >= '3.0':
    unicode = str


class Course(dict):
    """
    A course, which is a dict with at least the following attributes:
        - title
        - statut (REC or OPT)
    depending on the year it might have these ones:
        M1:
            - jury
        M2:
            - code
            - semester (1 or 2)
            - ects
    and possibly the following ones:
        - result (None or float or str)
        - session
    """

    def desc(self):
        """
        A textual description of this course
        """
        if 'ects' in self:
            fmt = '%s (%s, S%d) [%s, %.2f ECTS]'
            fields = ('title', 'code', 'semester', 'status', 'ects')
        else:
            fmt = '%s'
            fields = ('title',)

        s = fmt % tuple([self[f] for f in fields])

        if self['followed'] and self['session']:
            res = self['result']
            if self.get('jury', 0) > 0:
                res = self['jury']

            s += ' --> %.2f/20 (%s)' % (res, self['session'])

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
        trs = tables[0].select('tr')[1:]

        if len(trs[0]) == 5:
            # M1
            self._populate_small_table(trs)
        else:
            # M2
            self._populate_large_table(trs)

    def _populate_small_table(self, trs):
        """
        Populate the list, given that ``trs`` is a ``BeautifulSoup`` elements
        list from a large table (5 columns).
        """
        for tr in trs:
            tds = tr.select('td')
            cs = Course(
                title=text(tds[0]),
                followed=parsebool(tds[1]),
            )

            followed = cs['followed']
            cs['result'] = parsefloat(tds[2]) if followed else None
            cs['jury'] = parsefloat(tds[3]) if followed else None
            cs['session'] = text(tds[4]) if followed else None

            self.append(cs)

    def _populate_large_table(self, trs):
        """
        Populate the list, given that ``trs`` is a ``BeautifulSoup`` elements
        list from a large table (8 columns).
        """
        for tr in trs:
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
            cs['session'] = text(tds[7]) if followed else None
            cs['result'] = parseresult(tds[6]) if followed else None

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
