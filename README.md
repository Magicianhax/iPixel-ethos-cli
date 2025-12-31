# Ethos CLI

Check Ethos scores from your phone via command line. Optionally display on LED strip.

## Quick Start (Phone)

### Android (Termux)

```bash
# 1. Install Termux from F-Droid
# https://f-droid.org/packages/com.termux/

# 2. Setup
pkg update && pkg upgrade
pkg install python git

# 3. Clone & Run
git clone https://github.com/Magicianhax/iPixel-ethos-cli.git
cd iPixel-ethos-cli
python ethos_led.py
```

### iOS (a-Shell)

```bash
# Install a-Shell from App Store, then:
pip install requests
# Copy ethos_led.py via Files app
python ethos_led.py
```

## Usage

### Interactive Menu (default)
```bash
python ethos_led.py
```

```
========================================
       ETHOS LED DISPLAY
========================================

  1. Check score (one-time)
  2. Watch score (auto-refresh)
  3. Change refresh interval
  4. Toggle LED [OFF (score only)]
  5. Quit

----------------------------------------
  Refresh interval: 60s

Select option (1-5):
```

### Command Line
```bash
# One-time check (no LED)
python ethos_led.py username --no-led

# Watch mode - refresh every 60s
python ethos_led.py username --watch --no-led

# Custom interval (30 seconds)
python ethos_led.py username --watch 30 --no-led
```

## LED Mode (PC/Raspberry Pi only)

Bluetooth LED display only works on Linux/Windows/Mac - not on phones.

To use LED features:
1. Run on a PC or Raspberry Pi
2. Toggle LED ON in menu (option 4)
3. Or omit `--no-led` flag in CLI

```bash
# With LED (requires pypixelcolor)
pip install pypixelcolor
python ethos_led.py username --watch
```

## Score Tiers

| Score | Tier | Color |
|-------|------|-------|
| < 800 | Untrusted | Red |
| < 1200 | Questionable | Orange |
| < 1400 | Neutral | Gray |
| < 1600 | Known | Blue-Gray |
| < 1800 | Established | Light Blue |
| < 2000 | Reputable | Blue |
| < 2200 | Exemplary | Green |
| < 2400 | Distinguished | Dark Green |
| < 2600 | Revered | Purple |
| 2600+ | Renowned | Deep Purple |
