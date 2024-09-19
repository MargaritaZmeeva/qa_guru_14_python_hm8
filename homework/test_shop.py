"""
Протестируйте классы из модуля homework/models.py
"""
import random

import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        quantity = product.quantity

        if quantity > 0:
            assert product.check_quantity(quantity - 1) is True
        assert product.check_quantity(quantity) is True
        assert product.check_quantity(quantity + 1) is False
        pass

    def test_product_buy(self, product):
        quantity = product.quantity

        count_of_buys = 0
        product.buy(count_of_buys)
        assert product.quantity == quantity - count_of_buys

        if quantity > 0:
            count_of_buys = quantity - 1
            product.buy(count_of_buys)
            assert product.quantity == quantity - count_of_buys

        pass

    def test_product_buy_more_than_available(self, product):
        quantity = product.quantity

        with pytest.raises(ValueError, match="Not enough products"):
            product.buy(quantity + 1)


class TestCart:

    def test_add_product(self, product: Product, cart):
        if product in cart.products:
            count = cart.products[product]
        else:
            count = 0

        cart.add_product(product)
        assert cart.products[product] == count + 1

    def test_remove_product(self, product: Product, cart):
        if product in cart.products:
            count = cart.products[product]
        else:
            count = 0
        cart.remove_product(product, 1)

        if count > 1:
            assert cart.products[product] == count - 1

    def test_clear_cart_empty(self, product: Product, cart):  # проверка очистки пустой корзины
        cart.products = {}

        cart.clear()

        if product in cart.products:
            raise ValueError("Cart should be empty")

    def test_clear_cart(self, product: Product, cart):  # проверка очистки корзины с товарами
        cart.add_product(product, 1000)

        cart.clear()

        if product in cart.products:
            raise ValueError("Cart should be empty")

    def test_get_total_price(self, product: Product, cart):  # проверка получения общей стоимости
        if product in cart.products:
            total = cart.get_total_price()
            assert total != 0
        else:
            total = cart.get_total_price()
            assert total == 0

    def test_get_correct_total_price(self, product: Product, cart):  # проверка получения корректной общей стоимости
        cart.clear()
        quantity = 1
        cart.add_product(product, quantity)
        total_amount = product.price * quantity
        assert cart.get_total_price() == total_amount

    def test_buy(self, product: Product, cart):
        quantity = product.quantity
        cart.add_product(product, quantity + 1)

        with pytest.raises(ValueError, match="Not enough products"):
            cart.buy()
