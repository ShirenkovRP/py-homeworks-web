import requests


def get_ad():
    response = requests.get('http://127.0.0.1:8088/advert/3')
    print(response.text)


def create_ad():
    response = requests.post(
        'http://127.0.0.1:8088/advert',
        json={ 'author': "Roman", 'title': 'chandelier', 'description': 'for sale'}
    )
    print(response.text)


def delete_ad():
    response = requests.delete(f'http://127.0.0.1:8088/advert/1')
    print(response.text)

get_ad()
create_ad()
delete_ad()