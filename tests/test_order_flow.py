import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.order_page import OrderPage
from helpers.data import User1, User2


class TestOrderFlow:
    test_data = [
        ("header", User1),
        ("footer", User2)
    ]

    @allure.feature("Тесты процесса заказа")
    @pytest.mark.parametrize("order_button,user", test_data)
    def test_order_flow(self, driver, order_button, user):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        main_page.go_to_site()
        main_page.accept_cookies()

        # Выбор точки входа
        if order_button == "header":
            main_page.click_order_button_header()
        else:
            main_page.click_order_button_footer()

        # Ожидаем загрузки первой страницы формы
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='* Имя']"))
        )

        # Заполнение форм
        order_page.fill_first_page(
            user.NAME,
            user.LAST_NAME,
            user.ADDRESS,
            user.METRO_STATION,
            user.PHONE
        )

        # Ожидаем загрузки второй страницы формы
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='* Когда привезти самокат']"))
        )

        order_page.fill_second_page(
            user.DATE,
            user.RENTAL_PERIOD,
            user.COLOR,
            user.COMMENT
        )

        order_page.confirm_order()

        # Проверка успешного заказа
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]"))
        )
        success_message = order_page.get_success_message()
        assert "Заказ оформлен" in success_message
