"""
inventory.py — manages a collection of Item objects.

TEACHING FOCUS: Composition (HAS-MANY)
    * An Inventory HAS-MANY Items. It stores the real Item OBJECTS in a
      list — not their names — which is what lets us call item.use() later.
    * The Player will own exactly ONE Inventory (see player.py).

Grade 9 OOP Exemplar — Sci-Fi Station Crawler
"""


class Inventory:
    """A fixed-capacity backpack that holds Item objects."""

    def __init__(self, capacity=5):
        self.capacity = capacity
        # OOP CONCEPT: Class Composition — this list holds real Item OBJECTS.
        self.items = []

    def is_full(self):
        """True when there is no space left."""
        return len(self.items) >= self.capacity

    def is_empty(self):
        """True when nothing is carried (safety check before using items)."""
        return len(self.items) == 0

    def add_item(self, item):
        """Add an Item object if there is room.

        Returns True on success, False when the inventory is full.
        The boolean return lets OTHER objects react (e.g. Player.pick_up).
        """
        if self.is_full():
            print(f"  [!] Inventory full ({self.capacity}/{self.capacity}). No room for {item.name}.")
            return False
        self.items.append(item)
        print(f"  [+] Packed: {item.name}")
        return True

    def remove_item(self, item_name: str):
        """Remove and return the first Item whose name matches.

        Matching is case-insensitive, so "MEDKIT" finds "MedKit".
        Returns the Item object, or None if nothing matched.
        """
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                return item
        return None

    def get_item(self, item_name: str):
        """Find an Item by name WITHOUT removing it. Returns None if absent."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def list_items(self):
        """Print a neatly formatted list of everything being carried."""
        print("\n  ================== INVENTORY ==================")
        if self.is_empty():
            print("   (empty)")
        else:
            for index, item in enumerate(self.items, start=1):
                # f-string alignment: {item.name:<12} pads names to 12 letters
                print(f"   {index}. {item.name:<12} - {item.description}")
        print(f"   Capacity used: {len(self.items)}/{self.capacity}")
        print("  ===============================================\n")
