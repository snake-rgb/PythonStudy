import requests
import json

requestCount = 0
failedJoke = 0
niceJoke = 0
jokesCounter = 0
person_dict = {
    "Jokes": {},
    "Results": {
        "Requests": 0,
        "Saved jokes": 0,
        "Failed jokes": 0,
        "Nice jokes": 0,
    }
}

for i in range(1, 101):
    res = requests.get('https://v2.jokeapi.dev/joke/Any?type=single')
    if res.ok:
        requestCount = requestCount + 1
        req = res.json()
        print(req['joke'])
        print('________________________________')

    if len(req['joke']) < 60 and req['joke'].find('code') == -1:
        failedJoke = failedJoke + 1
    else:
        niceJoke = niceJoke + 1
        jokesCounter = jokesCounter + 1
        person_dict['Jokes']['joke_' + str(jokesCounter)] = req['joke']
        with open("data_file.json", "w") as write_file:
            json.dump(person_dict, write_file)

person_dict['Results']['Requests'] = requestCount
person_dict['Results']['Saved jokes'] = niceJoke
person_dict['Results']['Failed jokes'] = failedJoke
person_dict['Results']['Nice jokes'] = niceJoke
with open("data_file.json", "w") as write_file:
    json.dump(person_dict, write_file, indent=4, sort_keys=False)
