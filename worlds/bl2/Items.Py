from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification, MultiWorld

class BL2Item(Item):
    game = "Borderlands 2"


class BL2ItemData(NamedTuple):
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    quantity: int = 1


item_data_table = {"Item_White": BL2ItemData(quantity=9)}
item_table = []
for name, data in item_data_table.items():
    item_table += [name] * data.quantity
