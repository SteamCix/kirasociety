import requests
from concurrent.futures import ThreadPoolExecutor
import os

def check_proxy(proxy):
    try:
        response = requests.get(
            "http://httpbin.org/ip",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=5
        )
        if response.status_code == 200:
            print(f"[✓] ÇALIŞIYOR: {proxy}")
            return proxy
    except Exception as e:
        print(f"[✗] HATALI: {proxy} ({e})")
    return None

def main():
    if not os.path.exists("http.txt"):
        print("[!] http.txt bulunamadı!")
        return

    with open("http.txt", "r") as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"[i] {len(proxies)} proxy test ediliyor...")

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_proxy, proxies)
        working_proxies = [proxy for proxy in results if proxy]

    with open("proxy.txt", "w") as f:
        f.write("\n".join(working_proxies))

    print(f"\n[+] {len(working_proxies)} çalışan proxy bulundu ve proxy.txt'ye kaydedildi!")

if __name__ == "__main__":
    print('''        .-"      "-.
       /            \\
      |,  .-.  .-.  ,|
      | )(_o/  \o_)( |
      |/     /\\     \|
      (_     ^^     _)
       \\__|IIIIII|__/
        | \\IIIIII/ |
        \\          /
         `--------`
       ~KIRA SOCIETY~''')
    main()
    input("\nÇıkmak için Enter'a basın...")
