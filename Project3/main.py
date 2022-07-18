import requests
from bs4 import BeautifulSoup

url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3' \
      '%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2'

request = requests.get(url)

list_countries = {0: {'country_name': '',
                      'full_country_name': '',
                      'same_letter_count': 0,
                      'flag_url': '',
                      'words_full_country_name': 0
                      }
                  }


def main():
    soup = BeautifulSoup(request.text, "html.parser")
    countries_url = soup.find("table", class_="wikitable").findAll("img")
    table_fields = soup.find("table", class_="wikitable").findAll("tr")

    # Удаляем поле с наименованиям столбцов таблицы
    del table_fields[0]

    for i in range(0, len(table_fields)):
        # Создаем нужное количество элементов словаря расчитаное на количество стран в таблице
        list_countries[i] = {}
        # Берем полное название страны из столбца №4
        list_countries[i]["full_country_name"] = table_fields[i].find_all("td")[3].text
        # Делим строку с полным названием на слова
        word_count = list_countries[i]["full_country_name"].split()
        # Записываем количество слов
        list_countries[i]["words_full_country_name"] = len(word_count)
        # Короткое имя
        list_countries[i]["country_name"] = table_fields[i].find_all("td")[2].text

    # Считаем количество странн начинающихся на одну и ту же букву
    for i in range(0, len(table_fields)):
        counter = 0
        for j in range(0, len(table_fields)):
            # Преобразуем буквы к одному регистру и сравниваем их
            first_country_name = list_countries[i]["country_name"].lower()
            second_country_name = list_countries[j]["country_name"].lower()
            # Если буквы совпали увеличиваем счетчик
            if first_country_name[0] == second_country_name[0]:
                counter += 1
        # Записываем в словарь полученные данные
        list_countries[i]["same_letter_count"] = counter

    for i in range(0, len(countries_url)):
        list_countries[i]["flag_url"] = countries_url[i].get("src")


# Функция для полученния данных конкретной странны по ее короткому имени
def find_country(country_name):
    country_name = country_name.lower()
    i = 0

    while i < len(list_countries):
        # Убираем лишний символ переноса строки
        buffer = list_countries[i]["country_name"].lower().replace("\n", "")

        # Сравниваем именна стран при совпадении выводим полную информацию о стране
        if country_name == buffer:
            print(list_countries[i]["country_name"].replace("\n", ""))
            print(list_countries[i]["full_country_name"].replace("\n", ""))
            print(list_countries[i]["same_letter_count"])
            print(list_countries[i]["words_full_country_name"])
            print(list_countries[i]["flag_url"])
            print("\n")
        i += 1


if __name__ == '__main__':
    main()
    find_country("Австралия")
    find_country("Украина")
