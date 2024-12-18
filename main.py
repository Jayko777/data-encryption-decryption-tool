import tkinter as tk
from tkinter import messagebox, ttk, filedialog, PhotoImage
from PIL import Image, ImageTk


import random


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
    random_key_text = random.randint(1, 10000)
    key_entry_text.delete(0, tk.END)
    key_entry_text.insert(0, str(random_key_text))


def generate_random_key_file():
    global key_entry_file
    random_key_file = random.randint(1, 10000)
    key_entry_file.delete(0, tk.END)
    key_entry_file.insert(0, str(random_key_file))


def process_text(action, input_field, key_entry_text, encryption_method, output_field, history_text):
    input_text = input_field.get("1.0", tk.END).rstrip('\n')
    key = xor_key_type(key_entry_text.get())
    method = encryption_method.get()

    if not input_text:
        messagebox.showerror("Error", "Input text cannot be empty.")
        return

    try:
        if method == "Caesar":
            if action == "Encrypt":
                result = sezar_encryption(input_text, key)
            else:
                result = sezar_decryption(input_text, key)
        elif method == "XOR":
            if action == "Encrypt":
                result = xor_encryption(input_text, key)
            else:
                result = xor_decryption(input_text, key)

        output_field.delete("1.0", tk.END)
        output_field.insert(tk.END, result)


        history_text.insert(tk.END, f"{result}\n")
        history_text.yview(tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def text_menu(current_language):
    def go_to_main_menu():
        root.destroy()
        main_menu()

    def exit_application():
        root.destroy()

    global key_entry_text, text_label, encryption_method_label, key_label, random_button, output_label, encrypt_button, decrypt_button
    root = tk.Tk()
    root.title(translations_text_file[current_language]["title"])
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    bg_image = Image.open("background.jpg").resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)


    text_label = tk.Label(root, text=translations_text_file[current_language]["text_label"],
                          font=("Arial", 26, "bold"), bg="#edb590")
    text_label.place(x=875, y=180)

    input_field = tk.Text(root, height=5, width=50, font=("Arial", 18), bg="#edb288",  bd=2, relief="solid")
    input_field.place(x=660, y=250)

    encryption_method_label = tk.Label(root, text=translations_text_file[current_language]["encryption_method_label"],
                                       font=("Arial", 20, "bold"), bg="#ecb187")
    encryption_method_label.place(x=790, y=405)

    encryption_method = ttk.Combobox(root, values=["Caesar", "XOR"], state="readonly", font=("Arial", 28))
    encryption_method.set("Caesar")
    encryption_method.place(x=750, y=460)

    key_label = tk.Label(root, text=translations_text_file[current_language]["key_label"],
                         font=("Arial", 18, "bold"), bg="#ecb187")
    key_label.place(x=850, y=530)

    key_entry_text = tk.Entry(root, font=("Arial", 36), bd=2,bg="#ecb48f", relief="solid")
    key_entry_text.place(x=705, y=575)

    random_button = tk.Button(root, text=translations_text_file[current_language]["random_button_text"],
                              font=("Arial", 20), command=lambda: generate_random_key_text(),
                              relief="solid", bg="#4CAF50", fg="white", activebackground="#45a049")
    random_button.place(x=401, y=577)

    output_label = tk.Label(root, text=translations_text_file[current_language]["output_label"],
                            font=("Arial", 18, "bold"), bg="#eab895")
    output_label.place(x=920, y=650)

    output_field = tk.Text(root, height=5, width=50, font=("Arial", 18), bd=2,bg="#eab897", relief="solid")
    output_field.place(x = 650, y=700)

    history_label = tk.Label(root, text=translations_text_file[current_language]["history_label"],
                             font=("Arial", 20, "bold"), bg="#dfbbad")
    history_label.place(x=1625, y=400)

    history_text = tk.Text(root, height=15, width=50, font=("Arial", 13), bd=2,bg="#dcc1ba", relief="solid")
    history_text.place(x=1450, y=450)

    # Buttons for Encrypt and Decrypt
    encrypt_button = tk.Button(root, text=translations_text_file[current_language]["encrypt_button"],
                               font=("Arial", 32), relief="solid", bg="#2196F3", fg="white",
                               activebackground="#1976D2",
                               command=lambda: process_text("Encrypt", input_field, key_entry_text, encryption_method,
                                                            output_field, history_text))
    encrypt_button.place(x=750, y=860)

    decrypt_button = tk.Button(root, text=translations_text_file[current_language]["decrypt_button"],
                               font=("Arial", 32), relief="solid", bg="#FF2343", fg="white",
                               activebackground="#E64A19",
                               command=lambda: process_text("Decrypt", input_field, key_entry_text, encryption_method,
                                                            output_field, history_text))
    decrypt_button.place(x=990, y=860 )


    try:
        back_icon = tk.PhotoImage(file="back_icon.png")
        back_button = tk.Button(root, image=back_icon, command=go_to_main_menu, borderwidth=1)
        back_button.image = back_icon
        back_button.place(x=10, y=10)
    except Exception as e:
        print(f"Error loading back icon: {e}")

    try:
        exit_icon = tk.PhotoImage(file="exit_icon.png")
        exit_button = tk.Button(root, image=exit_icon, command=exit_application, borderwidth=0)
        exit_button.image = exit_icon
        exit_button.place(x=screen_width - 60, y=10)
    except Exception as e:
        print(f"Error loading exit icon: {e}")

    root.mainloop()


