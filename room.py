"""
room.py — one location on the station map.

TEACHING FOCUS: Composition (HAS-MANY) & Object References
    * A Room HAS-MANY Items (its list holds real Item objects).
    * A Room's exits dict holds REFERENCES to other Room objects —
      that is how rooms link together into a map.
    * A Room never stores the Player. The PLAYER holds a reference to
      the room they are in (player.current_room). One direction only —
      this keeps the design simple and bug-free.

Grade 9 OOP Exemplar — Sci-Fi Station Crawler
"""


class Room:
    """A single location: it holds items, exits, and optional game rules."""

    def __init__(self, name: str, description: str,
                 hazard_damage=0, locked=False, required_clearance=0):
        self.name = name
        self.description = description

        # OOP CONCEPT: Class Composition — Room HAS-MANY Items.
        self.items = []

        # Maps a direction word to a neighbouring Room OBJECT, e.g.
        # {"north": med_bay_room}. The VALUES are object references.
        self.exits = {}

        # --- optional game-rule DATA (the rules are enforced by main.py) ---
        self.hazard_damage = hazard_damage        # HP lost when you enter
        self.locked = locked                      # True = door needs a keycard
        self.required_clearance = required_clearance

    def connect_room(self, direction: str, room_object):
        """Link this room to another Room object (a one-way link)."""
        self.exits[direction.lower()] = room_object

    def add_item(self, item):
        """Place an Item object on the floor of this room."""
        self.items.append(item)

    def remove_item(self, item_name: str):
        """Take an Item off the floor. Returns the Item, or None."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                return item
        return None

    def get_details(self):
        """Print everything a player can perceive in this room."""
        print("\n  " + "=" * 44)
        print(f"   {self.name.upper()}")
        print("  " + "=" * 44)
        print(f"   {self.description}")

        if self.hazard_damage > 0:
            print(f"   [!] WARNING: hazardous zone! Entering costs {self.hazard_damage} HP.")

        if self.locked:
            print(f"   [!] This door is LOCKED (needs keycard clearance level {self.required_clearance}).")

        if self.items:
            print("\n   You see on the floor:")
            for item in self.items:
                print(f"     - {item.name}: {item.description}")
        else:
            print("\n   Nothing useful lies on the floor here.")

        # OOP CONCEPT: the exits dict stores OBJECT REFERENCES, so simply
        # joining its keys lists every direction you can travel.
        print(f"\n   Exits: {', '.join(self.exits)}")
        print("  " + "=" * 44 + "\n")
