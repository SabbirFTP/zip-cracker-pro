
# 🔓 ZIP Cracker Pro (Python)

A multi-strategy ZIP password recovery tool built in Python.  
Designed for **real-world recovery scenarios** using smart attack patterns instead of blind brute force.

---

## 📌 Overview

This tool attempts to recover passwords from protected `.zip` files using multiple techniques:

- Smart numeric brute-force (optimized for PIN-style passwords)
- Dictionary-based attacks
- Hybrid attacks (word + numbers)
- Pattern-based attacks (dates, common formats)
- Parallel brute-force (multi-core CPU)

It is **not meant to compete with GPU tools like hashcat**, but is highly effective for:
- Short passwords
- Human-pattern passwords
- Known formats (dates, PINs, common words)

---

## ⚙️ Features

### 🔢 Smart Numeric Attack
- Tries numbers in order: `0001 → 9999`
- Preserves leading zeros (`0616`)
- Extremely fast for PIN-style passwords

---

### 📚 Dictionary Attack
- Uses a wordlist file (e.g. `rockyou.txt`)
- Best for common passwords

---

### 🔀 Hybrid Attack
- Combines wordlist + numbers
- Examples:
  - `admin123`
  - `test2024`

---

### 📅 Pattern Attack
- Targets date-based passwords
- Examples:
  - `0616`
  - `2501`
  - `3112`

---

### ⚡ Parallel Brute Force
- Uses all CPU cores
- Tries full charset combinations
- Slow but exhaustive

---

## 📦 Requirements

- Python 3.x
- Linux / macOS / Windows (tested on Ubuntu)

---

## 📂 Installation

```bash
git clone https://github.com/SabbirFTP/zip-cracker-pro.git
cd zip-cracker-pro
python3 zip_cracker_pro.py
````

Or simply run the script directly if downloaded.

---

## ▶️ Usage

```bash
python3 zip_cracker_pro.py
```

You will be prompted:

```text
ZIP file path:
Select attack mode:
```

---

## 🧠 Attack Modes Explained

### 1. Smart Numeric (Recommended First)

Best for:

* PINs
* Dates
* Short numeric passwords

Example input:

```text
Min length: 1
Max length: 4
```

👉 If password = `0616`, it will be found around attempt ~616

---

### 2. Dictionary Attack

Requires:

```text
Wordlist path: /path/to/wordlist.txt
```

Recommended wordlists:

* `rockyou.txt`

---

### 3. Hybrid Attack

Combines:

```
[word] + [0000 → 9999]
```

Examples:

* `sabbir123`
* `admin2024`

---

### 4. Pattern Attack

Predefined patterns:

* DDMM (day-month)

Examples:

* `0616`
* `2501`

👉 Fastest for human-created passwords

---

### 5. Parallel Brute Force

* Uses:

  * letters + numbers
* Multi-core processing
* Very slow for large ranges

Use only if all other methods fail.

---

## 📊 Output & Progress

During execution, you will see:

```text
Trying: 0616 | 6.16% | 1200 pwd/sec | Attempts: 616
```

Meaning:

* Current password attempt
* Progress %
* Speed (passwords/sec)
* Total attempts

---

## ⚡ Performance Tips

### ✅ Always follow this order:

1. Smart Numeric
2. Pattern Attack
3. Dictionary
4. Hybrid
5. Brute Force (last)

---

### 🚀 Speed Optimization

* Keep password length range small
* Use targeted charset when possible
* Avoid full brute force unless necessary

---

## 🛑 Limitations

* Python is slower than:

  * `hashcat` (GPU)
  * `fcrackzip` (C-based)

* AES-encrypted ZIPs are significantly slower to crack

---

## 🔐 Security Note

* Do NOT upload sensitive ZIP files to online tools
* This script runs locally → safer for private data

---

## ⚠️ Disclaimer

This tool is intended for:

* Recovering your own forgotten passwords
* Educational purposes

Do not use it on files without proper authorization.

---

## 🚀 Future Improvements

* GPU acceleration (hashcat integration)
* Smart pattern learning (AI-based guessing)
* Resume from last checkpoint
* Custom mask attack support

---

## 👨‍💻 Author

Built for practical use by developers who:

* forget passwords 😄
* prefer control over black-box tools

---

## 💬 Final Note

If your password is:

* Short (≤6 chars) → this tool is effective
* Pattern-based → very fast recovery
* Strong/random → use **hashcat**

```