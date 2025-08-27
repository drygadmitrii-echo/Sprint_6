from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure
import time


class OrderPageLocators:
    # Форма заказа
    NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_STATION_OPTION = (By.XPATH, "//div[@class='select-search__select']//li/button")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    # Форма о аренде
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.XPATH, "//div[text()='* Срок аренды']")
    RENTAL_PERIOD_OPTION = (By.XPATH, "//div[@class='Dropdown-option']")
    COLOR_CHECKBOX_BLACK = (By.ID, "black")
    COLOR_CHECKBOX_GREY = (By.ID, "grey")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Заказать' and contains(@class, 'Button_Middle__1CSJM')]")

    # Модальное окно подтверждения
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")


class OrderPage(BasePage):
    @allure.step("Заполнить первую страницу формы заказа")
    def fill_first_page(self, name, last_name, address, metro_station, phone):
        self.input_text(OrderPageLocators.NAME_INPUT, name)
        self.input_text(OrderPageLocators.LAST_NAME_INPUT, last_name)
        self.input_text(OrderPageLocators.ADDRESS_INPUT, address)

        # Выбор станции метро
        self.click_element(OrderPageLocators.METRO_STATION_INPUT)
        metro_options = self.find_elements(OrderPageLocators.METRO_STATION_OPTION)
        self.click_via_js(metro_options[metro_station])

        self.input_text(OrderPageLocators.PHONE_INPUT, phone)
        self.click_element(OrderPageLocators.NEXT_BUTTON)
        time.sleep(2)  # Ожидание перехода на вторую страницу

    @allure.step("Заполнить вторую страницу формы заказа")
    def fill_second_page(self, date, rental_period, color, comment):
        # Ждем загрузки второй страницы
        time.sleep(2)

        # Заполнение даты - используем правильный локатор
        date_input = self.find_element(OrderPageLocators.DATE_INPUT)
        date_input.clear()
        date_input.send_keys(date)

        # Нажимаем Enter чтобы подтвердить дату и закрыть календарь
        date_input.send_keys("\n")

        # Выбор срока аренды
        self.click_element(OrderPageLocators.RENTAL_PERIOD_DROPDOWN)
        period_options = self.find_elements(OrderPageLocators.RENTAL_PERIOD_OPTION)
        self.click_via_js(period_options[rental_period])

        # Выбор цвета
        if color == "black":
            checkbox = self.find_element(OrderPageLocators.COLOR_CHECKBOX_BLACK)
            self.click_via_js(checkbox)

        # Комментарий
        self.input_text(OrderPageLocators.COMMENT_INPUT, comment)

        # Скролл и клик на заказ
        order_button = self.find_element(OrderPageLocators.ORDER_BUTTON)
        self.scroll_to_element(order_button)
        self.click_via_js(order_button)
        time.sleep(1)  # Ожидание модального окна

    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        self.click_element(OrderPageLocators.CONFIRM_BUTTON)
        time.sleep(1)  # Ожидание подтверждения

    @allure.step("Получить текст сообщения об успешном заказе")
    def get_success_message(self):
        return self.get_text(OrderPageLocators.SUCCESS_MESSAGE)