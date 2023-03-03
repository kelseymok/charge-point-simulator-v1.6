from dateutil import parser
from typing import List

from transaction import Transaction
from transaction_config import TransactionConfig


class Transactions:
    def __init__(self):
        self.current_transaction = 0
        self.transactions_list: List[TransactionConfig] = []
        self.played_transactions = []
        self.played = False

    def inc(self):
        self.current_transaction = self.current_transaction + 1
        return self.current_transaction

    def add_transactions(self, transactions: List[TransactionConfig]):
        self.transactions_list = self.transactions_list + transactions

    def sort_transactions(self):
        return sorted(self.transactions_list, key=lambda x: parser.parse(x.start_time))

    def play_transactions(self):
        if self.played:
            print("Transactions already played. Nothing to do here! \o/")
        else:
            print("Playing transactions...")
            self.played_transactions = [Transaction(id=self.inc(), **transaction.__dict__).start() for transaction in self.sort_transactions()]
            self.played = True
        return self.played_transactions