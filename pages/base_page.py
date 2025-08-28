from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from helpers.urls import Urls
import allure


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = Urls.BASE

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}"
        )

    @allure.step("Найти элементы {locator}")
    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Can't find elements by locator {locator}"
        )

    @allure.step("Найти кликабельный элемент {locator}")
    def find_clickable_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable: {locator}"
        )

    @allure.step("Перейти на сайт")
    def go_to_site(self):
        return self.driver.get(Urls.MAIN)

    @allure.step("Кликнуть на элемент {locator}")
    def click_element(self, locator):
        element = self.find_clickable_element(locator)
        element.click()

    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def input_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator):
        element = self.find_element(locator)
        return element.text

    @allure.step("Дождаться видимости элемента {locator}")
    def wait_for_visibility(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Переключиться на новое окно")
    def switch_to_new_window(self):
        return self.driver.switch_to.window(self.driver.window_handles[1])

    @allure.step("Принять куки")
    def accept_cookies(self):
        cookie_button = (By.ID, "rcc-confirm-button")
        try:
            self.click_element(cookie_button)
        except:
            pass

    @allure.step("Скроллить к элементу")
    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    @allure.step("Кликнуть через JavaScript")
    def click_via_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    @allure.step("Дождаться количества окон: {number}")
    def wait_for_number_of_windows(self, number, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.number_of_windows_to_be(number)
        )

    @allure.step("Проверить URL содержит {text}")
    def wait_for_url_contains(self, text, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )
