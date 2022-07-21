from datetime import date, timedelta
import itertools


def schedule2(date_start="2022-04-20", date_end="2022-04-23", days_work=1, days_skip=1):
    d0 = date.fromisoformat(date_start)
    d1 = date.fromisoformat(date_end)

    res = d1 - d0
    date_work = []
    data = []

    for i in itertools.compress([res.days, days_work, days_skip, d0], [1, 1, 1, 1]):
        data.append(i)

        if type(i) == date:
            for j in itertools.count(data[0], -1):
                if j <= 0:
                    break
                if data[1] > 0:
                    if data[1] != 1:
                        for k in itertools.count(0, 1):
                            if k < data[2]:
                                data[3] += timedelta(k)
                                date_work.append(data[3])
                            else:
                                break
                    else:
                        if len(date_work) >= 1:
                            data[3] += timedelta(1)
                            date_work.append(data[3])
                        else:
                            data[3] += timedelta(0)
                            date_work.append(data[3])

                data[3] += timedelta(days_skip)
                data[0] -= days_work + days_skip

    if days_skip == 0:
        d0 = date_work[-1] + timedelta(1)
        date_work.append(d0)
    return date_work
