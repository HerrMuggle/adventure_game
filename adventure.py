import pickle
import os
import random

# Game State Variables
inventory = []
time_remaining = 5 # You have 5 'units' of time before night falls
player_hp = 80
gold = 0
SAVE_FILE = "game_save.pkl"

def save_game():
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump((inventory, time_remaining, player_hp, gold), f)
    print("💾 Game saved.\n")

def load_game():
    global inventory, time_remaining, player_hp, gold
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'rb') as f:
            inventory, time_remaining, player_hp, gold = pickle.load(f)
        print("📂 Game loaded.\n")
    else:
        print("⚠️ No saved game found.\n")

def check_time():
    print(f"⏳ Time remaining before nightfall: {time_remaining}")
    if time_remaining <= 0:
        print("🌑 Night falls. The wolves have come out...")
        if "Sword" in inventory:
            print("🗡️ You fight them off with your sword and barely survive.")
        else:
            print("🐺 You are overwhelmed by wolves. Game Over.")
            exit()

def show_stats():
    print(f"\n❤️ HP: {player_hp} | 💰 Gold: {gold} | 🎒 Inventory: {inventory}\n")

def intro():
    print("\n🌲 You are in a mysterious forest.")
    print("What would you like to do?")
    print("1. Go to the Dragon's Cave")
    print("2. Explore the Forest")
    print("3. Return to the Town")
    print("4. Visit the Shopkeeper")
    print("5. Talk to a Traveler (NPC)")
    print("6. Save Game")
    print("7. Load Game")

def dragon_cave():
    global time_remaining
    print("\n🐉 You quietly enter the dragon’s cave. Smoke rises from its nose.")
    time_remaining -= 1
    if "Golden Egg" in inventory:
        print("You've already taken the Golden Egg. Time to leave before it wakes again!")
        return
    print("The dragon is asleep on a mountain of gold. The egg glows nearby.")
    choice = input("Do you try to steal the Golden Egg? (yes/no) > ").lower()
    if choice == "yes":
        if random.randint(1, 3) != 1:
            inventory.append("Golden Egg")
            print("🥚 You successfully steal the Golden Egg and sneak out!")
        else:
            print("🔥 The dragon awakens and breathes fire! You are burnt to a crisp. Game Over.")
            exit()
    else:
        print("You quietly retreat without waking the beast.")

def explore_forest():
    global time_remaining, gold, player_hp
    time_remaining -= 1
    print("\n🌳 You explore the forest...")
    event = random.choice(["berries", "goblin", "gold", "nothing"])
    if event == "berries":
        print("🍓 You find healing berries and eat them. +2 HP.")
        player_hp += 2
    elif event == "goblin":
        print("👺 A goblin ambushes you!")
        fight_enemy("Goblin", 6)
    elif event == "gold":
        print("💰 You find a pouch of gold. +10 gold.")
        gold += 10
    else:
        print("Nothing interesting happens.")

def visit_shop():
    global gold
    print("\n🛒 Shopkeeper: 'Take a look at my wares!'")
    print("1. Sword (20 gold)")
    print("2. Torch (10 gold)")
    print("3. Healing Potion (15 gold)")
    print("4. Leave Shop")

    choice = input("> ")
    if choice == "1" and gold >= 20:
        inventory.append("Sword")
        gold -= 20
        print("🗡️ You bought a Sword.")
    elif choice == "2" and gold >= 10:
        inventory.append("Torch")
        gold -= 10
        print("🔥 You bought a Torch.")
    elif choice == "3" and gold >= 15:
        inventory.append("Healing Potion")
        gold -= 15
        print("🧪 You bought a Healing Potion.")
    elif choice == "4":
        print("You leave the shop.")
    else:
        print("❌ Not enough gold or invalid option.")

def talk_to_npc():
    global gold
    print("\n🧙 You meet a mysterious traveler...")
    encounter = random.choice(["blessing", "curse", "gift", "riddle"])
    if encounter == "blessing":
        print("🌟 The traveler blesses you. +1 HP.")
        global player_hp
        player_hp += 1
    elif encounter == "curse":
        print("😈 A goblin disguised as a traveler curses you! -2 HP.")
        player_hp -= 2
    elif encounter == "gift":
        print("🎁 The traveler gives you 5 gold.")
        gold += 5
    elif encounter == "riddle":
        print("🧠 'What walks on four legs in the morning, two in the afternoon, and three in the evening?'")
        answer = input("Your answer: ").lower()
        if "man" in answer:
            print("✅ Correct! You earn 10 gold.")
            gold += 10
        else:
            print("❌ Wrong. The traveler disappears.")

def fight_enemy(name, hp):
    global player_hp, gold
    print(f"\n⚔️ Combat with {name} begins!")
    while hp > 0 and player_hp > 0:
        print(f"Your HP: {player_hp} | {name} HP: {hp}")
        action = input("Do you (a)ttack or (r)un? > ").lower()
        if action == "a":
            dmg = random.randint(1, 6)
            if "Sword" in inventory:
                dmg += 2
            print(f"You strike the {name} for {dmg} damage!")
            hp -= dmg
            if hp > 0:
                enemy_dmg = random.randint(1, 4)
                player_hp -= enemy_dmg
                print(f"The {name} hits back for {enemy_dmg} damage!")
        elif action == "r":
            print("You run away safely.")
            return
        else:
            print("Invalid choice.")
    if player_hp <= 0:
        print("💀 You died. Game Over.")
        exit()
    else:
        print(f"🏆 You defeated the {name}!")
        reward = random.randint(5, 15)
        print(f"You collect {reward} gold.")
        gold += reward

def go_to_town():
    global time_remaining
    time_remaining -= 1
    if "Golden Egg" in inventory:
        if time_remaining > 0:
            print("🏘️ You return to town with the Golden Egg before nightfall. YOU WIN!")
            exit()
        else:
            print("🐺 You made it to town... but wolves were waiting. Game Over.")
            exit()
    else:
        print("🚪 You can’t return to town without the Golden Egg.")

def game_loop():
    while True:
        check_time()
        show_stats()
        intro()
        choice = input("> ")
        if choice == "1":
            dragon_cave()
        elif choice == "2":
            explore_forest()
        elif choice == "3":
            go_to_town()
        elif choice == "4":
            visit_shop()
        elif choice == "5":
            talk_to_npc()
        elif choice == "6":
            save_game()
        elif choice == "7":
            load_game()
        else:
            print("❌ Invalid option.")

if __name__ == "__main__":
    print("=== 🐉 Golden Egg Quest ===")
    print("Your goal is to retrieve the dragon’s egg and return before nightfall.")
    game_loop()
