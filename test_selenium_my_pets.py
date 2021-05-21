import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


class Pet:

    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    def __hash__(self):
        return hash(self.name) ^ hash(self.breed) ^ hash(self.age)

    def __eq__(self, other):
        if isinstance(other, Pet):
            return (self.name == other.name) and (self.breed == other.breed) and (self.age == other.age)
        else:
            return False


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('./chromedriver')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends1.herokuapp.com/login')

   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('natali_test@gmail.com')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('qwerty1234')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

   pytest.driver.get('http://petfriends1.herokuapp.com/my_pets')

   yield

   pytest.driver.quit()


def test_number_of_pets_match_pets_blocks_on_the_screen():
    div_with_overall_number_of_pets_element = WebDriverWait(pytest.driver, 10).until(presence_of_element_located((By.CSS_SELECTOR, "html > body > div > div > div")))

    div_with_overall_number_of_pets =div_with_overall_number_of_pets_element.text
    number_of_pets = int(div_with_overall_number_of_pets.split('\n')[1].split('Питомцев: ')[1])
    names = pytest.driver.find_elements_by_css_selector('div#all_my_pets > table > tbody > tr > td')
    number_of_presented_pets = len(names) / 4
    assert number_of_pets == number_of_presented_pets


def test_at_least_half_have_photo_uploaded():
    div_with_overall_number_of_pets = pytest.driver.find_elements_by_css_selector('html > body > div > div > div')[0].text
    number_of_pets = int(div_with_overall_number_of_pets.split('\n')[1].split('Питомцев: ')[1])
    images = pytest.driver.find_elements_by_css_selector('div#all_my_pets > table > tbody > tr > th > img')
    number_of_uploaded_images = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_of_uploaded_images = number_of_uploaded_images + 1

    assert number_of_pets / number_of_uploaded_images < 2


def test_all_pets_have_all_text_attributes():
    text_attributes = pytest.driver.find_elements_by_css_selector('div#all_my_pets > table > tbody > tr > td')
    for i in range(len(text_attributes))[::4]:
        assert text_attributes[i].text != ''
        assert text_attributes[i+1].text != ''
        assert text_attributes[i+2].text != ''


def test_all_pets_have_different_names():
    text_attributes = pytest.driver.find_elements_by_css_selector('div#all_my_pets > table > tbody > tr > td')
    pets_names = set()
    for i in range(0, len(text_attributes), 4):
        pet_name = text_attributes[i].text
        assert pet_name not in pets_names
        pets_names.add(pet_name)


def test_there_is_no_pet_with_the_same_attributes():
    text_attributes = pytest.driver.find_elements_by_css_selector('div#all_my_pets > table > tbody > tr > td')
    pets = set()
    for i in range(0, len(text_attributes), 4):
        pet = Pet(text_attributes[i].text, text_attributes[i+1].text, text_attributes[i+2].text)
        assert pet not in pets
        pets.add(pet)
