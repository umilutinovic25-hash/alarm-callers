#!/usr/bin/env python3
"""
Loop Caller – koristi FaceTime/iPhone (bez Twilio)
Pokreni: python3 loop_caller.py
"""

import subprocess
import time
import sys

# ─── PODEŠAVANJA ──────────────────────────────────────────────
MOJ_BROJ      = "+381613006524"   # broj koji će biti pozvan
BROJ_POKUSAJA = 10                # koliko puta da zove
TRAJANJE      = 20                # sekundi pre prekida poziva
PAUZA         = 30                # sekundi između poziva
# ──────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
GRAY   = "\033[90m"

def print_header():
    print(f"\n{BOLD}{CYAN}{'─' * 50}{RESET}")
    print(f"{BOLD}{CYAN}   📞 Loop Caller (FaceTime){RESET}")
    print(f"{CYAN}{'─' * 50}{RESET}")
    print(f"  {GRAY}Do:      {RESET}{MOJ_BROJ}")
    print(f"  {GRAY}Poziva:  {RESET}{BROJ_POKUSAJA}x  |  Trajanje: {TRAJANJE}s  |  Pauza: {PAUZA}s")
    print(f"{CYAN}{'─' * 50}{RESET}\n")

def progress_bar(done, total, width=30):
    filled = int(width * done / total)
    bar = "█" * filled + "░" * (width - filled)
    pct = int(100 * done / total)
    return f"[{bar}] {pct:3d}%  ({done}/{total})"

def hangup():
    subprocess.run(["osascript", "-e", """
        tell application "System Events"
            if exists process "FaceTime" then
                tell process "FaceTime"
                    keystroke "w" using command down
                end tell
            end if
        end tell
    """], capture_output=True)

def call(number):
    subprocess.run(["open", f"tel://{number}"])

def main():
    print_header()
    uspesnih = 0

    try:
        for i in range(BROJ_POKUSAJA):
            ts = time.strftime("%H:%M:%S")
            print(f"  {GRAY}[{ts}]{RESET}  Poziv {BOLD}{i+1}/{BROJ_POKUSAJA}{RESET} → {MOJ_BROJ} ... ", end="", flush=True)

            try:
                call(MOJ_BROJ)
                time.sleep(TRAJANJE)
                hangup()
                print(f"{GREEN}✓ okoncano{RESET}")
                uspesnih += 1
            except Exception as e:
                print(f"{RED}✗ Greška: {e}{RESET}")

            prog = progress_bar(i + 1, BROJ_POKUSAJA)
            print(f"  {GRAY}{prog}{RESET}")

            if i < BROJ_POKUSAJA - 1:
                print(f"  {YELLOW}⏳ Čekam {PAUZA}s...{RESET}", end="\r", flush=True)
                time.sleep(PAUZA)
                print(" " * 40, end="\r")

    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}⚠  Prekinuto (Ctrl+C){RESET}")
        hangup()

    print(f"\n{CYAN}{'─' * 50}{RESET}")
    print(f"{BOLD}  Završeno:{RESET}  {GREEN}{uspesnih}{RESET}/{BROJ_POKUSAJA} poziva")
    print(f"{CYAN}{'─' * 50}{RESET}\n")

if __name__ == "__main__":
    main()
