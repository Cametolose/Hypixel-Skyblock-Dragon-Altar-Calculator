import os
import requests
import random
import tkinter as tk
from tkinter import messagebox


def run_simulation():
    try:
        amount = int(entry_amount.get())
        iterations = int(entry_iterations.get())
        instabuy_buyorder = var_buyorder.get() == 1

        url = "https://api.hypixel.net/v2/skyblock/bazaar"
        response = requests.get(url)
        data = response.json()["products"]

        # Fragment prices
        prices = [
            ("Protector", data["PROTECTOR_FRAGMENT"]["quick_status"]["sellPrice"],
             data["PROTECTOR_FRAGMENT"]["quick_status"]["buyPrice"]),
            ("Old", data["OLD_FRAGMENT"]["quick_status"]["sellPrice"], data["OLD_FRAGMENT"]["quick_status"]["buyPrice"]),
            ("Unstable", data["UNSTABLE_FRAGMENT"]["quick_status"]["sellPrice"],
             data["UNSTABLE_FRAGMENT"]["quick_status"]["buyPrice"]),
            ("Wise", data["WISE_FRAGMENT"]["quick_status"]["sellPrice"],
             data["WISE_FRAGMENT"]["quick_status"]["buyPrice"]),
            ("Young", data["YOUNG_FRAGMENT"]["quick_status"]["sellPrice"],
             data["YOUNG_FRAGMENT"]["quick_status"]["buyPrice"]),
            ("Strong", data["STRONG_FRAGMENT"]["quick_status"]["sellPrice"],
             data["STRONG_FRAGMENT"]["quick_status"]["buyPrice"]),
            ("Superior", data["SUPERIOR_FRAGMENT"]["quick_status"]["sellPrice"],
             data["SUPERIOR_FRAGMENT"]["quick_status"]["buyPrice"]),
            ("Holy", data["HOLY_FRAGMENT"]["quick_status"]["sellPrice"],
             data["HOLY_FRAGMENT"]["quick_status"]["buyPrice"])
        ]

        # Find cheapest fragment
        if instabuy_buyorder:
            cheapest_fragment = min(prices, key=lambda x: x[1])
        else:
            cheapest_fragment = min(prices, key=lambda x: x[2])

        # Fragment name & price
        fragment_name = cheapest_fragment[0]
        lowest_value = cheapest_fragment[1] if instabuy_buyorder else cheapest_fragment[2]
        total_price = amount * lowest_value

        # Profit
        essence_sellorder = data["ESSENCE_DRAGON"]["quick_status"]["buyPrice"] * 0.99
        ritual_sellorder = data["RITUAL_RESIDUE"]["quick_status"]["buyPrice"] * 0.99
        summoning_sellorder = data["SUMMONING_EYE"]["quick_status"]["buyPrice"] * 0.99
        horn_sellorder = data["DRAGON_HORN"]["quick_status"]["buyPrice"] * 0.99

        # Chances
        bonus = 0.55
        fragment_chance = 0.8193
        ritual_chance = 0.1084
        summoning_chance = 0.0482
        horn_chance = 0.0241

        # int thing
        total_fragment_amount = 0
        total_ritual_amount = 0
        total_summoning_amount = 0
        total_horn_amount = 0
        total_profit = 0

        for _ in range(iterations):
            # Checking for items
            fragment_amount = 0
            ritual_amount = 0
            summoning_amount = 0
            horn_amount = 0

            total_rolls = amount // 40

            # Chance calculation
            for _ in range(total_rolls):
                if random.random() < bonus:
                    roll = random.random()
                    if roll < fragment_chance:
                        fragment_amount += random.randint(15, 20)
                    elif roll < fragment_chance + ritual_chance:
                        ritual_amount += 1
                    elif roll < fragment_chance + ritual_chance + summoning_chance:
                        summoning_amount += 1
                    else:
                        horn_amount += 1

            # End Calculation
            profit = ((essence_sellorder * amount / 2) + (ritual_amount * ritual_sellorder) + (
                        summoning_amount * summoning_sellorder) + (horn_amount * horn_sellorder) + (
                                  fragment_amount * lowest_value)) - total_price

            total_fragment_amount += fragment_amount
            total_ritual_amount += ritual_amount
            total_summoning_amount += summoning_amount
            total_horn_amount += horn_amount
            total_profit += profit

        avg_fragment_amount = total_fragment_amount / iterations
        avg_ritual_amount = total_ritual_amount / iterations
        avg_summoning_amount = total_summoning_amount / iterations
        avg_horn_amount = total_horn_amount / iterations
        avg_profit = total_profit / iterations

        result_text = (
            f"\nCheapest Fragment: {fragment_name}\nAmount: {amount:,}\nTotal Price: {int(total_price):,} coins\n"
            f"Price per Fragment: {int(lowest_value):,} coins\nAverage Profit: {int(avg_profit):,} coins\n\n"
            f"Average Drops:\n"
            f"{fragment_name} Fragments: {avg_fragment_amount:,}\nRitual Residue: {avg_ritual_amount:,}\n"
            f"Summoning Eye: {avg_summoning_amount:,}\nDragon Horn: {avg_horn_amount:,}")

        result_label.config(text=result_text)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI setup
root = tk.Tk()
root.title("Altar Calculator - Cametolose")

tk.Label(root, text="How many Fragments do you want to buy? ").grid(row=0, column=0)
entry_amount = tk.Entry(root)
entry_amount.grid(row=0, column=1)

tk.Label(root, text="How many runs should the code run?\n(1000+ recommended)").grid(row=1, column=0)
entry_iterations = tk.Entry(root)
entry_iterations.grid(row=1, column=1)

var_buyorder = tk.IntVar()
tk.Checkbutton(root, text="Do you use buy orders?", variable=var_buyorder).grid(row=2, columnspan=2)

tk.Button(root, text="Calculate", command=run_simulation).grid(row=3, columnspan=2)

result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.grid(row=4, columnspan=2)

root.mainloop()
