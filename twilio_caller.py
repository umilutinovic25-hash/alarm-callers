#!/usr/bin/env python3
"""
Twilio Alarm Caller – terminal verzija
Pokreni: python3 twilio_caller.py
"""

from twilio.rest import Client
import time
import sys

# ─── PODEŠAVANJA ──────────────────────────────────────────────
ACCOUNT_SID  = "ACxxxxxxxxxxxxxxxx"
AUTH_TOKEN   = "xxxxxxxxxxxxxxxx"
TWILIO_BROJ  = "+1XXXXXXXXXX"   # tvoj Twilio broj
MOJ_BROJ     = "+381XXXXXXXXX"  # broj koji će biti pozvan

BROJ_POKUSAJA = 10   # koliko puta da zove
PAUZA         = 30   # sekundi između poziva
TIMEOUT       = 20   # sekundi pre auto prekida
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
    print(f"{BOLD}{CYAN}   📞 Twilio Alarm Caller{RESET}")
    print(f"{CYAN}{'─' * 50}{RESET}")
    print(f"  {GRAY}Od:      {RESET}{TWILIO_BROJ}")
    print(f"  {GRAY}Do:      {RESET}{MOJ_BROJ}")
    print(f"  {GRAY}Poziva:  {RESET}{BROJ_POKUSAJA}x  |  Pauza: {PAUZA}s  |  Timeout: {TIMEOUT}s")
    print(f"{CYAN}{'─' * 50}{RESET}\n")

def progress_bar(done, total, width=30):
    filled = int(width * done / total)
    bar = "█" * filled + "░" * (width - filled)
    pct = int(100 * done / total)
    return f"[{bar}] {pct:3d}%  ({done}/{total})"

def main():
    print_header()

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    twiml  = f"<Response><Pause length='{TIMEOUT}'/><Hangup/></Response>"
    uspesnih = 0

    try:
        for i in range(BROJ_POKUSAJA):
            ts = time.strftime("%H:%M:%S")
            print(f"  {GRAY}[{ts}]{RESET}  Poziv {BOLD}{i+1}/{BROJ_POKUSAJA}{RESET} → {MOJ_BROJ} ... ", end="", flush=True)

            try:
                call = client.calls.create(
                    to=MOJ_BROJ,
                    from_=TWILIO_BROJ,
                    twiml=twiml,
                    timeout=TIMEOUT
                )
                print(f"{GREEN}✓ {call.status}{RESET}  {GRAY}SID: {call.sid}{RESET}")
                uspesnih += 1

            except Exception as e:
                print(f"{RED}✗ Greška: {e}{RESET}")

            prog = progress_bar(i + 1, BROJ_POKUSAJA)
            print(f"  {GRAY}{prog}{RESET}")

            if i < BROJ_POKUSAJA - 1:
                print(f"  {YELLOW}⏳ Čekam {PAUZA}s...{RESET}", end="\r", flush=True)
                time.sleep(PAUZA)
                print(" " * 40, end="\r")  # obrisi red

    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}⚠  Prekinuto (Ctrl+C){RESET}")

    print(f"\n{CYAN}{'─' * 50}{RESET}")
    print(f"{BOLD}  Završeno:{RESET}  {GREEN}{uspesnih}{RESET}/{BROJ_POKUSAJA} uspješnih poziva")
    print(f"{CYAN}{'─' * 50}{RESET}\n")

if __name__ == "__main__":
    main()
