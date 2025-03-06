import glob
import os
import re
import uuid
import json
import shared_enum
from parse import ParseFromPDF
from calculate_balance import CalculateBalanceHelper

class TokenizeUtil:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.parsed = ParseFromPDF(pdf_path=self.pdf_path).parse()
        self.parsed_list = self.parsed.output_as_list()
        self.tahun = self.parsed.get_periode()
        self.all_parsed = {}
        self.output_json_path = "./parsed.json"
        self.calculate_balance_helper = CalculateBalanceHelper()
        self.types = shared_enum.Transaction.TYPES
    
    def find_payee_amount_balance(self, line):
        payee = ""
        amount = None
        balance = None
        for word in line.split(" "):
            if re.match(shared_enum.Pattern.AMOUNT_PATTERN, word):
                # memastikan bahwa ketika balance sudah di assign, tidak akan merubahnya, begitu pula dengan amount
                # Edge case ketika halaman terakhir, saldo akhir di anggap balance, fix dengan memastikan bahwa balance sudah pernah di assign
                if amount != None and balance == None: balance = float(word.replace(",",""))
                if amount == None and balance == None: amount = float(word.replace(",",""))
                continue
            payee += f" {word}"
        payee = re.sub(shared_enum.Pattern.BERSAMBUNG, "", payee)
        payee = payee.strip()
        balance = self.calculate_balance_helper.calculate_balance(payee, amount)
        amount = self.get_minus_amount_if_spent(payee, amount)
        return payee, amount, balance
    
    def get_minus_amount_if_spent(self, payee, amount):
        for key,formula in self.types.items():
            if payee.startswith(key):
                # balance + amount get the symbol only
                symbol_string = formula[8:9]
                return float(f"{symbol_string}{amount}")
        return None

    def tokenize(self):
        for line in self.parsed_list:
            line = line.strip()

            tanggal_bulan = line[0:5] # 31/01
            tanggal = tanggal_bulan.split("/")[0] # 31
            bulan = tanggal_bulan.split("/")[1] # 01

            date_assemble = f"{self.tahun}-{bulan}-{tanggal}"

            payee, amount, balance = self.find_payee_amount_balance(line[6:].strip()) 
            
            template = {
                "date": date_assemble,
                "payee": payee,
                "amount": amount,
                "balance": balance,
            }

            __uuid = uuid.uuid4()
            self.all_parsed[f"{__uuid}"] = template
        return self
    
    def output_as_json(self):
        with open(self.output_json_path, "w") as f:
            json.dump(self.all_parsed, f)
    
    def output_as_dict(self):
        return self.all_parsed
    
    def get_parsed_pdf_obj(self):
        return self.parsed

if __name__ == "__main__":
    pdf_files = glob.glob("./input/*.pdf")
    for file in pdf_files:
        tokenizer = TokenizeUtil(file)
        file_name = os.path.basename(file)
        tokenizer.output_json_path = f"./{file_name}_{uuid.uuid4()}.json"
        tokenizer.tokenize().output_as_json()
        print(f"Done ... [{file_name}]")
    # tokenizer = TokenizeUtil("./sample.pdf").tokenize().output_as_json()