def change_language(event):
    selected_language = event.widget.get()
    update_language(selected_language)


def update_language(language_code):
    global current_language
    current_language = language_code

    text_label.config(text=translations_text_file[current_language]["text_label"])
    encryption_method_label.config(text=translations_text_file[current_language]["encryption_method_label"])
    key_label.config(text=translations_text_file[current_language]["key_label"])
    encrypt_button.config(text=translations_text_file[current_language]["encrypt_button"])
    decrypt_button.config(text=translations_text_file[current_language]["decrypt_button"])
    random_button.config(text=translations_text_file[current_language]["random_button_text"])
    output_label.config(text=translations_text_file[current_language]["output_label"])


translations_main_menu = {
    "en": {
        "title": "English",
        "choose_option": "Choose your option:",
        "text_option": "Text",
        "file_option": "File",
        "language_option": "Change Language",
        "choose_language": "Choose a language:"
    },
    "az": {
        "title": "Azerbaijani",
        "choose_option": "Seçiminizi edin:",
        "text_option": "Mətn",
        "file_option": "Fayl",
        "language_option": "Dili Dəyişdirin",
        "choose_language": "Bir dil seçin:"
    },
    "ru": {
        "title": "Russian",
        "choose_option": "Выберите опцию:",
        "text_option": "Текст",
        "file_option": "Файл",
        "language_option": "Изменить язык",
        "choose_language": "Выберите язык:"
    },
    "it": {
        "title": "Italian",
        "choose_option": "Scegli un'opzione:",
        "text_option": "Testo",
        "file_option": "File",
        "language_option": "Cambia Lingua",
        "choose_language": "Scegli una lingua:"
    },
    "tr": {
        "title": "Turkish",
        "choose_option": "Bir seçenek seçin:",
        "text_option": "Metin",
        "file_option": "Dosya",
        "language_option": "Dili Değiştir",
        "choose_language": "Bir dil seçin:"
    },
    "ar": {
        "title": "Arabian",
        "choose_option": "اختر خيارًا:",
        "text_option": "نص",
        "file_option": "ملف",
        "language_option": "تغيير اللغة",
        "choose_language": "اختر لغة:"
    },
    "zh": {
        "title": "Chinese",
        "choose_option": "请选择一个选项:",
        "text_option": "文本",
        "file_option": "文件",
        "language_option": "更改语言",
        "choose_language": "选择一种语言:"
    },
    "no": {
        "title": "Norwegian",
        "choose_option": "Velg et alternativ:",
        "text_option": "Tekst",
        "file_option": "Fil",
        "language_option": "Endre Språk",
        "choose_language": "Velg et språk:"
    },
    "ge": {
        "title": "Georgian",
        "choose_option": "აირჩიეთ პარამეტრი:",
        "text_option": "ტექსტი",
        "file_option": "ფაილი",
        "language_option": "შეცვალეთ ენა",
        "choose_language": "აირჩიეთ ენა:"
    },
    "so": {
        "title": "Somalian",
        "choose_option": "Dooro xulashadaada:",
        "text_option": "Qoraal",
        "file_option": "Fayl",
        "language_option": "Bedel Luuqadda",
        "choose_language": "Dooro luuqad:"
    }
}
translations_text_file = {
    "en": {
        "title": "Encryption/Decryption Tool",
        "text_label": "Enter Text:",
        "encryption_method_label": "Select Encryption Method:",
        "key_label": "Enter Key (Number):",
        "random_button_text": "Generate Random Key",
        "output_label": "Output:",
        "encrypt_button": "Encrypt",
        "decrypt_button": "Decrypt",
        "history_label": "History:"
    },
    "az": {
        "title": "Şifrələmə/Şifre Açma Aləti",
        "text_label": "Mətn daxil edin:",
        "encryption_method_label": "Şifrələmə Metodunu Seçin:",
        "key_label": "Açar Daxil Edin (Rəqəm):",
        "random_button_text": "Təsadüfi Açar Yarat",
        "output_label": "Çıxış:",
        "encrypt_button": "Şifrələmək",
        "decrypt_button": "Şifrəni Aç",
        "history_label": "Tarix:"
    },
    "ru": {
        "title": "Инструмент для шифрования/дешифрования",
        "text_label": "Введите текст:",
        "encryption_method_label": "Выберите метод шифрования:",
        "key_label": "Введите ключ (число):",
        "random_button_text": "Сгенерировать случайный ключ",
        "output_label": "Вывод:",
        "encrypt_button": "Зашифровать",
        "decrypt_button": "Расшифровать",
        "history_label": "История:"
    },
    "it": {
        "title": "Strumento di crittografia/decrittografia",
        "text_label": "Inserisci il testo:",
        "encryption_method_label": "Seleziona il metodo di crittografia:",
        "key_label": "Inserisci la chiave (numero):",
        "random_button_text": "Genera chiave casuale",
        "output_label": "Risultato:",
        "encrypt_button": "Crittografa",
        "decrypt_button": "Decrittografa",
        "history_label": "Storia:"
    },
    "tr": {
        "title": "Şifreleme/Şifre Çözme Aracı",
        "text_label": "Metni Girin:",
        "encryption_method_label": "Şifreleme Yöntemini Seçin:",
        "key_label": "Anahtar Girin (Sayı):",
        "random_button_text": "Rastgele Anahtar Oluştur",
        "output_label": "Çıktı:",
        "encrypt_button": "Şifrele",
        "decrypt_button": "Şifreyi Çöz",
        "history_label": "Geçmiş:"
    },
    "ar": {
        "title": "أداة التشفير / فك التشفير",
        "text_label": "أدخل النص:",
        "encryption_method_label": "اختر طريقة التشفير:",
        "key_label": "أدخل المفتاح (رقم):",
        "random_button_text": "إنشاء مفتاح عشوائي",
        "output_label": "الناتج:",
        "encrypt_button": "تشفير",
        "decrypt_button": "فك التشفير",
        "history_label": "التاريخ:"
    },
    "zh": {
        "title": "加密/解密工具",
        "text_label": "输入文本：",
        "encryption_method_label": "选择加密方法：",
        "key_label": "输入密钥（数字）：",
        "random_button_text": "生成随机密钥",
        "output_label": "输出：",
        "encrypt_button": "加密",
        "decrypt_button": "解密",
        "history_label": "历史:"
    },
    "no": {
        "title": "Kryptering / Dekryptering Verktøy",
        "text_label": "Skriv inn tekst:",
        "encryption_method_label": "Velg krypteringsmetode:",
        "key_label": "Skriv inn nøkkel (nummer):",
        "random_button_text": "Generer tilfeldig nøkkel",
        "output_label": "Resultat:",
        "encrypt_button": "Krypter",
        "decrypt_button": "Dekrypter",
        "history_label": "Historie:"
    },
    "ge": {
        "title": "შიფრირების/შიფრის გარჩევის ინსტრუმენტი",
        "text_label": "მომართეთ ტექსტი:",
        "encryption_method_label": "აირჩიეთ შიფრირების მეთოდი:",
        "key_label": "შეიყვანეთ გასაღები (ნუმერი):",
        "random_button_text": "გადააგზავნოთ შემთხვევითი გასაღები",
        "output_label": "გამოყენება:",
        "encrypt_button": "შიფრირება",
        "decrypt_button": "გარჩევა",
        "history_label": "ისტორია:"
    },
    "so": {
        "title": "Qalabka Sirta/ Furfurnaanta",
        "text_label": "Geli qoraalka:",
        "encryption_method_label": "Xulo habka sirta:",
        "key_label": "Geli furaha (lambarka):",
        "random_button_text": "Abuur furaha Random",
        "output_label": "Natiijada:",
        "encrypt_button": "Sir",
        "decrypt_button": "Furfurnaan",
        "history_label": "Taariikh:"
    },
}
translations_file_menu = {
    "en": {
        "title": "Encryption/Decryption Tool",
        "text_label": "Enter Text:",
        "encryption_method_label": "Select Encryption Method:",
        "key_label": "Enter Key (Number):",
        "random_button_text": "Generate Random Key",
        "output_label": "Output:",
        "encrypt_button": "Encrypt",
        "decrypt_button": "Decrypt",
        "file_encryption_decryption_tool_title": "File Encryption/Decryption Tool",
        "select_file_label": "Select File:",
        "browse_button_text": "Browse",
        "select_encryption_method_label": "Select Encryption Method:",
        "enter_key_label": "Enter Key (Number):",
        "generate_random_key": "Generate Random Key",
        "save_file_title": "Save File",
        "file_processed_success": "File processed and saved successfully!",
        "error": "Error",
        "unknown_method_error": "Unknown method.",
        "key_is_digit_error": "Key must be a number.",
        "no_file_selected": "No file selected.",
        "your_key": "Your key is: ",
        "browse_file_title": "Select File",
        "an_error_occurred": "An error occurred",
    },
    "az": {
        "title": "Şifreleme/Şifrə Açma Aləti",
        "text_label": "Mətn daxil edin:",
        "encryption_method_label": "Şifrələmə Metodunu Seçin:",
        "key_label": "Açar Daxil Edin (Rəqəm):",
        "random_button_text": "Təsadüfi Açar Yarat",
        "output_label": "Çıxış:",
        "encrypt_button": "Şifrələmək",
        "decrypt_button": "Şifrəni Aç",
        "file_encryption_decryption_tool_title": "Fayl Şifrələmə/Şifrə Açma Aləti",
        "select_file_label": "Fayl Seçin:",
        "browse_button_text": "Gözət",
        "select_encryption_method_label": "Şifrələmə Metodunu Seçin:",
        "enter_key_label": "Açar Daxil Edin (Rəqəm):",
        "generate_random_key": "Təsadüfi Açar Yarat",
        "save_file_title": "Faylı Saxla",
        "file_processed_success": "Fayl uğurla işlənib saxlanıldı!",
        "error": "Xəta",
        "unknown_method_error": "Bilinməyən metod.",
        "key_is_digit_error": "Açar bir rəqəm olmalıdır.",
        "no_file_selected": "Heç bir fayl seçilməyib.",
        "your_key": "Açarınız: ",
        "browse_file_title": "Fayl Seç",
        "an_error_occurred": "Bir xəta baş verdi"
    },
    "ru": {
        "title": "Инструмент для шифрования/расшифровки",
        "text_label": "Введите текст:",
        "encryption_method_label": "Выберите метод шифрования:",
        "key_label": "Введите ключ (число):",
        "random_button_text": "Сгенерировать случайный ключ",
        "output_label": "Вывод:",
        "encrypt_button": "Зашифровать",
        "decrypt_button": "Расшифровать",
        "file_encryption_decryption_tool_title": "Инструмент для шифрования/расшифровки файлов",
        "select_file_label": "Выберите файл:",
        "browse_button_text": "Обзор",
        "select_encryption_method_label": "Выберите метод шифрования:",
        "enter_key_label": "Введите ключ (число):",
        "generate_random_key": "Сгенерировать случайный ключ",
        "save_file_title": "Сохранить файл",
        "file_processed_success": "Файл обработан и сохранен успешно!",
        "error": "Ошибка",
        "unknown_method_error": "Неизвестный метод.",
        "key_is_digit_error": "Ключ должен быть числом.",
        "no_file_selected": "Файл не выбран.",
        "your_key": "Ваш ключ: ",
        "browse_file_title": "Выберите файл",
        "an_error_occurred": "Произошла ошибка",
    },
    "it": {
        "title": "Strumento di crittografia/decrittografia",
        "text_label": "Inserisci testo:",
        "encryption_method_label": "Seleziona metodo di crittografia:",
        "key_label": "Inserisci chiave (numero):",
        "random_button_text": "Genera chiave casuale",
        "output_label": "Output:",
        "encrypt_button": "Crittografa",
        "decrypt_button": "Decrittografa",
        "file_encryption_decryption_tool_title": "Strumento di crittografia/decrittografia file",
        "select_file_label": "Seleziona file:",
        "browse_button_text": "Sfoglia",
        "select_encryption_method_label": "Seleziona metodo di crittografia:",
        "enter_key_label": "Inserisci chiave (numero):",
        "generate_random_key": "Genera chiave casuale",
        "save_file_title": "Salva file",
        "file_processed_success": "File elaborato e salvato con successo!",
        "error": "Errore",
        "unknown_method_error": "Metodo sconosciuto.",
        "key_is_digit_error": "La chiave deve essere un numero.",
        "no_file_selected": "Nessun file selezionato.",
        "your_key": "La tua chiave è: ",
        "browse_file_title": "Seleziona file",
        "an_error_occurred": "Si è verificato un errore",
    },
    "tr": {
        "title": "Şifreleme/Şifre Çözme Aracı",
        "text_label": "Metin Girin:",
        "encryption_method_label": "Şifreleme Yöntemi Seçin:",
        "key_label": "Anahtar Girin (Sayı):",
        "random_button_text": "Rastgele Anahtar Oluştur",
        "output_label": "Çıktı:",
        "encrypt_button": "Şifrele",
        "decrypt_button": "Şifre Çöz",
        "file_encryption_decryption_tool_title": "Dosya Şifreleme/Şifre Çözme Aracı",
        "select_file_label": "Dosya Seçin:",
        "browse_button_text": "Gözat",
        "select_encryption_method_label": "Şifreleme Yöntemi Seçin:",
        "enter_key_label": "Anahtar Girin (Sayı):",
        "generate_random_key": "Rastgele Anahtar Oluştur",
        "save_file_title": "Dosyayı Kaydet",
        "file_processed_success": "Dosya başarıyla işlenip kaydedildi!",
        "error": "Hata",
        "unknown_method_error": "Bilinmeyen yöntem.",
        "key_is_digit_error": "Anahtar bir sayı olmalı.",
        "no_file_selected": "Hiçbir dosya seçilmedi.",
        "your_key": "Anahtarınız: ",
        "browse_file_title": "Dosya Seç",
        "an_error_occurred": "Bir hata oluştu",
    },
    "ar": {
        "title": "أداة التشفير / فك التشفير",
        "text_label": "أدخل النص:",
        "encryption_method_label": "اختر طريقة التشفير:",
        "key_label": "أدخل المفتاح (رقم):",
        "random_button_text": "توليد مفتاح عشوائي",
        "output_label": "الإخراج:",
        "encrypt_button": "تشفير",
        "decrypt_button": "فك التشفير",
        "file_encryption_decryption_tool_title": "أداة تشفير / فك تشفير الملفات",
        "select_file_label": "اختر ملف:",
        "browse_button_text": "تصفح",
        "select_encryption_method_label": "اختر طريقة التشفير:",
        "enter_key_label": "أدخل المفتاح (رقم):",
        "generate_random_key": "توليد مفتاح عشوائي",
        "save_file_title": "حفظ الملف",
        "file_processed_success": "تم معالجة الملف وحفظه بنجاح!",
        "error": "خطأ",
        "unknown_method_error": "طريقة غير معروفة.",
        "key_is_digit_error": "يجب أن يكون المفتاح رقمًا.",
        "no_file_selected": "لم يتم اختيار ملف.",
        "your_key": "مفتاحك هو: ",
        "browse_file_title": "اختر ملف",
        "an_error_occurred": "حدث خطأ",
    },
    "zh": {
        "title": "加密/解密工具",
        "text_label": "请输入文本：",
        "encryption_method_label": "选择加密方法：",
        "key_label": "输入密钥（数字）：",
        "random_button_text": "生成随机密钥",
        "output_label": "输出：",
        "encrypt_button": "加密",
        "decrypt_button": "解密",
        "file_encryption_decryption_tool_title": "文件加密/解密工具",
        "select_file_label": "选择文件：",
        "browse_button_text": "浏览",
        "select_encryption_method_label": "选择加密方法：",
        "enter_key_label": "输入密钥（数字）：",
        "generate_random_key": "生成随机密钥",
        "save_file_title": "保存文件",
        "file_processed_success": "文件处理并成功保存！",
        "error": "错误",
        "unknown_method_error": "未知方法。",
        "key_is_digit_error": "密钥必须是数字。",
        "no_file_selected": "没有选择文件。",
        "your_key": "您的密钥是：",
        "browse_file_title": "选择文件",
        "an_error_occurred": "发生错误",
    },
    "no": {
        "title": "Kryptering/Dekryptering Verktøy",
        "text_label": "Skriv inn tekst:",
        "encryption_method_label": "Velg krypteringsmetode:",
        "key_label": "Skriv inn nøkkel (nummer):",
        "random_button_text": "Generer tilfeldig nøkkel",
        "output_label": "Utdata:",
        "encrypt_button": "Krypter",
        "decrypt_button": "Dekrypter",
        "file_encryption_decryption_tool_title": "Fil kryptering/dekryptering verktøy",
        "select_file_label": "Velg fil:",
        "browse_button_text": "Bla gjennom",
        "select_encryption_method_label": "Velg krypteringsmetode:",
        "enter_key_label": "Skriv inn nøkkel (nummer):",
        "generate_random_key": "Generer tilfeldig nøkkel",
        "save_file_title": "Lagre fil",
        "file_processed_success": "Fil behandlet og lagret!",
        "error": "Feil",
        "unknown_method_error": "Ukjent metode.",
        "key_is_digit_error": "Nøkkelen må være et nummer.",
        "no_file_selected": "Ingen fil valgt.",
        "your_key": "Din nøkkel er: ",
        "browse_file_title": "Velg fil",
        "an_error_occurred": "En feil oppstod",
    },
    "ge": {
        "title": "შეფერის/გაშიფვრის ხელსაწყო",
        "text_label": "შეიყვანეთ ტექსტი:",
        "encryption_method_label": "აირჩიეთ შიფრაციის მეთოდი:",
        "key_label": "შეიყვანეთ გასაღები (რაოდენობა):",
        "random_button_text": "შექმენით შემთხვევითი გასაღები",
        "output_label": "გამოსავალი:",
        "encrypt_button": "შეფერე",
        "decrypt_button": "გაშიფრე",
        "file_encryption_decryption_tool_title": "ფაილების შიფრაციის/გაშიფვრის ხელსაწყო",
        "select_file_label": "აირჩიეთ ფაილი:",
        "browse_button_text": "მოძიება",
        "select_encryption_method_label": "აირჩიეთ შიფრაციის მეთოდი:",
        "enter_key_label": "შეიყვანეთ გასაღები (რაოდენობა):",
        "generate_random_key": "შექმენით შემთხვევითი გასაღები",
        "save_file_title": "შენახვა",
        "file_processed_success": "ფაილი წარმატებით დამუშავდა და შეინახა!",
        "error": "შეცდომა",
        "unknown_method_error": "უცნობი მეთოდი.",
        "key_is_digit_error": "გასაღები უნდა იყოს რიცხვი.",
        "no_file_selected": "ფაილი არ არის არჩეული.",
        "your_key": "თქვენი გასაღებია: ",
        "browse_file_title": "აირჩიეთ ფაილი",
        "an_error_occurred": "შეცდომა მოხდა",
    },
    "so": {
        "title": "Qalabka Qarsoodiga/Ka-dejinta Qarsoodiga",
        "text_label": "Geli qoraalka:",
        "encryption_method_label": "Xulo Habka Qarsoodiga:",
        "key_label": "Geli Furaha (Nambarka):",
        "random_button_text": "Abuur Furaha Aan Caadi Ahayn",
        "output_label": "Natiijada:",
        "encrypt_button": "Qarsoodi",
        "decrypt_button": "Ka-deji",
        "file_encryption_decryption_tool_title": "Qalabka Qarsoodiga/Ka-dejinta Qarsoodiga ee Faalada",
        "select_file_label": "Xulo Faalad:",
        "browse_button_text": "Raadi",
        "select_encryption_method_label": "Xulo Habka Qarsoodiga:",
        "enter_key_label": "Geli Furaha (Nambarka):",
        "generate_random_key": "Abuur Furaha Aan Caadi Ahayn",
        "save_file_title": "Keydi Faalada",
        "file_processed_success": "Faalada waa la farsameeyey oo si guul leh loo kaydiyey!",
        "error": "Khalad",
        "unknown_method_error": "Hab aan la aqoon.",
        "key_is_digit_error": "Furaha waa inuu noqdaa nambor.",
        "no_file_selected": "Faalad lama xushay.",
        "your_key": "Furahaaga waa: ",
        "browse_file_title": "Xulo Faalada",
        "an_error_occurred": "Khalad ayaa dhacay",
    },
}


