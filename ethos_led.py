"""
Ethos Score Display on LED Strip
Shows score with color based on tier

Usage:
    python ethos_led.py <username>              # One-time display
    python ethos_led.py <username> --watch      # Auto-refresh every 60s
    python ethos_led.py <username> --watch 30   # Auto-refresh every 30s
"""
import asyncio
import urllib.request
import json
import sys
from datetime import datetime
from pypixelcolor import AsyncClient

DEVICE_ADDRESS = "5D:C8:1C:36:B7:AC"
ETHOS_API = "https://api.ethos.network/api/v2/user/by/x/"
DEFAULT_REFRESH_INTERVAL = 60  # seconds

# Score tiers with colors (hex without #)
SCORE_TIERS = [
    (800,  "Untrusted",     "b72b38"),
    (1200, "Questionable",  "C29010"),
    (1400, "Neutral",       "c1c0b6"),
    (1600, "Known",         "7C8DA8"),
    (1800, "Established",   "4E86B9"),
    (2000, "Reputable",     "2E7BC3"),
    (2200, "Exemplary",     "427B56"),
    (2400, "Distinguished", "127f31"),
    (2600, "Revered",       "836DA6"),
    (2800, "Renowned",      "7A5EA0"),
]

def get_tier_color(score: int) -> tuple:
    """Get tier name and color based on score"""
    for threshold, name, color in SCORE_TIERS:
        if score < threshold:
            return name, color
    return "Renowned", "7A5EA0"

def get_ethos_score(twitter_username: str) -> dict:
    """Fetch Ethos score for a Twitter username"""
    url = ETHOS_API + twitter_username
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                "success": True,
                "username": data.get("username", twitter_username),
                "displayName": data.get("displayName", "Unknown"),
                "score": data.get("score", 0),
            }
    except urllib.error.HTTPError as e:
        return {"success": False, "error": "User not found" if e.code == 404 else f"HTTP {e.code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def display_ethos_score(twitter_username: str, device=None):
    """Fetch and display Ethos score on LED strip"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] Looking up @{twitter_username}...")

    result = get_ethos_score(twitter_username)

    if not result["success"]:
        print(f"Error: {result['error']}")
        return None

    score = result["score"]
    tier_name, tier_color = get_tier_color(score)

    print(f"User: {result['displayName']} (@{result['username']})")
    print(f"Score: {score}")
    print(f"Tier: {tier_name} (#{tier_color})")

    # Connect to LED if no device passed
    should_disconnect = False
    if device is None:
        print(f"\nConnecting to LED strip...")
        device = AsyncClient(DEVICE_ADDRESS)
        await device.connect()
        print("Connected!")
        should_disconnect = True

    # Display score with tier color
    print(f"Displaying: {score}")
    await device.set_brightness(80)
    await device.send_text(str(score), color=tier_color)

    if should_disconnect:
        await asyncio.sleep(2)
        await device.disconnect()
        print("Done!")

    return score


async def watch_ethos_score(twitter_username: str, interval: int = DEFAULT_REFRESH_INTERVAL):
    """Continuously monitor and display Ethos score"""
    print(f"\n{'=' * 40}")
    print(f"WATCHING @{twitter_username}")
    print(f"Refresh interval: {interval}s | Ctrl+C to stop")
    print(f"{'=' * 40}")

    # Connect once and keep connection open
    print(f"\nConnecting to LED strip...")
    device = AsyncClient(DEVICE_ADDRESS)
    await device.connect()
    print("Connected! Starting watch mode...\n")

    last_score = None
    try:
        while True:
            score = await display_ethos_score(twitter_username, device)

            if score is not None and last_score is not None and score != last_score:
                diff = score - last_score
                print(f"  -> Score changed: {'+' if diff > 0 else ''}{diff}")

            last_score = score
            print(f"\nNext refresh in {interval}s...")
            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nStopping watch mode...")
    finally:
        await device.disconnect()
        print("Disconnected. Goodbye!")

def show_menu():
    """Display the main menu"""
    print("\n" + "=" * 40)
    print("       ETHOS LED DISPLAY")
    print("=" * 40)
    print("\n  1. Check score (one-time)")
    print("  2. Watch score (auto-refresh)")
    print("  3. Change refresh interval")
    print("  4. Quit")
    print("\n" + "-" * 40)


async def interactive_mode():
    """Interactive menu-based mode"""
    refresh_interval = DEFAULT_REFRESH_INTERVAL
    last_username = None

    while True:
        show_menu()
        if last_username:
            print(f"  Last user: @{last_username}")
        print(f"  Refresh interval: {refresh_interval}s")
        print()

        choice = input("Select option (1-4): ").strip()

        if choice == '1':
            username = input("\nEnter Twitter/X username: ").strip().lstrip('@')
            if not username:
                print("Invalid username")
                continue
            last_username = username
            await display_ethos_score(username)
            input("\nPress Enter to continue...")

        elif choice == '2':
            if last_username:
                use_last = input(f"Use @{last_username}? (Y/n): ").strip().lower()
                if use_last in ('', 'y', 'yes'):
                    username = last_username
                else:
                    username = input("Enter Twitter/X username: ").strip().lstrip('@')
            else:
                username = input("Enter Twitter/X username: ").strip().lstrip('@')

            if not username:
                print("Invalid username")
                continue

            last_username = username
            await watch_ethos_score(username, refresh_interval)

        elif choice == '3':
            try:
                new_interval = int(input(f"\nNew interval in seconds (current: {refresh_interval}): ").strip())
                if new_interval < 10:
                    print("Minimum interval is 10 seconds")
                else:
                    refresh_interval = new_interval
                    print(f"Interval set to {refresh_interval}s")
            except ValueError:
                print("Invalid number")

        elif choice == '4' or choice.lower() == 'q':
            print("\nGoodbye!")
            break

        else:
            print("Invalid option, try again")

async def main():
    args = sys.argv[1:]

    if not args:
        await interactive_mode()
        return

    username = args[0].lstrip('@')

    # Check for --watch flag
    if '--watch' in args or '-w' in args:
        # Get custom interval if provided
        interval = DEFAULT_REFRESH_INTERVAL
        for i, arg in enumerate(args):
            if arg in ('--watch', '-w') and i + 1 < len(args):
                try:
                    interval = int(args[i + 1])
                except ValueError:
                    pass
        await watch_ethos_score(username, interval)
    else:
        await display_ethos_score(username)


if __name__ == "__main__":
    asyncio.run(main())
