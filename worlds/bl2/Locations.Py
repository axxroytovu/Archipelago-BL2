from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Location, MultiWorld

class BL2Location(Location):  # or from Locations import MyGameLocation
    game = "Borderlands 2"  # name of the game/world this location is in

class BL2LocationData(NamedTuple):
    region: str
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    locked_item: Optional[bool] = None

location_data_table = {f"Click {n}": BL2LocationData(region="Menu") for n in range(1, 11)}
locked_locations = {}
