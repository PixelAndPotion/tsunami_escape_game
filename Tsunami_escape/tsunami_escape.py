import random
import time

balance = 10000  # user starting money


def get_crash_probability(multiplier):
    if multiplier < 2:
        return 0.05
    elif multiplier < 3.5:
        return 0.15
    else:
        return 0.30


def simulate_ai_players():
    players = []
    types = ["safe", "unsafe", "random"]

    for i in range(5):
        player_type = random.choice(types)

        if player_type == "safe":
            cash_out = round(random.uniform(1.2, 2.0), 2)
        elif player_type == "unsafe":
            cash_out = round(random.uniform(2.5, 5.0), 2)
        else:
            cash_out = round(random.uniform(1.0, 5.0), 2)

        players.append({
            "name": f"Surfer{i+1}",
            "cash_out": cash_out,
            "active": True
        })

    return players


def play_round(bet):
    multiplier = 1.0
    crashed = False
    players = simulate_ai_players()

    print("\n🌊 Tsunami is forming... Escape before you drown!\n")

    while not crashed:
        time.sleep(1)
        multiplier = round(multiplier + random.uniform(0.1, 0.5), 2)

        print(f"🌊 Wave Height: x{multiplier}")

        # AI players cash out
        for p in players:
            if p["active"] and multiplier >= p["cash_out"]:
                print(f"{p['name']} escaped at x{p['cash_out']}")
                p["active"] = False

        # Crash check
        if random.random() < get_crash_probability(multiplier):
            print("\n You have drowned!")
            return 0  # player loses bet

        user_input = input("Press ENTER to stay or type 'c' to escape: ")

        if user_input.lower() == 'c':
            winnings = round(bet * multiplier, 2)
            print(f"\n🏄 You escaped at x{multiplier} and won R{winnings}!")
            return winnings


def main():
    global balance

    print(" Welcome to Tsunami Escape ")

    while balance > 0:
        print(f"\n Your Balance: R{balance}")

        try:
            bet = float(input("Enter your bet amount: R"))

            if bet <= 0 or bet > balance:
                print("⚠️ Invalid bet amount.")
                continue

        except ValueError:
            print("⚠️ Please enter a valid number.")
            continue

        balance -= bet
        winnings = play_round(bet)
        balance += winnings

        print(f" New Balance: R{balance}")

        if balance <= 0:
            print(" You’ve run out of money!")
            break

        again = input("\nPlay again? (y/n): ").lower()
        if again != 'y':
            break

    print("\n Thanks for playing Tsunami Escape. Stay Safe!")


if __name__ == "__main__":
    main()