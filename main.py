"""
main.py — the interactive game driver for the Sci-Fi Station Crawler.

Run with:   python main.py

Grade 9 OOP Exemplar — Sci-Fi Station Crawler
"""

# =====================================================================
#  OOP RELATIONSHIP MAP (simplified UML class diagram)
#
#    IS-A   = inheritance  (MedKit / Keycard inherit from Item)
#    HAS-A  = composition  (one object owns another object)
#
#    +----------------+  HAS-A     +----------------+
#    |     Player     |----------->|   Inventory    |
#    +----------------+            +----------------+
#    | name           |            | capacity = 5   |
#    | health         |            | items = [] ---------> list of Item
#    | current_room --|----.       +----------------+      objects
#    | inventory *    |    |
#    +----------------+    |             +---------------+
#           |              |             |     Item      |  (base class)
#           | HAS-A ref    |             +---------------+
#           v              |             | name          |
#    +----------------+    |             | description   |
#    |      Room      |    |             | use()         |
#    +----------------+    |             | consumable    |
#    | name           |    |             +---------------+
#    | description    |    |                ^         ^
#    | items = [] ---------'                |         |   IS-A (inheritance)
#    | exits = {} ---------> other Rooms    |         |
#    +----------------+        |   +----------------+  +----------------+
#                              |   |     MedKit     |  |    Keycard     |
#                              '---| use() -> heal  |  | use() -> scan  |
#                                  +----------------+  +----------------+
#                                  | heal_amount=30 |  | clearance = 2  |
#                                  +----------------+  +----------------+
#
#    ( * = holds a reference to another object )
#  =====================================================================
#
#  DESIGN NOTE: Locks and hazards are stored as plain DATA on Room
#  objects (locked, required_clearance, hazard_damage). The game RULES
#  that use that data live here in the driver (main.py). Classes hold
#  data + abilities; the driver decides the story.

from item import MedKit, Keycard
from room import Room
from player import Player


# =====================================================================
#  WORLD SETUP — build the station map
#
#              [Med Bay]
#                  |
#   [Control Room]--[Airlock]--[Reactor Corridor]
# =====================================================================

def build_world():
    """Create every Room object, wire the exits, and scatter the items."""
    # --- Rooms (each is an independent OBJECT) --------------------------
    airlock = Room(
        "Airlock",
        "A cramped chamber between the station and open space. Warning lights spin lazily.",
    )
    med_bay = Room(
        "Med Bay",
        "White cabinets, a humming scanner, and the faint smell of antiseptic.",
    )
    reactor = Room(
        "Reactor Corridor",
        "A cracked conduit spits radiation sparks across the walkway.",
        hazard_damage=15,                     # game rule: entering costs 15 HP
    )
    control_room = Room(
        "Control Room",
        "The station's nerve centre, dark since the captain vanished.",
        locked=True, required_clearance=2,    # game rule: needs a level-2 keycard
    )

    # --- Exits (each room stores REFERENCES to other Room objects) ------
    airlock.connect_room("north", med_bay)
    airlock.connect_room("east", reactor)
    airlock.connect_room("west", control_room)
    med_bay.connect_room("south", airlock)
    reactor.connect_room("west", airlock)
    control_room.connect_room("east", airlock)

    # --- Items (placed with room.add_item) ------------------------------
    med_bay.add_item(MedKit(heal_amount=40))          # stronger kit: keyword argument
    airlock.add_item(MedKit())                        # default heal_amount=30
    reactor.add_item(Keycard(clearance_level=2))      # guarded by the hazard!

    return airlock  # the room the player starts in


# =====================================================================
#  GAME HELPERS
# =====================================================================

def find_keycard(player, required_level):
    """Search the player's inventory for a Keycard with enough clearance.

    OOP CONCEPT: isinstance() lets us ASK an object which class it
    belongs to — one of the rewards of a clean inheritance tree.
    """
    for item in player.inventory.items:
        if isinstance(item, Keycard) and item.clearance_level >= required_level:
            return item
    return None


