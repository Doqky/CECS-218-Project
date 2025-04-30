import re

def extract_text_from_txt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

