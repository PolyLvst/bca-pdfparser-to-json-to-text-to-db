from tokenize_util import TokenizeUtil
from prepare_dict import PrepareDictBuilder
from db import DatabaseInserter
import glob
import os

class PipelineRun:
    def __init__(self, input_folder):
        self.input_folder = input_folder
        self.__check_folder()

    def run(self):
        pdf_files = glob.glob(f"{self.input_folder}/*.pdf")
        for file in pdf_files:
            print(f"->> Parsing file [{file}] ...")

            tokenizer = TokenizeUtil(file)
            database_insert = DatabaseInserter()
            dict_parsed = tokenizer.tokenize().output_as_dict()
            source = os.path.basename(file)
            account_number = tokenizer.get_parsed_pdf_obj().get_account_number()
            for key,value in dict_parsed.items():
                value = PrepareDictBuilder(value).set_acno(account_number).set_source(source).build()
                database_insert.append(value)

            print(f"->> Inserting to db total [{database_insert.get_insert_len()}] ...")
            database_insert.insert()
            print("->> Inserted to db ...")
    
    def __check_folder(self):
        if not os.path.exists(self.input_folder):
            os.mkdir(self.input_folder)

if __name__ == "__main__":
    runner = PipelineRun("./input")
    runner.run()