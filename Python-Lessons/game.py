import random

class Case:
    def __init__(self, case_name, case_price, item_count):
        self.case_name = case_name
        self.case_price = case_price
        self.item_count = item_count

    def open_case(self):
        return random.randint(1, self.item_count)

    def __str__(self):
        return f"Case info: name - {self.case_name}, price - {self.case_price}"

                                        