import zipfile
import string
import itertools
import time
import os
from multiprocessing import Pool, cpu_count

# ---------------- CONFIG ----------------
SAVE_FILE = "progress.txt"

# ---------------- CORE ----------------
def try_password(args):
    zip_path, password = args
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(pwd=password.encode())
        return password
    except:
        return None


def save_progress(password):
    with open(SAVE_FILE, "w") as f:
        f.write(password)


def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return f.read().strip()
    return None


# ---------------- ATTACKS ----------------

def numeric_attack(zip_path, min_len, max_len):
    print("\n🔢 Numeric Attack (Smart Ordered)\n")

    for length in range(min_len, max_len + 1):
        for num in range(10 ** length):
            password = str(num).zfill(length)

            result = try_password((zip_path, password))
            if result:
                return result

    return None


def dictionary_attack(zip_path, wordlist):
    print("\n📚 Dictionary Attack\n")

    with open(wordlist, "r", errors="ignore") as f:
        for line in f:
            password = line.strip()

            result = try_password((zip_path, password))
            if result:
                return result

    return None


def hybrid_attack(zip_path, wordlist):
    print("\n🔀 Hybrid Attack (word + numbers)\n")

    with open(wordlist, "r", errors="ignore") as f:
        words = [w.strip() for w in f]

    for word in words:
        for num in range(10000):
            password = f"{word}{num}"

            result = try_password((zip_path, password))
            if result:
                return result

    return None


def pattern_attack(zip_path):
    print("\n📅 Pattern Attack (dates)\n")

    for day in range(1, 32):
        for month in range(1, 13):
            password = f"{day:02d}{month:02d}"

            result = try_password((zip_path, password))
            if result:
                return result

    return None


def brute_force_parallel(zip_path, charset, min_len, max_len):
    print("\n⚡ Parallel Brute Force\n")

    pool = Pool(cpu_count())

    for length in range(min_len, max_len + 1):
        combos = ("".join(p) for p in itertools.product(charset, repeat=length))

        batch = []
        for pwd in combos:
            batch.append((zip_path, pwd))

            if len(batch) >= 500:
                results = pool.map(try_password, batch)
                for res in results:
                    if res:
                        pool.terminate()
                        return res
                batch = []

    pool.close()
    pool.join()
    return None


# ---------------- MAIN ----------------

def main():
    zip_path = input("ZIP file path: ").strip()

    if not os.path.exists(zip_path):
        print("❌ File not found")
        return

    print("\nSelect attack mode:")
    print("1. Smart Numeric")
    print("2. Dictionary")
    print("3. Hybrid (word + numbers)")
    print("4. Pattern (dates)")
    print("5. Full brute force (parallel)")

    choice = input("Choice: ").strip()

    start = time.time()
    found = None

    if choice == "1":
        found = numeric_attack(zip_path, 1, 6)

    elif choice == "2":
        wl = input("Wordlist path: ")
        found = dictionary_attack(zip_path, wl)

    elif choice == "3":
        wl = input("Wordlist path: ")
        found = hybrid_attack(zip_path, wl)

    elif choice == "4":
        found = pattern_attack(zip_path)

    elif choice == "5":
        charset = string.ascii_letters + string.digits
        found = brute_force_parallel(zip_path, charset, 1, 5)

    if found:
        print(f"\n✅ PASSWORD FOUND: {found}")
        print(f"⏱ Time: {round(time.time() - start, 2)} sec")
    else:
        print("\n❌ Not found")


if __name__ == "__main__":
    main()