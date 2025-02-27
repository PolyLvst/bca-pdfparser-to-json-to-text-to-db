from tokenize_util import TokenizeUtil
from prepare_dict import PrepareDictBuilder
from db import DatabaseInserter
import glob
import os

class PipelineRun:
    def __init__(self, input_folder):
        self.database_insert = DatabaseInserter()
        self.input_folder = input_folder
        self.__check_folder()

    def run(self):
        pdf_files = glob.glob(f"{self.input_folder}/*.pdf")
        for file in pdf_files:
            print(f"->> Parsing file [{file}] ...")

            dict_parsed = TokenizeUtil(file).tokenize().output_as_dict()
            source = os.path.basename(file)
            # TODO get from parsed pdf
            account_number = "00000"
            for key,value in dict_parsed.items():
                value = PrepareDictBuilder(value).set_acno(account_number).set_source(source).build()
                self.database_insert.append(value)

            self.database_insert.insert()
            print("->> Inserted to db ...")
    
    def __check_folder(self):
        if not os.path.exists(self.input_folder):
            os.mkdir(self.input_folder)

if __name__ == "__main__":
    runner = PipelineRun("./input")
    runner.run()