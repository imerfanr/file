#!/bin/bash
set -e

echo "========================================"
echo "   نصب کننده سیستم کاشف - شبح حبشی"
echo "========================================"

# بررسی Node.js
if ! command -v node &>/dev/null; then
  echo "[خطا] Node.js نصب نیست. ابتدا Node.js نسخه 18+ نصب کنید."
  exit 1
fi

echo "[موفق] Node.js یافت شد: $(node --version)"

# پوشه‌ها
mkdir -p logs data uploads backups temp

# نصب وابستگی‌ها
echo "[نصب] npm dependencies..."
npm install --production --no-optional

# دیتابیس اولیه (sqlite)
if [ ! -f ilam_mining.db ]; then
  node -e "const sqlite3 = require('sqlite3'); const db = new sqlite3.Database('ilam_mining.db'); db.close();"
fi

# ساخت جداول و کاربر پیش‌فرض
node -e "
const bcrypt = require('bcrypt');
const sqlite3 = require('sqlite3');
const db = new sqlite3.Database('ilam_mining.db');
db.serialize(() => {
  db.run(\`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'admin',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
  )\`);
  db.run(\`CREATE TABLE IF NOT EXISTS detected_miners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    mac_address TEXT,
    hostname TEXT,
    latitude REAL,
    longitude REAL,
    city TEXT,
    detection_method TEXT NOT NULL,
    suspicion_score INTEGER DEFAULT 0,
    confidence_score INTEGER DEFAULT 0,
    threat_level TEXT DEFAULT 'low',
    power_consumption REAL,
    hash_rate TEXT,
    device_type TEXT,
    process_name TEXT,
    notes TEXT,
    is_active TEXT DEFAULT 'true',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )\`);
  db.run(\`CREATE TABLE IF NOT EXISTS system_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    description TEXT,
    user_id INTEGER,
    ip_address TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
  )\`);
  const hashedPassword = bcrypt.hashSync('admin123', 10);
  db.run(\`INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', ?, 'admin')\`, [hashedPassword]);
  console.log('دیتابیس و جداول ایجاد شدند');
});
db.close();
"

# فایل .env
if [ ! -f .env ]; then
cat <<EOF > .env
NODE_ENV=production
PORT=3000
SESSION_SECRET=kashif-secret-key-change-in-production
JWT_SECRET=kashif-jwt-secret-change-in-production
DB_PATH=./ilam_mining.db
CORS_ORIGIN=*
RATE_LIMIT_WINDOW=15
RATE_LIMIT_MAX=100
LOG_LEVEL=info
LOG_FILE=./logs/kashif.log
SCAN_INTERVAL=300000
MAX_CONCURRENT_SCANS=5
EOF
fi

echo "نصب با موفقیت انجام شد."
echo "اطلاعات ورود: admin / admin123"
echo "برای اجرا: npm start"