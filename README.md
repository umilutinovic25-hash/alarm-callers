# Alarm Callers

Dve Python skripte za automatsko pozivanje — korisno kao budilnik koji ne možeš da ignorišeš.

## loop_caller.py — FaceTime/iPhone (bez eksternih naloga)

Poziva broj koristeći macOS `tel://` protokol (radi i sa iPhoneom pored Maca).

```bash
python3 loop_caller.py
```

Podesi na vrhu fajla:
- `MOJ_BROJ` — broj koji se poziva
- `BROJ_POKUSAJA` — koliko puta
- `TRAJANJE` — sekundi pre prekida poziva
- `PAUZA` — sekundi između poziva

## twilio_caller.py — Twilio (poziva bilo koji broj sa bilo kog mesta)

Zahteva Twilio nalog (besplatna probna verzija radi).

```bash
pip install twilio
python3 twilio_caller.py
```

Podesi na vrhu fajla:
- `ACCOUNT_SID`, `AUTH_TOKEN`, `TWILIO_BROJ` — sa Twilio konzole
- `MOJ_BROJ` — broj koji se poziva
