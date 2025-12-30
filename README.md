# Ethos LED Display

Display your Ethos score on an LED strip with color-coded tiers.

## Running on Phone

### Android (Termux)

1. **Install Termux** from F-Droid (recommended) or Play Store
   - F-Droid: https://f-droid.org/packages/com.termux/

2. **Open Termux** and run these commands:
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   pip install pypixelcolor
   ```

3. **Copy the script** to your phone:
   ```bash
   # Option A: Clone from git (if you have a repo)
   git clone <your-repo-url>

   # Option B: Download directly
   curl -O https://your-url/ethos_led.py

   # Option C: Copy manually
   # Put ethos_led.py in your Downloads folder, then:
   cp /sdcard/Download/ethos_led.py ~
   ```

4. **Run the script**:
   ```bash
   python ethos_led.py
   ```

5. **Select from menu**:
   ```
   ========================================
          ETHOS LED DISPLAY
   ========================================

     1. Check score (one-time)
     2. Watch score (auto-refresh)
     3. Change refresh interval
     4. Quit
   ```

### iOS (a-Shell or iSH)

1. **Install a-Shell** from App Store (easier) or **iSH** (more powerful)

2. **In a-Shell**, run:
   ```bash
   pip install pypixelcolor
   ```

3. **Copy script** via Files app to a-Shell's folder

4. **Run**:
   ```bash
   python ethos_led.py
   ```

## Alternative: SSH from Phone

If Bluetooth doesn't work directly from your phone, run the script on a PC/Raspberry Pi and SSH into it:

1. **On your PC/Pi**, keep the script running

2. **On your phone**, install an SSH app:
   - Android: Termux or JuiceSSH
   - iOS: Termux, Blink, or Prompt

3. **Connect via SSH**:
   ```bash
   ssh user@192.168.x.x
   cd /path/to/script
   python ethos_led.py
   ```

## Usage

### Interactive Menu (recommended for phone)
```bash
python ethos_led.py
```

### Command Line
```bash
# One-time check
python ethos_led.py username

# Watch mode (refresh every 60s)
python ethos_led.py username --watch

# Custom refresh interval (30 seconds)
python ethos_led.py username --watch 30
```

## Score Tiers & Colors

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

## Troubleshooting

**Bluetooth not connecting?**
- Make sure LED strip is powered on and in range
- On Android, grant Termux location permission (required for BLE)
- Try restarting Bluetooth on your phone

**Permission denied?**
```bash
chmod +x ethos_led.py
```

**Module not found?**
```bash
pip install pypixelcolor
```
