import json
import os.path
import random
import re
from pydoc import plaintext

HOW_MANY_BOOK =3
LINE = 128
PAGE = 64
line_window = {}
char_window = []
line_number = 0
pages = {}
page_number = 0

def clean_line(line):
    return line.strip().replace( '-', '' ) + ' '

def process_char(char):
    global char_window
    char_window.append(char)
    if len(char_window) == LINE:
       add_line()

def add_line():
    global char_window, line_number
    line_number  += 1
    process_page(''.join(char_window), line_number )
    char_window.clear()


def process_page(line, line_num):
    global line_window, pages, page_number
    line_window[line_num]= line
    if len(line_window) == PAGE:
       add_page()

def add_page():
    global line_window, pages, page_number, line_number
    page_number += 1
    pages[page_number] = dict(line_window)
    line_window.clear()
    line_number = 0

def read_book(file_path):
    global char_window
    with open(file_path, 'r' , encoding='utf-8-sig') as fp:
        for line in fp:
            line = clean_line(line)
            if line.strip():
                for c in line :
                    process_char(c)
    if len(char_window) > 0:
        add_line()
    if len(line_window) > 0:
        add_page()

def generate_code_book():
    global pages
    code_book ={}
    for page, lines in pages.items():
        for num, line in lines.items():
            for pos, char in enumerate(line):
                code_book.setdefault(char, []).append(f'{page}-{num}-{pos}')
    return code_book

def proccess_book(*paths):
    for path in paths:
        read_book( path )

def load(file_path, *key_books, reverse=False):
    if os.path.exists(file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)
    else:
        proccess_book(*key_books)
        if reverse:
            save(file_path, pages)
            return pages
        else:
            code_book = generate_code_book()
            save(file_path, code_book)
            return code_book



def save(file_path, book):
    with open(file_path, 'w') as fp:
        json.dump(book, fp)

def encrypt(code_book, message):
    cipher_text =[]
    for char in message:
        index = random.randint( 0, len(code_book[char]) - 1)
        cipher_text.append(code_book[char].pop(index))
    return '-'.join(cipher_text)

def decrypt(rev_code_book, ciphertext):
    plaintext = []
    for cc in re.findall(r'\d+-\d+-\d+' , ciphertext):
        page, line, pos = cc.split('-')
        plaintext.append(
        rev_code_book[page][line][int(pos)]
        )
    return ''.join(plaintext)

def main_menu():
    print("""1).encrypt
2). decrypt
 3). quit""")
    return int(input("make a selection [1,2,3]: "))

def main():
    key_books=( 'books/DR. jekyll.txt', "books/war and peace.txt", 'books/william_shakespeare.txt')
    code_book_path = 'code_books/real_deal.json'
    rev_code_book_path = 'code_books/rev_real_deal.json'

    code_book =load(code_book_path, *key_books)
    rev_code_book = load(rev_code_book_path, *key_books, reverse=True)
    print(encrypt(code_book, "get rich or die trying. "))
    ciphertext = "883-24-42-825-23-44-715-5-18-730-20-8-324-2-32-912-60-55-892-57-56-206-11-20-616-43-55-333-31-49-708-16-72-70-48-63-892-12-68-680-49-67-727-50-87-357-44-8-316-9-33-964-54-121-695-44-77-307-9-75-980-64-75-715-12-44-928-12-46-332-22-123"
    print(decrypt(rev_code_book, ciphertext))

    while True:
        try:
            choice= main_menu()
            match choice:
                case 1:
                    message = input("please input message: ")
                    print(encrypt(code_book, message))
                    continue
                case 2:
                    message = input("please enter ciphertext: ")
                    print(decrypt(rev_code_book, message))
                    continue
                case 3:
                    break
        except valueError:
            print("improper input")

if __name__ == '__main__':
    main()