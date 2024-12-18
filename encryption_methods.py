def sezar_encryption(word, key_number):
    encrypted_word = ""
    for i in word:
        ascii_place = ord(i)
        encrypted_character = chr(ascii_place + key_number)
        encrypted_word += encrypted_character
    return encrypted_word


def sezar_decryption(word, key_number):
    decrypted_word = ""
    for i in word:
        ascii_place = ord(i)
        decrypted_character = chr(ascii_place - key_number)
        decrypted_word += decrypted_character
    return decrypted_word


def xor_key_type(key):
    if str(key).isalpha():
        number = ord(key)
    else:
        number = int(key) % 256
    return number


def decimal_to_binary(number):
    bin = ''
    while number != 0:
        bin = str(number % 2) + bin
        number = number // 2
    while len(bin) != 8:
        bin = '0' + bin
    return bin


def binary_to_decimal(number):
    decimal = 0
    power = 7
    for i in number:
        decimal = decimal + int(i)* 2 ** power
        power -= 1
    return decimal


def xor_encryption(word, key):
    encrypted_word = ""
    key_number_binary = decimal_to_binary(xor_key_type(key))
    for i in word:
        ascii_place = ord(i)
        binary_symbol = decimal_to_binary(ascii_place)
        xor_binary = ''
        for k in range(8):
            if (key_number_binary[k] == '1' and binary_symbol[k] == '0') or (
                    key_number_binary[k] == '0' and binary_symbol[k] == '1'):
                xor_binary = xor_binary + '1'
            else:
                xor_binary = xor_binary + '0'
        xor_element = chr(binary_to_decimal(xor_binary))
        encrypted_word = encrypted_word + xor_element
    return encrypted_word


def xor_decryption(word, key):
    decrypted_word = ""
    key_number_binary = decimal_to_binary(xor_key_type(key))
    for i in word:
        ascii_place = ord(i)
        binary_symbol = decimal_to_binary(ascii_place)
        xor_binary = ''
        for k in range(8):
            if (key_number_binary[k] == '1' and binary_symbol[k] == '0') or (
                    key_number_binary[k] == '0' and binary_symbol[k] == '1'):
                xor_binary = xor_binary + '1'
            else:
                xor_binary = xor_binary + '0'
        xor_element = chr(binary_to_decimal(xor_binary))
        decrypted_word = decrypted_word + xor_element
    return decrypted_word

def generate_random_key_text():
    random_key_text = random.randint(1, 1000)
    key_entry_text.delete(0, tk.END)
    key_entry_text.insert(0, str(random_key_text))


def generate_random_key_file():
    global key_entry_file
    random_key_file = random.randint(1, 1000)
    key_entry_file.delete(0, tk.END)
    key_entry_file.insert(0, str(random_key_file))
