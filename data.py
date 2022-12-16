from faker import Faker
from brands import brands
from string import ascii_uppercase

fake = Faker()
Faker.seed(2022)


def get_brand():
    return fake.random_element(elements=tuple(brands))


def get_model():
    name = fake.first_name_female()
    return fake.bothify(text=f'{name} ??-##', letters=ascii_uppercase)


def get_year():
    return fake.random_int(min=1970, max=2022)


def get_price():
    return fake.random_int(min=2000000, max=50000000) / 100
