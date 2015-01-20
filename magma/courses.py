# -*- coding: UTF-8 -*-

class Course(dict):
    pass


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
                    code=tds[0].text,
                    name=tds[1].text,
                    semester=tds[2].text,
                    status=tds[3].text,
                    ects=tds[4].text,
                    followed=tds[5].text,
                    score=tds[6].text,
                    session=tds[7].text,
            )
            self.append(cs)
