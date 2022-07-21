from datetime import date, timedelta
import itertools
from additional import schedule2


def schedule(date_start="2022-04-20", date_end="2022-04-23", days_work=1, days_skip=1):
    d0 = date.fromisoformat(date_start)
    d1 = date.fromisoformat(date_end)
    # количество дней в расписании
    res = d1 - d0

    date_work = []
    days = res.days

    # print(f"{res.days} - Количество дней в расписании")
    # # Количество рабочих дней подряд
    # print(f"{days_work} - Количество рабочих дней подряд")
    # print(f"{days_skip} - Количество выходных дней подряд")

    while days > 0 and days_work > 0:

        if days_work != 1:
            for i in itertools.count(0, 1):
                if i < days_work:
                    d0 += timedelta(i)
                    date_work.append(d0)
                else:
                    break
        else:
            if len(date_work) >= 1:
                d0 += timedelta(1)
                date_work.append(d0)
            else:
                d0 += timedelta(0)
                date_work.append(d0)

        d0 += timedelta(days_skip)
        days -= days_work + days_skip

    if days_skip == 0:
        d0 += timedelta(1)
        date_work.append(d0)
    # print(f"{len(date_work)} - Количество рабочих дней")
    # for i in range(len(date_work)):
    # print(date_work[i])
    return date_work


def main():
    print(f"""1 schedule - {schedule("2022-04-20", "2022-04-23", 1, 0)}""")
    print(f"""2 schedule - {schedule("2022-04-25", "2022-06-26", 0, 4)}""")
    print(f"""3 schedule - {schedule("2022-05-14", "2022-05-24", 1, 95)}""")
    print(f"""4 schedule - {schedule("2022-05-14", "2022-05-30", 5, 2)}""")
    print(f"""5 schedule - {schedule("2022-05-14", "2022-06-24", 2, 5)}""")
    print(f"""6 schedule - {schedule2("2022-03-12", "2022-03-24", 1, 0)}""")


if __name__ == '__main__':
    main()
