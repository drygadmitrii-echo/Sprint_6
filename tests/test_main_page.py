import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from helpers.data import Questions, Urls


class TestMainPage:
    @allure.feature("Тесты раздела 'Вопросы о важном'")
    @pytest.mark.parametrize("index, expected_answer",
                             list(enumerate(Questions.EXPECTED_ANSWERS)))
    def test_questions_about_important(self, driver, index, expected_answer):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.accept_cookies()

        # Получаем текст ответа до клика (должен быть скрыт)
        initial_answer = main_page.get_answer_text(index)

        # Кликаем на вопрос
        main_page.click_question(index)

        # Ждем появления ответа
        WebDriverWait(driver, 10).until(
            lambda d: main_page.get_answer_text(index) != initial_answer
        )

        actual_answer = main_page.get_answer_text(index)
        assert actual_answer == expected_answer

    @allure.feature("Тесты переходов по логотипам")
    def test_scooter_logo_redirect(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.accept_cookies()
        main_page.click_scooter_logo()

        assert driver.current_url == Urls.MAIN_PAGE

    @allure.feature("Тесты переходов по логотипам")
    def test_yandex_logo_redirect(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.accept_cookies()
        main_page.click_yandex_logo()

        # Ждем открытия нового окна
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        main_page.switch_to_new_window()

        # Ждем загрузки страницы
        WebDriverWait(driver, 15).until(
            lambda d: "dzen.ru" in d.current_url or "yandex.ru" in d.current_url
        )
        assert "dzen.ru" in driver.current_url or "yandex.ru" in driver.current_url