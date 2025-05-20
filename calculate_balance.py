import shared_enum

class CalculateBalanceHelper:
    def __init__(self):
        self.saldo_awal = 0
        self.balance = 0
        self.types = shared_enum.Transaction.TYPES

    def calculate_balance(self, payee:str, amount:float):
        if payee.startswith(shared_enum.Pattern.SALDO_AWAL): self.set_saldo_awal(amount)
        # Used by eval formula, dont remove
        balance = self.balance
        for key,formula in self.types.items():
            if payee.startswith(key):
                self.balance = eval(formula)
        # Balance or Unknown types
        return self.balance if self.balance else None
    
    def set_saldo_awal(self, saldo_awal):
        self.saldo_awal = saldo_awal
        self.balance = saldo_awal

    def get_saldo_awal(self):
        return self.saldo_awal

    def get_balance(self):
        return self.balance