current_language = "en"
def main_menu():
    def exit_application():
        root.destroy()

    def open_text_menu():
        root.destroy()
        text_menu(current_language)

    def open_file_menu():
        root.destroy()
        file_menu(current_language)

    def change_language(event):
        selected_lang = language_combobox.get()
        if selected_lang in language_titles:
            lang_code = language_titles[selected_lang]
            global current_language
            current_language = lang_code
            update_main_menu_text()

    def update_main_menu_text():
        root.title(translations_main_menu[current_language]["title"])
        text_button.config(text=translations_main_menu[current_language]["text_option"])
        file_button.config(text=translations_main_menu[current_language]["file_option"])
        choose_option_label.config(text=translations_main_menu[current_language]["choose_option"])
        language_label.config(text=translations_main_menu[current_language]["language_option"])
        language_combobox.set(translations_main_menu[current_language]["title"])


    root = tk.Tk()
    root.title(translations_main_menu[current_language]["title"])
    root.attributes('-fullscreen', True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    bg_image = Image.open("background.jpg").resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)


    choose_option_label = tk.Label(root, text=translations_main_menu[current_language]["choose_option"], font=("Helvetica", 40), bg="#debfa2")
    choose_option_label.place(relx=0.5, rely=0.2, anchor="center")


    text_button = tk.Button(
        root,
        text=translations_main_menu[current_language]["text_option"],
        font=("Helvetica", 35), relief="solid", bg="#00ffb6", fg="white", activebackground="#006a4b",
        command=open_text_menu
    )
    text_button.place(relx=0.46, rely=0.35, anchor="center")


    file_button = tk.Button(
        root,
        text=translations_main_menu[current_language]["file_option"],
        font=("Helvetica", 35), relief="solid", bg="#aa67ff", fg="white", activebackground="#7000ff",
        command=open_file_menu
    )
    file_button.place(relx=0.54, rely=0.35, anchor="center")


    language_label = tk.Label(root, text=translations_main_menu[current_language]["language_option"], font=("Helvetica", 40), bg="#eeb185")
    language_label.place(relx=0.5, rely=0.5, anchor="center")

    language_titles = {lang_data["title"]: lang_code for lang_code, lang_data in translations_main_menu.items()}
    language_combobox = ttk.Combobox(root, values=list(language_titles.keys()), state="readonly", width=35, font=("Helvetica", 25))
    language_combobox.place(relx=0.5, rely=0.6, anchor="center")
    language_combobox.set(translations_main_menu[current_language]["title"])


    language_combobox.bind("<<ComboboxSelected>>", change_language)

    try:
        exit_icon = PhotoImage(file="exit_icon.png")
        exit_button = tk.Button(root, image=exit_icon, command=exit_application, borderwidth=0)
        exit_button.image = exit_icon
        exit_button.place(x=1870, y=10)
    except Exception as e:
        print(f"Error loading exit icon: {e}")


    update_main_menu_text()

    root.mainloop()



