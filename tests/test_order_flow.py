import pytest
import allure
from pages.main_page import MainPage
from pages.order_page import OrderPage
from helpers.data import User1, User2


class TestOrderFlow:
    @allure.feature("Тесты процесса заказа через хедер")
    def test_order_flow_header(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        main_page.go_to_site()
        main_page.accept_cookies()
        main_page.click_order_button_header()

        order_page.fill_first_page(
            User1.NAME,
            User1.LAST_NAME,
            User1.ADDRESS,
            User1.METRO_STATION,
            User1.PHONE
        )

        order_page.fill_second_page(
            User1.DATE,
            User1.RENTAL_PERIOD,
            User1.COLOR,
            User1.COMMENT
        )

        order_page.confirm_order()

        success_message = order_page.get_success_message()
        assert "Заказ оформлен" in success_message

    @allure.feature("Тесты процесса заказа через футер")
    def test_order_flow_footer(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        main_page.go_to_site()
        main_page.accept_cookies()
        main_page.click_order_button_footer()

        order_page.fill_first_page(
            User2.NAME,
            User2.LAST_NAME,
            User2.ADDRESS,
            User2.METRO_STATION,
            User2.PHONE
        )

        order_page.fill_second_page(
            User2.DATE,
            User2.RENTAL_PERIOD,
            User2.COLOR,
            User2.COMMENT
        )

        order_page.confirm_order()

        success_message = order_page.get_success_message()
        assert "Заказ оформлен" in success_message
