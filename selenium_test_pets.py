import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
    # Указываем путь до веб-драйвера
    pytest.driver = webdriver.Chrome('/Users/Necros/Desktop/pythonProject4/chromedriver/chromedriver')
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_all_pets():
    # Вводим почту, пароль + клик "Войти"
    pytest.driver.find_element_by_id('email').send_keys('qwerty@test.ru')
    pytest.driver.find_element_by_id('pass').send_keys('qwerty')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    pytest.driver.implicitly_wait(10)

    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    pytest.driver.implicitly_wait(10)
    
    images = pytest.driver.find_elements_by_class_name('card-img-top')
    names = pytest.driver.find_elements_by_class_name('card-title')
    descriptions = pytest.driver.find_elements_by_class_name('card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ' '
        assert names[i].text != ' '
        assert descriptions[i].text != ' '
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(",")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def list_of_my_pets():
    pytest.driver.find_element_by_id('email').send_keys('qwerty@test.ru')
    pytest.driver.find_element_by_id('pass').send_keys('qwerty')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    wait = WebDriverWait(pytest.driver, 5)

    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

    pytest.driver.find_element_by_css_selector('a[href="/my_pets"]').click()

    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "QWERTY"))

    # Ищем в таблице все строки с полными данными питомцев
    css_locator = 'tbody>tr'
    data_my_pets = pytest.driver.find_elements_by_css_selector(css_locator)

    for i in range(len(data_my_pets)):
        assert wait.until(EC.visibility_of(data_my_pets[i]))
    # Проверка, что у питомца есть фото/имя/порода/возраст
    image_my_pets = pytest.driver.find_elements_by_css_selector('img[style="max-width: 100px; max-height: 100px;"]')
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            assert wait.until(EC.visibility_of(image_my_pets[i]))

    name_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
    for i in range(len(name_my_pets)):
        assert wait.until(EC.visibility_of(name_my_pets[i]))

    type_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr/td[2]')
    for i in range(len(type_my_pets)):
        assert wait.until(EC.visibility_of(type_my_pets[i]))

    age_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr/td[3]')
    for i in range(len(age_my_pets)):
        assert wait.until(EC.visibility_of(age_my_pets[i]))

    all_statistics = pytest.driver.find_element_by_xpath('//div[@class=".col-sm-4 left"]').text.split("\n")
    statistics_pets = all_statistics[1].split(" ")
    all_my_pets = int(statistics_pets[-1])

    assert len(data_my_pets) == all_my_pets

    # Проверка, у половины питомцев есть фото
    m = 0
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            m += 1
    assert m >= all_my_pets / 2

    # Проверка, у всех питомцев есть имя
    for i in range(len(name_my_pets)):
        assert name_my_pets[i].text != ''

    # Проверка, у всех питомцев есть порода
    for i in range(len(type_my_pets)):
        assert type_my_pets[i].text != ''

    # Проверка, у всех питомцев есть возраст
    for i in range(len(age_my_pets)):
        assert age_my_pets[i].text != ''

    # Проверка, у всех питомцев разные имена
    list_name_my_pets = []
    for i in range(len(name_my_pets)):
        list_name_my_pets.append(name_my_pets[i].text)
    set_name_my_pets = set(list_name_my_pets)  # преобразовываем список в множество
    assert len(list_name_my_pets) == len(
        set_name_my_pets)  # сравниваем длину списка и множества: без повторов должны совпасть

    # Проверка, в списке нет дублирующихся питомцев
    list_data_my_pets = []
    for i in range(len(data_my_pets)): 
        list_data = data_my_pets[i].text.split("\n")
        list_data_my_pets.append(list_data[0])  
    set_data_my_pets = set(list_data_my_pets)  
    assert len(list_data_my_pets) == len(
        set_data_my_pets)  
