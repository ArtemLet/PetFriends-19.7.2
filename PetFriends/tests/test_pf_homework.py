import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_invalid_user(email='abcdef@mm.com', password=valid_password):
    """ Проверяем что запрос api ключа с невалидным email возвращает статус 403
     и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_password(email=valid_email, password='777'):
    """ Проверяем что запрос api ключа c невалидным password возвращает статус 403
     и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_without_name(name= '', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpeg'):
    """Проверяем что нельзя добавить питомца с пустым name"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца и сохраняем полученный ответ с кодом статуса в status
    status = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом, статус-код с некорректными данными должен быть = 400
    assert status == 400

def test_add_new_pet_without_age(name= 'Бобик', animal_type='двортерьер',
                                     age='', pet_photo='images/cat1.jpeg'):
    """Проверяем что нельзя добавить питомца с пустым age"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца и сохраняем полученный ответ с кодом статуса в status
    status = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом, статус-код с некорректными данными должен быть = 400
    assert status == 400

def test_add_new_pet_without_type(name= 'Бобик', animal_type='',
                                     age='3', pet_photo='images/cat1.jpeg'):
    """Проверяем что нельзя добавить питомца с пустым animal_type"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца и сохраняем полученный ответ с кодом статуса в status
    status = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом, статус-код с некорректными данными должен быть = 400
    assert status == 400

def test_add_new_pet_without_photo(name= 'Бобик', animal_type='собака',
                                     age='3'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_add_pet_photo_jpeg(pet_photo = 'images/cat1.jpeg'):
    """Проверяем возможность успешного добавления фото питомца с корректными данными"""

    # Получаем ключ auth_key и список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    # Если список не пустой, то пробуем добавить фото
    if len(pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, pets['pets'][0]['id'], pet_photo)

        # Проверяем что фото успешно добавилось
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомцев
        raise Exception("Pet list is empty")

def test_successful_add_pet_photo_png(pet_photo = 'images/cat2.png'):
    """Проверяем возможность успешного добавления фото питомца с корректными данными"""

    # Получаем ключ auth_key и список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    # Если список не пустой, то пробуем добавить фото
    if len(pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, pets['pets'][0]['id'], pet_photo)

        # Проверяем что фото успешно добавилось
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомцев
        raise Exception("Pet list is empty")

def test_add_pet_photo_with_invalid_format(pet_photo = 'images/cat3.ico'):
    """Проверяем что нельзя добавить фото питомца с недопустимым форматом"""

    # Получаем ключ auth_key и список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    # Если список не пустой, то пробуем добавить фото
    if len(pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, pets['pets'][0]['id'], pet_photo)

        # Проверяем что фото не добавилось
        assert status == 400
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомцев
        raise Exception("Pet list is empty")

def test_add_new_pet_with_digits_in_name(name= '12345', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpeg'):
    """Проверяем что нельзя добавить питомца с числами в name"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца и сохраняем полученный ответ с кодом статуса в status
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом, статус-код с некорректными данными должен быть = 400
    assert status == 400
    assert result['name'] == name



