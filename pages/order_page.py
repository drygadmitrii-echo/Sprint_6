from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class OrderPageLocators:
    NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_STATION_OPTION = (By.XPATH, "//div[@class='select-search__select']//li/button")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.XPATH, "//div[text()='* Срок аренды']")
    RENTAL_PERIOD_OPTION = (By.XPATH, "//div[@class='Dropdown-option']")
    COLOR_CHECKBOX_BLACK = (By.ID, "black")
    COLOR_CHECKBOX_GREY = (By.ID, "grey")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Заказать' and contains(@class, 'Button_Middle__1CSJM')]")
    CONFIRM_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")


class OrderPage(BasePage):
    @allure.step("Заполнить первую страницу формы заказа")
    def fill_first_page(self, name, last_name, address, metro_station, phone):
        self.input_text(OrderPageLocators.NAME_INPUT, name)
        self.input_text(OrderPageLocators.LAST_NAME_INPUT, last_name)
        self.input_text(OrderPageLocators.ADDRESS_INPUT, address)

        self.click_element(OrderPageLocators.METRO_STATION_INPUT)
        metro_options = self.find_elements(OrderPageLocators.METRO_STATION_OPTION)
        self.click_via_js(metro_options[metro_station])

        self.input_text(OrderPageLocators.PHONE_INPUT, phone)
        self.click_element(OrderPageLocators.NEXT_BUTTON)
        self.wait_for_visibility(OrderPageLocators.DATE_INPUT)

    @allure.step("Заполнить вторую страницу формы заказа")
    def fill_second_page(self, date, rental_period, color, comment):
        date_input = self.find_element(OrderPageLocators.DATE_INPUT)
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys("\n")

        self.click_element(OrderPageLocators.RENTAL_PERIOD_DROPDOWN)
        period_options = self.find_elements(OrderPageLocators.RENTAL_PERIOD_OPTION)
        self.click_via_js(period_options[rental_period])

        if color == "black":
            checkbox = self.find_element(OrderPageLocators.COLOR_CHECKBOX_BLACK)
            self.click_via_js(checkbox)

        self.input_text(OrderPageLocators.COMMENT_INPUT, comment)

        order_button = self.find_element(OrderPageLocators.ORDER_BUTTON)
        self.scroll_to_element(order_button)
        self.click_via_js(order_button)
        self.wait_for_visibility(OrderPageLocators.CONFIRM_BUTTON)

    @allure.step("Подтвердить заказ")
    def confirm_order(self):
        self.click_element(OrderPageLocators.CONFIRM_BUTTON)
        self.wait_for_visibility(OrderPageLocators.SUCCESS_MESSAGE)

    @allure.step("Получить текст сообщения об успешном заказе")
    def get_success_message(self):
        return self.get_text(OrderPageLocators.SUCCESS_MESSAGE)
