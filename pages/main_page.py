from selenium.webdriver.common.by import By
from .base_page import BasePage
import allure


class MainPageLocators:
    ORDER_BUTTON_HEADER = (By.XPATH, "//button[text()='Заказать' and @class='Button_Button__ra12g']")
    ORDER_BUTTON_FOOTER = (By.XPATH, "//div[contains(@class, 'Home_FinishButton')]//button[text()='Заказать']")
    QUESTION_LOCATOR = (By.XPATH, "//div[@class='accordion__item']")
    QUESTION_BUTTON = (By.XPATH, ".//div[@class='accordion__button']")
    ANSWER_LOCATOR = (By.XPATH, ".//div[@class='accordion__panel']/p")
    SCOOTER_LOGO = (By.CLASS_NAME, "Header_LogoScooter__3lsAR")
    YANDEX_LOGO = (By.CLASS_NAME, "Header_LogoYandex__3TSOI")
    NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")


class MainPage(BasePage):
    @allure.step("Нажать на вопрос номер {index}")
    def click_question(self, index):
        questions = self.find_elements(MainPageLocators.QUESTION_LOCATOR)
        question = questions[index]
        self.scroll_to_element(question)
        
        question_button = question.find_element(*MainPageLocators.QUESTION_BUTTON)
        self.click_via_js(question_button)
        
        # Ждем появления ответа
        answer = question.find_element(*MainPageLocators.ANSWER_LOCATOR)
        self.wait_for_visibility((By.XPATH, f"{MainPageLocators.ANSWER_LOCATOR[1]}"))

    @allure.step("Получить текст ответа номер {index}")
    def get_answer_text(self, index):
        questions = self.find_elements(MainPageLocators.QUESTION_LOCATOR)
        question = questions[index]
        answer = question.find_element(*MainPageLocators.ANSWER_LOCATOR)
        return answer.text

    @allure.step("Нажать на кнопку 'Заказать' в хедере")
    def click_order_button_header(self):
        self.click_element(MainPageLocators.ORDER_BUTTON_HEADER)
        self.wait_for_visibility(MainPageLocators.NAME_INPUT)

    @allure.step("Нажать на кнопку 'Заказать' в футере")
    def click_order_button_footer(self):
        footer_button = self.find_element(MainPageLocators.ORDER_BUTTON_FOOTER)
        self.scroll_to_element(footer_button)
        self.click_via_js(footer_button)
        self.wait_for_visibility(MainPageLocators.NAME_INPUT)

    @allure.step("Нажать на логотип Самоката")
    def click_scooter_logo(self):
        self.click_element(MainPageLocators.SCOOTER_LOGO)

    @allure.step("Нажать на логотип Яндекса")
    def click_yandex_logo(self):
        self.click_element(MainPageLocators.YANDEX_LOGO)
        self.wait_for_number_of_windows(2)
        self.switch_to_new_window()
