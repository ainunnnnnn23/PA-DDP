#last update 28-10-08.16

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
    dataheader_akun = ["nama", "password", "role", "ipk", "saldo"]
    data_akun = [
        {"nama": nama, "password": password, "role": "user", "ipk": ipk, "saldo": 0} 
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
    dataheader_beasiswa = ["id", "nama", "ipk", "jumlah", "Kuota"]
    
    try:
        with open('beasiswa.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            id_terakhir = max([int(row['id']) for row in reader], default=0) + 1
    except FileNotFoundError:
        id_terakhir = 1 

    data_beasiswa = [
        {"id": id_terakhir, "nama": nama, "ipk": ipk, "jumlah": jumlah, "Kuota": kuota}
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

#buat update beasiswa
def update_beasiswa(beasiswa_id, ipk=None, jumlah=None, kuota=None):
    updated = False
    data = []
    try:
        with open('beasiswa.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        for row in data:
            if row['id'] == beasiswa_id:
                if ipk is not None:
                    row['ipk'] = ipk
                if jumlah is not None:
                    row['jumlah'] = jumlah
                if kuota is not None:
                    row['Kuota'] = kuota
                updated = True

        if updated:
            with open('beasiswa.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Data beasiswa dengan ID {beasiswa_id} berhasil diperbarui.")
        else:
            print(f"Beasiswa dengan ID {beasiswa_id} tidak ditemukan.")
    except FileNotFoundError:
        print("File beasiswa.csv tidak ditemukan.")

#Buat update data
def update_data_user(nama, role=None, saldo=None):
    updated = False
    data = []
    try:
        with open('data.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        
        for row in data:
            if row['nama'] == nama:
                if role:
                    row['role'] = role
                if saldo is not None:
                    row['saldo'] = saldo
                updated = True
        
        if updated:
            with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Data user {nama} berhasil diperbarui.")
        else:
            print(f"User {nama} tidak ditemukan.")
    except FileNotFoundError:
        print("File data.csv tidak ditemukan.")


# Buat menu Admin
def menu_admin():
    while True:
        print("==== Menu Admin ====")
        print("1. Lihat beasiswa/user")
        print("2. Tambah beasiswa")
        print("3. Update beasiswa/user")
        print("5. Logout")
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
                try:
                    ipk = float(input("Masukan jumlah minimal ipk: "))
                    if ipk > 4.0:
                        print("IPK tidak boleh melebihi 4")
                        continue
                    jumlah = float(input("Masukan jumlah beasiswa: "))
                    kuota = int(input("Masukan kuota beasiswa: "))
                    tambah_beasiswa(nama, ipk, jumlah, kuota)
                    break
                except ValueError:
                    print("Nilai yang anda masukan bukan merupakan angka")
        
        elif pilihan == "3":
            print("1. Update akun")
            print("2. Update Beasiswa")
            pil_1 = input("Masukan pilihan: ")
            
            if pil_1 == "1":
                lihat_data_user()
                nama = input("Masukkan nama user: ")
                print("Pilih Role Baru:")
                print("1. Admin")
                print("2. User")
                valid_input = True  # Flag untuk cek validitas input
                
                # Memilih role dengan validasi
                role_option = input("Masukkan pilihan role (1 untuk Admin, 2 untuk User): ")
                if role_option == "1":
                    role = "admin"
                elif role_option == "2":
                    role = "user"
                else:
                    print("Pilihan role tidak valid")
                    valid_input = False  # Set flag ke False jika input tidak valid

                # Memasukkan saldo dengan validasi
                if valid_input:  
                    saldo_input = input("Masukkan saldo baru (kosongkan jika tidak ingin mengubah): ")
                    try:
                        saldo = float(saldo_input) if saldo_input else None
                    except ValueError:
                        print("Nilai saldo yang anda masukan bukan merupakan angka")
                        valid_input = False  # Set flag ke False jika input saldo tidak valid

                # Panggil update_data_user hanya jika semua input valid
                if valid_input:
                    update_data_user(nama, role, saldo)
                else:
                    print("Data tidak dapat diperbarui karena input tidak valid.")

            elif pil_1 == "2":
                lihat_beasiswa()
                beasiswa_id = input("Masukkan ID beasiswa: ")
                valid_input = True  # Flag untuk cek validitas input
                
                # Validasi input IPK
                ipk_input = input("Masukkan IPK baru (kosongkan jika tidak ingin mengubah): ")
                try:
                    ipk = float(ipk_input) if ipk_input else None
                except ValueError:
                    print("Nilai IPK yang anda masukkan bukan merupakan angka")
                    valid_input = False         

                # Validasi input Jumlah Beasiswa
                if valid_input:  
                    jumlah_input = input("Masukkan jumlah beasiswa baru (kosongkan jika tidak ingin mengubah): ")
                    try:
                        jumlah = float(jumlah_input) if jumlah_input else None
                    except ValueError:
                        print("Nilai jumlah beasiswa yang anda masukkan bukan merupakan angka")
                        valid_input = False 

                # Validasi input Kuota
                if valid_input: 
                    kuota_input = input("Masukkan kuota beasiswa baru (kosongkan jika tidak ingin mengubah): ")
                    try:
                        kuota = int(kuota_input) if kuota_input else None
                    except ValueError:
                        print("Nilai kuota yang anda masukkan bukan merupakan angka")
                        valid_input = False  

                if valid_input:
                    update_beasiswa(beasiswa_id, ipk, jumlah, kuota)
                else:
                    print("Data beasiswa tidak dapat diperbarui karena input tidak valid.")

        elif pilihan == "5":
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
                    try:
                        ipk = float(input("Masukan IPK: "))
                        if ipk > 4:
                            print("IPK tidak boleh melebihi 4")
                            continue
                        simpan_data_akun(nama, password, ipk)
                        break
                    except ValueError:
                        print("Nilai yang anda masukan bukan merupakan angka")

        # Buat keluar program
        elif pil_1 == "3": 
            print("Keluar Program.")
            exit()

        # Buat pilihan tidak valid
        else:
            print("Pilihan tidak valid, coba lagi.")

menu_login()