def handle_move(player):
    """Menu option 2: try to walk through one of the room's exits."""
    direction = input("  Move where? (north / south / east / west): ").strip().lower()

    # dict.get() returns None when the direction does not exist — no crash.
    next_room = player.current_room.exits.get(direction)
    if next_room is None:
        print("  [!] You cannot go that way.")
        return

    # --- game rule: locked doors --------------------------------------
    if next_room.locked:
        print(f"  [!] The {next_room.name} door is sealed.")
        print(f"      (Requires keycard clearance level {next_room.required_clearance})")
        keycard = find_keycard(player, next_room.required_clearance)
        if keycard is None:
            print("      Your card is not strong enough. Search the station...")
            return
        print(f"      You swipe your {keycard.name} ... ACCESS GRANTED.")
        # OOP CONCEPT: an object's state can change while the program runs.
        next_room.locked = False  # the door stays open from now on

    # OOP CONCEPT: Object References — moving is just re-pointing the
    # player's current_room reference at a different Room object.
    player.current_room = next_room
    print(f"\n  You head {direction}...")
    player.current_room.get_details()

    # --- game rule: hazards -------------------------------------------
    if player.current_room.hazard_damage > 0:
        print("  [!] HAZARD: radiation washes over you!")
        player.take_damage(player.current_room.hazard_damage)

    # --- win condition --------------------------------------------------
    if player.current_room.name == "Control Room":
        print_victory(player)


def handle_pick_up(player):
    """Menu option 3: transfer an item from the room into the inventory."""
    if player.current_room.items:
        names = ", ".join(item.name for item in player.current_room.items)
        print(f"  On the floor here: {names}")
    else:
        print("  (Nothing lies on the floor in this room.)")

    item_name = input("  Pick up what? (type a name, or press Enter to cancel): ").strip()
    if item_name:
        player.pick_up(item_name)


def handle_use_item(player):
    """Menu option 5: choose an inventory item and use it."""
    # SAFETY GUARD: nothing to use if the bag is empty.
    if player.inventory.is_empty():
        print("  [!] Your inventory is empty — nothing to use.")
        return

    player.inventory.list_items()
    item_name = input("  Use which item? (type a name, or press Enter to cancel): ").strip()
    if item_name:
        player.use_item(item_name)


def print_victory(player):
    """Celebration banner for reaching the Control Room."""
    print("\n  " + "*" * 44)
    print("     MISSION COMPLETE!")
    print(f"     {player.name} has reached the Control Room")
    print("     and restored command of the station.")
    print("  " + "*" * 44)
    print("     (Choose 7 - Exit Station to fly home.)\n")


def show_menu():
    """Print the main action menu."""
    print("  ---------------- MAIN MENU ----------------")
    print("   1. Look around")
    print("   2. Move (north / south / east / west)")
    print("   3. Pick up an item")
    print("   4. View inventory")
    print("   5. Use an item")
    print("   6. Check status")
    print("   7. Exit station")
    print("  -------------------------------------------")


# =====================================================================
#  THE MAIN GAME LOOP
# =====================================================================

def game():
    """Set up the world, create the player, and run the menu loop."""
    print("\n" + "=" * 46)
    print("     SCI-FI STATION CRAWLER")
    print("     You wake in the airlock. The captain is missing.")
    print("=" * 46)

    cadet_name = input("\n  State your name, cadet: ").strip() or "Cadet"
    starting_room = build_world()          # the world exists first...
    hero = Player(cadet_name, starting_room)  # ...then the player is placed in it
    # OOP CONCEPT: hero.current_room now holds a reference to a Room object.

    print(f"\n  Welcome aboard, {hero.name}. Good luck out there.")
    hero.current_room.get_details()

    # ------------------- play until the player quits -------------------
    while True:
        show_menu()
        choice = input("  Choose an option (1-7): ").strip()

        if choice == "1":
            hero.current_room.get_details()
        elif choice == "2":
            handle_move(hero)
        elif choice == "3":
            handle_pick_up(hero)
        elif choice == "4":
            hero.inventory.list_items()
        elif choice == "5":
            handle_use_item(hero)
        elif choice == "6":
            hero.get_status()
        elif choice == "7":
            break  # leave the loop → the game ends
        else:
            print("  [!] Invalid choice — please type a number from 1 to 7.")

        # --- lose condition: checked after every action ----------------
        if hero.is_defeated():
            print("\n  [x] GAME OVER — your vitals flatline in the dark...")
            break

    if hero.is_defeated():
        print("\n  The station's lights flicker out behind you.")
    else:
        print("\n  Docking clamps release. You drift home among the stars.")
    print("  Thanks for playing the Sci-Fi Station Crawler!\n")


if __name__ == "__main__":
    try:
        game()
    except KeyboardInterrupt:
        # Pressing Ctrl+C quits cleanly instead of dumping a scary traceback.
        print("\n\n  Emergency escape pod launched. (Game closed with Ctrl+C)")
