import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from tkinter import ttk  # Menggunakan ttk untuk Dropdown

# --- Helper Functions ---
def text_to_numeric(text):
    return [ord(char) - ord('a') for char in text.lower() if char.isalpha()]

def numeric_to_text(numbers):
    return ''.join(chr(num + ord('a')) for num in numbers)

def mod_inverse(matrix, modulus):
    determinant = int(np.round(np.linalg.det(matrix))) % modulus
    determinant_inv = pow(determinant, -1, modulus)
    adjugate = np.round(np.linalg.det(matrix) * np.linalg.inv(matrix)).astype(int)
    return (determinant_inv * adjugate) % modulus

# --- Vigenere Cipher ---
def vigenere_encrypt(plain_text, key):
    key = key.lower()
    key_sequence = (key * ((len(plain_text) // len(key)) + 1))[:len(plain_text)]
    cipher_text = ''.join(chr((ord(p) + ord(k) - 2 * ord('a')) % 26 + ord('a')) for p, k in zip(plain_text, key_sequence))
    return cipher_text

def vigenere_decrypt(cipher_text, key):
    key = key.lower()
    key_sequence = (key * ((len(cipher_text) // len(key)) + 1))[:len(cipher_text)]
    plain_text = ''.join(chr((ord(c) - ord(k) + 26) % 26 + ord('a')) for c, k in zip(cipher_text, key_sequence))
    return plain_text

# --- Playfair Cipher --- #
def playfair_encrypt(plain_text, key):
    key_matrix = generate_key_matrix(key)
    processed_text = preprocess_text(plain_text)
    cipher_text = process_text(processed_text, key_matrix, mode='encrypt')
    return cipher_text

def playfair_decrypt(cipher_text, key):
    key_matrix = generate_key_matrix(key)
    decrypted_text = process_text(cipher_text, key_matrix, mode='decrypt')
    return decrypted_text

# Helper functions for Playfair Cipher
def generate_key_matrix(key):
    key = ''.join(dict.fromkeys(key.lower().replace("j", "i")))
    key += ''.join(c for c in "abcdefghiklmnopqrstuvwxyz" if c not in key)
    key_matrix = [key[i:i + 5] for i in range(0, 25, 5)]
    return key_matrix

def preprocess_text(text):
    text = text.lower().replace("j", "i")
    processed_text = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'x'
        if a == b:
            processed_text += a + 'x'
            i += 1
        else:
            processed_text += a + b
            i += 2
    if len(processed_text) % 2 != 0:
        processed_text += 'x'
    return processed_text

def process_text(text, key_matrix, mode):
    result_text = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        row1, col1 = divmod(find_position(a, key_matrix), 5)
        row2, col2 = divmod(find_position(b, key_matrix), 5)

        if row1 == row2:
            result_text += key_matrix[row1][(col1 + (1 if mode == 'encrypt' else -1)) % 5]
            result_text += key_matrix[row2][(col2 + (1 if mode == 'encrypt' else -1)) % 5]
        elif col1 == col2:
            result_text += key_matrix[(row1 + (1 if mode == 'encrypt' else -1)) % 5][col1]
            result_text += key_matrix[(row2 + (1 if mode == 'encrypt' else -1)) % 5][col2]
        else:
            result_text += key_matrix[row1][col2]
            result_text += key_matrix[row2][col1]

    return result_text

def find_position(char, key_matrix):
    for i, row in enumerate(key_matrix):
        if char in row:
            return i * 5 + row.index(char)
    return -1

# --- Hill Cipher ---
def hill_encrypt(plain_text, key_matrix):
    key_size = key_matrix.shape[0]
    plain_numeric = text_to_numeric(plain_text)
    while len(plain_numeric) % key_size != 0:
        plain_numeric.append(0)
    plain_numeric = np.array(plain_numeric).reshape(-1, key_size)
    cipher_numeric = np.dot(plain_numeric, key_matrix) % 26
    return numeric_to_text(cipher_numeric.flatten())

def hill_decrypt(cipher_text, key_matrix):
    key_size = key_matrix.shape[0]
    cipher_numeric = text_to_numeric(cipher_text)
    cipher_numeric = np.array(cipher_numeric).reshape(-1, key_size)
    key_matrix_inv = mod_inverse(key_matrix, 26)
    plain_numeric = np.dot(cipher_numeric, key_matrix_inv) % 26
    return numeric_to_text(plain_numeric.flatten())

# --- GUI Application ---
class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cipher Encrypt & Decrypt")
        self.root.configure(bg="#f0f0f0")

        # Input area
        self.input_label = tk.Label(root, text="Input Text / File:", bg="#f0f0f0", font=("Arial", 12))
        self.input_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.input_text = tk.Text(root, height=10, width=50, bg="#ffffff", fg="#000000")
        self.input_text.grid(row=1, column=0, padx=10, pady=5)
        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file, bg="#4CAF50", fg="#ffffff")
        self.upload_button.grid(row=2, column=0, pady=5)

        # Key area
        self.key_label = tk.Label(root, text="Key (min 12 chars):", bg="#f0f0f0", font=("Arial", 12))
        self.key_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.key_entry = tk.Entry(root, width=50, bg="#ffffff", fg="#000000")
        self.key_entry.grid(row=4, column=0, padx=10, pady=5)

        # Cipher selection
        self.cipher_label = tk.Label(root, text="Select Cipher:", bg="#f0f0f0", font=("Arial", 12))
        self.cipher_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.cipher_var = tk.StringVar(value="Vigenere")
        self.cipher_menu = ttk.Combobox(root, textvariable=self.cipher_var, state="readonly", font=("Arial", 12))
        self.cipher_menu["values"] = ["Vigenere", "Playfair", "Hill"]
        self.cipher_menu.grid(row=6, column=0, pady=5)
        self.cipher_menu.set("Vigenere")

        # Action buttons
        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt, bg="#2196F3", fg="#ffffff")
        self.encrypt_button.grid(row=7, column=0, pady=5)
        self.decrypt_button = tk.Button(root, text="Decrypt", command=self.decrypt, bg="#FF5722", fg="#ffffff")
        self.decrypt_button.grid(row=8, column=0, pady=5)

        # Output area
        self.output_label = tk.Label(root, text="Output:", bg="#f0f0f0", font=("Arial", 12))
        self.output_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.output_text = tk.Text(root, height=10, width=50, bg="#ffffff", fg="#000000")
        self.output_text.grid(row=10, column=0, padx=10, pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, file.read())

    def encrypt(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()
        cipher = self.cipher_var.get()
        if len(key) < 12:
            messagebox.showerror("Error", "Key must be at least 12 characters long!")
            return
        if cipher == "Vigenere":
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, vigenere_encrypt(text, key))
        elif cipher == "Playfair":
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, playfair_encrypt(text, key))
        elif cipher == "Hill":
            key_matrix = np.array(text_to_numeric(key[:9])).reshape(3, 3)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, hill_encrypt(text, key_matrix))
        else:
            messagebox.showerror("Error", "Invalid cipher selected!")

    def decrypt(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()
        cipher = self.cipher_var.get()
        if len(key) < 12:
            messagebox.showerror("Error", "Key must be at least 12 characters long!")
            return
        if cipher == "Vigenere":
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, vigenere_decrypt(text, key))
        elif cipher == "Playfair":
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, playfair_decrypt(text, key))
        elif cipher == "Hill":
            key_matrix = np.array(text_to_numeric(key[:9])).reshape(3, 3)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, hill_decrypt(text, key_matrix))
        else:
            messagebox.showerror("Error", "Invalid cipher selected!")

# --- Run Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()
