import random
from datetime import datetime
import os
import time
import requests

# Warna ANSI escape sequences
CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
MAGENTA = "\033[1;35m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
NC = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

API_URL = "https://bin.zerostore.web.id"

def check_bin(bin_number):
    try:
        response = requests.post(API_URL, json={"bin": bin_number}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                return f"{RED}❌ BIN {bin_number} tidak valid.{NC}"
            
            return f"""
{GREEN}✅ BIN: {bin_number}{NC}
{CYAN}🏦 Bank: {data.get('bank', 'Unknown')}
💳 Brand: {data.get('scheme', 'Unknown')}
📌 Tipe: {data.get('type', 'Unknown')}
🌎 Negara: {data.get('country_name', 'Unknown')} {data.get('country_emoji', '')}{NC}
"""
        else:
            return f"{RED}❌ Error API untuk BIN {bin_number}{NC}"
    except Exception as e:
        return f"{RED}⚠️ Gagal mengecek BIN {bin_number}: {e}{NC}"

def show_loading():
    print(f"{YELLOW}Memuat...", end="", flush=True)
    for _ in range(5):
        print(".", end="", flush=True)
        time.sleep(0.1)
    print(NC, flush=True)

def luhn_check(card_number_str):
    digits = [int(d) for d in card_number_str]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    
    for d in even_digits:
        checksum += sum(divmod(d * 2, 10))
    
    return checksum % 10 == 0

def generate_expiry():
    return f"{random.randint(1,12):02d}|{random.randint(2025,2039)}"

def generate_cvv():
    return f"{random.randint(000,999):03d}"

def generate_bin():
    return ''.join(str(random.randint(0,9)) for _ in range(random.randint(6,14)))

def generate_card_number(bin_code):
    card_number = list(bin_code)
    while len(card_number) < 15:
        card_number.append(str(random.randint(0,9)))
    
    for i in range(10):
        candidate = ''.join(card_number + [str(i)])
        if luhn_check(candidate):
            return candidate
    return ''.join(card_number + ['0'])

def display_header():
    current_time = datetime.now()
    print(f"""
{CYAN}╔═══════════════════════════════════════╗
║{GREEN}          █▀▀▀▀▀▀▀▀▀▀▀▀▀█              {NC}{CYAN}║
║{GREEN}          │ KILLER TOOLS│              {NC}{CYAN}║
║{GREEN}          █▄▄▄▄▄▄▄▄▄▄▄▄▄█              {NC}{CYAN}║
╠═══════════════════════════════════════╣
║ {MAGENTA}📅 {current_time.strftime('%A, %d %B %Y')}{NC}{CYAN}           ║
║ {MAGENTA}⏰ {current_time.strftime('%H:%M:%S')}{NC}{CYAN}                          ║
╚═══════════════════════════════════════╝{NC}""")

def display_results(cards):
    print(f"{CYAN}╔═══════════════════════════════════════╗")
    print(f"║{YELLOW}   HASIL GENERATE KARTU KREDIT         {NC}{CYAN}║")
    print(f"╠═══════════════════════════════════════╣")
    print(f"║ No. Kartu       Expiry    CVV  Status ║")
    print(f"╠═══════════════════════════════════════╣")
    
    for card in cards:
        parts = card.split("|")
        if len(parts) != 4:
            print(f"{RED}Format kartu tidak valid!{NC}")
            continue
            
        number, month, year, cvv = parts
        status = f"{GREEN}Hidup{NC}" if luhn_check(number) else f"{RED}Mati{NC}"
        print(f"║ {number.ljust(16)} {month}/{year} {cvv}  {status.ljust(7)} ║")
    
    print(f"{CYAN}╚═══════════════════════════════════════╝{NC}")

def show_menu():
    print(f"""
{CYAN}╔═══════════════════════════════════════╗
║{YELLOW}         K I L L E R  T O O L S        {NC}{CYAN}║
╠═══════════════════════════════════════╣
║ {GREEN}1. Generate Kartu dengan BIN          ║
║ {GREEN}2. Generate dengan BIN,Exp,CVV        ║
║ {GREEN}3. Cek BIN                            ║
║ {RED}4. Keluar                             ║
╚═══════════════════════════════════════╝{NC}""")

def validate_expiry(expiry):
    try:
        month, year = expiry.split("|")
        if 1 <= int(month) <= 12 and 2023 <= int(year) <= 2039:
            return True
    except:
        return False
    return False

def main():
    clear_screen()
    display_header()
    
    while True:
        show_menu()
        choice = input("\nPilih opsi (1/2/3/4): ")
        
        if choice == "1":
            clear_screen()
            display_header()
            bin_code = input("Masukkan BIN (6-14 digit): ").strip()
            
            if not bin_code.isdigit() or 6 > len(bin_code) > 14:
                print(f"{RED}⚠ BIN tidak valid!{NC}")
                time.sleep(1)
                continue
                
            cards = []
            try:
                total = int(input("Jumlah kartu: "))
                for _ in range(total):
                    card = f"{generate_card_number(bin_code)}|{generate_expiry()}|{generate_cvv()}"
                    cards.append(card)
                
                clear_screen()
                display_header()
                display_results(cards)
            except:
                print(f"{RED}⚠ Input tidak valid!{NC}")
            
            input("\nTekan Enter untuk lanjut...")
            clear_screen()
            display_header()

        elif choice == "2":
            clear_screen()
            display_header()
            
            bin_code = input("Masukkan BIN (6-14 digit): ").strip()
            if not bin_code.isdigit() or 6 > len(bin_code) > 14:
                print(f"{RED}⚠ BIN tidak valid!{NC}")
                time.sleep(1)
                continue
                
            expiry = input("Expiry (MM|YYYY): ")
            if not validate_expiry(expiry):
                print(f"{RED}⚠ Format expiry salah!{NC}")
                time.sleep(1)
                continue
                
            cvv = input("CVV: ").zfill(3)
            if len(cvv) != 3 or not cvv.isdigit():
                print(f"{RED}⚠ CVV tidak valid!{NC}")
                time.sleep(1)
                continue
                
            cards = []
            try:
                total = int(input("Jumlah kartu: "))
                for _ in range(total):
                    card = f"{generate_card_number(bin_code)}|{expiry}|{cvv}"
                    cards.append(card)
                
                clear_screen()
                display_header()
                display_results(cards)
            except:
                print(f"{RED}⚠ Input tidak valid!{NC}")
            
            input("\nTekan Enter untuk lanjut...")
            clear_screen()
            display_header()

        elif choice == "3":
            clear_screen()
            display_header()
            bin_input = input("Masukkan BIN: ").strip()
            print(check_bin(bin_input))
            input("\nTekan Enter untuk lanjut...")
            clear_screen()
            display_header()

        elif choice == "4":
            print(f"\n{RED}✌️ Terima kasih!{NC}")
            break

        else:
            print(f"{RED}⚠ Pilihan tidak valid!{NC}")
            time.sleep(0.5)
            clear_screen()
            display_header()

if __name__ == "__main__":
    main()
