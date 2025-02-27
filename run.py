import tokenize_util
import glob
import os

# class PipelineRun:
#     def __init__(self):

# parsed_list = parse.ParseFromPDF("./sample.pdf").parse().output_as_list()
# print(parsed_list)
# with open("hasil-fitz.txt", "r") as file:
#     for line in file:

input_folder = "input"
if not os.path.exists(input_folder):
    os.mkdir(input_folder)
pdf_files = glob.glob(f"{input_folder}/*.pdf")
for file in pdf_files:
    dict_parsed = tokenize_util.TokenizeUtil(file, "0000000").tokenize().output_as_dict()
    # TODO insert to db
    print(f"{dict_parsed.popitem()}")