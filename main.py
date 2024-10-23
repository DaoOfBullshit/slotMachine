import random
import os


def spin_row():
    symbols = ["🍒", "🍓", "🍉", "🍌", "🤑"]

    return [random.choice(symbols) for i in range(3)]


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
        initial_balance = input("Please enter amount of funds: ")
        try:
            initial_balance = float(initial_balance)
            if initial_balance <= 0:
                print("Please enter amount greater than 0... ")
                continue
            balance = initial_balance
            balance = save_balance(balance)
            break
        except ValueError:
            print("Please enter a number... ")
    return initial_balance


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


def main():
    print("\nWelcome to the Slot Machine!!!")
    print("Symbols: 🍒 🍓 🍉 🍌 🤑")

    balance = load_balance()

    if balance != 0:
        balance = save_choice(balance)

    if balance == 0:
        balance = initial_balance(balance)
        save_balance(balance)

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
        elif bet <= 0:
            print("Please enter amount greater than 0... \n")
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

    save_balance(balance)


if __name__ == "__main__":
    main()
