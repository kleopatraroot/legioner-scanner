import socket
import threading
import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor

class LegionerTool:
    def __init__(self):
        self.version = "2.0"
        
    def show_banner(self):
        banner = """
╔══════════════════════════════════════════════╗
║               LEGIONER v1.0                  ║
║              Internet Scanner                ║
╚══════════════════════════════════════════════╝
        """
        print(banner)
    
    def show_menu(self):
        menu = """
ВЫБЕРИТЕ ТИП СКАНИРОВАНИЯ:

1.  Port Scanner
2.  WebSite Scanner
3.  Info in system
0.  ВЫХОД

Выберите опцию: """
        return input(menu)

    def mega_port_scan(self):
        target = input("Введите IP или домен: ").strip()
        
        try:
            ip = socket.gethostbyname(target)
            print(f" Цель: {target} [{ip}]")
            print(" Запуск мега скана...")
            
           
            ports = list(range(1, 501))
            open_ports = []
            
            def scan_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        try:
                            service = socket.getservbyport(port)
                        except:
                            service = "unknown"
                        print(f" Порт {port} открыт - {service}")
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
            
            
            print(" Сканирование портов...")
            with ThreadPoolExecutor(max_workers=200) as executor:
                executor.map(scan_port, ports)
            
            print(f"\n Найдено открытых портов: {len(open_ports)}")
            if open_ports:
                print(" Открытые порты:", sorted(open_ports))
                
        except Exception as e:
            print(f" Ошибка: {e}")
        
        input("\nНажмите Enter чтобы продолжить...")

    def website_scan(self):
        target = input("Введите URL сайта: ").strip()
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
            
        print(f" Сканирование: {target}")
        
        try:
            response = requests.get(target, timeout=10, verify=False)
            print(f" Сайт доступен. Статус: {response.status_code}")
            print(f" Сервер: {response.headers.get('Server', 'Неизвестно')}")
            
           
            security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 'Strict-Transport-Security']
            for header in security_headers:
                if header in response.headers:
                    print(f" {header}: {response.headers[header]}")
                else:
                    print(f" {header}: Отсутствует")
                    
        except Exception as e:
            print(f" Ошибка: {e}")
        
        input("\nНажмите Enter чтобы продолжить...")

    def system_info(self):
        print(" ИНФОРМАЦИЯ О СИСТЕМЕ:")
        print("=" * 40)
        
        try:
            print(f" Имя компьютера: {socket.gethostname()}")
            print(f" Рабочая папка: {os.getcwd()}")
            print(f" Процессоров: {os.cpu_count()}")
            
            
            hostname = socket.gethostname()
            try:
                ip = socket.gethostbyname(hostname)
                print(f" Локальный IP: {ip}")
            except:
                print(" IP: Не определен")
                
        except Exception as e:
            print(f" Ошибка: {e}")
        
        input("\nНажмите Enter чтобы продолжить...")

    def run(self):
        self.show_banner()
        
        while True:
            try:
                choice = self.show_menu()
                
                if choice == '1':
                    self.mega_port_scan()
                elif choice == '2':
                    self.website_scan()
                elif choice == '3':
                    self.system_info()
                elif choice == '0':
                    print(" Завершение работы...")
                    break
                else:
                    print(" Неверный выбор!")
                    input("Нажмите Enter чтобы продолжить...")
                
                os.system('cls' if os.name == 'nt' else 'clear')
                
            except KeyboardInterrupt:
                print("\n Программа прервана")
                break
            except Exception as e:
                print(f" Критическая ошибка: {e}")
                input("Нажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    tool = LegionerTool()
    tool.run()