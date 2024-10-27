import pwinput
import csv

csv_file = 'data.csv'

simbol  = [
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", 
    "{", "}", "[", "]", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "|", "~"
]
angka = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

dataheader_akun = ["nama", "password"]

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

def simpan_data_akun(nama, password):
    data_akun = [
        {"nama": nama, "password": password}
    ]
    try:
        with open(csv_file, "a", newline="", encoding="utf-8") as akun:
            writer = csv.DictWriter(akun, fieldnames=dataheader_akun)
            akun.seek(0, 2)  
            if akun.tell() == 0:  
                writer.writeheader()
            writer.writerows(data_akun)  
        print("Data berhasil disimpan!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def menu_login():
    while True:
        print("======== Menu Login =========")
        print("1. Login")
        print("2. Register")
        print("3. Keluar Program")
        pil_1 = input("Masukan Pilihan: ")

        if pil_1 == "1":
            print("===== Login ======")
            while True:
                nama = input("Masukan nama: ")
                if nama == "":
                    print("Nama tidak boleh kosong")
                    continue
                if any(char in simbol for char in nama) or any(char in angka for char in nama):
                    print("Nama tidak boleh mengandung angka atau simbol")
                    continue
                else:
                    password = pwinput.pwinput("Masukaan Password: ")
                    if password == "":
                        print("Password tidak boeh kosong")
                    

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
                    simpan_data_akun(nama, password)
                    break

        elif pil_1 == "3":
            print("Keluar Program.")
            exit()

        else:
            print("Pilihan tidak valid, coba lagi.")

nama, password = menu_login()
