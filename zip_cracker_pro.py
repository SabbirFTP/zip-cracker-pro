import zipfile
import string
import itertools
import time
import os
from multiprocessing import Pool, cpu_count

# ---------------- CONFIG ----------------
SAVE_FILE = "progress.txt"
PROGRESS_INTERVAL = 500

# ---------------- CORE ----------------
def try_password_fast(zip_file, password):
    try:
        zip_file.extractall(pwd=password.encode())
        return True
    except:
        return False


def save_progress(password):
    with open(SAVE_FILE, "w") as f:
        f.write(password)


def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return f.read().strip()
    return None


# ---------------- ATTACKS ----------------

def numeric_attack(zip_file, min_len, max_len):
    print("\n🔢 Numeric Attack (Smart Ordered)\n")

    attempts = 0
    start = time.time()

    for length in range(min_len, max_len + 1):
        total = 10 ** length
        print(f"\n👉 Trying length {length} (Total: {total})")

        for num in range(total):
            password = str(num).zfill(length)
            attempts += 1

            if attempts % PROGRESS_INTERVAL == 0:
                elapsed = time.time() - start
                speed = attempts / elapsed if elapsed else 0
                percent = (num / total) * 100

                print(
                    f"Trying: {password} | "
                    f"{percent:.2f}% | "
                    f"{speed:.0f} pwd/sec | "
                    f"Attempts: {attempts}",
                    end="\r"
                )

            if try_password_fast(zip_file, password):
                print(f"\n\n✅ FOUND (numeric): {password}")
                print(f"Attempts: {attempts}")
                print(f"Time: {round(time.time() - start, 2)} sec")
                return password

    return None


def dictionary_attack(zip_file, wordlist):
    print("\n📚 Dictionary Attack\n")

    attempts = 0
    start = time.time()

    with open(wordlist, "r", errors="ignore") as f:
        for line in f:
            password = line.strip()
            attempts += 1

            if attempts % PROGRESS_INTERVAL == 0:
                elapsed = time.time() - start
                speed = attempts / elapsed if elapsed else 0
                print(
                    f"Trying: {password} | {speed:.0f} pwd/sec | Attempts: {attempts}",
                    end="\r"
                )

            if try_password_fast(zip_file, password):
                print(f"\n\n✅ FOUND (dictionary): {password}")
                return password

    return None


def hybrid_attack(zip_file, wordlist):
    print("\n🔀 Hybrid Attack (word + numbers)\n")

    attempts = 0
    start = time.time()

    with open(wordlist, "r", errors="ignore") as f:
        words = [w.strip() for w in f]

    for word in words:
        for num in range(10000):
            password = f"{word}{num}"
            attempts += 1

            if attempts % PROGRESS_INTERVAL == 0:
                elapsed = time.time() - start
                speed = attempts / elapsed if elapsed else 0
                print(
                    f"Trying: {password} | {speed:.0f} pwd/sec | Attempts: {attempts}",
                    end="\r"
                )

            if try_password_fast(zip_file, password):
                print(f"\n\n✅ FOUND (hybrid): {password}")
                return password

    return None


def pattern_attack(zip_file):
    print("\n📅 Pattern Attack (dates like 0616)\n")

    attempts = 0
    start = time.time()

    for day in range(1, 32):
        for month in range(1, 13):
            password = f"{day:02d}{month:02d}"
            attempts += 1

            print(f"Trying: {password}", end="\r")

            if try_password_fast(zip_file, password):
                print(f"\n\n✅ FOUND (pattern): {password}")
                return password

    return None


def brute_force_parallel(zip_path, charset, min_len, max_len):
    print("\n⚡ Parallel Brute Force\n")

    def worker(password):
        try:
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(pwd=password.encode())
            return password
        except:
            return None

    pool = Pool(cpu_count())

    for length in range(min_len, max_len + 1):
        print(f"\n👉 Length {length}")

        combos = ("".join(p) for p in itertools.product(charset, repeat=length))

        batch = []
        for pwd in combos:
            batch.append(pwd)

            if len(batch) >= 500:
                results = pool.map(worker, batch)

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

    zip_file = zipfile.ZipFile(zip_path)

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
        min_len = int(input("Min length: "))
        max_len = int(input("Max length: "))
        found = numeric_attack(zip_file, min_len, max_len)

    elif choice == "2":
        wl = input("Wordlist path: ")
        found = dictionary_attack(zip_file, wl)

    elif choice == "3":
        wl = input("Wordlist path: ")
        found = hybrid_attack(zip_file, wl)

    elif choice == "4":
        found = pattern_attack(zip_file)

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