"""
item.py — The base Item class and its specialized subclasses.

TEACHING FOCUS: Inheritance & Polymorphism
    * MedKit and Keycard both INHERIT from Item (each one IS-A Item).
    * Each subclass OVERRIDES the use() method with its own behavior.
    * When other code calls item.use(player), Python automatically runs
      the correct version. That automatic selection is POLYMORPHISM.

Grade 9 OOP Exemplar — Sci-Fi Station Crawler
"""


class Item:
    """Any object that can sit on a Room floor or inside an Inventory."""

    def __init__(self, name: str, description: str, consumable=True):
        # OOP CONCEPT: Encapsulation — every Item object manages its own data.
        self.name = name
        self.description = description
        # 'consumable' stores a BEHAVIOR RULE as DATA:
        #   True  -> the item disappears after it is used (MedKit)
        #   False -> the item stays after use (Keycard)
        self.consumable = consumable

    def use(self, target_player):
        """The base version of use().

        Subclasses OVERRIDE this method. If a subclass ever forgets to,
        this safe default runs instead of crashing the game.
        """
        print(f"  {self.name} does nothing special.")


class MedKit(Item):
    """A medical kit that heals the player. IS-A Item (inherits from Item)."""

    def __init__(self, heal_amount=30):
        # OOP CONCEPT: Inheritance — super().__init__() calls the PARENT
        # constructor so Item can set up name/description for us. A MedKit
        # only adds what is NEW about itself: its heal_amount.
        super().__init__("MedKit", "Restores health.", consumable=True)
        self.heal_amount = heal_amount

    def use(self, target_player):
        """OVERRIDE of Item.use() — this is polymorphism in action."""
        print(f"  {target_player.name} applies the {self.name}...")
        # OOP CONCEPT: Encapsulation — we ask the Player object to heal
        # itself through its heal() METHOD. We never edit
        # target_player.health directly from outside the Player class.
        target_player.heal(self.heal_amount)


class Keycard(Item):
    """A security card that can open locked doors. IS-A Item."""

    def __init__(self, clearance_level=1):
        super().__init__(
            "Keycard",
            f"Security keycard (clearance level {clearance_level}).",
            consumable=False,  # keycards are NOT consumed when used
        )
        self.clearance_level = clearance_level

    def use(self, target_player):
        """OVERRIDE of Item.use() — same method name, different behavior."""
        print(f"  The scanner reads {target_player.name}'s {self.name}:")
        print(f"    Clearance level : {self.clearance_level}")
        print(f"    Door access     : level {self.clearance_level} and below")
