import random
import os


def spin_row():
    symbols = ["🍒", "🍓", "🍉", "🍌", "🤑"]
    weights = [2, 2, 3, 2, 1]

    return random.choices(symbols, weights=weights, k=3)


def print_row(row):
    print(" | ".join(row))


def get_payout(row, bet):
    if row[0] == row[1] == row[2]:
        if row[0] == "🍒":
            return bet * 5
        elif row[0] == "🍓":
            return bet * 3
        elif row[0] == "🍉":
            return bet * 1
        elif row[0] == "🍌":
            return bet * 3
        elif row[0] == "🤑":
            return bet * 1000
    return 0


def save_balance(balance):
    with open("balance.txt", "w") as file:
        file.write(str(balance))


def load_balance():
    if os.path.exists("balance.txt"):
        with open("balance.txt", "r") as file:
            content = file.read().strip()
            if content:
                try:
                    return float(content)
                except ValueError:
                    print("ValueError... ")
    return 0


def initial_balance(balance):
    while True:
        initialBalance = input("Please enter amount of funds: ")
        try:
            initialBalance = float(initialBalance)
            if initialBalance <= 0:
                print("Please enter amount greater than 0... ")
                continue
            balance = initialBalance
            save_balance(balance)
            break
        except ValueError:
            print("Please enter a number... ")
    return initialBalance


def save_choice(balance):
    while True:
        saveChoice = input("Type 'save' to pick up where you left off or 'wipe' to start fresh: ")
        if saveChoice.lower() == "save":
            balance = load_balance()
            break
        elif saveChoice.lower() == "wipe":
            balance = initial_balance(balance)
            break
        else:
            print("Please enter one of the keywords... ")
            continue
    return balance


def manual_spin(balance):
    while balance > 0:
        print(f"\nCurrent Balance: ${balance:,.2f}")
        bet = input("Enter bet amount (or 'q' to quit): ")

        if bet.lower() == "q":
            print("Thanks for playing! Goodbye... ")
            save_balance(balance)
            break

        try:
            bet = float(bet)
        except ValueError:
            print("Please enter a number... \n")
            continue

        bet = float(bet)

        if bet > balance:
            print("Insufficient Funds... \n")
            continue
        elif bet < 0.01:
            print("Minimum Bet Amount is 1 cent... \n")
            continue

        balance -= bet
        save_balance(balance)

        row = spin_row()
        print_row(row)

        payout = get_payout(row, bet)
        if payout > 0:
            print(f"\nYOU WON ${payout:,.2f}!")
        else:
            print("\nYOU LOST!")

        balance += payout
        save_balance(balance)

        if balance == 0:
            print(f"\nBetter Luck Next Time! \nCurrent Balance: ${balance:,.2f}")
            break
    return balance


def auto_spin(balance):
    stats = {"Wins": 0,
             "Losses": 0,
             "Net Gain": 0,
             "Symbol Wins": {"🍒": 0, "🍓": 0, "🍉": 0, "🍌": 0, "🤑": 0}}

    startBalance = balance  # setting start balance for later calculation

    # prompt user to input bet of either 10, 100, or 1000
    while True:
        try:
            bet = int(input("Choose bet amount (10, 100, 1000): "))
            if bet in [10, 100, 1000]:
                break
            else:
                print("Please enter one of the specified values... ")
        except ValueError:
            print("Please enter one of the specified values... ")

    # Prompt user for number of rounds
    while True:
        roundsChoice = input("Enter a specified number of rounds or type 'max' to spin until balance is empty: ")
        if roundsChoice.lower() == "max":
            rounds = float("inf")
            break
        else:
            try:
                rounds = int(roundsChoice)
                break
            except ValueError:
                print("Please enter a specified number of rounds or type 'max'... ")

    spins = 0  # counter for num of spins

    # Start spinning either for the specified rounds or until balance reaches zero
    while balance >= bet and spins < rounds:
        spins += 1
        balance -= bet
        row = spin_row()
        payout = get_payout(row, bet)

        if payout > 0:
            stats["Wins"] += 1
            balance += payout
            symbolWin = row[0]
            stats["Symbol Wins"][symbolWin] += 1
        else:
            stats["Losses"] += 1

    # stats calculations
    winPct = (stats["Wins"] / spins) * 100 if spins > 0 else 0
    endBalance = balance
    stats["Net Gain"] = endBalance - startBalance

    symbolMode = max(stats["Symbol Wins"], key=stats["Symbol Wins"].get)
    symbolModeCount = stats["Symbol Wins"][symbolMode]

    # create summary txt file
    with open("Stats Summary.txt", "w", encoding='utf-8') as file:
        file.write(
            f"Wins: {stats["Wins"]}"
            f"\nLosses: {stats["Losses"]}"
            f"\nWin Percentage: {winPct:.2f}%"
            f"\n1000x hits: {stats["Symbol Wins"]["🤑"]}"
            f"\nMost Frequent Symbol: {symbolMode}"
            f"\n  Number of times hit: {symbolModeCount}"
            f"\n\nNet Gain/Loss: ${stats["Net Gain"]:,.2f}"
            f"\nFinal Balance: ${balance:,.2f}"
        )

    save_balance(balance)
    return balance


def choose_mode(balance):
    while True:
        mode = input("""
Select '1' or '2' to choose mode
    1. Auto Spin (has stats summary)
    2. Manual Spin
    Input: """)
        try:
            mode = int(mode)
            if mode == 1:
                balance = auto_spin(balance)
                break
            elif mode == 2:
                balance = manual_spin(balance)
                break
            else:
                print("Please select either '1' or '2'... ")
        except ValueError:
            print("Please select either '1' or '2'... ")

    return balance


def main():
    print("\nWelcome to the Slot Machine!!!")
    print("Symbols: 🍒 🍓 🍉 🍌 🤑")

    balance = load_balance()

    if balance != 0:
        balance = save_choice(balance)

    if balance == 0:
        balance = initial_balance(balance)
        save_balance(balance)

    print(f"Balance: ${balance:,.2f}")

    balance = choose_mode(balance)
    print(f"""
    Thanks for Playing!
    Remaining Balance: ${balance:,.2f}""")


if __name__ == "__main__":
    main()
