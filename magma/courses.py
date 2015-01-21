# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

from magma.souputils import text, coursecode, parseint, parsefloat, parsebool

import platform
if platform.python_version() >= '3.0':
    unicode = str

class Course(dict):

    def __str__(self):
        results = ''
        if self['followed'] and self['session']:
            results = ' --> %.2f/20 (%s)' % (self['result'], self['session'])

        return '%s (%s, S%d) [%s, %.2f ECTS]%s' % (
            self['title'], self['code'], self['semester'], self['status'],
            self['ects'], results)


class CoursesList(list):

    def __init__(self, lst):
        super(list, self).__init__()
        if hasattr(lst, 'HTML_FORMATTERS'):  # is a soup
            self._populate(lst)
        else:
            for c in lst:
                self.append(c)


    def _populate(self, soup):
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

    # filters

    def filter(self, criteria):
        if isinstance(criteria, str) or isinstance(criteria, unicode):
            _criteria = criteria
            criteria = lambda x: x.get(_criteria)

        return CoursesList(filter(criteria, self))

    def followed(self):
        return self.filter('followed')

    def with_results(self):
        return self.filter('result')