def file_menu(current_language):
    def go_to_main_menu():
        root.destroy()
        main_menu()

    def exit_application():
        root.destroy()

    global key_entry_file, method, file_path_entry, key_entry_file

    def browse_file():
        file_path = filedialog.askopenfilename(title=translations_file_menu[current_language]["browse_file_title"])
        if file_path:
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, file_path)

    def process_file(action):
        file_path = file_path_entry.get()
        key = key_entry_file.get()

        if not file_path:
            messagebox.showerror(translations_file_menu[current_language]["error"],
                                 translations_file_menu[current_language]["no_file_selected"])
            return

        if not key.isdigit():
            messagebox.showerror(translations_file_menu[current_language]["error"],
                                 translations_file_menu[current_language]["key_is_digit_error"])
            return

        key = int(key)
        try:
            with open(file_path, 'r') as file:
                content = file.read()


            if method.get() == "Caesar":
                result = sezar_encryption(content, key) if action == "Encrypt" else sezar_decryption(content, key)
            elif method.get() == "XOR":
                result = xor_encryption(content, key) if action == "Encrypt" else xor_decryption(content, key)
            else:
                messagebox.showerror(translations_file_menu[current_language]["error"],
                                     translations_file_menu[current_language]["unknown_method_error"])
                return

            save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     title=translations_file_menu[current_language]["save_file_title"])
            if save_path:
                with open(save_path, 'w') as file:
                    file.write(result + '\n' + translations_file_menu[current_language]["your_key"] + str(key))
                messagebox.showinfo(translations_file_menu[current_language]["file_processed_success"],
                                    translations_file_menu[current_language]["file_processed_success"])

        except Exception as e:
            messagebox.showerror(translations_file_menu[current_language]["error"],
                                 f"{translations_file_menu[current_language]['an_error_occurred']}: {str(e)}")

    def update_ui_language():

        root.title(translations_file_menu[current_language]["file_encryption_decryption_tool_title"])
        file_label.config(text=translations_file_menu[current_language]["select_file_label"])
        browse_button.config(text=translations_file_menu[current_language]["browse_button_text"])
        method_label.config(text=translations_file_menu[current_language]["select_encryption_method_label"])
        key_label.config(text=translations_file_menu[current_language]["enter_key_label"])
        random_button.config(text=translations_file_menu[current_language]["generate_random_key"])
        encrypt_button.config(text=translations_file_menu[current_language]["encrypt_button"])
        decrypt_button.config(text=translations_file_menu[current_language]["decrypt_button"])


    root = tk.Tk()
    root.attributes('-fullscreen', True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    bg_image = Image.open("background.jpg").resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)




    file_label = tk.Label(root, text=translations_file_menu[current_language]["select_file_label"], font=("Arial", 30), bg="#debfa2", relief="solid")
    file_label.place(relx=0.5, rely=0.145, anchor="center")

    file_path_entry = tk.Entry(root, width=35, font=("Arial", 30), bg="#debfa2", relief="solid")
    file_path_entry.place(relx=0.513, rely=0.25, anchor="center")

    browse_button = tk.Button(root, text=translations_file_menu[current_language]["browse_button_text"], command=browse_file, font=("Arial", 20), bg="#debfa2", relief="solid")
    browse_button.place(relx=0.28, rely=0.25, anchor="center")

    method_label = tk.Label(root, text=translations_file_menu[current_language]["select_encryption_method_label"], font=("Arial", 30), bg="#debfa2", relief="solid")
    method_label.place(relx=0.5, rely=0.34, anchor="center")

    method = tk.StringVar(value="Caesar")
    method_option = tk.OptionMenu(root, method, "Caesar", "XOR")
    method_option.config(font=("Arial", 25), bg="#debfa2", relief="solid", activebackground="#debfa2")
    method_option.place(relx=0.5, rely=0.42, anchor="center")

    key_label = tk.Label(root, text=translations_file_menu[current_language]["enter_key_label"], font=("Arial", 30), bg="#debfa2", relief="solid")
    key_label.place(relx=0.5, rely=0.5, anchor="center")

    key_entry_file = tk.Entry(root, font=("Arial", 30), bg="#debfa2", relief="solid")
    key_entry_file.place(relx=0.5, rely=0.58, anchor="center")

    random_button = tk.Button(root, text=translations_file_menu[current_language]["generate_random_key"], command=lambda: generate_random_key_file(), font=("Arial", 20), relief="solid", bg="#4CAF50", fg="white", activebackground="#00FF00")
    random_button.place(relx=0.304, rely=0.58, anchor="center")


    button_frame = tk.Frame(root, bg="#f9f9f9")
    button_frame.place(relx=0.5, rely=0.7, anchor="center")
    encrypt_button = tk.Button(button_frame, text=translations_file_menu[current_language]["encrypt_button"], command=lambda: process_file("Encrypt"), font=("Arial", 40), relief="solid", bg="#2196F3", fg="white", activebackground="#033a64")
    encrypt_button.pack(side=tk.LEFT, padx=1)

    decrypt_button = tk.Button(button_frame, text=translations_file_menu[current_language]["decrypt_button"], command=lambda: process_file("Decrypt"), font=("Arial", 40), relief="solid", bg="#FF2343", fg="white", activebackground="#68000f")
    decrypt_button.pack(side=tk.RIGHT, padx=1)


    update_ui_language()

    try:
        back_icon = PhotoImage(file="back_icon.png")
        back_button = tk.Button(root, image=back_icon, command=go_to_main_menu, borderwidth=0)
        back_button.image = back_icon
        back_button.place(x=10, y=10)
    except Exception as e:
        print(f"Error loading back icon: {e}")

    try:
        exit_icon = PhotoImage(file="exit_icon.png")
        exit_button = tk.Button(root, image=exit_icon, command=exit_application, borderwidth=0)
        exit_button.image = exit_icon
        exit_button.place(x=1870, y=10)
    except Exception as e:
        print(f"Error loading exit icon: {e}")

    root.mainloop()


main_menu()
