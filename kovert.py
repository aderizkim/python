import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import pandas as pd
from tkinter import ttk

class DatabaseToExcelConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi konverter db ke excel")
        root.configure(bg="#161A30")

        # Mendapatkan lebar dan tinggi layar
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Menghitung posisi x dan y untuk menempatkannya di tengah
        x = (screen_width - 1300) // 2
        y = (screen_height - 710) // 2

        # Menetapkan geometri aplikasi
        self.root.geometry(f"1800x1000+{x}+{y}")

        # Membuat frame utama dengan warna latar belakang
        main_frame = ttk.Frame(self.root, padding=(100, 100, 100, 100), style='Main.TFrame')
        main_frame.grid(row=0, column=0, padx=420, pady=100, sticky="nsew")

        # Membuat frame untuk label dan tombol dengan warna latar belakang
        
        # Membuat label di atas tombol "Pilih Database"
        label_above_button = ttk.Label(main_frame, text="Database To Excel Converter", font=("TeachersStudent", 16))
        label_above_button.grid(row=0, column=0, pady=20, sticky="n")

        # Membuat label
        label = ttk.Label(main_frame, text="Pilih Database:",font=("TeachersStudent", 14))
        label.grid(row=1, column=0, pady=15, sticky="n")

        # Membuat tombol untuk memilih database
        choose_db_button = ttk.Button(main_frame, text="Pilih Database", command=self.choose_db,style="TButton")
        choose_db_button.grid(row=3, column=0, pady=10, sticky="n")

        # Membuat tombol untuk mengkonversi ke Excel
        convert_button = ttk.Button(main_frame, text="Konversi ke Excel", command=self.convert_to_excel,style="TButton")
        convert_button.grid(row=4, column=0, pady=15, sticky="n")

        # Membuat gaya untuk tombol (style)
        style = ttk.Style()
        style.configure("TButton", font=("TeacherStudent", 12))

        # Inisialisasi atribut
        self.db_file = None
        self.label_var = tk.StringVar()
        self.label_var.set("")

        # Membuat label untuk menampilkan path database terpilih
        self.path_label = ttk.Label(main_frame, textvariable=self.label_var)
        self.path_label.grid(row=2, column=0, pady=2,padx=0, sticky="n")  

        # Memanggil metode untuk memusatkan semua widget di tengah
        self.center_window(main_frame)

    def center_window(self, frame):
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def choose_db(self):
        # Memilih file database
        db_file = filedialog.askopenfilename(filetypes=[("Database files", "*.db;*.sqlite;*.db3")])

        if db_file:
            self.db_file = db_file
            self.label_var.set(f" {db_file}")
        else:
            self.label_var.set("")

    def convert_to_excel(self):
        if self.db_file:
            # Membaca data dari database ke DataFrame
            try:
                connection = sqlite3.connect(self.db_file)
                query = "SELECT * FROM deteksi"  # Gantilah your_table_name dengan nama tabel Anda
                df = pd.read_sql_query(query, connection)

                # Memilih lokasi untuk menyimpan file Excel
                excel_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

                # Menyimpan DataFrame ke Excel
                df.to_excel(excel_file, index=False)

                # Menampilkan pesan sukses
                messagebox.showinfo("Sukses", "Konversi ke Excel berhasil!")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        else:
            # Menampilkan pesan error jika belum memilih database
            messagebox.showerror("Error", "Silakan pilih database terlebih dahulu.")

if __name__ == "__main__":
    root = tk.Tk()

    # Menambahkan gaya untuk frame utama
    style = ttk.Style()
    style.configure('Main.TFrame', background='#0766AD')  # Ganti dengan warna yang diinginkan

   

    root.iconbitmap("icon/foto.ico")  # Ganti dengan path ke file ikon Anda
    app = DatabaseToExcelConverter(root)
    root.mainloop()
