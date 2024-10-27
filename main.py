#LAST UPDATE 28-10-07.00

import pwinput
import csv
from prettytable import PrettyTable

csv_file = 'data.csv'

simbol  = [
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", 
    "{", "}", "[", "]", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "|", "~"
]
angka = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

# Buat cek akun sudah terdaftar belum
def cek_akun_terdaftar(nama):
    try:
        with open(csv_file, mode="r", newline="", encoding="utf-8") as akun_file:
            reader = csv.DictReader(akun_file)
            for row in reader:
                if row["nama"] == nama:
                    return True
        return False
    except FileNotFoundError:
        return False

# Buat nyimpan nama akun di file csv dengan role sebagai "user"
def simpan_data_akun(nama, password, ipk):
    dataheader_akun = ["nama", "password", "role", "ipk"]
    data_akun = [
        {"nama": nama, "password": password, "role": "user", "ipk": ipk} 
    ]
    try:
        with open(csv_file, "a", newline="", encoding="utf-8") as akun_file:
            writer = csv.DictWriter(akun_file, fieldnames=dataheader_akun)
            akun_file.seek(0, 2)  
            if akun_file.tell() == 0:  
                writer.writeheader()
            writer.writerows(data_akun)  
        print("Data berhasil disimpan!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Buat cek login berdasarkan nama dan password
def cek_login(nama, password):
    try:
        with open(csv_file, mode="r", newline="", encoding="utf-8") as akun_file:
            reader = csv.DictReader(akun_file)
            for row in reader:
                if row['nama'] == nama and row['password'] == password:
                    return row['role']  
        return None  
    except FileNotFoundError:
        print("Database akun tidak ditemukan.")
        return None

#Buat liat beasiswa
def lihat_beasiswa():
    table = PrettyTable()
    table.field_names = ["ID", "Nama Beasiswa", "Minimal IPK", "Jumlah Hadiah", "Kuota"]

    try:
        with open('beasiswa.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                table.add_row([row['id'], row['nama'], row['ipk'], row['jumlah'], row['pendaftar']])
        
        print(table)
    except FileNotFoundError:
        print("File beasiswa.csv tidak ditemukan.")

def lihat_data_user():
    table = PrettyTable()
    table.field_names = ["Nama", "Password", "Role"]
    
    try:
        with open('data.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                table.add_row([row['nama'], row['password'], row['role']])

        print(table)
    except FileNotFoundError:
        print("File data.csv tidak ditemukan.")

def tambah_beasiswa(nama, ipk, jumlah, kuota):
    dataheader_beasiswa = ["id", "nama", "ipk", "jumlah", "pendaftar"]
    
    try:
        with open('beasiswa.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            id_terakhir = max([int(row['id']) for row in reader], default=0) + 1
    except FileNotFoundError:
        id_terakhir = 1 

    data_beasiswa = [
        {"id": id_terakhir, "nama": nama, "ipk": ipk, "jumlah": jumlah, "pendaftar": kuota}
    ]

    try:
        with open('beasiswa.csv', mode='a', newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=dataheader_beasiswa)
            file.seek(0, 2)  
            if file.tell() == 0:  
                writer.writeheader()
            writer.writerows(data_beasiswa)  
        print("Beasiswa berhasil ditambahkan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Buat menu Admin
def menu_admin():
    while True:
        print("==== Menu Admin ====")
        print("1. Lihat beasiswa/user")
        print("2. Tambah beasiswa")
        print("3. Logout")
        pilihan = input("Masukan pilihan: ")

        #Buat lihat
        if pilihan == "1":
            print("1. Lihat akun")
            print("2. Lihat Beasiswa")
            pil_1 = input("Masukan pilihan: ")
            if pil_1 == "1":
                lihat_data_user()
            if pil_1 == "2":
                lihat_beasiswa()
        
        #Buat nambah
        elif pilihan == "2":
            while True:
                nama = input("Masukan nama beasiswa: ")
                ipk = float(input("Masukan jumlah minimal ipk: "))
                if ipk > 4.0:
                    print("IPK tidak boleh melebihi 4")
                    continue
                jumlah = float(input("Masukan jumlah beasiswa: "))
                kuota = int(input("Masukan kuota beasiswa: "))
                tambah_beasiswa(nama, ipk, jumlah, kuota)
                break
        
        elif pilihan == "3":
            menu_login()  

# Buat menu user
def menu_user():
    print("==== Menu user ====")
    print("1. Daftar beasiswa")
    print("2. Biodata diri")
    print("3. Status pendaftaran")
    print("4. Notifikasi")
    print("5. Logout")
    pil_1 = input("Masukan pilihan: ")
    
    if pil_1 == "1":
        print("Masih dalam pengembangan")

    if pil_1 == "5":
        menu_login()  

def akses_pengguna(nama, password):
    role = cek_login(nama, password)
    if role == "admin":
        print(f"Selamat datang, {nama}! Anda login sebagai Admin.")
        menu_admin()
    elif role == "user":
        print(f"Selamat datang, {nama}! Anda login sebagai User.")
        menu_user()
    else:
        print("Nama atau password salah, atau peran tidak ditemukan.")  

def menu_login():
    while True:
        print("======== Menu Login =========")
        print("1. Login")
        print("2. Register")
        print("3. Keluar Program")
        pil_1 = input("Masukan Pilihan: ")

        # Buat login
        if pil_1 == "1": 
            print("===== Login ======")
            nama = input("Masukan nama: ")
            password = pwinput.pwinput("Masukan Password: ")
            akses_pengguna(nama, password)

        # Buat register
        elif pil_1 == "2": 
            print("==== Register ====")
            while True:
                nama = input("Masukan nama: ")
                if nama == "":
                    print("Nama tidak boleh kosong")
                    continue
                if any(char in simbol for char in nama) or any(char in angka for char in nama):
                    print("Nama tidak boleh mengandung angka atau simbol. Coba lagi.")
                    continue
                if cek_akun_terdaftar(nama):
                    print("Nama sudah terdaftar! Coba nama lain.")
                    continue
                else:
                    password = pwinput.pwinput("Masukan Password: ")
                    if password == "":
                        print("Password tidak boleh kosong")
                        continue
                    ipk = float(input("Masukan IPK: "))
                    simpan_data_akun(nama, password, ipk)
                    break

        # Buat keluar program
        elif pil_1 == "3": 
            print("Keluar Program.")
            exit()

        # Buat pilihan tidak valid
        else:
            print("Pilihan tidak valid, coba lagi.")

menu_login()
