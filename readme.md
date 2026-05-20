# 🔓 ZIP Cracker Pro (Python)

A multi-strategy ZIP password recovery tool built in Python.  
Supports **both Standard ZIP and AES-encrypted ZIP (WinRAR / 7zip / Ubuntu)**.

---

## 📌 Overview

This tool attempts to recover passwords from protected `.zip` files using multiple techniques:

- Smart numeric brute-force (optimized for PIN-style passwords)
- Dictionary-based attacks
- Hybrid attacks (word + numbers)
- Pattern-based attacks (dates, common formats)
- Parallel brute-force (multi-core CPU)

✅ Works with:
- Standard ZIP (ZipCrypto)
- AES-encrypted ZIP (Ubuntu / WinRAR / 7zip)

---

## ⚙️ Features

- ✔ Accurate password validation (no false positives)
- ✔ AES ZIP support (via `pyzipper`)
- ✔ Smart attack ordering (fast real-world cracking)
- ✔ Multi-core brute-force
- ✔ Live progress tracking
- ✔ Safe memory usage (stream-based validation)

---

## 📦 Requirements

- Python 3.10+
- pip (or pipx)
- OS: Linux / macOS / Windows

---

## 📂 Installation (IMPORTANT ⚠️)

### 🔥 Ubuntu / Debian (Recommended Method)

Due to **PEP 668**, you MUST use a virtual environment.

### Step 1: Install venv
```bash
sudo apt install python3-venv -y
````

### Step 2: Clone project

```bash
git clone https://github.com/SabbirFTP/zip-cracker-pro.git
cd zip-cracker-pro
```

### Step 3: Create virtual environment

```bash
python3 -m venv venv
```

### Step 4: Activate environment

```bash
source venv/bin/activate
```

👉 You should now see:

```
(venv) user@machine:
```

### Step 5: Install dependencies

```bash
pip install pyzipper
```

---

### ⚡ Alternative (Quick but NOT recommended)

```bash
pip install pyzipper --break-system-packages
```

---

## ▶️ Usage

```bash
python zip_cracker_pro.py
```

---

## 🧠 Attack Modes Explained

### 1. 🔢 Smart Numeric (Recommended First)

Best for:

* PINs
* Dates
* Short numeric passwords

Example:

```
Min length: 1
Max length: 4
```

---

### 2. 📚 Dictionary Attack

Requires:

```
Wordlist path: /path/to/wordlist.txt
```

Recommended:

* rockyou.txt

---

### 3. 🔀 Hybrid Attack

Combines:

```
[word] + [0000 → 9999]
```

Examples:

* admin123
* sabbir2026

---

### 4. 📅 Pattern Attack

Targets:

* Date-based passwords

Examples:

* 0616
* 2501
* 3112

---

### 5. ⚡ Parallel Brute Force

* Uses all CPU cores
* Full charset (a-z, A-Z, 0-9)
* Slow but exhaustive

---

## 📊 Output & Progress

Example:

```
Trying: 0616 | 6.16% | 1200 pwd/sec | Attempts: 616
```

---

## ⚡ Performance Strategy (IMPORTANT)

Always follow:

1. Smart Numeric
2. Pattern Attack
3. Dictionary
4. Hybrid
5. Brute Force (last)

---

## 🔍 How It Works (Technical)

Instead of extracting full files, the tool:

```python
zf.open(file, pwd=password).read(1)
```

✔ Forces real decryption
✔ Prevents false positives
✔ Works for AES + standard ZIP

---

## 🔐 AES ZIP Support

Modern tools (Ubuntu Archive Manager, WinRAR, 7zip) use **AES encryption**.

Standard Python `zipfile`:
❌ Cannot handle AES properly

This tool uses:

```
pyzipper
```

✔ Enables AES decryption
✔ Ensures correct password validation

---

## 🛑 Limitations

* Python is slower than:

  * hashcat (GPU)
  * fcrackzip (C-based)

* AES ZIP cracking is significantly slower

---

## 🧪 Tested On

* Ubuntu (Archive Manager ZIP)
* WinRAR encrypted ZIP
* 7zip AES ZIP

---

## 🔐 Security Note

* Runs locally (safe for sensitive data)
* No external API calls
* No file uploads

---

## ⚠️ Disclaimer

Use only for:

* Your own files
* Authorized recovery

Do NOT use for unauthorized access.

---

## 🚀 Future Improvements

* CLI flags (non-interactive mode)
* Resume per attack mode
* GPU acceleration (hashcat bridge)
* Smart password ranking
* Distributed cracking

---

## 👨‍💻 Author

Built for developers who:

* forget passwords 😄
* want control over cracking process
* prefer transparent tools over black-box software

---

## 💬 Final Note

If your password is:

* ≤6 characters → HIGH success rate
* Pattern-based → VERY fast recovery
* Strong/random → use hashcat

---