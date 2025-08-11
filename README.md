# نصب و اجرای سیستم کشف ماینر (کاشف شبح حبشی)

## پیش‌نیازها
- Node.js 18+
- Python 3.10+
- npm
- git

## نصب و اجرا
```sh
git clone <REPO_URL>
cd <project-folder>
npm install
cd client
npm install
cd ..
npm run setup
npm run dev
```

## دسترسی به داشبورد
آدرس: [http://localhost:3000](http://localhost:3000)
ورود اولیه:  
user: admin  
pass: admin123

## اجرای اسکنرها
```sh
python miner_hunter.py --targets 192.168.100.0/24 --ble --wifi --rf --snmp
```

## خروجی و گزارش
گزارش‌ها در داشبورد و فایل export قابل دانلود است.

## نکات امنیتی
پس از نصب، رمز admin را تغییر دهید.