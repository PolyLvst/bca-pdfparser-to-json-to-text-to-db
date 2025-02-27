import glob
import uuid
import fitz
import re
import os
import shared_enum

class ParseFromPDF:
    def __init__(self, pdf_path):
        # area picker, hindari scan di luar area
        self.scan_area = fitz.Rect(30.457792207792295, 253.28463203463207, 570.3766233766235, 784.0909090909091)
        self.scan_area_periode = fitz.Rect(431.41017316017326, 105.20562770562776, 558.9859307359309, 123.43073593073598)
        self.scan_area_account_number = fitz.Rect(431.41017316017326, 73.31168831168827, 568.098484848485, 86.98051948051955)
        # Amount pattern
        self.AMOUNT_PATTERN = shared_enum.Pattern.AMOUNT_PATTERN
        # Define regex to match MM/DD format
        self.DATE_PATTERN = shared_enum.Pattern.DATE_PATTERN
        self.pdf_path = pdf_path
        self.output_txt_path = './parsed.txt'
        self.text = ""
        self.periode = ""
        self.account_number = ""
    
    def parse(self):
        IS_AMOUNT_SEEN = False
        if not os.path.exists(self.pdf_path): return self
        with fitz.open(self.pdf_path) as doc:
            for page in doc:
                # 31/01 TRSF E-BANKING CR 31/01 /ABCDE/00000 ABCDE 10,000,000.00 
                # Edge case ketika payee memiliki HH/BB di dalam keterangan
                words = page.get_text("words")
                filtered_words = []
                for word in words:
                    # word index 0 - 3 : coordinate, word index 4 adalah content nya
                    if fitz.Rect(word[:4]).intersects(self.scan_area_periode): 
                        # Bisa berupa JANUARI atau 2025, karena looping word terakhir 2025 maka akan terassign 2025
                        self.periode = word[4]
                        continue
                    if fitz.Rect(word[:4]).intersects(self.scan_area_account_number):
                        self.account_number = word[4]
                        continue
                    if not fitz.Rect(word[:4]).intersects(self.scan_area): continue
                    if re.match(self.AMOUNT_PATTERN, word[4]): IS_AMOUNT_SEEN = True
                    if re.match(self.DATE_PATTERN, word[4]):
                        # Edge case pada saat payee memberikan keterangan 31/01 atau HH/BB
                        date_transaction = f"{word[4].strip()}" if IS_AMOUNT_SEEN == False else f"\n{word[4].strip()}"
                        IS_AMOUNT_SEEN = False
                        filtered_words.append(date_transaction)
                    else:
                        filtered_words.append(word[4].strip())
                self.text += " ".join(filtered_words)
        # Finished parsing
        return self

    def output_as_string(self):
        return self.text

    def output_as_list(self):
        return [row for row in self.text.split("\n")] if self.text else []
        
    def output_as_txt(self):
        with open(self.output_txt_path, 'w') as f:
            f.write(self.text)
    
    def get_periode(self):
        return self.periode

    def get_account_number(self):
        return self.account_number

if __name__ == "__main__":
    pdf_files = glob.glob("./input/*.pdf")
    for file in pdf_files:
        parser = ParseFromPDF(file)
        file_name = os.path.basename(file)
        parser.output_txt_path = f"./{file_name}_{uuid.uuid4()}.txt"
        parser.parse().output_as_txt()
        print(f"Done ... [{file_name}]")
    # periode = parser.parse().get_periode()
    # print(periode)
    # account_number = parser.parse().get_account_number()
    # print(account_number)