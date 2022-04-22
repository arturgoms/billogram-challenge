from faker import Faker

from commons.tests.faker import providers

faker = Faker(includes=["commons.tests.faker.providers.file"])
