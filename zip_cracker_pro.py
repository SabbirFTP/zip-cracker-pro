import zipfile
import pyzipper
import string
import itertools
import time
import os
from multiprocessing import Pool, cpu_count

# ---------------- CONFIG ----------------
SAVE_FILE = "progress.txt"
PROGRESS_INTERVAL = 500
BATCH_SIZE = 500

# ---------------- CORE ----------------

def is_aes_zip(zip_path):
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            return any(zinfo.flag_bits & 0x1 for zinfo in zf.infolist())
    except:
        return False


def try_password(zip_path, password):
    password_bytes = password.encode()

    # Try AES first
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            name = zf.namelist()[0]
            with zf.open(name, pwd=password_bytes) as f:
                f.read(1)
        return True
    except:
        pass

    # Fallback to standard ZIP
    try:
        with zipfile.ZipFile(zip_path) as zf:
            name = zf.namelist()[0]
            with zf.open(name, pwd=password_bytes) as f:
                f.read(1)
        return True
    except:
        return False


def worker(args):
    zip_path, password = args
    if try_password(zip_path, password):
        return password
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
                    f"Trying: {password} | {percent:.2f}% | "
                    f"{speed:.0f} pwd/sec | Attempts: {attempts}",
                    end="\r",
                    flush=True
                )

            if try_password(zip_path, password):
                print(f"\n\n✅ FOUND (numeric): {password}")
                return password

    return None


def dictionary_attack(zip_path, wordlist):
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
                    end="\r",
                    flush=True
                )

            if try_password(zip_path, password):
                print(f"\n\n✅ FOUND (dictionary): {password}")
                return password

    return None


def hybrid_attack(zip_path, wordlist):
    print("\n🔀 Hybrid Attack\n")

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
                    end="\r",
                    flush=True
                )

            if try_password(zip_path, password):
                print(f"\n\n✅ FOUND (hybrid): {password}")
                return password

    return None


def pattern_attack(zip_path):
    print("\n📅 Pattern Attack\n")

    for day in range(1, 32):
        for month in range(1, 13):
            password = f"{day:02d}{month:02d}"

            print(f"Trying: {password}", end="\r", flush=True)

            if try_password(zip_path, password):
                print(f"\n\n✅ FOUND (pattern): {password}")
                return password

    return None


def brute_force_parallel(zip_path, charset, min_len, max_len):
    print("\n⚡ Parallel Brute Force\n")

    attempts = 0
    start = time.time()

    pool = Pool(cpu_count())

    for length in range(min_len, max_len + 1):
        print(f"\n👉 Length {length}")

        generator = ("".join(p) for p in itertools.product(charset, repeat=length))

        while True:
            batch = list(itertools.islice(generator, BATCH_SIZE))
            if not batch:
                break

            tasks = [(zip_path, pwd) for pwd in batch]
            results = pool.map(worker, tasks)

            for pwd, res in zip(batch, results):
                attempts += 1

                if attempts % PROGRESS_INTERVAL == 0:
                    elapsed = time.time() - start
                    speed = attempts / elapsed if elapsed else 0

                    print(
                        f"[Len {length}] {pwd} | {speed:.0f} pwd/sec | Attempts: {attempts}",
                        end="\r",
                        flush=True
                    )

                if res:
                    pool.terminate()
                    pool.join()
                    print(f"\n\n✅ FOUND (brute): {res}")
                    return res

    pool.close()
    pool.join()
    return None


# ---------------- MAIN ----------------

def main():
    print("\n[ ZC ] Initializing Zip Cracker Pro...\n")

    zip_path = input("ZIP file path: ").strip()

    if not os.path.exists(zip_path):
        print("❌ File not found")
        return

    print("\nSelect attack mode:")
    print("1. Smart Numeric")
    print("2. Dictionary")
    print("3. Hybrid")
    print("4. Pattern")
    print("5. Full brute force (parallel)")

    choice = input("Choice: ").strip()

    start = time.time()
    found = None

    if choice == "1":
        min_len = int(input("Min length: "))
        max_len = int(input("Max length: "))
        found = numeric_attack(zip_path, min_len, max_len)

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
        found = brute_force_parallel(zip_path, charset, 1, 6)

    if found:
        print(f"\n✅ PASSWORD FOUND: {found}")
        print(f"⏱ Time: {round(time.time() - start, 2)} sec")
    else:
        print("\n❌ Not found")


if __name__ == "__main__":
    main()