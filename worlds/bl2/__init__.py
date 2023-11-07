from typing import Callable, Dict, NamedTuple, Optional, List, ClassVar

import settings
from BaseClasses import Region, Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import BL2Item, item_data_table, item_table
from .Locations import BL2Location, location_data_table, locked_locations
from .Options import bl2_options
#from .Regions import region_data_table
#from .Rules import rules_data

class BL2WebWorld(WebWorld):
    tutorials = []


class MyGameSettings(settings.Group):
    pass

class BL2Region(NamedTuple):
    connecting_regions: Optional[List[str]] = []


class MyGameWorld(World):
    """Insert description of the world/game here."""
    game = "Borderlands 2"  # name of the game/world
    option_definitions = bl2_options  # options the player can set
    settings: ClassVar[MyGameSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 0b010000100100110000110011
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = {}
    location_name_to_id = {name: id for
                           id, name in enumerate(location_data_table.keys(), base_id)}
 

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    # item_name_groups = {
    #     "weapons": {"sword", "lance"},
    # }

    def create_item(self, name: str, id: int):
        return BL2Item(name, item_data_table[name].type, id, self.player)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return BL2Item(event, ItemClassification.progression, None, self.player)

    def create_items(self):
        item_pool = []
        id = self.base_id
        for name, item in item_data_table.items():
            for i in range(item.quantity):
                if item.can_create(self.multiworld, self.player):
                    item_pool.append(self.create_item(name, id))
                    id += 1
        self.multiworld.itempool += item_pool

    def create_regions(self):
        # Create regions.
        region_data_table = {"Menu": BL2Region()}
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        self.location_name_to_id["Click 10"] = None
        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({
                location_name: self.location_name_to_id[location_name] for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self.multiworld, self.player)
            }, BL2Location)
            region.add_exits(region_data_table[region_name].connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self.multiworld, self.player):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)

    def get_filler_item_name(self):
        return "Item_White"

    def generate_basic(self):
        self.multiworld.get_location("Click 10", self.player).place_locked_item(self.create_event("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
