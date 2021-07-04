import requests


HOST = "http://127.0.0.1:5000/"


# Получение записи из БД
def check_of_work_get(variable):
    resp = requests.get(f"{HOST}advert/{variable}")
    return resp.json()


# Добавление записи в БД
def check_of_work_post(json_data):
    requests.post(f"{HOST}advert", json=json_data)


# Удаление записи из БД
def check_of_work_del(variable):
    requests.delete(f"{HOST}advert/{variable}")


# Изменение записи в БД
def check_of_work_patch(variable, json_data):
    resp = requests.patch(f"{HOST}advert/{variable}", json=json_data)
    return resp.json()


advert = [{"title": "Чайник",
          "description": "ЭЛККТРО ЧАЙНИК",
           "author": "Вовчик"},
          {"title": "Люстра",
           "description": "Люстра новая 5 рожков",
           "author": "Левчик"},
          {"title": "Кресло",
           "description": "Кресло мегкое, новое",
           "author": "User"}]

for i in advert:
    check_of_work_post(i)

print(check_of_work_get(1))
print(check_of_work_get(3))
advert_up = {"title": "Диван"}
check_of_work_patch(3, advert_up)
print(check_of_work_get(3))

check_of_work_del(2)
