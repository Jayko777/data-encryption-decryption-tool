import tkinter as tk
import sys
import os
from tkinter import messagebox, ttk, filedialog, PhotoImage
from PIL import Image, ImageTk
from file_menu_library import translations_file_menu
from text_menu_library import translations_text_file
from main_menu_library import translations_main_menu
import random

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for both dev and PyInstaller builds. """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

bg_image_path = resource_path("background.jpg")
bg_image = Image.open(bg_image_path)


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
    text_label.place(relx=0.43, rely=0.1)

    input_field = tk.Text(root, height=5, width=50, font=("Arial", 18), bg="#edb288",  bd=2, relief="solid")
    input_field.place(relx=0.30, rely=0.17)

    encryption_method_label = tk.Label(root, text=translations_text_file[current_language]["encryption_method_label"],
                                       font=("Arial", 20, "bold"), bg="#ecb187")
    encryption_method_label.place(relx=0.395, rely=0.35)

    encryption_method = ttk.Combobox(root, values=["Caesar", "XOR"], state="readonly", font=("Arial", 28))
    encryption_method.set("Caesar")
    encryption_method.place(relx=0.36, rely=0.42)

    key_label = tk.Label(root, text=translations_text_file[current_language]["key_label"],
                         font=("Arial", 18, "bold"), bg="#ecb187")
    key_label.place(relx=0.425, rely=0.49)

    key_entry_text = tk.Entry(root, font=("Arial", 36), bd=2, bg="#ecb48f", relief="solid")
    key_entry_text.place(relx=0.33, rely=0.53)

    random_button = tk.Button(root, text=translations_text_file[current_language]["random_button_text"],
                              font=("Arial", 20), command=lambda: generate_random_key_text(),
                              relief="solid", bg="#4CAF50", fg="white", activebackground="#45a049")
    random_button.place(relx=0.132, rely=0.533)

    output_label = tk.Label(root, text=translations_text_file[current_language]["output_label"],
                            font=("Arial", 18, "bold"), bg="#eab895")
    output_label.place(relx=0.465, rely=0.61)

    output_field = tk.Text(root, height=5, width=50, font=("Arial", 18), bd=2, bg="#eab897", relief="solid")
    output_field.place(relx=0.305, rely=0.66)

    history_label = tk.Label(root, text=translations_text_file[current_language]["history_label"],
                             font=("Arial", 20, "bold"), bg="#dfbbad")
    history_label.place(relx=0.84, rely=0.31)

    history_text = tk.Text(root, height=15, width=50, font=("Arial", 9), bd=2, bg="#dcc1ba", relief="solid")
    history_text.place(relx=0.76, rely=0.36)

    # Buttons for Encrypt and Decrypt
    encrypt_button = tk.Button(root, text=translations_text_file[current_language]["encrypt_button"],
                               font=("Arial", 32), relief="solid", bg="#2196F3", fg="white",
                               activebackground="#1976D2",
                               command=lambda: process_text("Encrypt", input_field, key_entry_text, encryption_method,
                                                            output_field, history_text))
    encrypt_button.place(relx=0.34, rely=0.86)

    decrypt_button = tk.Button(root, text=translations_text_file[current_language]["decrypt_button"],
                               font=("Arial", 32), relief="solid", bg="#FF2343", fg="white",
                               activebackground="#E64A19",
                               command=lambda: process_text("Decrypt", input_field, key_entry_text, encryption_method,
                                                            output_field, history_text))
    decrypt_button.place(relx=0.52, rely=0.86)

    try:
        back_icon = tk.PhotoImage(file="back_icon.png")
        back_button = tk.Button(root, image=back_icon, command=go_to_main_menu, borderwidth=1)
        back_button.image = back_icon
        back_button.place(relx=0.01, rely=0.01)
    except Exception as e:
        print(f"Error loading back icon: {e}")

    try:
        exit_icon = tk.PhotoImage(file="exit_icon.png")
        exit_button = tk.Button(root, image=exit_icon, command=exit_application, borderwidth=0)
        exit_button.image = exit_icon
        exit_button.place(relx=0.99, rely=0.01, anchor="ne")
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
    text_button.place(relx=0.42, rely=0.35, anchor="center")


    file_button = tk.Button(
        root,
        text=translations_main_menu[current_language]["file_option"],
        font=("Helvetica", 35), relief="solid", bg="#aa67ff", fg="white", activebackground="#7000ff",
        command=open_file_menu
    )
    file_button.place(relx=0.58, rely=0.35, anchor="center")


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
        exit_button.place(relx=0.97, y=0.08)
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
    file_path_entry.place(relx=0.54, rely=0.23, anchor="center")

    browse_button = tk.Button(root, text=translations_file_menu[current_language]["browse_button_text"], command=browse_file, font=("Arial", 20), bg="#debfa2", relief="solid")
    browse_button.place(relx=0.25, rely=0.23, anchor="center")

    method_label = tk.Label(root, text=translations_file_menu[current_language]["select_encryption_method_label"], font=("Arial", 30), bg="#debfa2", relief="solid")
    method_label.place(relx=0.5, rely=0.34, anchor="center")

    method = tk.StringVar(value="Caesar")
    method_option = tk.OptionMenu(root, method, "Caesar", "XOR")
    method_option.config(font=("Arial", 25), bg="#debfa2", relief="solid", activebackground="#debfa2")
    method_option.place(relx=0.5, rely=0.42, anchor="center")

    key_label = tk.Label(root, text=translations_file_menu[current_language]["enter_key_label"], font=("Arial", 30), bg="#debfa2", relief="solid")
    key_label.place(relx=0.5, rely=0.5, anchor="center")

    key_entry_file = tk.Entry(root, font=("Arial", 30), bg="#debfa2", relief="solid")
    key_entry_file.place(relx=0.51, rely=0.58, anchor="center")

    random_button = tk.Button(root, text=translations_file_menu[current_language]["generate_random_key"], command=lambda: generate_random_key_file(), font=("Arial", 18), relief="solid", bg="#4CAF50", fg="white", activebackground="#00FF00")
    random_button.place(relx=0.277, rely=0.58, anchor="center")


    button_frame_encrypt = tk.Frame(root, bg="#f9f9f9")
    button_frame_encrypt.place(relx=0.43, rely=0.74, anchor="center")
    encrypt_button = tk.Button(button_frame_encrypt, text=translations_file_menu[current_language]["encrypt_button"], command=lambda: process_file("Encrypt"), font=("Arial", 40), relief="solid", bg="#2196F3", fg="white", activebackground="#033a64")
    encrypt_button.pack(side=tk.LEFT, padx=1)
    
    button_frame_decrypt = tk.Frame(root, bg="#f9f9f9")
    button_frame_decrypt.place(relx=0.59, rely=0.74, anchor="center")
    decrypt_button = tk.Button(button_frame_decrypt, text=translations_file_menu[current_language]["decrypt_button"], command=lambda: process_file("Decrypt"), font=("Arial", 40), relief="solid", bg="#FF2343", fg="white", activebackground="#68000f")
    decrypt_button.pack(side=tk.RIGHT, padx=1)


    update_ui_language()

    try:
        back_icon = PhotoImage(file="back_icon.png")
        back_button = tk.Button(root, image=back_icon, command=go_to_main_menu, borderwidth=0)
        back_button.image = back_icon
        back_button.place(relx=0.005, rely=0.005)
    except Exception as e:
        print(f"Error loading back icon: {e}")

    try:
        exit_icon = PhotoImage(file="exit_icon.png")
        exit_button = tk.Button(root, image=exit_icon, command=exit_application, borderwidth=0)
        exit_button.image = exit_icon
        exit_button.place(relx=0.97, rely=0.005)
    except Exception as e:
        print(f"Error loading exit icon: {e}")

    root.mainloop()


main_menu()

