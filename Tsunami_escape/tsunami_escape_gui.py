import tkinter as tk
import random

# Game Variables 
balance = 10000
multiplier = 1.0
running = False
crashed = False
bet = 0
players = []
skill_active = False
skill_success = False
leaderboard = []  # stores top 5 multipliers

#  AI Players
ai_funny_msgs = [
    "tried to be brave but failed!",
    "riding the wave like a mermaid!",
    "was eating popcorn but got popped!!!",
    "can't handle the wave?"
]

def simulate_ai_players():
    players_list = []
    types = ["safe", "unsafe", "random"]
    for i in range(5):
        player_type = random.choice(types)
        if player_type == "safe":
            cash_out = round(random.uniform(1.2, 2.0), 2)
        elif player_type == "unsafe":
            cash_out = round(random.uniform(2.5, 5.0), 2)
        else:
            cash_out = round(random.uniform(1.0, 5.0), 2)
        msg = random.choice(ai_funny_msgs)
        players_list.append({
            "name": f"Surfer{i+1}",
            "cash_out": cash_out,
            "msg": msg,
            "active": True
        })
    return players_list

#  Crash Probability 
def get_crash_probability(mult):
    if mult < 2:
        return 0.05
    elif mult < 3.5:
        return 0.15
    else:
        return 0.30

#  Update Game 
def update_game():
    global multiplier, running, crashed, players, skill_active, skill_success

    if not running:
        return

    multiplier += round(random.uniform(0.1, 0.5), 2)
    multiplier_label.config(text=f"Wave Height: x{round(multiplier,2)}")
    log(f"🌊 Wave rising... x{round(multiplier,2)}")

    # Trigger skill event randomly
    if not skill_active and random.random() < 0.15:
        trigger_skill_event()

    # AI players cashing out
    for p in players:
        if p["active"] and multiplier >= p["cash_out"]:
            log(f"{p['name']} escaped at x{p['cash_out']} → {p['msg']}")
            p["active"] = False

    # Crash check
    crash_chance = get_crash_probability(multiplier)
    if skill_active and skill_success:
        crash_chance /= 2  # skill reduces crash chance

    if random.random() < crash_chance:
        log(" The tsunami has crashed!")
        running = False
        crashed = True
        skill_active = False
        return

    root.after(1000, update_game)

# Start Round 
def start_round():
    global running, multiplier, crashed, bet, balance, players
    try:
        bet_value = float(bet_entry.get())
    except:
        log("⚠️ Enter a valid bet amount")
        return

    if bet_value <= 0 or bet_value > balance:
        log("⚠️ Invalid bet amount")
        return

    global bet
    bet = bet_value
    balance -= bet
    update_balance()

    multiplier = 1.0
    crashed = False
    running = True
    players = simulate_ai_players()

    log(f"🌊 Round started! Bet: R{bet}")
    update_game()

#  Cash Out 
def cash_out():
    global balance, running, multiplier, bet, leaderboard
    if not running:
        log("⚠️ No active round")
        return

    winnings = round(bet * multiplier, 2)
    balance += winnings
    log(f"🏄 Cashed out at x{round(multiplier,2)} → Won R{winnings}")
    running = False
    update_balance()

    # Update leaderboard
    leaderboard.append(round(multiplier,2))
    leaderboard.sort(reverse=True)
    if len(leaderboard) > 5:
        leaderboard.pop()
    update_leaderboard_display()

#  Leaderboard 
def update_leaderboard_display():
    leaderboard_box.delete(1.0, tk.END)
    leaderboard_box.insert(tk.END, " Top Multipliers\n")
    for i, score in enumerate(leaderboard, start=1):
        leaderboard_box.insert(tk.END, f"{i}. x{score}\n")

#  Update Balance 
def update_balance():
    balance_label.config(text=f"Balance: R{round(balance,2)}")

#  Logging 
def log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)

# Skill Event
def trigger_skill_event():
    global skill_active, skill_success
    skill_active = True
    skill_success = False

    skill_btn = tk.Button(root, text="⚡ Stabilize Wave!", font=("Arial",12), fg="white", bg="red",
                          command=lambda: activate_skill(skill_btn))
    skill_btn.pack(pady=5)
    log(" Skill Event! Click FAST to stabilize the wave!")

    # auto-remove button after 2 seconds
    root.after(2000, lambda: remove_skill(skill_btn))

def activate_skill(button):
    global skill_success, skill_active
    skill_success = True
    skill_active = False
    log("✅ You stabilized the wave!")
    button.destroy()

def remove_skill(button):
    global skill_active
    if skill_active:
        log("❌ Missed skill! No stabilization.")
        skill_active = False
    button.destroy()

# UI
root = tk.Tk()
root.title("🌊 Tsunami Escape GUI")
root.geometry("500x650")

title = tk.Label(root, text=" Tsunami Escape GUI", font=("Arial", 18))
title.pack(pady=10)

balance_label = tk.Label(root, text=f"Balance: R{balance}", font=("Arial", 12))
balance_label.pack()

multiplier_label = tk.Label(root, text=f"Wave Height: x1.0", font=("Arial", 14))
multiplier_label.pack(pady=10)

bet_entry = tk.Entry(root)
bet_entry.pack(pady=5)
bet_entry.insert(0, "Enter bet amount")

start_btn = tk.Button(root, text="Start Round", command=start_round)
start_btn.pack(pady=5)

cashout_btn = tk.Button(root, text="Cash Out", command=cash_out)
cashout_btn.pack(pady=5)

log_box = tk.Text(root, height=15, width=60)
log_box.pack(pady=10)

leaderboard_box = tk.Text(root, height=8, width=60)
leaderboard_box.pack(pady=10)
update_leaderboard_display()

update_balance()
root.mainloop()