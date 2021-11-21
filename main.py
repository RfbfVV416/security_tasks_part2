
alph = 'a b c d e f g h i j k l m n o p q r s t u v w x y z . /'.split()
code = '1 2 3 4 5 6 7 81 82 83 84 85 86 87 88 89 80 91 92 93 94 95 96 97 98 99 90 01 02 03 04 05 06 07'.split()


def mark_encrypt():
    text = input("Enter message: ").upper()
    new_text = ''
    for character in text:

        if character.isdigit() or character.isspace():
            new_text += character
        elif character.isalpha() or character == '.' or character == '/':
            if character == 'ё':
                character = 'е'
            i = alph.index(character.lower())
            new_text += code[i]
    print("Encrypted Text: {}".format(new_text))


def mark_decrypt():
    text = input("Enter message: ").upper()
    new_text = ''
    sym = ''
    for character in text:
        if character.isspace():
            new_text += ' '
        else:
            if character in code and len(sym) == 0:
                new_text += alph[code.index(character)]
            else:
                sym += character
                if sym in code:
                    new_text += alph[code.index(sym)]
                    sym = ''
    print("Decrypted Text: {}".format(new_text))


def main():
    choice = int(input("1. Encryption\n2.Decryption\nChoose(1,2): "))
    if choice == 1:
        print("---Encryption---")
        mark_encrypt()
    elif choice == 2:
        print("---Decryption---")
        mark_decrypt()
    else:
        print("Wrong Choice")


if __name__ == "__main__":
    main()