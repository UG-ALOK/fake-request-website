import concurrent.futures
import sys
import time
import requests

# Light Gold & Premium ANSI Color Codes
RST = "\033[0m"
BOLD = "\033[1m"
LIGHT_GOLD = "\033[93m"
BRIGHT_GOLD = "\033[38;5;220m"
NEON_PINK = "\033[38;5;201m"
BLOOD_RED = "\033[91m"
DARK_GRAY = "\033[90m"


def print_banner():
  banner = f"""
{LIGHT_GOLD}{BOLD}╔══════════════════════════════════════════╗
║ {BRIGHT_GOLD}   HTTP LOAD BENCHMARKER // CLI UTILITY   {LIGHT_GOLD}║
╚══════════════════════════════════════════╝
{BRIGHT_GOLD}   [ - Performance & Concurrency Testing ]{RST}
{DARK_GRAY}──────────────────────────────────────────{RST}
"""
  print(banner)


def elite_loader():
  frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
  for _ in range(6):
    for frame in frames:
      sys.stdout.write(
          f"\r{LIGHT_GOLD}{BOLD}[⚙️] PROCESSING {frame}{RST}"
      )
      sys.stdout.flush()
      time.sleep(0.05)
  print("\n")


def send_request(url, worker_id):
  try:
    headers = {"User-Agent": f"Benchmarker-Worker-{worker_id}"}
    response = requests.get(url, headers=headers, timeout=3)
    return response.status_code
  except requests.exceptions.RequestException:
    return None


def main_console():
  while True:
    print_banner()
    print(f" {LIGHT_GOLD}[1]{RST} {BRIGHT_GOLD} Start Benchmark{RST}")
    print(f" {BLOOD_RED}[2]{RST} {LIGHT_GOLD}Exit{RST}")
    print(f"{DARK_GRAY}──────────────────────────────────────────{RST}")

    choice = input(
        f"{LIGHT_GOLD}{BOLD}BENCHMARK ❯❯{RST} {BRIGHT_GOLD}Select (1-2): {RST}"
    ).strip()

    if choice == "1":
      print(f"\n{NEON_PINK}--- CONFIGURATION ---{RST}")
      target_url = input(f"{LIGHT_GOLD}Target URL: {RST}").strip()

      if not target_url:
        print(f"{BLOOD_RED}[✖] URL required!{RST}")
        continue

      try:
        workers = int(input(f"{LIGHT_GOLD}Workers (1-1000): {RST}").strip())
        if not (1 <= workers <= 1000):
          print(f"{BLOOD_RED}[✖] Range: 1 to 1000!{RST}")
          continue
      except ValueError:
        print(f"{BLOOD_RED}[✖] Integer only!{RST}")
        continue

      print(
          f"\n{LIGHT_GOLD}[✔] Target: {target_url}\n{LIGHT_GOLD}[✔] Workers:"
          f" {workers}{RST}"
      )

      elite_loader()

      print(f"{LIGHT_GOLD}[⚡] EXECUTING BENCHMARK...\n{RST}")
      success_hits = 0
      failed_hits = 0
      start_time = time.time()

      try:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(workers, 100)
        ) as executor:
          futures = [
              executor.submit(send_request, target_url, worker_id)
              for worker_id in range(1, workers + 1)
          ]

          for future in concurrent.futures.as_completed(futures):
            status = future.result()
            if status:
              success_hits += 1
              print(f"{LIGHT_GOLD}[HIT] Status: {status}{RST}")
            else:
              failed_hits += 1
              print(f"{BLOOD_RED}[DROP] Failed{RST}")

      except KeyboardInterrupt:
        print(f"\n{BLOOD_RED}[!] Aborted.{RST}")

da      total_time = time.time() - start_time

      print("\n" + "═" * 42)
      print(f"{BRIGHT_GOLD}            REPORT SUMMARY{RST}")
      print("═" * 42)
      print(f" Target   : {target_url}")
      print(f" Workers  : {workers}")
      print(f" Success  : {success_hits}")
      print(f" Failed   : {failed_hits}")
      print(f" Time     : {total_time:.2f}s")
      print("═" * 42)

      input(f"\n{LIGHT_GOLD}Press [Enter] to continue...{RST}")

    elif choice == "2":
      print(f"{BLOOD_RED}[✖] Exiting.{RST}")
      break
    else:
      print(f"{BLOOD_RED}[!] Select 1 or 2.{RST}")


if __name__ == "__main__":
  main_console()
