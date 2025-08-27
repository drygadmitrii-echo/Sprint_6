from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure
import time


class MainPageLocators:
    # Кнопки заказа
    ORDER_BUTTON_HEADER = (By.XPATH, "//button[text()='Заказать' and @class='Button_Button__ra12g']")
    ORDER_BUTTON_FOOTER = (By.XPATH, "//div[contains(@class, 'Home_FinishButton')]//button[text()='Заказать']")

    # Вопросы о важном
    QUESTION_LOCATOR = (By.XPATH, "//div[@class='accordion__item']")
    QUESTION_BUTTON = (By.XPATH, ".//div[@class='accordion__button']")
    ANSWER_LOCATOR = (By.XPATH, ".//div[@class='accordion__panel']/p")

    # Логотипы
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")


class MainPage(BasePage):
    @allure.step("Нажать на вопрос номер {index}")
    def click_question(self, index):
        # Скроллим к вопросам
        questions = self.find_elements(MainPageLocators.QUESTION_LOCATOR)
        question = questions[index]
        self.scroll_to_element(question)

        # Находим кнопку вопроса внутри элемента
        question_button = question.find_element(*MainPageLocators.QUESTION_BUTTON)
        self.click_via_js(question_button)
        time.sleep(1)  # Небольшая задержка для анимации

    @allure.step("Получить текст ответа номер {index}")
    def get_answer_text(self, index):
        questions = self.find_elements(MainPageLocators.QUESTION_LOCATOR)
        question = questions[index]

        # Находим ответ внутри элемента вопроса
        answer = question.find_element(*MainPageLocators.ANSWER_LOCATOR)
        return answer.text

    @allure.step("Нажать на кнопку 'Заказать' в хедере")
    def click_order_button_header(self):
        self.click_element(MainPageLocators.ORDER_BUTTON_HEADER)

    @allure.step("Нажать на кнопку 'Заказать' в футере")
    def click_order_button_footer(self):
        footer_button = self.find_element(MainPageLocators.ORDER_BUTTON_FOOTER)
        self.scroll_to_element(footer_button)
        self.click_via_js(footer_button)

    @allure.step("Нажать на логотип Самоката")
    def click_scooter_logo(self):
        self.click_element(MainPageLocators.SCOOTER_LOGO)

    @allure.step("Нажать на логотип Яндекса")
    def click_yandex_logo(self):
        self.click_element(MainPageLocators.YANDEX_LOGO)
        self.switch_to_new_window()