# -*- coding: UTF-8 -*-

from souputils import text, coursecode, parseint, parsefloat

class Course(dict):

    def __str__(self):
        results = ''
        if self['followed'] and self['session']:
            results = ' --> %.2f/20 (%s)' % (self['result'], self['session'])

        return '%s (%s, S%d) [%s, %.2f ECTS]%s' % (
            self['title'], self['code'], self['semester'], self['status'],
            self['ects'], results)


class CoursesList(list):

    def __init__(self, soup):
        super(list, self).__init__()
        self._soup = soup  # TEST

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
                    followed=text(tds[5]),
            )

            if cs['followed']:
                cs['result'] = parsefloat(tds[6])
                cs['session'] = text(tds[7])
            self.append(cs)

    def followed(self):
        return filter(lambda x: x['followed'], self)
