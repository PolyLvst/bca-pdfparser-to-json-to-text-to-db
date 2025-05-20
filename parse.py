import glob
import uuid
import fitz
import re
import os
import shared_enum

class ParseFromPDF:
    def __init__(self, pdf_path):
        # area picker, hindari scan di luar area
        self.scan_area = fitz.Rect(14.510822510822607, 180.3841991341991, 588.6017316017318, 831.9318181818182)
        self.scan_area_periode_account_number = fitz.Rect(315.22510822510833, 77.86796536796533, 565.8203463203464, 162.15909090909088)
        # Amount pattern
        self.AMOUNT_PATTERN = shared_enum.Pattern.AMOUNT_PATTERN
        # Define regex to match MM/DD format
        self.DATE_PATTERN = shared_enum.Pattern.DATE_PATTERN
        self.pdf_path = pdf_path
        self.output_txt_path = './parsed.txt'
        self.text = ""
        self.text_with_middle_tokens = ""
        self.periode = ""
        self.account_number = ""
    
    def parse(self):
        if not os.path.exists(self.pdf_path): return self
        IS_AMOUNT_SEEN = False
        with fitz.open(self.pdf_path) as doc:
            for page in doc:
                IS_DATE_SEEN = False
                IS_MIDDLE_TO_LEFT_COLUMN_TOKEN_ADDED = False
                # 31/01 TRSF E-BANKING CR 31/01 /ABCDE/00000 ABCDE 10,000,000.00 
                # Edge case ketika payee memiliki HH/BB di dalam keterangan
                words = page.get_text("words")
                filtered_words = []
                filtered_words_with_middle_tokens = []
                for word in words:
                    # word index 0 - 3 : coordinate, word index 4 adalah content nya
                    coordinate = word[:4] # x, y, z
                    word_extracted = word[4]

                    if fitz.Rect(coordinate).intersects(self.scan_area_periode_account_number):
                        if re.match(shared_enum.Pattern.ACCOUNT_NUMBER_PATTERN, word_extracted): self.account_number = word_extracted
                        if re.match(shared_enum.Pattern.YEAR_PATTERN, word_extracted): self.periode = word_extracted
                        continue
                    if not fitz.Rect(coordinate).intersects(self.scan_area): continue
                    if re.match(self.AMOUNT_PATTERN, word_extracted):
                        IS_AMOUNT_SEEN = True
                        if coordinate[0] >= shared_enum.Pattern.MIDDLE_X_COORDINATE and not IS_MIDDLE_TO_LEFT_COLUMN_TOKEN_ADDED:
                            # print(coordinate, "added in line : ", word_extracted)
                            filtered_words_with_middle_tokens.append(shared_enum.Pattern.MIDDLE_COLUMN_TOKEN)
                            IS_MIDDLE_TO_LEFT_COLUMN_TOKEN_ADDED = True
                    if re.match(self.DATE_PATTERN, word_extracted):
                        date_string = word_extracted
                        # Edge case pada saat payee memberikan keterangan 31/01 atau HH/BB
                        date_transaction = f"{date_string.strip()}" if IS_AMOUNT_SEEN == False else f"\n{date_string.strip()}"
                        IS_AMOUNT_SEEN = False
                        IS_DATE_SEEN = True
                        IS_MIDDLE_TO_LEFT_COLUMN_TOKEN_ADDED = False
                        filtered_words.append(date_transaction)
                        filtered_words_with_middle_tokens.append(date_transaction)
                        continue
                    if IS_DATE_SEEN:
                        filtered_words.append(word_extracted.strip())
                        filtered_words_with_middle_tokens.append(word_extracted.strip())
                self.text += " ".join(filtered_words)
                self.text_with_middle_tokens += " ".join(filtered_words_with_middle_tokens)
        # Finished parsing
        return self

    def output_as_string(self):
        return self.text

    def output_as_list(self):
        return [row for row in self.text.split("\n")] if self.text else []
        
    def output_as_txt(self):
        with open(self.output_txt_path, 'w') as f:
            f.write(self.text)

    def output_as_string_with_middle_tokens(self):
        return self.text_with_middle_tokens

    def output_as_list_with_middle_tokens(self):
        return [row for row in self.text_with_middle_tokens.split("\n")] if self.text_with_middle_tokens else []

    def output_as_txt_with_middle_tokens(self):
        with open(self.output_txt_path, 'w') as f:
            f.write(self.text_with_middle_tokens)
    
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
        # parser.parse().output_as_txt_with_middle_tokens()
        print(f"Done ... [{file_name}]")
    # periode = parser.parse().get_periode()
    # print(periode)
    # account_number = parser.parse().get_account_number()
    # print(account_number)