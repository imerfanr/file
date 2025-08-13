
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
سامانه مهندسی تخصصی جامع جستجو، شناسایی، تحلیل، تشخیص، کشف و یافتن 
همه مدل و همه نوع دستگاه های استخراج و ماین رمزارزها
Compatible with all Windows versions
"""

import os
import sys
import socket
import threading
import subprocess
import re
import json
import time
import sqlite3
import math
import urllib.request
import urllib.error
from datetime import datetime
from collections import defaultdict
import concurrent.futures
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font
import webbrowser

# Try to import optional packages
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("هشدار: psutil در دسترس نیست. برخی قابلیت‌ها محدود خواهند بود.")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("هشدار: requests در دسترس نیست. از urllib استفاده می‌شود.")

# استان‌ها و شهرهای ایران
IRAN_PROVINCES = {
    'آذربایجان شرقی': {
        'center': (38.08, 46.29),
        'cities': {
            'تبریز': (38.08, 46.29),
            'مراغه': (37.39, 46.24),
            'میانه': (37.43, 47.70),
            'مرند': (38.43, 45.77),
            'اهر': (38.47, 47.07),
            'بناب': (37.34, 46.05),
            'ملکان': (37.14, 46.11),
            'سراب': (37.94, 47.98),
            'شبستر': (38.20, 45.70),
            'اسکو': (37.93, 46.12)
        }
    },
    'آذربایجان غربی': {
        'center': (37.45, 45.00),
        'cities': {
            'ارومیه': (37.53, 45.08),
            'خوی': (38.55, 44.97),
            'سلماس': (38.20, 44.77),
            'مهاباد': (36.76, 45.72),
            'بوکان': (36.52, 46.21),
            'پیرانشهر': (36.69, 45.14),
            'میاندوآب': (36.97, 46.10),
            'نقده': (37.31, 45.38),
            'چالدران': (39.05, 44.65),
            'تکاب': (36.40, 47.11)
        }
    },
    'اردبیل': {
        'center': (38.25, 48.30),
        'cities': {
            'اردبیل': (38.25, 48.30),
            'پارس‌آباد': (39.65, 47.92),
            'خلخال': (37.62, 48.52),
            'مشگین‌شهر': (38.40, 47.67),
            'گرمی': (39.01, 48.08),
            'نمین': (38.43, 48.47),
            'نیر': (38.03, 47.98),
            'کوثر': (38.30, 48.18),
            'بیله‌سوار': (39.36, 48.68),
            'رضی': (38.13, 48.12)
        }
    },
    'اصفهان': {
        'center': (32.65, 51.68),
        'cities': {
            'اصفهان': (32.65, 51.68),
            'کاشان': (33.98, 51.43),
            'نجف‌آباد': (32.63, 51.36),
            'خمینی‌شهر': (32.68, 51.52),
            'شاهین‌شهر': (32.85, 51.55),
            'فولادشهر': (32.47, 51.42),
            'مبارکه': (32.35, 51.50),
            'زرین‌شهر': (32.39, 51.38),
            'دولت‌آباد': (32.82, 51.63),
            'خوانسار': (33.21, 50.32)
        }
    },
    'ایلام': {
        'center': (33.63, 46.42),
        'cities': {
            'ایلام': (33.6374, 46.4227),
            'مهران': (33.1221, 46.1641),
            'دهلران': (32.6942, 47.2678),
            'آبدانان': (32.9928, 47.4164),
            'دره‌شهر': (33.1458, 47.3667),
            'ایوان': (33.8081, 46.2892),
            'چرداول': (33.7333, 46.8833),
            'بدره': (33.0833, 47.1167),
            'سرابله': (32.9667, 46.5833),
            'ملکشاهی': (33.3833, 46.5667),
            'شیروان چرداول': (33.9, 46.95)
        }
    },
    'البرز': {
        'center': (35.82, 50.88),
        'cities': {
            'کرج': (35.82, 50.88),
            'نظرآباد': (35.95, 50.61),
            'ساوجبلاغ': (35.57, 50.34),
            'طالقان': (36.17, 50.77),
            'فردیس': (35.73, 50.98),
            'هشتگرد': (35.96, 50.68),
            'محمدشهر': (35.80, 50.95),
            'اشتهارد': (35.72, 50.37),
            'کمال‌شهر': (35.83, 50.91),
            'مهرشهر': (35.71, 50.98)
        }
    },
    'بوشهر': {
        'center': (28.97, 50.82),
        'cities': {
            'بوشهر': (28.97, 50.82),
            'برازجان': (29.27, 50.87),
            'گناوه': (29.58, 50.52),
            'خارک': (29.26, 50.32),
            'کنگان': (27.82, 52.06),
            'عسلویه': (27.47, 52.62),
            'دیر': (27.87, 51.96),
            'جم': (27.77, 52.32),
            'دلوار': (28.72, 50.89),
            'دشتی': (28.40, 51.17)
        }
    },
    'تهران': {
        'center': (35.70, 51.42),
        'cities': {
            'تهران': (35.70, 51.42),
            'ورامین': (35.32, 51.65),
            'اسلام‌شهر': (35.53, 51.23),
            'پاکدشت': (35.48, 51.68),
            'قدس': (35.71, 51.11),
            'شهریار': (35.66, 51.04),
            'ملارد': (35.66, 50.98),
            'رباط‌کریم': (35.48, 51.08),
            'بهارستان': (35.49, 51.24),
            'نسیم‌شهر': (35.58, 51.00)
        }
    },
    'چهارمحال و بختیاری': {
        'center': (31.96, 50.84),
        'cities': {
            'شهرکرد': (32.33, 50.86),
            'بروجن': (31.96, 51.28),
            'فارسان': (32.26, 50.57),
            'لردگان': (31.52, 50.83),
            'اردل': (32.17, 50.66),
            'سامان': (32.45, 50.92),
            'گندمان': (31.60, 50.70),
            'بن': (32.04, 51.42),
            'کیان': (32.50, 50.95),
            'نافچ': (31.83, 50.89)
        }
    },
    'خراسان جنوبی': {
        'center': (32.86, 59.22),
        'cities': {
            'بیرجند': (32.86, 59.22),
            'قائن': (33.73, 59.17),
            'فردوس': (34.02, 58.17),
            'طبس': (33.60, 56.92),
            'نهبندان': (31.53, 60.02),
            'سرایان': (33.38, 58.48),
            'درمیان': (32.57, 59.70),
            'سربیشه': (32.57, 59.80),
            'بشرویه': (33.85, 57.43),
            'خوسف': (32.77, 58.65)
        }
    }
}

class ComprehensiveMinerDetector:
    def __init__(self):
        # تنظیمات پیش‌فرض
        self.selected_province = None
        self.selected_cities = []
        self.scan_range_type = "auto"  # auto, custom, province
        self.custom_ip_ranges = []
        
        # پورت‌های تشخیص ماینر
        self.miner_ports = {
            # API های ماینینگ
            4028: "CGMiner API", 4029: "SGMiner API", 4030: "BFGMiner API",
            4031: "CPUMiner API", 4032: "XMRig API", 4033: "T-Rex API",
            4034: "PhoenixMiner API", 4035: "Claymore API", 4036: "Gminer API",
            4037: "NBMiner API", 4038: "TeamRedMiner API", 4039: "lolMiner API",
            
            # رابط‌های وب
            8080: "Web Interface", 8888: "Web Interface Alt", 8081: "Miner Web UI",
            3000: "Miner Dashboard", 3001: "Mining Pool UI", 8000: "HTTP Server",
            8008: "Alternative Web", 9090: "Management Interface",
            
            # استراتوم پول‌ها
            3333: "Stratum Pool", 4444: "Stratum Pool Alt", 9999: "Stratum SSL",
            14444: "Stratum SSL Alt", 5555: "Stratum Pool", 7777: "Stratum Pool",
            8333: "Bitcoin P2P", 8332: "Bitcoin RPC", 9332: "Litecoin RPC",
            
            # پراکسی و VPN
            1080: "SOCKS Proxy", 3128: "HTTP Proxy", 8118: "Privoxy",
            9050: "Tor SOCKS", 1194: "OpenVPN", 1723: "PPTP VPN",
            
            # پورت‌های اضافی
            25: "SMTP (مشکوک)", 587: "SMTP TLS", 465: "SMTP SSL",
            21: "FTP", 22: "SSH", 23: "Telnet", 53: "DNS"
        }
        
        # فرآیندهای ماینر شناخته شده
        self.miner_processes = {
            'cgminer.exe', 'bfgminer.exe', 'sgminer.exe', 'cpuminer.exe',
            'xmrig.exe', 'xmr-stak.exe', 'claymore.exe', 'phoenixminer.exe',
            't-rex.exe', 'gminer.exe', 'nbminer.exe', 'teamredminer.exe',
            'lolminer.exe', 'miniZ.exe', 'bminer.exe', 'z-enemy.exe',
            'ccminer.exe', 'ethminer.exe', 'nanominer.exe', 'srbminer.exe',
            'wildrig.exe', 'xmrig-nvidia.exe', 'xmrig-amd.exe', 'nicehash.exe',
            'minergate.exe', 'multiminer.exe', 'bfgminer', 'cgminer'
        }
        
        # کلمات کلیدی مشکوک
        self.suspicious_keywords = [
            'miner', 'mining', 'crypto', 'bitcoin', 'ethereum', 'monero',
            'xmr', 'btc', 'eth', 'hash', 'pool', 'stratum', 'asic',
            'antminer', 'whatsminer', 'avalon', 'innosilicon', 'bitmain'
        ]
        
        # راه‌اندازی پایگاه داده
        self.init_database()

    def init_database(self):
        """راه‌اندازی پایگاه داده SQLite"""
        try:
            self.conn = sqlite3.connect('comprehensive_miners.db')
            cursor = self.conn.cursor()
            
            # جدول ماینرهای تشخیص داده شده
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detected_miners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT,
                    mac_address TEXT,
                    hostname TEXT,
                    latitude REAL,
                    longitude REAL,
                    province TEXT,
                    city TEXT,
                    detection_method TEXT,
                    device_type TEXT,
                    open_ports TEXT,
                    services TEXT,
                    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    confidence_score INTEGER,
                    threat_level TEXT,
                    notes TEXT
                )
            ''')
            
            # جدول نظارت بر فرآیندها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS process_monitoring (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_name TEXT,
                    pid INTEGER,
                    cpu_percent REAL,
                    memory_mb REAL,
                    command_line TEXT,
                    suspicious_score INTEGER,
                    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول نظارت بر شبکه
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS network_monitoring (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    local_address TEXT,
                    remote_address TEXT,
                    protocol TEXT,
                    status TEXT,
                    process_name TEXT,
                    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول گزارش‌های اسکن
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scan_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_type TEXT,
                    target_area TEXT,
                    total_scanned INTEGER,
                    suspicious_found INTEGER,
                    confirmed_miners INTEGER,
                    scan_duration INTEGER,
                    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    report_data TEXT
                )
            ''')
            
            self.conn.commit()
            print("پایگاه داده با موفقیت راه‌اندازی شد")
            
        except Exception as e:
            print(f"خطا در راه‌اندازی پایگاه داده: {e}")

    def ping_host(self, ip):
        """بررسی دسترسی به IP"""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], 
                                      capture_output=True, text=True)
            else:  # Unix/Linux
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                      capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def scan_port(self, ip, port, timeout=2):
        """اسکن یک پورت"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False

    def get_hostname(self, ip):
        """دریافت نام میزبان"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return None

    def get_mac_address(self, ip):
        """دریافت آدرس MAC"""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if ip in line:
                            parts = line.split()
                            for part in parts:
                                if '-' in part and len(part) == 17:
                                    return part.replace('-', ':')
            else:  # Unix/Linux
                result = subprocess.run(['arp', '-n'], capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if ip in line:
                            parts = line.split()
                            if len(parts) >= 3:
                                mac = parts[2]
                                if ':' in mac and len(mac) == 17:
                                    return mac
        except:
            pass
        return None

    def geolocate_ip(self, ip_address):
        """مکان‌یابی IP"""
        try:
            url = f'http://ip-api.com/json/{ip_address}?lang=fa'
            
            if REQUESTS_AVAILABLE:
                import requests
                response = requests.get(url, timeout=5)
                data = response.json()
            else:
                with urllib.request.urlopen(url, timeout=5) as response:
                    data = json.loads(response.read().decode())
            
            if data['status'] == 'success':
                location_data = {
                    'lat': float(data['lat']),
                    'lon': float(data['lon']),
                    'city': data.get('city', ''),
                    'region': data.get('regionName', ''),
                    'country': data.get('country', ''),
                    'isp': data.get('isp', ''),
                    'org': data.get('org', '')
                }
                
                # بررسی قرار گیری در استان انتخابی
                location_data['in_target_area'] = self.is_in_target_area(
                    location_data['lat'], location_data['lon'])
                
                return location_data
        except Exception as e:
            print(f"خطا در مکان‌یابی IP {ip_address}: {e}")
        
        return None

    def is_in_target_area(self, lat, lon):
        """بررسی قرار گیری در منطقه هدف"""
        if not self.selected_province:
            return True
        
        province_data = IRAN_PROVINCES.get(self.selected_province)
        if not province_data:
            return False
        
        # محاسبه فاصله تا مرکز استان
        center_lat, center_lon = province_data['center']
        distance = self.haversine(lat, lon, center_lat, center_lon)
        
        # اگر فاصله کمتر از 200 کیلومتر باشد، در محدوده استان است
        return distance < 200

    def haversine(self, lat1, lon1, lat2, lon2):
        """محاسبه فاصله بین دو نقطه"""
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # شعاع زمین بر حسب کیلومتر
        return c * r

    def monitor_processes(self):
        """نظارت بر فرآیندها"""
        suspicious_processes = []
        
        if not PSUTIL_AVAILABLE:
            print("نظارت بر فرآیندها نیاز به psutil دارد. در حال رد شدن...")
            return suspicious_processes
        
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'cmdline']):
                try:
                    proc_info = proc.info
                    process_name = proc_info['name'].lower()
                    
                    suspicion_score = 0
                    detection_reasons = []
                    
                    # بررسی فرآیندهای ماینر شناخته شده
                    if process_name in [p.lower() for p in self.miner_processes]:
                        suspicion_score += 50
                        detection_reasons.append('فرآیند ماینر شناخته شده')
                    
                    # بررسی کلمات کلیدی مشکوک
                    if any(keyword in process_name for keyword in self.suspicious_keywords):
                        suspicion_score += 30
                        detection_reasons.append('نام مشکوک')
                    
                    # بررسی استفاده از CPU
                    cpu_percent = proc_info['cpu_percent'] or 0
                    if cpu_percent > 80:
                        suspicion_score += 20
                        detection_reasons.append('استفاده بالای CPU')
                    
                    # بررسی استفاده از حافظه
                    memory_mb = proc_info['memory_info'].rss / 1024 / 1024 if proc_info['memory_info'] else 0
                    if memory_mb > 500:
                        suspicion_score += 10
                        detection_reasons.append('استفاده بالای حافظه')
                    
                    # بررسی آرگومان‌های خط فرمان
                    cmdline = ' '.join(proc_info['cmdline'] or []).lower()
                    mining_args = ['--algo', '--pool', '--user', '--pass', '--worker', 
                                 'stratum+tcp', '--cuda', '--opencl', '--intensity']
                    if any(arg in cmdline for arg in mining_args):
                        suspicion_score += 35
                        detection_reasons.append('آرگومان‌های ماینینگ')
                    
                    if suspicion_score > 20:
                        suspicious_processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cpu_percent': cpu_percent,
                            'memory_mb': memory_mb,
                            'cmdline': cmdline,
                            'suspicion_score': suspicion_score,
                            'detection_reasons': detection_reasons
                        })
                        
                        # ذخیره در پایگاه داده
                        self.save_process_to_db(proc_info, suspicion_score)
                        
                except (Exception,):
                    continue
        except Exception as e:
            print(f"خطا در نظارت بر فرآیندها: {e}")
        
        return suspicious_processes

    def advanced_device_scan(self, ip):
        """اسکن پیشرفته دستگاه"""
        if not self.ping_host(ip):
            return None
        
        device_info = {
            'ip': ip,
            'timestamp': datetime.now().isoformat(),
            'hostname': self.get_hostname(ip),
            'mac_address': self.get_mac_address(ip),
            'open_ports': [],
            'services': {},
            'suspicion_score': 0,
            'detection_methods': [],
            'geolocation': None
        }
        
        # اسکن پورت‌ها
        suspicious_ports = list(self.miner_ports.keys())
        
        def scan_single_port(port):
            if self.scan_port(ip, port, timeout=1):
                return port
            return None
        
        # اسکن همزمان پورت‌ها
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan_single_port, port) for port in suspicious_ports[:20]]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    service = self.miner_ports.get(result, "سرویس نامعلوم")
                    device_info['open_ports'].append(result)
                    device_info['services'][result] = service
                    device_info['suspicion_score'] += 25
                    device_info['detection_methods'].append(f'پورت_{result}')
        
        # تحلیل نام میزبان
        if device_info['hostname']:
            hostname = device_info['hostname'].lower()
            if any(keyword in hostname for keyword in self.suspicious_keywords):
                device_info['suspicion_score'] += 35
                device_info['detection_methods'].append('نام میزبان مشکوک')
        
        # مکان‌یابی برای دستگاه‌های مشکوک
        if device_info['suspicion_score'] > 20:
            device_info['geolocation'] = self.geolocate_ip(ip)
        
        return device_info if device_info['suspicion_score'] > 10 else None

    def scan_ip_range(self, range_base, progress_callback=None):
        """اسکن محدوده IP"""
        devices = []
        
        def update_progress(message):
            if progress_callback:
                progress_callback(message)
        
        update_progress(f"اسکن محدوده {range_base}.x...")
        
        # کشف IP های فعال
        active_ips = []
        
        def ping_ip(i):
            ip = f"{range_base}.{i}"
            if self.ping_host(ip):
                return ip
            return None
        
        # استفاده از threading برای اسکن سریع‌تر
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(ping_ip, i) for i in range(1, 255)]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    active_ips.append(result)
        
        # اسکن تفصیلی IP های فعال
        for ip in active_ips:
            update_progress(f"اسکن تفصیلی {ip}...")
            device = self.advanced_device_scan(ip)
            if device:
                devices.append(device)
        
        return devices

    def get_network_ranges(self):
        """دریافت محدوده‌های شبکه"""
        ranges = []
        
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                if result.returncode == 0:
                    output = result.stdout
                    ip_pattern = re.compile(r'IPv4 Address[.\s]*:\s*(\d+\.\d+\.\d+\.\d+)')
                    ips = ip_pattern.findall(output)
                    
                    for ip in ips:
                        if not ip.startswith('127.'):
                            ip_parts = ip.split('.')
                            network_base = '.'.join(ip_parts[:-1])
                            if network_base not in ranges:
                                ranges.append(network_base)
            else:  # Unix/Linux
                result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
                if result.returncode == 0:
                    ips = result.stdout.strip().split()
                    for ip in ips:
                        if not ip.startswith('127.'):
                            ip_parts = ip.split('.')
                            network_base = '.'.join(ip_parts[:-1])
                            if network_base not in ranges:
                                ranges.append(network_base)
        except:
            pass
        
        # افزودن محدوده‌های پیش‌فرض در صورت عدم یافت
        if not ranges:
            ranges = ['192.168.1', '192.168.0', '10.0.0', '172.16.0']
        
        return ranges

    def comprehensive_scan(self, progress_callback=None):
        """اسکن جامع"""
        def update_progress(message):
            if progress_callback:
                progress_callback(message)
            else:
                print(message)
        
        start_time = datetime.now()
        update_progress("شروع اسکن جامع...")
        
        results = {
            'timestamp': start_time.isoformat(),
            'scan_area': self.selected_province or 'همه مناطق',
            'scan_type': 'جامع',
            'network_devices': [],
            'suspicious_processes': [],
            'geolocated_miners': [],
            'statistics': {}
        }
        
        # نظارت بر فرآیندها
        update_progress("نظارت بر فرآیندها...")
        results['suspicious_processes'] = self.monitor_processes()
        
        # اسکن شبکه
        update_progress("اسکن شبکه...")
        
        if self.scan_range_type == "auto":
            ranges = self.get_network_ranges()
        elif self.scan_range_type == "custom":
            ranges = self.custom_ip_ranges
        else:  # province
            # برای اسکن استانی، از محدوده‌های عمومی استفاده می‌کنیم
            ranges = ['192.168.1', '192.168.0', '10.0.0']
        
        for range_base in ranges:
            devices = self.scan_ip_range(range_base, update_progress)
            results['network_devices'].extend(devices)
            
            # محدود کردن برای عملکرد بهتر
            if len(results['network_devices']) > 50:
                break
        
        # شناسایی ماینرهای مکان‌یابی شده
        update_progress("تحلیل مکان‌یابی...")
        for device in results['network_devices']:
            if device.get('suspicion_score', 0) > 30 and device.get('geolocation'):
                if device['geolocation'].get('in_target_area', True):
                    results['geolocated_miners'].append(device)
        
        # محاسبه آمار
        end_time = datetime.now()
        scan_duration = (end_time - start_time).total_seconds()
        
        results['statistics'] = {
            'total_devices_scanned': len(results['network_devices']),
            'suspicious_devices': len([d for d in results['network_devices'] 
                                     if d.get('suspicion_score', 0) > 20]),
            'confirmed_miners': len(results['geolocated_miners']),
            'suspicious_processes': len(results['suspicious_processes']),
            'scan_duration': int(scan_duration),
            'threat_level': self.calculate_threat_level(results)
        }
        
        # ذخیره در پایگاه داده
        update_progress("ذخیره در پایگاه داده...")
        self.save_scan_results(results)
        
        update_progress("اسکن با موفقیت تکمیل شد!")
        return results

    def calculate_threat_level(self, results):
        """محاسبه سطح تهدید"""
        confirmed = results['statistics']['confirmed_miners']
        suspicious = results['statistics']['suspicious_devices']
        processes = results['statistics']['suspicious_processes']
        
        total_threats = confirmed * 3 + suspicious * 2 + processes
        
        if total_threats == 0:
            return 'پایین'
        elif total_threats <= 5:
            return 'متوسط'
        elif total_threats <= 15:
            return 'بالا'
        else:
            return 'بحرانی'

    def save_process_to_db(self, proc_info, suspicion_score):
        """ذخیره فرآیند در پایگاه داده"""
        try:
            cursor = self.conn.cursor()
            cmdline = ' '.join(proc_info.get('cmdline', []))
            memory_mb = proc_info.get('memory_info', type('obj', (object,), {'rss': 0})).rss / 1024 / 1024
            
            cursor.execute('''
                INSERT INTO process_monitoring 
                (process_name, pid, cpu_percent, memory_mb, command_line, suspicious_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                proc_info.get('name', ''),
                proc_info.get('pid', 0),
                proc_info.get('cpu_percent', 0),
                memory_mb,
                cmdline,
                suspicion_score
            ))
            self.conn.commit()
        except Exception as e:
            print(f"خطا در ذخیره فرآیند: {e}")

    def save_scan_results(self, results):
        """ذخیره نتایج اسکن"""
        try:
            cursor = self.conn.cursor()
            
            # ذخیره ماینرهای تشخیص داده شده
            for device in results.get('geolocated_miners', []):
                geolocation = device.get('geolocation', {})
                
                cursor.execute('''
                    INSERT INTO detected_miners 
                    (ip_address, mac_address, hostname, latitude, longitude, 
                     province, city, detection_method, device_type, open_ports, 
                     services, confidence_score, threat_level, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    device['ip'],
                    device.get('mac_address', ''),
                    device.get('hostname', ''),
                    geolocation.get('lat', 0),
                    geolocation.get('lon', 0),
                    self.selected_province or '',
                    geolocation.get('city', ''),
                    ','.join(device.get('detection_methods', [])),
                    'ماینر رمزارز',
                    ','.join(map(str, device.get('open_ports', []))),
                    json.dumps(device.get('services', {}), ensure_ascii=False),
                    device.get('suspicion_score', 0),
                    results['statistics']['threat_level'],
                    json.dumps(device, ensure_ascii=False)
                ))
            
            # ذخیره گزارش اسکن
            cursor.execute('''
                INSERT INTO scan_reports 
                (scan_type, target_area, total_scanned, suspicious_found, 
                 confirmed_miners, scan_duration, report_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                results['scan_type'],
                results['scan_area'],
                results['statistics']['total_devices_scanned'],
                results['statistics']['suspicious_devices'],
                results['statistics']['confirmed_miners'],
                results['statistics']['scan_duration'],
                json.dumps(results, ensure_ascii=False)
            ))
            
            self.conn.commit()
            print("نتایج اسکن با موفقیت ذخیره شد")
            
        except Exception as e:
            print(f"خطا در ذخیره نتایج: {e}")

    def generate_html_report(self, results):
        """تولید گزارش HTML"""
        html = f'''
        <!DOCTYPE html>
        <html dir="rtl" lang="fa">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>گزارش تشخیص ماینر رمزارز</title>
            <style>
                @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v27.2.2/dist/font-face.css');
                
                body {{
                    font-family: 'B Nazanin', 'Vazir', Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                
                .header {{
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                
                .header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: bold;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                
                .header p {{
                    margin: 10px 0 0;
                    font-size: 1.2em;
                    opacity: 0.9;
                }}
                
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    padding: 30px;
                    background: #f8f9fa;
                }}
                
                .stat-card {{
                    background: white;
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                    transition: transform 0.3s ease;
                }}
                
                .stat-card:hover {{
                    transform: translateY(-5px);
                }}
                
                .stat-number {{
                    font-size: 3em;
                    font-weight: bold;
                    margin-bottom: 10px;
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }}
                
                .stat-label {{
                    font-size: 1.1em;
                    color: #666;
                    font-weight: bold;
                }}
                
                .threat-level {{
                    padding: 20px;
                    margin: 20px;
                    border-radius: 15px;
                    text-align: center;
                    font-size: 1.2em;
                    font-weight: bold;
                }}
                
                .threat-low {{ background: #d4edda; color: #155724; border: 2px solid #c3e6cb; }}
                .threat-medium {{ background: #fff3cd; color: #856404; border: 2px solid #ffeaa7; }}
                .threat-high {{ background: #f8d7da; color: #721c24; border: 2px solid #f5c6cb; }}
                .threat-critical {{ background: #f8d7da; color: #721c24; border: 2px solid #dc3545; }}
                
                .section {{
                    padding: 30px;
                }}
                
                .section h2 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                    margin-bottom: 25px;
                    font-size: 1.8em;
                }}
                
                .device-card {{
                    background: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                    margin: 15px 0;
                    padding: 20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                }}
                
                .device-high {{ border-right: 5px solid #e74c3c; }}
                .device-medium {{ border-right: 5px solid #f39c12; }}
                .device-low {{ border-right: 5px solid #f1c40f; }}
                
                .device-header {{
                    font-size: 1.3em;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 15px;
                }}
                
                .device-details {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                }}
                
                .detail-item {{
                    background: #f8f9fa;
                    padding: 10px;
                    border-radius: 8px;
                }}
                
                .detail-label {{
                    font-weight: bold;
                    color: #495057;
                    margin-bottom: 5px;
                }}
                
                .process-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                    background: white;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                
                .process-table th {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px;
                    text-align: center;
                    font-weight: bold;
                }}
                
                .process-table td {{
                    padding: 12px;
                    text-align: center;
                    border-bottom: 1px solid #e0e0e0;
                }}
                
                .process-table tr:hover {{
                    background: #f8f9fa;
                }}
                
                .map-section {{
                    background: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                }}
                
                .footer {{
                    background: #2c3e50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 گزارش تشخیص ماینر رمزارز</h1>
                    <p>تاریخ اسکن: {results['timestamp']}</p>
                    <p>منطقه هدف: {results['scan_area']}</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{results['statistics']['confirmed_miners']}</div>
                        <div class="stat-label">ماینرهای تأیید شده</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{results['statistics']['suspicious_devices']}</div>
                        <div class="stat-label">دستگاه‌های مشکوک</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{results['statistics']['suspicious_processes']}</div>
                        <div class="stat-label">فرآیندهای مشکوک</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{results['statistics']['total_devices_scanned']}</div>
                        <div class="stat-label">کل دستگاه‌های اسکن شده</div>
                    </div>
                </div>
                
                <div class="threat-level threat-{results['statistics']['threat_level'].lower()}">
                    سطح تهدید: {results['statistics']['threat_level']}
                </div>
        '''
        
        # افزودن دستگاه‌های تشخیص داده شده
        if results['network_devices']:
            html += '''
                <div class="section">
                    <h2>🖥️ دستگاه‌های تشخیص داده شده</h2>
            '''
            
            for device in results['network_devices']:
                score = device.get('suspicion_score', 0)
                if score >= 50:
                    risk_class = 'device-high'
                    risk_label = 'خطر بالا'
                elif score >= 30:
                    risk_class = 'device-medium'
                    risk_label = 'خطر متوسط'
                else:
                    risk_class = 'device-low'
                    risk_label = 'خطر پایین'
                
                geolocation = device.get('geolocation', {})
                location_info = f"{geolocation.get('city', 'نامعلوم')} ({geolocation.get('lat', 0):.4f}, {geolocation.get('lon', 0):.4f})" if geolocation else "نامعلوم"
                
                html += f'''
                    <div class="device-card {risk_class}">
                        <div class="device-header">{risk_label} - IP: {device['ip']} (امتیاز: {score})</div>
                        <div class="device-details">
                            <div class="detail-item">
                                <div class="detail-label">🖥️ نام میزبان:</div>
                                <div>{device.get('hostname', 'نامعلوم')}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">🌐 آدرس MAC:</div>
                                <div>{device.get('mac_address', 'نامعلوم')}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">🚪 پورت‌های باز:</div>
                                <div>{', '.join(map(str, device.get('open_ports', [])))}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">📍 موقعیت مکانی:</div>
                                <div>{location_info}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">🔍 روش‌های تشخیص:</div>
                                <div>{', '.join(device.get('detection_methods', []))}</div>
                            </div>
                        </div>
                    </div>
                '''
            
            html += '</div>'
        
        # افزودن فرآیندهای مشکوک
        if results['suspicious_processes']:
            html += '''
                <div class="section">
                    <h2>⚙️ فرآیندهای مشکوک</h2>
                    <table class="process-table">
                        <thead>
                            <tr>
                                <th>نام فرآیند</th>
                                <th>شناسه فرآیند</th>
                                <th>استفاده از CPU (%)</th>
                                <th>حافظه (MB)</th>
                                <th>امتیاز مشکوک</th>
                                <th>دلایل تشخیص</th>
                            </tr>
                        </thead>
                        <tbody>
            '''
            
            for proc in results['suspicious_processes']:
                html += f'''
                    <tr>
                        <td><strong>{proc.get('name', 'نامعلوم')}</strong></td>
                        <td>{proc.get('pid', 'ندارد')}</td>
                        <td>{proc.get('cpu_percent', 0):.1f}%</td>
                        <td>{proc.get('memory_mb', 0):.1f}</td>
                        <td>{proc.get('suspicion_score', 0)}</td>
                        <td>{', '.join(proc.get('detection_reasons', []))}</td>
                    </tr>
                '''
            
            html += '''
                        </tbody>
                    </table>
                </div>
            '''
        
        html += '''
                <div class="map-section">
                    <h2>🗺️ نقشه تشخیص</h2>
                    <p>برای مشاهده نقشه تعاملی، از ابزارهای GIS استفاده کنید.</p>
                </div>
                
                <div class="footer">
                    <p>سامانه مهندسی تخصصی جامع تشخیص ماینر رمزارز</p>
                    <p>تولید شده در: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        # ذخیره فایل HTML
        filename = f'گزارش_ماینر_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filename

    def close_database(self):
        """بستن اتصال پایگاه داده"""
        if hasattr(self, 'conn'):
            self.conn.close()


class ScanThread(threading.Thread):
    def __init__(self, detector, callback, progress_callback):
        threading.Thread.__init__(self)
        self.detector = detector
        self.callback = callback
        self.progress_callback = progress_callback
        self.daemon = True
        self._stop_event = threading.Event()
        
    def run(self):
        try:
            results = self.detector.comprehensive_scan(self.progress_callback)
            html_report = self.detector.generate_html_report(results)
            
            # ذخیره نتایج JSON
            json_filename = f'نتایج_اسکن_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            self.callback(results, html_report, json_filename)
            
        except Exception as e:
            import traceback
            self.progress_callback(f"خطا در اسکن: {str(e)}")
            traceback.print_exc()
    
    def stop(self):
        self._stop_event.set()


class ComprehensiveMinerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("سامانه مهندسی تخصصی جامع تشخیص ماینر رمزارز")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # تنظیم فونت فارسی
        try:
            self.farsi_font = font.Font(family="B Nazanin", size=12)
            self.farsi_font_bold = font.Font(family="B Nazanin", size=12, weight="bold")
            self.farsi_font_large = font.Font(family="B Nazanin", size=16, weight="bold")
        except:
            self.farsi_font = font.Font(family="Arial", size=12)
            self.farsi_font_bold = font.Font(family="Arial", size=12, weight="bold")
            self.farsi_font_large = font.Font(family="Arial", size=16, weight="bold")
        
        # تنظیم استایل
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # متغیرها
        self.detector = ComprehensiveMinerDetector()
        self.results = None
        self.html_report = None
        self.json_report = None
        self.scan_thread = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # کانتینر اصلی
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # عنوان
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, 
                               text="🔍 سامانه مهندسی تخصصی جامع تشخیص ماینر رمزارز", 
                               font=self.farsi_font_large)
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="شناسایی، تحلیل، تشخیص و کشف دستگاه‌های استخراج رمزارز", 
                                  font=self.farsi_font)
        subtitle_label.pack(pady=(5, 0))
        
        # پنل کنترل
        control_frame = ttk.LabelFrame(main_container, text="پنل کنترل", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # تنظیمات اسکن
        settings_frame = ttk.Frame(control_frame)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # انتخاب استان
        province_frame = ttk.Frame(settings_frame)
        province_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(province_frame, text="انتخاب استان:", font=self.farsi_font_bold).pack(side=tk.LEFT)
        
        self.province_var = tk.StringVar()
        province_combo = ttk.Combobox(province_frame, textvariable=self.province_var,
                                     values=list(IRAN_PROVINCES.keys()), state="readonly",
                                     font=self.farsi_font)
        province_combo.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        province_combo.bind('<<ComboboxSelected>>', self.on_province_selected)
        
        # نوع اسکن
        scan_type_frame = ttk.Frame(settings_frame)
        scan_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(scan_type_frame, text="نوع اسکن:", font=self.farsi_font_bold).pack(side=tk.LEFT)
        
        self.scan_type_var = tk.StringVar(value="auto")
        
        ttk.Radiobutton(scan_type_frame, text="خودکار", variable=self.scan_type_var, 
                       value="auto", font=self.farsi_font).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(scan_type_frame, text="سفارشی", variable=self.scan_type_var, 
                       value="custom", font=self.farsi_font).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(scan_type_frame, text="استانی", variable=self.scan_type_var, 
                       value="province", font=self.farsi_font).pack(side=tk.LEFT, padx=10)
        
        # دکمه‌های کنترل
        buttons_row = ttk.Frame(control_frame)
        buttons_row.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(buttons_row, text="🚀 شروع اسکن جامع", 
                                      command=self.start_scan, width=20)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(buttons_row, text="⏹️ توقف اسکن", 
                                     command=self.stop_scan, state=tk.DISABLED, width=15)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_report_button = ttk.Button(buttons_row, text="📊 باز کردن گزارش", 
                                           command=self.open_report, state=tk.DISABLED, width=15)
        self.open_report_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # نوار پیشرفت
        progress_frame = ttk.Frame(control_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(progress_frame, text="پیشرفت:", font=self.farsi_font_bold).pack(anchor=tk.W)
        
        self.progress_var = tk.StringVar(value="آماده برای اسکن...")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var, 
                                       font=self.farsi_font)
        self.progress_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # منطقه محتوای اصلی با تب‌ها
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # ایجاد تب‌ها
        self.create_dashboard_tab()
        self.create_devices_tab()
        self.create_processes_tab()
        self.create_log_tab()
        self.create_map_tab()
        self.create_settings_tab()
        
        # نوار وضعیت
        self.status_bar = ttk.Frame(main_container)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_bar, text="وضعیت: آماده", 
                                     font=self.farsi_font)
        self.status_label.pack(side=tk.LEFT)
        
        # دکمه‌های فایل
        file_buttons = ttk.Frame(self.status_bar)
        file_buttons.pack(side=tk.RIGHT)
        
        ttk.Button(file_buttons, text="💾 ذخیره نتایج", 
                  command=self.save_results, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="📁 بارگذاری نتایج", 
                  command=self.load_results, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="🗄️ پایگاه داده", 
                  command=self.view_database, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="❌ خروج", 
                  command=self.root.quit, width=8).pack(side=tk.LEFT, padx=2)

    def create_dashboard_tab(self):
        """ایجاد تب داشبورد"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="📊 داشبورد")
        
        # کارت‌های خلاصه
        summary_frame = ttk.LabelFrame(dashboard_frame, text="خلاصه اسکن", padding=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        cards_frame = ttk.Frame(summary_frame)
        cards_frame.pack(fill=tk.X)
        
        self.summary_cards = {}
        card_titles = [
            ("ماینرهای تأیید شده", "confirmed"),
            ("دستگاه‌های مشکوک", "suspicious"), 
            ("فرآیندهای مشکوک", "processes"),
            ("کل اسکن شده", "total")
        ]
        
        for i, (title, card_type) in enumerate(card_titles):
            card = ttk.LabelFrame(cards_frame, text=title, padding=10)
            card.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            cards_frame.columnconfigure(i, weight=1)
            
            value_label = ttk.Label(card, text="0", font=self.farsi_font_large)
            value_label.pack()
            
            self.summary_cards[title] = value_label
        
        # نشانگر سطح تهدید
        threat_frame = ttk.LabelFrame(dashboard_frame, text="ارزیابی تهدید", padding=10)
        threat_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.threat_level_label = ttk.Label(threat_frame, text="نامعلوم", 
                                           font=self.farsi_font_large)
        self.threat_level_label.pack()
        
        self.threat_description = ttk.Label(threat_frame, text="هنوز اسکنی انجام نشده است", 
                                           wraplength=600, font=self.farsi_font)
        self.threat_description.pack(pady=(10, 0))
        
        # آخرین تشخیص‌ها
        recent_frame = ttk.LabelFrame(dashboard_frame, text="آخرین تشخیص‌ها", padding=10)
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("IP", "نوع", "امتیاز", "زمان")
        self.recent_tree = ttk.Treeview(recent_frame, columns=columns, 
                                       show="headings", height=10)
        
        for col in columns:
            self.recent_tree.heading(col, text=col)
            self.recent_tree.column(col, width=150)
        
        recent_scrollbar = ttk.Scrollbar(recent_frame, orient="vertical", 
                                        command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=recent_scrollbar.set)
        
        self.recent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        recent_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_devices_tab(self):
        """ایجاد تب دستگاه‌های شبکه"""
        devices_frame = ttk.Frame(self.notebook)
        self.notebook.add(devices_frame, text="🖥️ دستگاه‌های شبکه")
        
        columns = ("IP", "نام میزبان", "MAC", "پورت‌ها", "امتیاز", "موقعیت")
        self.devices_tree = ttk.Treeview(devices_frame, columns=columns, show="headings")
        
        for col in columns:
            self.devices_tree.heading(col, text=col)
            self.devices_tree.column(col, width=150)
        
        devices_v_scroll = ttk.Scrollbar(devices_frame, orient="vertical", 
                                        command=self.devices_tree.yview)
        devices_h_scroll = ttk.Scrollbar(devices_frame, orient="horizontal", 
                                        command=self.devices_tree.xview)
        
        self.devices_tree.configure(yscrollcommand=devices_v_scroll.set,
                                   xscrollcommand=devices_h_scroll.set)
        
        self.devices_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        devices_v_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

    def create_processes_tab(self):
        """ایجاد تب فرآیندها"""
        processes_frame = ttk.Frame(self.notebook)
        self.notebook.add(processes_frame, text="⚙️ فرآیندها")
        
        columns = ("نام", "PID", "CPU %", "حافظه", "امتیاز", "دلایل")
        self.processes_tree = ttk.Treeview(processes_frame, columns=columns, show="headings")
        
        for col in columns:
            self.processes_tree.heading(col, text=col)
            self.processes_tree.column(col, width=120)
        
        processes_v_scroll = ttk.Scrollbar(processes_frame, orient="vertical", 
                                          command=self.processes_tree.yview)
        
        self.processes_tree.configure(yscrollcommand=processes_v_scroll.set)
        
        self.processes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        processes_v_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

    def create_log_tab(self):
        """ایجاد تب گزارش اسکن"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="📝 گزارش اسکن")
        
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(log_controls, text="پاک کردن گزارش", 
                  command=self.clear_log).pack(side=tk.LEFT)
        ttk.Button(log_controls, text="ذخیره گزارش", 
                  command=self.save_log).pack(side=tk.LEFT, padx=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, 
                                                 font=self.farsi_font)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def create_map_tab(self):
        """ایجاد تب نقشه"""
        map_frame = ttk.Frame(self.notebook)
        self.notebook.add(map_frame, text="🗺️ نقشه")
        
        map_info = ttk.Label(map_frame, 
                            text="نقشه تعاملی پس از تکمیل اسکن نمایش داده خواهد شد.\n\n"
                                 "این بخش شامل:\n"
                                 "• موقعیت دقیق ماینرهای شناسایی شده\n"
                                 "• مسیریابی و ناوبری\n"
                                 "• جزئیات هر دستگاه روی نقشه\n"
                                 "• امکان فیلتر بر اساس نوع تهدید",
                            font=self.farsi_font, justify=tk.CENTER)
        map_info.pack(expand=True)

    def create_settings_tab(self):
        """ایجاد تب تنظیمات"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ تنظیمات")
        
        # تنظیمات اسکن
        scan_settings = ttk.LabelFrame(settings_frame, text="تنظیمات اسکن", padding=10)
        scan_settings.pack(fill=tk.X, padx=10, pady=10)
        
        # محدوده شبکه
        ttk.Label(scan_settings, text="محدوده شبکه:", 
                 font=self.farsi_font_bold).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.network_range_var = tk.StringVar(value="تشخیص خودکار")
        ttk.Entry(scan_settings, textvariable=self.network_range_var, 
                 width=30, font=self.farsi_font).grid(row=0, column=1, padx=10, pady=5)
        
        # تایم اوت اسکن
        ttk.Label(scan_settings, text="تایم اوت اسکن پورت (ثانیه):", 
                 font=self.farsi_font_bold).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.timeout_var = tk.StringVar(value="2")
        ttk.Entry(scan_settings, textvariable=self.timeout_var, 
                 width=10, font=self.farsi_font).grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        # حساسیت تشخیص
        ttk.Label(scan_settings, text="حساسیت تشخیص:", 
                 font=self.farsi_font_bold).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sensitivity_var = tk.StringVar(value="متوسط")
        sensitivity_combo = ttk.Combobox(scan_settings, textvariable=self.sensitivity_var, 
                                        values=["پایین", "متوسط", "بالا"], state="readonly",
                                        font=self.farsi_font)
        sensitivity_combo.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        # تنظیمات پایگاه داده
        db_settings = ttk.LabelFrame(settings_frame, text="تنظیمات پایگاه داده", padding=10)
        db_settings.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(db_settings, text="مشاهده پایگاه داده", 
                  command=self.view_database).pack(side=tk.LEFT, padx=5)
        ttk.Button(db_settings, text="خروجی پایگاه داده", 
                  command=self.export_database).pack(side=tk.LEFT, padx=5)
        ttk.Button(db_settings, text="پاک کردن پایگاه داده", 
                  command=self.clear_database).pack(side=tk.LEFT, padx=5)

    def on_province_selected(self, event):
        """انتخاب استان"""
        self.detector.selected_province = self.province_var.get()
        self.update_log(f"استان انتخاب شده: {self.detector.selected_province}")

    def update_log(self, message):
        """به‌روزرسانی گزارش"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.progress_var.set(message)
        self.status_label.config(text=f"وضعیت: {message}")
        self.root.update_idletasks()

    def start_scan(self):
        """شروع اسکن"""
        # تنظیم نوع اسکن
        self.detector.scan_range_type = self.scan_type_var.get()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        
        # پاک کردن نتایج قبلی
        self.clear_results_display()
        
        # شروع thread اسکن
        self.scan_thread = ScanThread(self.detector, self.scan_finished, self.update_log)
        self.scan_thread.start()

    def stop_scan(self):
        """توقف اسکن"""
        if self.scan_thread and self.scan_thread.is_alive():
            self.scan_thread.stop()
            self.update_log("اسکن توسط کاربر متوقف شد")
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_bar.stop()

    def scan_finished(self, results, html_report, json_report):
        """تکمیل اسکن"""
        self.progress_bar.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.open_report_button.config(state=tk.NORMAL)
        
        self.results = results
        self.html_report = html_report
        self.json_report = json_report
        
        # به‌روزرسانی داشبورد
        self.update_dashboard(results)
        
        # به‌روزرسانی تب دستگاه‌ها
        self.update_devices_tab(results)
        
        # به‌روزرسانی تب فرآیندها
        self.update_processes_tab(results)
        
        self.update_log("اسکن با موفقیت تکمیل شد!")
        self.status_label.config(text="وضعیت: اسکن تکمیل شد")

    def update_dashboard(self, results):
        """به‌روزرسانی داشبورد"""
        if not results:
            return
        
        stats = results['statistics']
        
        # به‌روزرسانی کارت‌های خلاصه
        self.summary_cards["ماینرهای تأیید شده"].config(text=str(stats['confirmed_miners']))
        self.summary_cards["دستگاه‌های مشکوک"].config(text=str(stats['suspicious_devices']))
        self.summary_cards["فرآیندهای مشکوک"].config(text=str(stats['suspicious_processes']))
        self.summary_cards["کل اسکن شده"].config(text=str(stats['total_devices_scanned']))
        
        # به‌روزرسانی سطح تهدید
        threat_level = stats['threat_level']
        self.threat_level_label.config(text=threat_level)
        
        # رنگ‌بندی برای سطح تهدید
        threat_descriptions = {
            'پایین': 'تهدید کمی شناسایی شد. سیستم سالم به نظر می‌رسد.',
            'متوسط': 'فعالیت مشکوک شناسایی شد. بررسی توصیه می‌شود.',
            'بالا': 'تهدیدات مهمی شناسایی شد. اقدام فوری لازم است.',
            'بحرانی': 'تهدیدات بحرانی شناسایی شد. سیستم ممکن است در خطر باشد.'
        }
        
        self.threat_description.config(text=threat_descriptions.get(threat_level, 'سطح تهدید نامعلوم'))
        
        # به‌روزرسانی آخرین تشخیص‌ها
        self.recent_tree.delete(*self.recent_tree.get_children())
        
        # افزودن دستگاه‌های شبکه
        for device in results.get('network_devices', [])[:10]:
            score = device.get('suspicion_score', 0)
            if score > 20:
                self.recent_tree.insert('', 'end', values=(
                    device['ip'],
                    'دستگاه شبکه',
                    score,
                    device.get('timestamp', '')[:19]
                ))
        
        # افزودن فرآیندها
        for process in results.get('suspicious_processes', [])[:5]:
            self.recent_tree.insert('', 'end', values=(
                process.get('name', 'نامعلوم'),
                'فرآیند',
                process.get('suspicion_score', 0),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

    def update_devices_tab(self, results):
        """به‌روزرسانی تب دستگاه‌ها"""
        if not results:
            return
        
        self.devices_tree.delete(*self.devices_tree.get_children())
        
        for device in results.get('network_devices', []):
            ports_str = ', '.join(map(str, device.get('open_ports', [])))
            if len(ports_str) > 30:
                ports_str = ports_str[:30] + '...'
            
            geolocation = device.get('geolocation', {})
            location = f"{geolocation.get('city', 'نامعلوم')}" if geolocation else 'نامعلوم'
            
            self.devices_tree.insert('', 'end', values=(
                device['ip'],
                device.get('hostname', 'نامعلوم'),
                device.get('mac_address', 'نامعلوم'),
                ports_str,
                device.get('suspicion_score', 0),
                location
            ))

    def update_processes_tab(self, results):
        """به‌روزرسانی تب فرآیندها"""
        if not results:
            return
        
        self.processes_tree.delete(*self.processes_tree.get_children())
        
        for process in results.get('suspicious_processes', []):
            reasons_str = ', '.join(process.get('detection_reasons', []))
            if len(reasons_str) > 50:
                reasons_str = reasons_str[:50] + '...'
            
            self.processes_tree.insert('', 'end', values=(
                process.get('name', 'نامعلوم'),
                process.get('pid', 'ندارد'),
                f"{process.get('cpu_percent', 0):.1f}",
                f"{process.get('memory_mb', 0):.1f}",
                process.get('suspicion_score', 0),
                reasons_str
            ))

    def clear_results_display(self):
        """پاک کردن نمایش نتایج"""
        # پاک کردن داشبورد
        for card in self.summary_cards.values():
            card.config(text="0")
        
        self.threat_level_label.config(text="در حال اسکن...")
        self.threat_description.config(text="اسکن در حال انجام...")
        
        # پاک کردن درخت‌ها
        self.recent_tree.delete(*self.recent_tree.get_children())
        self.devices_tree.delete(*self.devices_tree.get_children())
        self.processes_tree.delete(*self.processes_tree.get_children())

    def open_report(self):
        """باز کردن گزارش HTML"""
        if self.html_report and os.path.exists(self.html_report):
            webbrowser.open('file://' + os.path.abspath(self.html_report))
        else:
            messagebox.showerror("خطا", "فایل گزارش یافت نشد.")

    def save_results(self):
        """ذخیره نتایج"""
        if not self.results:
            messagebox.showwarning("هشدار", "نتایجی برای ذخیره وجود ندارد.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("فایل‌های JSON", "*.json"), ("همه فایل‌ها", "*.*")],
            title="ذخیره نتایج"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.results, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("موفقیت", "نتایج با موفقیت ذخیره شد.")
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در ذخیره نتایج: {e}")

    def load_results(self):
        """بارگذاری نتایج"""
        file_path = filedialog.askopenfilename(
            filetypes=[("فایل‌های JSON", "*.json"), ("همه فایل‌ها", "*.*")],
            title="بارگذاری نتایج قبلی"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.results = json.load(f)
                
                self.update_log(f"نتایج قبلی بارگذاری شد: {file_path}")
                
                # به‌روزرسانی نمایش
                self.update_dashboard(self.results)
                self.update_devices_tab(self.results)
                self.update_processes_tab(self.results)
                
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در بارگذاری نتایج: {e}")

    def view_database(self):
        """مشاهده پایگاه داده"""
        try:
            cursor = self.detector.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM detected_miners")
            miners_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM process_monitoring")
            processes_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM scan_reports")
            reports_count = cursor.fetchone()[0]
            
            info = f"آمار پایگاه داده:\n\n"
            info += f"ماینرهای تشخیص داده شده: {miners_count}\n"
            info += f"فرآیندهای نظارت شده: {processes_count}\n"
            info += f"گزارش‌های اسکن: {reports_count}"
            
            messagebox.showinfo("پایگاه داده", info)
            
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در دسترسی به پایگاه داده: {e}")

    def export_database(self):
        """خروجی پایگاه داده"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("فایل‌های JSON", "*.json"), ("همه فایل‌ها", "*.*")],
            title="خروجی پایگاه داده"
        )
        
        if file_path:
            try:
                cursor = self.detector.conn.cursor()
                
                # استخراج همه داده‌ها
                cursor.execute("SELECT * FROM detected_miners")
                miners = [dict(zip([col[0] for col in cursor.description], row)) 
                         for row in cursor.fetchall()]
                
                cursor.execute("SELECT * FROM process_monitoring")
                processes = [dict(zip([col[0] for col in cursor.description], row)) 
                           for row in cursor.fetchall()]
                
                cursor.execute("SELECT * FROM scan_reports")
                reports = [dict(zip([col[0] for col in cursor.description], row)) 
                         for row in cursor.fetchall()]
                
                export_data = {
                    'miners': miners,
                    'processes': processes,
                    'reports': reports,
                    'export_time': datetime.now().isoformat()
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("موفقیت", "پایگاه داده با موفقیت صادر شد.")
                
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در صدور پایگاه داده: {e}")

    def clear_database(self):
        """پاک کردن پایگاه داده"""
        if messagebox.askyesno("تأیید", "آیا از پاک کردن کامل پایگاه داده اطمینان دارید؟"):
            try:
                cursor = self.detector.conn.cursor()
                cursor.execute("DELETE FROM detected_miners")
                cursor.execute("DELETE FROM process_monitoring")
                cursor.execute("DELETE FROM network_monitoring")
                cursor.execute("DELETE FROM scan_reports")
                self.detector.conn.commit()
                
                messagebox.showinfo("موفقیت", "پایگاه داده با موفقیت پاک شد.")
                
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در پاک کردن پایگاه داده: {e}")

    def clear_log(self):
        """پاک کردن گزارش"""
        self.log_text.delete(1.0, tk.END)

    def save_log(self):
        """ذخیره گزارش"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("فایل‌های متنی", "*.txt"), ("همه فایل‌ها", "*.*")],
            title="ذخیره گزارش"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("موفقیت", "گزارش با موفقیت ذخیره شد.")
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در ذخیره گزارش: {e}")


def main():
    """تابع اصلی"""
    # بررسی نسخه پایتون
    if sys.version_info.major < 3:
        print("خطا: این برنامه نیاز به پایتون 3 دارد.")
        input("برای خروج Enter بزنید...")
        return
    
    print("راه‌اندازی سامانه مهندسی تخصصی جامع تشخیص ماینر رمزارز...")
    print("=" * 70)
    
    try:
        root = tk.Tk()
        app = ComprehensiveMinerGUI(root)
        
        # تنظیم رنگ و ظاهر
        root.configure(bg='#f0f0f0')
        
        # شروع حلقه اصلی
        root.mainloop()
        
    except Exception as e:
        print(f"خطا در راه‌اندازی برنامه: {e}")
        import traceback
        traceback.print_exc()
        input("برای خروج Enter بزنید...")


if __name__ == "__main__":
    main()
