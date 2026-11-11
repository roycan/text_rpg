"""
player.py — the character the human controls.

TEACHING FOCUS: Composition & Encapsulation
    * A Player HAS-A Inventory (composition: the Player creates and owns it).
    * A Player HAS-A reference to the Room they are currently in.
    * Health is changed ONLY through methods (heal / take_damage), so the
      value can never escape its 0..100 safety range.

Grade 9 OOP Exemplar — Sci-Fi Station Crawler
"""

from inventory import Inventory  # needed so a Player can create an Inventory


class Player:
    """The station explorer: name, health, location, and an inventory."""

    MAX_HEALTH = 100  # a CLASS constant: one shared safety limit for every player

    def __init__(self, name: str, starting_room):
        """A new Player is born COMPLETE: with a name, full health,
        an inventory, AND a starting location.

        Good habit: constructors should produce a fully working object —
        not one that is broken until someone patches it up later.
        """
        self.name = name
        self.health = Player.MAX_HEALTH
        self.current_room = starting_room  # a reference to a Room object

        # OOP CONCEPT: Class Composition (Player HAS-A Inventory).
        # The Player object builds its own Inventory the moment it is born.
        self.inventory = Inventory(capacity=5)

    # ------------------------------------------------------ health & safety
    def heal(self, amount: int):
        """Increase health, clamped so it never exceeds MAX_HEALTH."""
        # min() is the clamp: health can never overshoot 100.
        self.health = min(self.health + amount, Player.MAX_HEALTH)
        print(f"  {self.name}'s health is now {self.health}/{Player.MAX_HEALTH}.")

    def take_damage(self, amount: int):
        """Decrease health, clamped so it never drops below 0."""
        # max() is the clamp: health can never go negative.
        self.health = max(self.health - amount, 0)
        print(f"  {self.name} takes {amount} damage! ({self.health}/{Player.MAX_HEALTH})")

    def is_defeated(self):
        """True when health has hit 0 (the game-over check for main.py)."""
        return self.health == 0

    # ------------------------------------------------------ item handling
    def pick_up(self, item_name: str):
        """Transfer an Item object from the current Room into the inventory.

        OOP CONCEPT: Object Reference & State Transfer (Moving items
        between Room and Inventory). The SAME Item object changes owner:
        out of the Room's list, into the Inventory's list. We move the
        reference — we never copy the object.
        """
        # SAFETY FIRST: check bag space BEFORE touching the room.
        # (If we removed the item from the room first and THEN discovered
        #  the bag was full, the item would be lost in limbo — owned by
        #  nobody! Checking first makes the transfer safe.)
        if self.inventory.is_full():
            print("  [!] Your inventory is full. Use something or move on.")
            return

        item = self.current_room.remove_item(item_name)
        if item is None:
            print(f"  [!] There is no '{item_name}' on the floor here.")
            return

        self.inventory.add_item(item)  # guaranteed to fit — we checked above

    def use_item(self, item_name: str):
        """Use an item from the inventory ON THIS PLAYER."""
        # SAFETY GUARD: never use an item you do not carry.
        if self.inventory.is_empty():
            print("  [!] Your inventory is empty — nothing to use.")
            return

        item = self.inventory.get_item(item_name)
        if item is None:
            print(f"  [!] You have no '{item_name}' in your inventory.")
            return

        # OOP CONCEPT: Polymorphic Method Calling (item.use(self)).
        # We do NOT test whether the item is a MedKit or a Keycard.
        # We just call use() and Python automatically runs the correct
        # overridden method for whichever object the item happens to be.
        item.use(self)

        # The item's own DATA decides what happens next:
        # consumables disappear after use, reusables stay.
        if item.consumable:
            self.inventory.remove_item(item.name)
            print(f"  ({item.name} was consumed.)")

    # ------------------------------------------------------ display
    def get_status(self):
        """Print a health bar, the current room, and a load summary."""
        bar_width = 20
        filled_blocks = int(self.health / Player.MAX_HEALTH * bar_width)
        # Building the bar from '#' and '-' needs no external libraries.
        health_bar = "#" * filled_blocks + "-" * (bar_width - filled_blocks)

        print("\n  ---------------- STATUS ----------------")
        print(f"  {self.name}")
        print(f"  Health : [{health_bar}] {self.health}/{Player.MAX_HEALTH}")
        print(f"  Room   : {self.current_room.name}")
        print(f"  Bag    : {len(self.inventory.items)}/{self.inventory.capacity} slots used")
        print("  ----------------------------------------\n")
