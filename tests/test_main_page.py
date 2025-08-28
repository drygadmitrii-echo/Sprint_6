import pytest
import allure
from pages.main_page import MainPage
from helpers.data import Questions
from helpers.urls import Urls


class TestMainPage:
    @allure.feature("Тесты раздела 'Вопросы о важном'")
    @pytest.mark.parametrize("index, expected_answer",
                             list(enumerate(Questions.EXPECTED_ANSWERS)))
    def test_questions_about_important(self, driver, index, expected_answer):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.accept_cookies()

        initial_answer = main_page.get_answer_text(index)
        main_page.click_question(index)
        
        actual_answer = main_page.get_answer_text(index)
        assert actual_answer == expected_answer
        assert actual_answer != initial_answer  # Проверяем, что ответ изменился

    @allure.feature("Тесты переходов по логотипам")
    def test_scooter_logo_redirect(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.accept_cookies()
        main_page.click_scooter_logo()

        assert driver.current_url == Urls.MAIN

    @allure.feature("Тесты переходов по логотипам")
    def test_yandex_logo_redirect(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_site()
        main_page.accept_cookies()
        main_page.click_yandex_logo()

        main_page.wait_for_url_contains("dzen.ru")
        assert "dzen.ru" in driver.current_url or "yandex.ru" in driver.current_url
