from typing import Dict
from Options import Toggle, Range, Choice, PerGameCommonOptions

class Goal(Choice):
    """Customize your button! Now available in 12 unique colors."""
    display_name = "Button Color"
    option_bnk3r = 0
    option_warrior = 1
    default = 1

bl2_options = {
  "goal": Goal,
}