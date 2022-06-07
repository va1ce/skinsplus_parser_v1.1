from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

url = "https://skins.plus/buy"
options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
options.add_argument("--headless")
options.set_preference('dom.webnotifications.enabled', False)
driver = webdriver.Firefox(
    executable_path="E:\selenium\geckodriver.exe",
    options=options
)

def print_hi():
    try:

        #driver.fullscreen_window() #делаем на весь экран
        driver.get(url=url) #открываем сайт
        time.sleep(15)
        action_chains = ActionChains(driver)
        element = driver.find_element(by=By.XPATH, value='//*[@id="app-scroll"]/div[3]')
        action_chains.drag_and_drop_by_offset(element, 0, 300).perform()
        time.sleep(4)
        # driver.find_element(by = By.XPATH , value = '/html/body/div[1]/div/div[1]/div/div/div/div[6]/div/div/div[2]/div[3]/div/div/div[1]/div[1]/label[1]/div/div/div[2]/input').send_keys('case')
        # skins = driver.find_element(by=By.XPATH, value = '//*[@id="skinsplus-items-list"]/div[2]/div[2]')
        # text = skins.find_element(by=By.CLASS_NAME, value='absolute absolute-center text-center error-message')
        # print(text)
        # Скролинг
        # element = driver.find_element(by = By.XPATH , value = '//*[@id="scroll-skinsplusItems"]/div[3]')
        # for i in range (50):
        #     action_chains.drag_and_drop_by_offset(element,0 , 10).perform()
        #     time.sleep(0.100)
        # print("перенес")
        with open("index_selenium.html", "w", encoding="UTF-8") as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    # finally:
    #     driver.close()
    #         src = file.read()
    #     return src
    #
    # 
def check_all_items():
    #     # СКРОЛИМ ДО КОНЦА СТРАНИЦЫ
    #     try:
    #     driver.quit()
    with open("index_selenium.html", encoding="UTF-8") as file:
        action_chains = ActionChains(driver)
        element = driver.find_element(by=By.XPATH, value='//*[@id="scroll-skinsplusItems"]/div[3]')
        for i in range (150):
            if (i <= 25):
                action_chains.drag_and_drop_by_offset(element,0 , 10).perform()
                time.sleep(0.1)
            else:
                action_chains.drag_and_drop_by_offset(element, 0, 10).perform()
                time.sleep(1)
        print("Считал")
        # СКАЧИВАЕМ HTML ФАЙЛ ЭТОЙ СТРАНИЦЫ
        with open("index_selenium_all_item.html", "w", encoding="UTF-8") as file:
            file.write(driver.page_source)
    # СЧИТЫВАЕМ В ПЕРЕМЕННУЮ scr
    with open("index_selenium_all_item.html", encoding="UTF-8") as file:
        src = file.read()
    all_item = {}
    # ПАРСИМ ВСЕ ДАННЫЕ В СЛОВАРЬ И ПОТОМ В JSON
    soup = BeautifulSoup(src, 'lxml')
    skins_card = soup.find_all('div', class_='col-md-2 col-6')
    for item in skins_card:
        try:
            namez = item.find('div', style="font-weight: 600;").find('div', ff266e3="")
            price = item.find('span', id="amount").text
            floatv = item.find('div', class_="flex items-center justify-center").text
            floatv = floatv.split("/")[-1]
            floatv = floatv[1:7]
        except:
            continue
        try:
            skins_name = namez.attrs["title"]
        except:
            print("Ошибка нейма")
        try:
            skins_sticker = item.find_all('div', class_="q-img overflow-hidden")
            stikers_base = []
            for sticker in skins_sticker:
                stik = sticker.attrs["title"]
                stikers_base.append(stik)
        except:
            stikers_base = {}

        all_item[floatv] = {
            # 'url': url,
            'market_hash_name': skins_name,
            'price': price,
            'float': floatv,
            'sticker': stikers_base,
        }
    with open('all_item.json', 'w', encoding="UTF-8") as file:
        json.dump(all_item, file, indent=4, ensure_ascii=False)
    print("ALL FILE IS LOAD")

def get_pars():
    with open("index_selenium.html", encoding="UTF-8") as file:
        src = file.read()
    result_data = {}
    soup = BeautifulSoup(src, 'lxml')
    skins_card = soup.find_all('div', class_='col-md-2 col-6')
    for item in skins_card:
        try:
            namez = item.find('div', style="font-weight: 600;").find('div', ff266e3="")
            price = item.find('span', id="amount").text
            floatv = item.find('div' , class_="flex items-center justify-center").text
            floatv = floatv.split("/")[-1]
            floatv = floatv[1:7]
        except:
            continue
        try:
            skins_name = namez.attrs["title"]
        except:
            print("Ошибка нейма")
        try:
            skins_sticker = item.find_all('div' ,class_="q-img overflow-hidden")
            stikers_base = []
            for sticker in skins_sticker:
                stik = sticker.attrs["title"]
                stikers_base.append(stik)
        except:
            stikers_base = {}

        result_data[floatv] = {
            #'url': url,
            'market_hash_name': skins_name,
            'price': price,
            'float': floatv,
            'sticker': stikers_base,
        }
    with open('result.json', 'w', encoding="UTF-8") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)
    return str(list(result_data.keys())[-1])

def check_new(src , last):
    with open('result.json', encoding="UTF-8") as file:
        result_data = json.load(file)
    fresh_new = {}
    soup = BeautifulSoup(src, 'lxml')
    skins_card = soup.find_all('div', class_='col-md-2 col-6')
    for item in skins_card:
        try:
            price = item.find('span', id="amount").text
            floatv = item.find('div', class_="flex items-center justify-center").text
            floatv = floatv.split("/")[-1]
            floatv = floatv[1:7]
            print(result_data[last]['price'])
        except:
            continue
        if floatv in result_data:
            continue
        elif (float(result_data[last]['price']) < float(price)):
            return True
        else:
            print("Не нашел ничего")
            return False

def f5():
    print("Обновляю страницу")
    driver.refresh()
    time.sleep(2)
    action_chains = ActionChains(driver)
    element = driver.find_element(by=By.XPATH, value='//*[@id="app-scroll"]/div[3]')
    action_chains.drag_and_drop_by_offset(element, 0, 300).perform()
    time.sleep(2)
    with open("index_selenium.html", "w", encoding="UTF-8") as file:
        file.write(driver.page_source)
    with open("index_selenium.html", encoding="UTF-8") as file:
        src = file.read()
    return src

if __name__ == '__main__':
    print("Запускаю браузер")
    print_hi()  # Запускаем браузер и парсим src
    print("Получаю последний элемент")
    last = get_pars() # Открываем src парсим все данные и возвращаем послдений елемент
    print("Чекаю на новые")
    reloud_page = f5()
    if (check_new(reloud_page,last)):
        print("Все гуд")
    else: (print("Нет новых скинов"))
