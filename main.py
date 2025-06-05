import pygame
import sys
import os
import json
import math
import time

pygame.init()

# -------------------------------------------------------------------------------
# 1. RESOURCE PATH HELPERS
# -------------------------------------------------------------------------------
def resource_path(relative_path):
    """
    Return absolute path to resource, works for development and for PyInstaller EXE.
    """
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base, relative_path)

# -------------------------------------------------------------------------------
# 2. SAVE & LOAD FUNCTIONS
# -------------------------------------------------------------------------------
def get_save_file_path():
    """
    Return the path to 'saves/save.json' under the project folder.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, "saves")
    os.makedirs(save_dir, exist_ok=True)
    return os.path.join(save_dir, "save.json")

def save_game(state: dict):
    """
    Write the entire game state dictionary to 'saves/save.json'.
    """
    path = get_save_file_path()
    try:
        with open(path, "w") as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Error saving game to {path}: {e}")

def load_game():
    """
    Load game state from 'saves/save.json'. Return None if no valid save exists.
    """
    path = get_save_file_path()
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading game from {path}: {e}")
        return None

# -------------------------------------------------------------------------------
# 3. UI UTILITIES
# -------------------------------------------------------------------------------
def format_number_parts(n):
    """
    Split a number into a mantissa and suffix (e.g., 1,234,000 → ("1.234", "Million")).
    """
    units = [
        " ", " Thousand", " Million", " Billion", " Trillion", " Quadrillion",
        " Quintillion", " Sextillion", " Septillion", " Octillion", " Nonillion",
        " Decillion", " Undecillion", " Duodecillion", " Tredécillion",
        " Quattuordecillion", " Quindecillion", " Sexdecillion",
        " Septendecillion", " Octodecillion", " Novemdecillion", " Vigintillion",
        " Unvigintillion", " Duovigintillion", " Trevigintillion",
        " Quattuorvigintillion", " Quinvigintillion", " Sexvigintillion",
        " Septenvigintillion", " Octovigintillion", " Novemnovigintillion",
        " Trigintillion", " Untrigintillion", " Duotrigintillion",
        " Trestrigintillion", " Quattuortrigintillion", " Quintrigintillion",
        " Sextrigintillion", " Septentrigintillion", " Octotrigintillion",
        " Novemtrigintillion", " Quadragintillion", " Unquadragintillion",
        " Duoquadragintillion", " Trequadragintillion", " Quattuorquadragintillion",
        " Quinquadragintillion", " Sexquadragintillion", " Septenquadragintillion",
        " Octoquadragintillion", " Novemquadragintillion", " Quinquagintillion",
        " Unquinquagintillion", " Duoquinquagintillion", " Trequinquagintillion",
        " Quattuorquinquagintillion", " Quinquinquagintillion", " Sexquinquagintillion",
        " Septenquinquagintillion", " Octoquinquagintillion", " Novemquinquagintillion",
        " Sexagintillion", " Unsexagintillion", " Duosexagintillion", " Tresexagintillion",
        " Quattuorsexagintillion", " Quinsexagintillion", " Sexsexagintillion",
        " Septensexagintillion", " Octosexagintillion", " Novemsexagintillion",
        " Septuagintillion", " Unseptuagintillion", " Duoseptuagintillion",
        " Treseptuagintillion", " Quattuorseptuagintillion", " Quinseptuagintillion",
        " Sexseptuagintillion", " Septenseptuagintillion", " Octoseptuagintillion",
        " Novemseptuagintillion", " Octogintillion", " Unoctogintillion",
        " Duooctogintillion", " Treoctogintillion", " Quattuoroctogintillion",
        " Quinoctogintillion", " Sexoctogintillion", " Septenoctogintillion",
        " Octooctogintillion", " Novemoctogintillion", " Nonagintillion",
        " Unnonagintillion", " Duononagintillion", " Trenonagintillion",
        " Quattuornonagintillion", " Quinnonagintillion", " Sexnonagintillion",
        " Septennonagintillion", " Octononagintillion", " Novemnonagintillion",
        " Centillion"
    ]
    scale = 0
    val = float(n)
    while abs(val) >= 1000.0 and scale < len(units) - 1:
        val /= 1000.0
        scale += 1
    mantissa = f"{val:.3f}"
    suffix = units[scale]
    return mantissa, suffix

def total_cost_for_next_N(biz, N):
    """
    Return the total cost to purchase N more of business 'biz', given its current owned count.
    """
    owned = biz["owned"]
    b0 = biz["base_cost"] * (biz["coef"] ** owned)
    if N == 0:
        return 0
    if biz["coef"] == 1:
        return int(b0 * N)
    numerator   = (biz["coef"] ** N) - 1
    denom       = biz["coef"] - 1
    total_cost  = b0 * (numerator / denom)
    return int(total_cost)

def max_affordable(biz, money_available):
    """
    Return the maximum number of biz items you can purchase with 'money_available'.
    """
    owned = biz["owned"]
    base_term = biz["base_cost"] * (biz["coef"] ** owned)
    if base_term == 0:
        return 0
    rhs = 1 + (money_available * (biz["coef"] - 1) / base_term)
    if rhs <= 1:
        return 0
    N = int(math.log(rhs, biz["coef"]))
    return max(0, N)

def format_time(seconds_left):
    """
    Format a float number of seconds as MM:SS.
    """
    secs = max(0, int(seconds_left))
    minutes = secs // 60
    seconds = secs % 60
    return f"{minutes:02d}:{seconds:02d}"

# -------------------------------------------------------------------------------
# 4. OFFLINE EARNINGS CALCULATION
# -------------------------------------------------------------------------------
def calculate_offline_earnings(data_loaded: dict, now_ts: float):
    """
    Compute earnings while offline for every owned business (whether or not it has a manager).
    """
    last_ts = data_loaded.get("last_timestamp", now_ts)
    offline_seconds = max(0.0, now_ts - last_ts)

    total_offline_earn = 0
    global_speed_mult   = data_loaded.get("global_speed_mult", 1.0)
    global_profit_mult  = data_loaded.get("global_profit_mult", 1.0)
    galactic_investors_total = data_loaded.get("galactic_investors_total", 0)

    for i, biz_saved in enumerate(data_loaded["businesses"]):
        owned = biz_saved["owned"]
        if owned <= 0:
            continue

        base_time      = biz_saved["base_time"]
        speed_mult     = biz_saved["speed_mult"]
        effective_time = (base_time / speed_mult) / global_speed_mult
        if effective_time <= 0:
            continue

        cycles = math.floor(offline_seconds / effective_time)
        one_cycle_value = biz_saved["base_payout"] * owned * biz_saved["profit_mult"] * global_profit_mult * (1.0 + 0.02 * galactic_investors_total)

        if cycles > 0:
            earned = one_cycle_value * cycles
            total_offline_earn += earned

            remainder = offline_seconds - (cycles * effective_time)
            if biz_saved.get("has_manager", False):
                if remainder >= effective_time:
                    total_offline_earn += one_cycle_value
                    biz_saved["in_progress"] = True
                    biz_saved["timer"] = effective_time - (remainder - effective_time)
                else:
                    biz_saved["in_progress"] = True
                    biz_saved["timer"] = effective_time - remainder
            else:
                if remainder >= effective_time:
                    total_offline_earn += one_cycle_value
                    biz_saved["in_progress"] = False
                    biz_saved["timer"] = 0.0
                else:
                    biz_saved["in_progress"] = True
                    biz_saved["timer"] = effective_time - remainder

            continue

        saved_timer = biz_saved.get("timer", 0.0)
        if saved_timer > 0:
            new_timer = saved_timer - offline_seconds
            if new_timer <= 0:
                total_offline_earn += one_cycle_value
                biz_saved["in_progress"] = False
                biz_saved["timer"] = 0.0
            else:
                biz_saved["in_progress"] = True
                biz_saved["timer"] = new_timer

    data_loaded["money"] += total_offline_earn
    data_loaded["space_lifetime_earnings"] += total_offline_earn
    data_loaded["last_timestamp"] = now_ts

    return total_offline_earn

# -------------------------------------------------------------------------------
# 5. DEFAULT GAME STATE
# -------------------------------------------------------------------------------
def default_game_state():
    """
    Returns a fresh initial game state dictionary with all needed fields.
    """
    return {
        "money": 5.0,
        "space_lifetime_earnings": 0,
        "global_speed_mult": 1.0,
        "global_profit_mult": 1.0,
        "last_timestamp": time.time(),
        "galactic_investors_total": 0,
        "galactic_investors_spent": 0,
        "businesses": [],
        "upgrades": [],
        "unlocked_shown": [],
        "galactic_upgrades": []
    }

# -------------------------------------------------------------------------------
# 6. PYGAME SETUP & ICON
# -------------------------------------------------------------------------------
WIDTH, HEIGHT = 1200, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("SpaceRace")

# Load & set window icon (using starlightfarm.png if available)
icon_path = resource_path("assets/starlightfarm.png")
if os.path.isfile(icon_path):
    try:
        raw_icon = pygame.image.load(icon_path).convert_alpha()
        icon_surf = pygame.transform.smoothscale(raw_icon, (96, 96))
        pygame.display.set_icon(icon_surf)
    except Exception as e:
        print(f"Failed to load or scale window icon: {e}")
else:
    print("Icon file not found at:", icon_path)

FPS = 60
clock = pygame.time.Clock()

WHITE              = (235, 235, 245)
ACCENT             = (82, 130, 255)
BG_DARK            = (30, 32, 41)
PANEL_DARK         = (42, 44, 58)
SIDEBAR_BG         = (36, 37, 50)
BUSINESS_BG        = (48, 52, 70)
BUSINESS_BG_LOCKED = (38, 40, 50)
PROGRESS_BG        = (40, 44, 55)
PROGRESS_FILL      = (90, 200, 150)
DARKER_GREEN       = (0, 100, 0, 120)
BTN_HOVER          = (90, 110, 200)
GRAYED             = (110, 110, 120)
YELLOW             = (255, 200, 100)
RED_DOT            = (220, 50, 50)

font_big   = pygame.font.SysFont(None, 44)
font_med   = pygame.font.SysFont(None, 32)
font_small = pygame.font.SysFont(None, 20)

# Scroll offsets & dragging state
business_scroll      = 0
manager_scroll       = 0
upgrade_scroll       = 0
unlock_scroll        = 0
investor_shop_scroll = 0
investor_shop_dragging = False
investor_shop_drag_offset = 0

manager_dragging      = False
manager_drag_offset   = 0
upgrade_dragging      = False
upgrade_drag_offset   = 0
unlock_dragging       = False
unlock_drag_offset    = 0

SIDEBAR_WIDTH  = 180
HEADER_HEIGHT  = 80
PANEL_X        = SIDEBAR_WIDTH + 20
PANEL_Y        = HEADER_HEIGHT + 20
PANEL_WIDTH    = WIDTH - PANEL_X - 20
PANEL_HEIGHT   = HEIGHT - PANEL_Y - 20
ROW_HEIGHT     = 110
ROW_GAP        = 16
INVESTOR_ICON_SIZE = 58
ENTRY_PADDING      = 20

prestige_count = 0

overlay_mode        = None
last_overlay_mode   = None
show_investor_shop  = False


# Add X50 and X100, keep MAX as -1
purchase_options = [1, 5, 10, 50, 100, -1]
purchase_index   = 0

popup_message          = None
popup_end_time         = 0
first_time_popup       = False
first_time_popup_rect  = None
first_time_popup_close = None

# ────────────────────────────────────────────────────────────────────────────────
# Keep track of which upgrades were affordable the last time Upgrades tab was viewed
# ────────────────────────────────────────────────────────────────────────────────
prev_affordable_upgrades = set()

# -------------------------------------------------------------------------------
# 7. BUSINESS DEFINITIONS
# -------------------------------------------------------------------------------
units = [
    " ",                      # 10^0
    " Thousand",              # 10^3
    " Million",               # 10^6
    " Billion",               # 10^9
    " Trillion",              # 10^12
    " Quadrillion",           # 10^15
    " Quintillion",           # 10^18
    " Sextillion",            # 10^21
    " Septillion",             # 10^24
    " Octillion",             # 10^27
    " Nonillion",             # 10^30
    " Decillion",             # 10^33
    " Undecillion",           # 10^36
    " Duodecillion",          # 10^39
    " Tredécillion",          # 10^42
    " Quattuordecillion",     # 10^45
    " Quindecillion",         # 10^48
    " Sexdecillion",          # 10^51
    " Septendecillion",       # 10^54
    " Octodecillion",         # 10^57
    " Novemdecillion",        # 10^60
    " Vigintillion",          # 10^63
    " Unvigintillion",        # 10^66
    " Duovigintillion",       # 10^69
    " Trevigintillion",       # 10^72
    " Quattuorvigintillion",  # 10^75
    " Quinvigintillion",      # 10^78
    " Sexvigintillion",       # 10^81
    " Septenvigintillion",    # 10^84
    " Octovigintillion",      # 10^87
    " Novemvigintillion",     # 10^90
    " Trigintillion",         # 10^93
    " Untrigintillion",       # 10^96
    " Duotrigintillion",      # 10^99
    " Trestrigintillion",     # 10^102
    " Quattuortrigintillion", # 10^105
    " Quintrigintillion",     # 10^108
    " Sextrigintillion",      # 10^111
    " Septentrigintillion",   # 10^114
    " Octotrigintillion",     # 10^117
    " Novemtrigintillion",    # 10^120
    " Quadragintillion",      # 10^123
    " Unquadragintillion",    # 10^126
    " Duoquadragintillion",   # 10^129
    " Trequadragintillion",   # 10^132
    " Quattuorquadragintillion", # 10^135
    " Quinquadragintillion",  # 10^138
    " Sexquadragintillion",   # 10^141
    " Septenquadragintillion",# 10^144
    " Octoquadragintillion",  # 10^147
    " Novemquadragintillion", # 10^150
    " Quinquagintillion",     # 10^153
    " Unquinquagintillion",   # 10^156
    " Duoquinquagintillion",  # 10^159
    " Trequinquagintillion",  # 10^162
    " Quattuorquinquagintillion", # 10^165
    " Quinquinquagintillion", # 10^168
    " Sexquinquagintillion",  # 10^171
    " Septenquinquagintillion",# 10^174
    " Octoquinquagintillion", # 10^177
    " Novemquinquagintillion",# 10^180
    " Sexagintillion",        # 10^183
    " Unsexagintillion",      # 10^186
    " Duosexagintillion",     # 10^189
    " Tresexagintillion",     # 10^192
    " Quattuorsexagintillion",# 10^195
    " Quinsexagintillion",    # 10^198
    " Sexsexagintillion",     # 10^201
    " Septensexagintillion",  # 10^204
    " Octosexagintillion",    # 10^207
    " Novemsexagintillion",   # 10^210
    " Septuagintillion",      # 10^213
    " Unseptuagintillion",    # 10^216
    " Duoseptuagintillion",   # 10^219
    " Treseptuagintillion",   # 10^222
    " Quattuorseptuagintillion", # 10^225
    " Quinseptuagintillion",  # 10^228
    " Sexseptuagintillion",   # 10^231
    " Septenseptuagintillion",# 10^234
    " Octoseptuagintillion",  # 10^237
    " Novemseptuagintillion", # 10^240
    " Octogintillion",        # 10^243
    " Unoctogintillion",      # 10^246
    " Duooctogintillion",     # 10^249
    " Treoctogintillion",     # 10^252
    " Quattuoroctogintillion",# 10^255
    " Quinoctogintillion",    # 10^258
    " Sexoctogintillion",     # 10^261
    " Septenoctogintillion",  # 10^264
    " Octooctogintillion",    # 10^267
    " Novemoctogintillion",   # 10^270
    " Nonagintillion",        # 10^273
    " Unnonagintillion",      # 10^276
    " Duononagintillion",     # 10^279
    " Trenonagintillion",     # 10^282
    " Quattuornonagintillion",# 10^285
    " Quinnonagintillion",    # 10^288
    " Sexnonagintillion",     # 10^291
    " Septennonagintillion",  # 10^294
    " Octononagintillion",    # 10^297
    " Novemnonagintillion",   # 10^300
    " Centillion"             # 10^303
]


# -----------------------------------
# Upgrades list (sorted by cost ascending)
# -----------------------------------
# -------------------------------------------------------------------------------
# 7. BUSINESS DEFINITIONS
# -------------------------------------------------------------------------------
businesses = [
    {
        "index": 0,
        "name": "Asteroid Miner",
        "icon": "🪨",
        "icon_color": (165, 165, 175),
        "owned": 0,
        "base_time": 1.8,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 1,
        "profit_mult": 1.0,
        "base_cost": 4,
        "coef": 1.07,
        "unlocked": True,
        "manager_cost": 1000,
        "has_manager": False,
        "asset_path": "assets/asteroidminer.png"
    },
    {
        "index": 1,
        "name": "Satellite Network",
        "icon": "🛰️",
        "icon_color": (140, 190, 255),
        "owned": 0,
        "base_time": 9.0,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 60,
        "profit_mult": 1.0,
        "base_cost": 60,
        "coef": 1.15,
        "unlocked": False,
        "manager_cost": 15000,
        "has_manager": False,
        "asset_path": "assets/satellitenetwork.png"
    },
    {
        "index": 2,
        "name": "Rocket Yard",
        "icon": "🚀",
        "icon_color": (200, 130, 255),
        "owned": 0,
        "base_time": 18.0,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 540,
        "profit_mult": 1.0,
        "base_cost": 720,
        "coef": 1.14,
        "unlocked": False,
        "manager_cost": 100_000,
        "has_manager": False,
        "asset_path": "assets/rocketyard.png"
    },
    {
        "index": 3,
        "name": "Lunar Colony",
        "icon": "🌑",
        "icon_color": (210, 210, 200),
        "owned": 0,
        "base_time": 36.0,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 4320,
        "profit_mult": 1.0,
        "base_cost": 8640,
        "coef": 1.13,
        "unlocked": False,
        "manager_cost": 500_000,
        "has_manager": False,
        "asset_path": "assets/lunarcolony.png"
    },
    {
        "index": 4,
        "name": "Starlight Farm",
        "icon": "✨",
        "icon_color": (240, 240, 180),
        "owned": 0,
        "base_time": 72.0,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 51840,
        "profit_mult": 1.0,
        "base_cost": 103_680,
        "coef": 1.12,
        "unlocked": False,
        "manager_cost": 1_200_000,
        "has_manager": False,
        "asset_path": "assets/starlightfarm.png"
    },
    {
        "index": 5,
        "name": "Alien Outpost",
        "icon": "👾",
        "icon_color": (180, 250, 160),
        "owned": 0,
        "base_time": 288.0,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 622080,
        "profit_mult": 1.0,
        "base_cost": 1_244_160,
        "coef": 1.11,
        "unlocked": False,
        "manager_cost": 10_000_000,
        "has_manager": False,
        "asset_path": "assets/alienoutpost.png"
    },
    {
        "index": 6,
        "name": "Solar Array",
        "icon": "☀️",
        "icon_color": (255, 255, 120),
        "owned": 0,
        "base_time": 1152.0,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 7_464_960,
        "profit_mult": 1.0,
        "base_cost": 14_929_920,
        "coef": 1.10,
        "unlocked": False,
        "manager_cost": 111_111_111,
        "has_manager": False,
        "asset_path": "assets/solararray.png"
    },
    {
        "index": 7,
        "name": "Black Hole Labs",
        "icon": "🌀",
        "icon_color": (90, 90, 180),
        "owned": 0,
        "base_time": 4608.0,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 89_579_520,
        "profit_mult": 1.0,
        "base_cost": 179_159_040,
        "coef": 1.09,
        "unlocked": False,
        "manager_cost": 555_555_555,
        "has_manager": False,
        "asset_path": "assets/blackholelabs.png"
    },
    {
        "index": 8,
        "name": "Wormhole Gate",
        "icon": "🕳️",
        "icon_color": (150, 80, 180),
        "owned": 0,
        "base_time": 18432.0,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 1_074_954_240,
        "profit_mult": 1.0,
        "base_cost": 2_149_908_480,
        "coef": 1.08,
        "unlocked": False,
        "manager_cost": 10_000_000_000,
        "has_manager": False,
        "asset_path": "assets/wormholegate.png"
    },
    {
        "index": 9,
        "name": "Galactic Senate",
        "icon": "🪐",
        "icon_color": (110, 180, 255),
        "owned": 0,
        "base_time": 110592.0,
        "speed_mult": 1.0,
        "timer": 0.0,
        "in_progress": False,
        "base_payout": 29_668_737_024,
        "profit_mult": 1.0,
        "base_cost": 25_798_901_760,
        "coef": 1.07,
        "unlocked": False,
        "manager_cost": 100_000_000_000,
        "has_manager": False,
        "asset_path": "assets/galacticsenate.png"
    },
]

# -------------------------------------------------------------------------------
# 8. CASH-UPGRADES
# -------------------------------------------------------------------------------
upgrades = [
    {
        "biz_index":   0,
        "name":        "Quantum Drill Bit",
        "multiplier":  3,
        "cost":        250_000,
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Warp Resonator",
        "multiplier":  3,
        "cost":        500_000,
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Hyperfuel Injector",
        "multiplier":  3,
        "cost":        1_000_000,
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Lunar Regolith Refiner",
        "multiplier":  3,
        "cost":        5_000_000,
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Stellar Crop Enhancer",
        "multiplier":  3,
        "cost":        10_000_000,
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Alien Energy Core",
        "multiplier":  3,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Solar Flare Amplifier",
        "multiplier":  3,
        "cost":        50_000_000,
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Event Horizon Stabilizer",
        "multiplier":  3,
        "cost":        100_000_000,
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Quantum Tunnel Expander",
        "multiplier":  3,
        "cost":        250_000_000,
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Galactic Charter Reform",
        "multiplier":  3,
        "cost":        500_000_000,
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Spill Proof Tankers",
        "multiplier":  3,
        "cost":        250_000_000_000,    # $250 Billion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Novelty Straws",
        "multiplier":  3,
        "cost":        20_000_000_000_000, # $20 Trillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Sports Pages",
        "multiplier":  3,
        "cost":        50_000_000_000_000, # $50 Trillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Automatic Vacuums",
        "multiplier":  3,
        "cost":        100_000_000_000_000,# $100 Trillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Online Ordering",
        "multiplier":  3,
        "cost":        500_000_000_000_000,# $500 Trillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Donut Holes",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000,# $1 Quadrillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Shrimp Magnets",
        "multiplier":  3,
        "cost":        2_000_000_000_000_000,# $2 Quadrillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Energy Drink Sponsors",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000,# $5 Quadrillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Green Screens",
        "multiplier":  3,
        "cost":        7_000_000_000_000_000,# $7 Quadrillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Free Fancy Pens",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000,# $10 Quadrillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Eco-safe Pipeline",
        "multiplier":  3,
        "cost":        20_000_000_000_000_000,# $20 Quadrillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Monopsony",
        "multiplier":  3,
        "cost":        50_000_000_000_000_000,# $50 Quadrillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Holy Moola",
        "multiplier":  0.01,    # Angel Investor effectiveness +1%
        "cost":        100_000_000_000_000_000,# $100 Quadrillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Imported Ice Cubes",
        "multiplier":  3,
        "cost":        2_000_000_000_000_000_000,# $2 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Business Pages",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000,# $5 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Microfiber Sponges",
        "multiplier":  3,
        "cost":        7_000_000_000_000_000_000,# $7 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Drone Delivery",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000,# $10 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Bacon Sprinkles",
        "multiplier":  3,
        "cost":        20_000_000_000_000_000_000,# $20 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Carbon Nanotube Nets",
        "multiplier":  3,
        "cost":        35_000_000_000_000_000_000,# $35 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "GPS Puck Tracker",
        "multiplier":  3,
        "cost":        50_000_000_000_000_000_000,# $50 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Smell-O-Vision",
        "multiplier":  3,
        "cost":        75_000_000_000_000_000_000,# $75 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Credit Card Implants",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000,# $100 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Hyperloop Pumps",
        "multiplier":  3,
        "cost":        200_000_000_000_000_000_000,# $200 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Illuminati",
        "multiplier":  3,
        "cost":        500_000_000_000_000_000_000,# $500 Quintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Immaculate Consumption",
        "multiplier":  0.01,    # Angel Investor effectiveness +1%
        "cost":        1_000_000_000_000_000_000_000,# $1 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Combustible Lemons",
        "multiplier":  3,
        "cost":        25_000_000_000_000_000_000,# $25 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Gossip Pages",
        "multiplier":  3,
        "cost":        50_000_000_000_000_000_000,# $50 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Blue Sky Brand Wax",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000,# $100 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Caviar Stuffed Crust",
        "multiplier":  3,
        "cost":        200_000_000_000_000_000_000,# $200 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Free Coffee",
        "multiplier":  3,
        "cost":        300_000_000_000_000_000_000,# $300 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "3D Printed Shrimp",
        "multiplier":  3,
        "cost":        400_000_000_000_000_000_000,# $400 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Lord Stanley's Cup",
        "multiplier":  3,
        "cost":        500_000_000_000_000_000_000,# $500 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "James Camera",
        "multiplier":  3,
        "cost":        600_000_000_000_000_000_000,# $600 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Dogecoin",
        "multiplier":  3,
        "cost":        700_000_000_000_000_000_000,# $700 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Biodiesel Derricks",
        "multiplier":  3,
        "cost":        800_000_000_000_000_000_000,# $800 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Profit Prophet",
        "multiplier":  3,
        "cost":        900_000_000_000_000_000_000,# $900 Sextillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Eternal Revenue Service",
        "multiplier":  0.02,   # Angel Investor effectiveness +2%
        "cost":        10_000_000_000_000_000_000_000,# $10 Septillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Monopsony (II)",
        "multiplier":  4,
        "cost":        1_000_000_000_000_000_000_000_000,# $1 Quin·duodecillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Self Picking Lemons",
        "multiplier":  3,
        "cost":        25_000_000_000_000_000_000_000,# $25 Quattuordecillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Trust Buster Buster",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000_000,# $100 Quattuordecillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Bias Detector",
        "multiplier":  3,
        "cost":        250_000_000_000_000_000_000_000,# $250 Quattuordecillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "New Car Odorants",
        "multiplier":  3,
        "cost":        500_000_000_000_000_000_000_000,# $500 Quattuordecillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Pizzaception",
        "multiplier":  3,
        "cost":        750_000_000_000_000_000_000_000,# $750 Quattuordecillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Graham's Donut",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000,# $1 Quindecillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Shrimp Is Life",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000_000_000,# $5 Quindecillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Teeth Replacements",
        "multiplier":  3,
        "cost":        15_000_000_000_000_000_000_000_000,# $15 Quindecillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Post-Credit Neuralizer",
        "multiplier":  3,
        "cost":        50_000_000_000_000_000_000_000_000,# $50 Quindecillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "No Service Charges",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000_000_000,# $100 Quindecillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Zombie Proof Rigs",
        "multiplier":  3,
        "cost":        250_000_000_000_000_000_000_000_000,# $250 Quindecillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Unlimited Refills",
        "multiplier":  3,
        "cost":        500_000_000_000_000_000_000_000_000,# $500 Quindecillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Smiles Are Free",
        "multiplier":  7,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Sexdecillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Heavenly Tax Shelter",
        "multiplier":  5,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Septendecillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Employ Humanity",
        "multiplier":  7,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Novemdecillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Old Timey Charm",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Novemdecillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Matchbox Adapter",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $100 Novemdecillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Moxie Injections",
        "multiplier":  9,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Unvigintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Deep Dish 9",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Unvigintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Mug-Friendly Dippers",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $100 Unvigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Immortality Research",
        "multiplier":  11,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Tresvigintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Talk Like A Pirate",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Tresvigintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Kicking Soundtrack",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $100 Tresvigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Your Body Is Ready",
        "multiplier":  13,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Quattuorvigintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Crass Pandering",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Quattuorvigintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Golden Money Clip",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $100 Quattuorvigintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "A Towel",
        "multiplier":  15,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Quinvigintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Air Fresheners",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Quinvigintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Lemon Hope",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $100 Quinvigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "LOTS of Sticky Notes",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Septenvigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Pi Charts",
        "multiplier":  3.1415926,
        "cost":        3_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $3 Octovigintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Faux News",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Novemvigintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Free Bobblehead",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Novemvigintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Superfood Status",
        "multiplier":  3,
        "cost":        25_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $25 Novemvigintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "King Horton",
        "multiplier":  3,
        "cost":        50_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $50 Novemvigintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Deadliest Catcher",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $100 Novemvigintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Shiny Pucks",
        "multiplier":  3,
        "cost":        250_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $250 Novemvigintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Kitten Ushers",
        "multiplier":  3,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Novemvigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "+1% Interest",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Trigintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Asteroid Drillers",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Trigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Mass Thirst-eria",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Trigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Golden Parachute",
        "multiplier":  2,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Trigintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Black Tuesday Deals",
        "multiplier":  2,
        "cost":        2_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $2 Untrigintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Crash Memorial Sale",
        "multiplier":  2,
        "cost":        11_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $11 Untrigintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Patriotic Pizza",
        "multiplier":  2,
        "cost":        66_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $66 Untrigintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Open Holidays",
        "multiplier":  2,
        "cost":        230_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $230 Untrigintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Sheesh-kabobs",
        "multiplier":  2,
        "cost":        400_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $400 Untrigintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Capped Salaries",
        "multiplier":  2,
        "cost":        700_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $700 Untrigintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Pleasing Distractions",
        "multiplier":  2,
        "cost":        4_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $4 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Googol",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "2 Googols",
        "multiplier":  6,
        "cost":        20_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $20 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Bailouts For Everyone",
        "multiplier":  2,
        "cost":        29_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $29 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Pumping Freedom",
        "multiplier":  2,
        "cost":        145_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $145 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "'Merica Flavored",
        "multiplier":  2,
        "cost":        300_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $300 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Recession Progression",
        "multiplier":  2,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Capitaltastic",
        "multiplier":  5,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Treduotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Car Wash Focus",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Treduotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Enable Employees",
        "multiplier":  3,
        "cost":        150_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $150 Treduotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Diversify Brand",
        "multiplier":  3,
        "cost":        400_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $400 Treduotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Pizza Focus",
        "multiplier":  3,
        "cost":        900_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $900 Treduotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Adorable Mascot",
        "multiplier":  3,
        "cost":        6_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $6 Quattuortrigintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Free Bread Sticks",
        "multiplier":  3,
        "cost":        15_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $15 Quattuortrigintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Donut Focus",
        "multiplier":  2,
        "cost":        60_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $60 Quattuortrigintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Soylent Frosting",
        "multiplier":  3,
        "cost":        185_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $185 Quattuortrigintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Hand Made",
        "multiplier":  3,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Quattuortrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Stock Tips",
        "multiplier":  3,
        "cost":        600_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $600 Quattuortrigintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Shrimp Focus",
        "multiplier":  2,
        "cost":        750_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $750 Quattuortrigintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Tiny Top Hats",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Quintrigintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Shrimp Shaped Boats",
        "multiplier":  3,
        "cost":        45_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $45 Quintrigintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Hockey Focus",
        "multiplier":  3,
        "cost":        125_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $125 Quintrigintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Cloud Based Goalies",
        "multiplier":  3,
        "cost":        300_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $300 Quintrigintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Friendly Commissioner",
        "multiplier":  3,
        "cost":        900_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $900 Quintrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Cigar Shaped Mansion",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Sextrigintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Movie Focus",
        "multiplier":  2,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Sextrigintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Catered Lunches",
        "multiplier":  3,
        "cost":        70_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $70 Sextrigintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "More Sparkles",
        "multiplier":  3,
        "cost":        250_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $250 Sextrigintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Bank Focus",
        "multiplier":  3,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Sextrigintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Booth Banks",
        "multiplier":  3,
        "cost":        900_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $900 Sextrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "More Evil",
        "multiplier":  3,
        "cost":        3_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $3 Septentrigintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Oil Focus",
        "multiplier":  3,
        "cost":        15_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $15 Septentrigintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "All The Lobbyists",
        "multiplier":  3,
        "cost":        75_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $75 Septentrigintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Climate Sch-limate",
        "multiplier":  3,
        "cost":        400_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $400 Septentrigintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Lemon Focus",
        "multiplier":  3,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Septentrigintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Hybrid Lemons",
        "multiplier":  3,
        "cost":        750_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $750 Septentrigintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Money In The Stand",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Octotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Newspaper Focus",
        "multiplier":  3,
        "cost":        2_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $2 Octotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Self Advertising",
        "multiplier":  3,
        "cost":        20_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $20 Octotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Free Puppies",
        "multiplier":  3,
        "cost":        150_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $150 Octotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "The Capital Capital",
        "multiplier":  5,
        "cost":        350_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $350 Octotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Make It Storm",
        "multiplier":  3,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Octotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Printed On Money",
        "multiplier":  3,
        "cost":        700_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $700 Octotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Conflict Free Suds",
        "multiplier":  3,
        "cost":        950_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $950 Octotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Anti-Terrorism Toppings",
        "multiplier":  3,
        "cost":        4_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $4 Novemtrigintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Freedom Infused",
        "multiplier":  3,
        "cost":        9_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $9 Novemtrigintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Shrimply Amazing",
        "multiplier":  3,
        "cost":        24_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $24 Novemtrigintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Elocution Lessons",
        "multiplier":  3,
        "cost":        111_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $111 Novemtrigintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Drama Llamas",
        "multiplier":  3,
        "cost":        222_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $222 Novemtrigintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "You Can Bank On It",
        "multiplier":  3,
        "cost":        333_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $333 Novemtrigintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Oil/Oil Hybrid",
        "multiplier":  3,
        "cost":        444_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $444 Novemtrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Frosted Glasses",
        "multiplier":  3,
        "cost":        555_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $555 Novemtrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "A Sinister Proposal",
        "multiplier":  6.66,
        "cost":        666_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $666 Novemtrigintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Frankly Ridiculous",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Self-Fetching",
        "multiplier":  3,
        "cost":        3_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $3 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Mr. Sheen",
        "multiplier":  3,
        "cost":        6_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $6 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "It's Not Delivery",
        "multiplier":  3,
        "cost":        12_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $12 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Mmmmm... Sprinkles",
        "multiplier":  3,
        "cost":        24_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $24 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "The Shrimp Must Flow",
        "multiplier":  3,
        "cost":        48_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $48 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Heated Seats",
        "multiplier":  3,
        "cost":        96_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $96 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Movie-ception",
        "multiplier":  3,
        "cost":        192_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $192 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Fat Cat Scratch Post",
        "multiplier":  3,
        "cost":        384_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $384 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Sparkly Derricks",
        "multiplier":  3,
        "cost":        768_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $768 Quadragintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Haunted Trees",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Unquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Cross Promotions",
        "multiplier":  5,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Unquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Car Sweaters",
        "multiplier":  3,
        "cost":        2_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $2 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Free Candy",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Shakers",
        "multiplier":  3,
        "cost":        13_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $13 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Complementary Pretzels",
        "multiplier":  3,
        "cost":        29_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $29 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Mineral Infused",
        "multiplier":  3,
        "cost":        71_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $71 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Action Figures",
        "multiplier":  3,
        "cost":        177_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $177 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Public Access Publishing",
        "multiplier":  3,
        "cost":        250_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $250 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Pre-Screen Ads",
        "multiplier":  3,
        "cost":        310_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $310 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Holiday Specials",
        "multiplier":  3,
        "cost":        555_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $555 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Inspiring Documentary",
        "multiplier":  3,
        "cost":        736_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $736 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Lax Regulations",
        "multiplier":  2,
        "cost":        900_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $900 Duoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Slow News Day",
        "multiplier":  2,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Trequadragintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Sluggish Sales",
        "multiplier":  2,
        "cost":        95_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $95 Trequadragintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "10 for 1 Sale",
        "multiplier":  2,
        "cost":        213_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $213 Trequadragintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Sprinkle Fatigue",
        "multiplier":  2,
        "cost":        400_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $400 Trequadragintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Antihistamine Cocktails",
        "multiplier":  2,
        "cost":        985_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $985 Trequadragintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Ratings Slippage",
        "multiplier":  2,
        "cost":        8_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $8 Quattuorquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Anti-Piracy Measures",
        "multiplier":  2,
        "cost":        29_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $29 Quattuorquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Credit Union Smear Ads",
        "multiplier":  2,
        "cost":        222_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $222 Quattuorquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Raise Prices",
        "multiplier":  2,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Quattuorquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Suppress Iced Tea",
        "multiplier":  2,
        "cost":        900_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $900 Quattuorquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Restructuring",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Quinquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Price Reduction",
        "multiplier":  3,
        "cost":        136_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $136 Quinquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Sign Spinners",
        "multiplier":  3,
        "cost":        700_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $700 Quinquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Buzzing Signs",
        "multiplier":  3,
        "cost":        925_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $925 Quinquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Couch Cushions Check",
        "multiplier":  3,
        "cost":        3_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $3 Sexquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Tax Free Tuesdays",
        "multiplier":  3,
        "cost":        21_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $21 Sexquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Pollock Substitu(t)e",
        "multiplier":  3,
        "cost":        55_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $55 Sexquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Kids Watch Free",
        "multiplier":  3,
        "cost":        111_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $111 Sexquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Cheap Night",
        "multiplier":  3,
        "cost":        223_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $223 Sexquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "ReOrg",
        "multiplier":  3,
        "cost":        393_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $393 Sexquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Think Tanks",
        "multiplier":  3,
        "cost":        600_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $600 Sexquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Artificial Sugar",
        "multiplier":  3,
        "cost":        799_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $799 Sexquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Market Recovery",
        "multiplier":  3,
        "cost":        2_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $2 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Newspaper Ads",
        "multiplier":  3,
        "cost":        3_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $3 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Germaphobic Public",
        "multiplier":  3,
        "cost":        6_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $6 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Secret Ingredients",
        "multiplier":  3,
        "cost":        9_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $9 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Mildly Addictive",
        "multiplier":  3,
        "cost":        21_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $21 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Fad Diet",
        "multiplier":  3,
        "cost":        44_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $44 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Collectible Players",
        "multiplier":  3,
        "cost":        89_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $89 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Effective DRM",
        "multiplier":  3,
        "cost":        129_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $129 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Staff Parties",
        "multiplier":  3,
        "cost":        180_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $180 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Rollin' Coal Kits",
        "multiplier":  3,
        "cost":        210_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $210 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "3 Star Stands",
        "multiplier":  3,
        "cost":        300_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $300 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "'e' Business",
        "multiplier":  2.71828,
        "cost":        450_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $450 Septquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Inflate Demand",
        "multiplier":  5,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Octoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Life Saving Instructions",
        "multiplier":  5,
        "cost":        30_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $30 Octoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Lifetime Guarantees",
        "multiplier":  5,
        "cost":        180_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $180 Octoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Tax Free Savings",
        "multiplier":  5,
        "cost":        900_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $900 Octoquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Reading Club",
        "multiplier":  5,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Novemquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Gas Additives",
        "multiplier":  3,
        "cost":        20_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $20 Novemquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Vending Machines",
        "multiplier":  3,
        "cost":        80_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $80 Novemquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Only Moisture Source",
        "multiplier":  5,
        "cost":        240_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $240 Novemquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Hypnotic Jumbotrons",
        "multiplier":  5,
        "cost":        720_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $720 Novemquadragintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "More Superheros",
        "multiplier":  5,
        "cost":        21_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $21 Quinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Four Score",
        "multiplier":  4.444444444,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Quinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Shrimp Consultants",
        "multiplier":  2,
        "cost":        777_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $777 Quinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Yes Men",
        "multiplier":  2,
        "cost":        888_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $888 Quinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Rainbow Suds",
        "multiplier":  2,
        "cost":        999_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $999 Quinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Tinted Windows",
        "multiplier":  2,
        "cost":        2_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $2 Unquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Cloth Napkins",
        "multiplier":  2,
        "cost":        4_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $4 Unquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Pay At The Pump",
        "multiplier":  2,
        "cost":        8_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $8 Unquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Mood Lighting",
        "multiplier":  2,
        "cost":        16_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $16 Unquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Fresh Paint",
        "multiplier":  2,
        "cost":        32_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $32 Unquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "24 Hour Channel",  
        "multiplier":  2,
        "cost":        64_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $64 Unquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Self Serve Butter",
        "multiplier":  2,
        "cost":        128_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $128 Unquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Oh say, can you 'c'?",
        "multiplier":  2.99792458,
        "cost":        514_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $514 Unquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Sustainable Methods",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Biodegradable Pages",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Scan to Pay",
        "multiplier":  3,
        "cost":        25_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $25 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Wheelchair Ramps",
        "multiplier":  3,
        "cost":        50_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $50 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Clean Bathrooms",
        "multiplier":  3,
        "cost":        75_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $75 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Smog Recycling",
        "multiplier":  3,
        "cost":        100_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $100 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Memberships",
        "multiplier":  3,
        "cost":        150_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $150 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Themed Idle Game",
        "multiplier":  3,
        "cost":        200_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $200 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Vuvuzelas",
        "multiplier":  3,
        "cost":        300_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $300 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Partisan Documentaries",
        "multiplier":  3,
        "cost":        400_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $400 Duoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Optimize Prime",
        "multiplier":  2.35711,
        "cost":        900_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $900 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "The Great Movie Upgrade",
        "multiplier":  24,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Trequinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Abacus Upgrades",
        "multiplier":  2,
        "cost":        250_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $250 Trequinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "The Huge Newspaper Upgrade",
        "multiplier":  22,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Trequinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Reinvest Profits",
        "multiplier":  2,
        "cost":        750_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $750 Trequinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "The Big Car Wash Upgrade",
        "multiplier":  20,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Quattuorquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Placate Investors",
        "multiplier":  2,
        "cost":        250_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $250 Quattuorquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "The Fat Bank Upgrade",
        "multiplier":  18,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Quattuorquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Market Buzz",
        "multiplier":  2,
        "cost":        750_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $750 Quattuorquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "The Giant Shrimp Upgrade",
        "multiplier":  16,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Quinquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Break the Piggy Bank",
        "multiplier":  2,
        "cost":        250_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $250 Quinquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "The Massive Hockey Upgrade",
        "multiplier":  14,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Quinquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Bed Mattress Savings",
        "multiplier":  2,
        "cost":        750_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $750 Quinquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "The Vast Oil Upgrade",
        "multiplier":  12,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Sexquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Wad Patent",
        "multiplier":  2,
        "cost":        250_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $250 Sexquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "The Mega Lemon Upgrade",
        "multiplier":  10,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Sexquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Cornu Copiae",
        "multiplier":  2,
        "cost":        750_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $750 Sexquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "The X Large Pizza Upgrade",
        "multiplier":  8,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Septquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Faboulus Fiat",
        "multiplier":  2,
        "cost":        250_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $250 Septquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "The Jumbo Donut Upgrade",
        "multiplier":  4,
        "cost":        500_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $500 Septquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Positive Thinking Upgrade",
        "multiplier":  1.8,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Octoquinquagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "The Final Countdown?",
        "multiplier":  9.87654321,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Sexagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Cana-dough Exchange",
        "multiplier":  5,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Duosexagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Diamond Teeth",
        "multiplier":  3,
        "cost":        27_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $27 Tresexagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Discontinue Pennies",
        "multiplier":  4,
        "cost":        13_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $13 Quattuorsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "T-Shirts For All",
        "multiplier":  5,
        "cost":        2_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $2 Quinsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Wandering Magicians",
        "multiplier":  3,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Sexsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Neato Bike Fleet",
        "multiplier":  3,
        "cost":        14_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $14 Sexsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Double Ply Napkins",
        "multiplier":  3,
        "cost":        198_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $198 Sexsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Swivel Chair",
        "multiplier":  3,
        "cost":        322_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $322 Sexsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Skate Sharpeners",
        "multiplier":  3,
        "cost":        888_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $888 Sexsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Weather Proof Cameras",
        "multiplier":  3,
        "cost":        19_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $19 Septsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Tea for protestors",
        "multiplier":  3,
        "cost":        199_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $199 Septsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Condensation Supplements",
        "multiplier":  3,
        "cost":        233_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $233 Septsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "More Ads",
        "multiplier":  3,
        "cost":        421_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $421 Septsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "A Skyler",
        "multiplier":  3,
        "cost":        607_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $607 Septsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "GPS Tracked",
        "multiplier":  3,
        "cost":        777_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $777 Septsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Gravy Filled",
        "multiplier":  3,
        "cost":        910_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $910 Septsexagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "The Angel Investors",
        "multiplier":  0.02,   # +2% GI effectiveness
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Octosexagintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Superflous Motors",
        "multiplier":  3,
        "cost":        2_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $2 Octosexagintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Animated Shorts",
        "multiplier":  3,
        "cost":        45_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $45 Octosexagintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Free Calendars",
        "multiplier":  3,
        "cost":        200_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $200 Octosexagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Chocolate Money",
        "multiplier":  5,
        "cost":        600_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $600 Octosexagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "End",
        "multiplier":  0.015,  # +1.5% GI effectiveness
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Refrigerated Straws",
        "multiplier":  11,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Aerodynamic Field",
        "multiplier":  11,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Can Transform",
        "multiplier":  11,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Aerodynamic Crust",
        "multiplier":  11,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Crispy Protocols",
        "multiplier":  11,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Blended With Ice",
        "multiplier":  11,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Simpsons Did It",
        "multiplier":  11,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "More Musicals",
        "multiplier":  11,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Scratch N Sniff Notes",
        "multiplier":  11,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Stress Balls",
        "multiplier":  3,
        "cost":        10_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $10 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Lemon Scientists",
        "multiplier":  3,
        "cost":        150_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $150 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Crowd Sourced",
        "multiplier":  3,
        "cost":        166_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $166 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Soapier Soap",
        "multiplier":  3,
        "cost":        193_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $193 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Show Pony Pepperoni",
        "multiplier":  3,
        "cost":        410_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $410 Septuagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Times",
        "multiplier":  0.01,   # +1% GI effectiveness
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Skull Helmets",
        "multiplier":  3,
        "cost":        12_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $12 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Call In Cumberbatch",
        "multiplier":  3,
        "cost":        67_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $67 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Sassy Clerks",
        "multiplier":  3,
        "cost":        123_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $123 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Brand Makeover",
        "multiplier":  3,
        "cost":        321_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $321 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Cross The Stream-ables",
        "multiplier":  5,
        "cost":        555_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $555 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Rind Recycling",
        "multiplier":  3,
        "cost":        800_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $800 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Bamboo-based Paper",
        "multiplier":  3,
        "cost":        800_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $800 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Scifi Sound Effects",
        "multiplier":  3,
        "cost":        800_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $800 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   3,
        "name":        "Anti-Pizza Roof Sealant",
        "multiplier":  3,
        "cost":        900_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $900 Unseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   None,
        "name":        "Are",
        "multiplier":  2,
        "cost":        1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $1 Duoseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Still More Glaze",
        "multiplier":  3,
        "cost":        3_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $3 Duoseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Sailing Lessons",
        "multiplier":  3,
        "cost":        4_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $4 Duoseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Extra Slippery Ice",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Duoseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Soft Lighting",
        "multiplier":  3,
        "cost":        6_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $6 Duoseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Cartoonish Vaults",
        "multiplier":  3,
        "cost":        300_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $300 Duoseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Operation Oil-E",
        "multiplier":  3,
        "cost":        421_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $421 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   0,
        "name":        "Lemon Based Cleanse",
        "multiplier":  3,
        "cost":        600_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $600 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   1,
        "name":        "Controversial Headline",
        "multiplier":  3,
        "cost":        789_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $789 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   2,
        "name":        "Quick Queues",
        "multiplier":  3,
        "cost":        845_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $845 Duotrigintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "Asbestos Free",
        "multiplier":  3,
        "cost":        2_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $2 Treseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   4,
        "name":        "10,000 Folds",
        "multiplier":  3,
        "cost":        5_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $5 Treseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   5,
        "name":        "Harpoons",
        "multiplier":  3,
        "cost":        14_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $14 Treseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   6,
        "name":        "Robot Refs",
        "multiplier":  3,
        "cost":        54_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $54 Treseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   7,
        "name":        "Pretension Dampeners",
        "multiplier":  3,
        "cost":        108_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $108 Treseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   8,
        "name":        "Evil Business Cards",
        "multiplier":  3,
        "cost":        219_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $219 Treseptuagintillion
        "purchased":   False
    },
    {
        "biz_index":   9,
        "name":        "Helpful Wise Old Guy",
        "multiplier":  3,
        "cost":        468_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000,# $468 Treseptuagintillion
        "purchased":   False
    }
]

# -------------------------------------------------------------------------------
# 9. UNLOCKS (per-business & global)
# -------------------------------------------------------------------------------
unlocks = [
    # -------------------
    # Asteroid Miner (biz_index 0)
    # -------------------
     { "biz_index": 0, "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2",    "asset_path": None },
    { "biz_index": 0, "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2",    "asset_path": None },
    { "biz_index": 0, "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2",    "asset_path": None },
    { "biz_index": 0, "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2",    "asset_path": None },
    { "biz_index": 0, "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2",    "asset_path": None },
    { "biz_index": 0, "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2",    "asset_path": None },
    { "biz_index": 0, "threshold":  500, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold":  600, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold":  700, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold":  800, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold":  900, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 1000, "type": "profit", "multiplier": 5.0,
      "description": "Asteroid Miner profit ×5",   "asset_path": None },
    { "biz_index": 0, "threshold": 1100, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 1200, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 1300, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 1400, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 1500, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 1600, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 1700, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 1800, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 1900, "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4",   "asset_path": None },
    { "biz_index": 0, "threshold": 2000, "type": "profit", "multiplier": 5.0,
      "description": "Asteroid Miner profit ×5",   "asset_path": None },
    { "biz_index": 0, "threshold": 2250, "type": "profit", "multiplier": 2.0,
      "description": "Asteroid Miner profit ×2",   "asset_path": None },
    { "biz_index": 0, "threshold": 2500, "type": "profit", "multiplier": 2.0,
      "description": "Asteroid Miner profit ×2",   "asset_path": None },
    { "biz_index": 0, "threshold": 2750, "type": "profit", "multiplier": 2.0,
      "description": "Asteroid Miner profit ×2",   "asset_path": None },
    { "biz_index": 0, "threshold": 3000, "type": "profit", "multiplier": 5.0,
      "description": "Asteroid Miner profit ×5",   "asset_path": None },
    { "biz_index": 0, "threshold": 3250, "type": "profit", "multiplier": 2.0,
      "description": "Asteroid Miner profit ×2",   "asset_path": None },
    { "biz_index": 0, "threshold": 3500, "type": "profit", "multiplier": 2.0,
      "description": "Asteroid Miner profit ×2",   "asset_path": None },
    { "biz_index": 0, "threshold": 3750, "type": "profit", "multiplier": 2.0,
      "description": "Asteroid Miner profit ×2",   "asset_path": None },
    { "biz_index": 0, "threshold": 4000, "type": "profit", "multiplier": 5.0,
      "description": "Asteroid Miner profit ×5",   "asset_path": None },
    { "biz_index": 0, "threshold": 4250, "type": "profit", "multiplier": 2.0,
      "description": "Asteroid Miner profit ×2",   "asset_path": None },
    { "biz_index": 0, "threshold": 4500, "type": "profit", "multiplier": 2.0,
      "description": "Asteroid Miner profit ×2",   "asset_path": None },
    { "biz_index": 0, "threshold": 4750, "type": "profit", "multiplier": 2.0,
      "description": "Asteroid Miner profit ×2",   "asset_path": None },
    { "biz_index": 0, "threshold": 5000, "type": "profit", "multiplier": 5.0,
      "description": "Asteroid Miner profit ×5",   "asset_path": None },
    { "biz_index": 0, "threshold": 5250, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 5500, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 5750, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 6000, "type": "profit", "multiplier": 5.0,
      "description": "Asteroid Miner profit ×5",   "asset_path": None },
    { "biz_index": 0, "threshold": 6250, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 6500, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 6750, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 7000, "type": "profit", "multiplier": 5.0,
      "description": "Asteroid Miner profit ×5",   "asset_path": None },
    { "biz_index": 0, "threshold": 7000, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 7250, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 7500, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 7777, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 8000, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 8200, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 8400, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 8600, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 8800, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 9000, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 9100, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 9200, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 9300, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 9400, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 9500, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 9600, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 9700, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold": 9800, "type": "profit", "multiplier": 3.0,
      "description": "Asteroid Miner profit ×3",   "asset_path": None },
    { "biz_index": 0, "threshold":  9999, "type": "profit", "multiplier": 1.9999,
      "description": "Asteroid Miner profit ×1.9999","asset_path": None },
    { "biz_index": 0, "threshold": 10000, "type": "profit", "multiplier": 5.0,
      "description": "Asteroid Miner profit ×5",   "asset_path": None },

    # -------------------
    # Satellite Network (biz_index 1)
    # -------------------
    { "biz_index": 1, "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2",    "asset_path": None },
    { "biz_index": 1, "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2",    "asset_path": None },
    { "biz_index": 1, "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2",    "asset_path": None },
    { "biz_index": 1, "threshold":  125, "type": "profit", "multiplier": 2.0,
      "description": "Satellite Network profit ×2",   "asset_path": None },
    { "biz_index": 1, "threshold":  150, "type": "profit", "multiplier": 2.0,
      "description": "Satellite Network profit ×2",   "asset_path": None },
    { "biz_index": 1, "threshold":  175, "type": "profit", "multiplier": 2.0,
      "description": "Satellite Network profit ×2",   "asset_path": None },
    { "biz_index": 1, "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2",    "asset_path": None },
    { "biz_index": 1, "threshold":  225, "type": "profit", "multiplier": 2.0,
      "description": "Satellite Network profit ×2",   "asset_path": None },
    { "biz_index": 1, "threshold":  250, "type": "profit", "multiplier": 3.0,
      "description": "Satellite Network profit ×3",   "asset_path": None },
    { "biz_index": 1, "threshold":  275, "type": "profit", "multiplier": 3.0,
      "description": "Satellite Network profit ×3",   "asset_path": None },
    { "biz_index": 1, "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2",    "asset_path": None },
    { "biz_index": 1, "threshold":  325, "type": "profit", "multiplier": 3.0,
      "description": "Satellite Network profit ×3",   "asset_path": None },
    { "biz_index": 1, "threshold":  350, "type": "profit", "multiplier": 3.0,
      "description": "Satellite Network profit ×3",   "asset_path": None },
    { "biz_index": 1, "threshold":  375, "type": "profit", "multiplier": 4.0,
      "description": "Satellite Network profit ×4",   "asset_path": None },
    { "biz_index": 1, "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2",    "asset_path": None },
    { "biz_index": 1, "threshold":  425, "type": "profit", "multiplier": 4.0,
      "description": "Satellite Network profit ×4",   "asset_path": None },
    { "biz_index": 1, "threshold":  450, "type": "profit", "multiplier": 4.0,
      "description": "Satellite Network profit ×4",   "asset_path": None },
    { "biz_index": 1, "threshold":  475, "type": "profit", "multiplier": 4.0,
      "description": "Satellite Network profit ×4",   "asset_path": None },
    { "biz_index": 1, "threshold":  500, "type": "profit", "multiplier": 11.0,
      "description": "Satellite Network profit ×11",  "asset_path": None },
    { "biz_index": 1, "threshold":  525, "type": "profit", "multiplier": 5.0,
      "description": "Satellite Network profit ×5",   "asset_path": None },
    { "biz_index": 1, "threshold":  550, "type": "profit", "multiplier": 5.0,
      "description": "Satellite Network profit ×5",   "asset_path": None },
    { "biz_index": 1, "threshold":  575, "type": "profit", "multiplier": 5.0,
      "description": "Satellite Network profit ×5",   "asset_path": None },
    { "biz_index": 1, "threshold":  600, "type": "profit", "multiplier": 11.0,
      "description": "Satellite Network profit ×11",  "asset_path": None },
    { "biz_index": 1, "threshold":  625, "type": "profit", "multiplier": 5.0,
      "description": "Satellite Network profit ×5",   "asset_path": None },
    { "biz_index": 1, "threshold":  650, "type": "profit", "multiplier": 6.0,
      "description": "Satellite Network profit ×6",   "asset_path": None },
    { "biz_index": 1, "threshold":  675, "type": "profit", "multiplier": 6.0,
      "description": "Satellite Network profit ×6",   "asset_path": None },
    { "biz_index": 1, "threshold":  700, "type": "profit", "multiplier": 11.0,
      "description": "Satellite Network profit ×11",  "asset_path": None },
    { "biz_index": 1, "threshold":  725, "type": "profit", "multiplier": 6.0,
      "description": "Satellite Network profit ×6",   "asset_path": None },
    { "biz_index": 1, "threshold":  750, "type": "profit", "multiplier": 6.0,
      "description": "Satellite Network profit ×6",   "asset_path": None },
    { "biz_index": 1, "threshold":  775, "type": "profit", "multiplier": 3.0,
      "description": "Satellite Network profit ×3",   "asset_path": None },
    { "biz_index": 1, "threshold":  800, "type": "profit", "multiplier": 11.0,
      "description": "Satellite Network profit ×11",  "asset_path": None },
    { "biz_index": 1, "threshold":  825, "type": "profit", "multiplier": 7.0,
      "description": "Satellite Network profit ×7",   "asset_path": None },
    { "biz_index": 1, "threshold":  850, "type": "profit", "multiplier": 7.0,
      "description": "Satellite Network profit ×7",   "asset_path": None },
    { "biz_index": 1, "threshold":  875, "type": "profit", "multiplier": 7.0,
      "description": "Satellite Network profit ×7",   "asset_path": None },
    { "biz_index": 1, "threshold":  900, "type": "profit", "multiplier": 11.0,
      "description": "Satellite Network profit ×11",  "asset_path": None },
    { "biz_index": 1, "threshold":  925, "type": "profit", "multiplier": 7.0,
      "description": "Satellite Network profit ×7",   "asset_path": None },
    { "biz_index": 1, "threshold":  950, "type": "profit", "multiplier": 7.0,
      "description": "Satellite Network profit ×7",   "asset_path": None },
    { "biz_index": 1, "threshold":  975, "type": "profit", "multiplier": 7.0,
      "description": "Satellite Network profit ×7",   "asset_path": None },
    { "biz_index": 1, "threshold": 1000, "type": "profit", "multiplier": 7777777.0,
      "description": "Satellite Network profit ×7777777","asset_path": None },
    { "biz_index": 1, "threshold": 1025, "type": "profit", "multiplier": 7.0,
      "description": "Satellite Network profit ×7",   "asset_path": None },
    { "biz_index": 1, "threshold": 1050, "type": "profit", "multiplier": 7.0,
      "description": "Satellite Network profit ×7",   "asset_path": None },
    { "biz_index": 1, "threshold": 1075, "type": "profit", "multiplier": 8.0,
      "description": "Satellite Network profit ×8",   "asset_path": None },
    { "biz_index": 1, "threshold": 1100, "type": "profit", "multiplier": 8.0,
      "description": "Satellite Network profit ×8",   "asset_path": None },
    { "biz_index": 1, "threshold": 1125, "type": "profit", "multiplier": 8.0,
      "description": "Satellite Network profit ×8",   "asset_path": None },
    { "biz_index": 1, "threshold": 1150, "type": "profit", "multiplier": 8.0,
      "description": "Satellite Network profit ×8",   "asset_path": None },
    { "biz_index": 1, "threshold": 1175, "type": "profit", "multiplier": 8.0,
      "description": "Satellite Network profit ×8",   "asset_path": None },
    { "biz_index": 1, "threshold": 1200, "type": "profit", "multiplier": 8.0,
      "description": "Satellite Network profit ×8",   "asset_path": None },
    { "biz_index": 1, "threshold": 1225, "type": "profit", "multiplier": 8.0,
      "description": "Satellite Network profit ×8",   "asset_path": None },
    { "biz_index": 1, "threshold": 1250, "type": "profit", "multiplier": 8.0,
      "description": "Satellite Network profit ×8",   "asset_path": None },
    { "biz_index": 1, "threshold": 1300, "type": "profit", "multiplier": 7777.0,
      "description": "Satellite Network profit ×7777","asset_path": None },
    { "biz_index": 1, "threshold": 1350, "type": "profit", "multiplier": 9.0,
      "description": "Satellite Network profit ×9",   "asset_path": None },
    { "biz_index": 1, "threshold": 1400, "type": "profit", "multiplier": 9.0,
      "description": "Satellite Network profit ×9",   "asset_path": None },
    { "biz_index": 1, "threshold": 1450, "type": "profit", "multiplier": 9.0,
      "description": "Satellite Network profit ×9",   "asset_path": None },
    { "biz_index": 1, "threshold": 1500, "type": "profit", "multiplier": 9.0,
      "description": "Satellite Network profit ×9",   "asset_path": None },
    { "biz_index": 1, "threshold": 1550, "type": "profit", "multiplier": 9.0,
      "description": "Satellite Network profit ×9",   "asset_path": None },
    { "biz_index": 1, "threshold": 1600, "type": "profit", "multiplier": 9.0,
      "description": "Satellite Network profit ×9",   "asset_path": None },
    { "biz_index": 1, "threshold": 1650, "type": "profit", "multiplier": 9.0,
      "description": "Satellite Network profit ×9",   "asset_path": None },
    { "biz_index": 1, "threshold": 1700, "type": "profit", "multiplier": 9.0,
      "description": "Satellite Network profit ×9",   "asset_path": None },
    { "biz_index": 1, "threshold": 1750, "type": "profit", "multiplier": 9.0,
      "description": "Satellite Network profit ×9",   "asset_path": None },
    { "biz_index": 1, "threshold": 1800, "type": "profit", "multiplier": 10.0,
      "description": "Satellite Network profit ×10",  "asset_path": None },
    { "biz_index": 1, "threshold": 1850, "type": "profit", "multiplier": 10.0,
      "description": "Satellite Network profit ×10",  "asset_path": None },
    { "biz_index": 1, "threshold": 1900, "type": "profit", "multiplier": 10.0,
      "description": "Satellite Network profit ×10",  "asset_path": None },
    { "biz_index": 1, "threshold": 1950, "type": "profit", "multiplier": 10.0,
      "description": "Satellite Network profit ×10",  "asset_path": None },
    { "biz_index": 1, "threshold": 2000, "type": "profit", "multiplier": 7777.0,
      "description": "Satellite Network profit ×7777","asset_path": None },
    { "biz_index": 1, "threshold": 2100, "type": "profit", "multiplier": 15.0,
      "description": "Satellite Network profit ×15",  "asset_path": None },
    { "biz_index": 1, "threshold": 2200, "type": "profit", "multiplier": 15.0,
      "description": "Satellite Network profit ×15",  "asset_path": None },
    { "biz_index": 1, "threshold": 2300, "type": "profit", "multiplier": 15.0,
      "description": "Satellite Network profit ×15",  "asset_path": None },
    { "biz_index": 1, "threshold": 2400, "type": "profit", "multiplier": 15.0,
      "description": "Satellite Network profit ×15",  "asset_path": None },
    { "biz_index": 1, "threshold": 2500, "type": "profit", "multiplier": 777.0,
      "description": "Satellite Network profit ×777",  "asset_path": None },
    { "biz_index": 1, "threshold": 2600, "type": "profit", "multiplier": 15.0,
      "description": "Satellite Network profit ×15",  "asset_path": None },
    { "biz_index": 1, "threshold": 2700, "type": "profit", "multiplier": 15.0,
      "description": "Satellite Network profit ×15",  "asset_path": None },
    { "biz_index": 1, "threshold": 2800, "type": "profit", "multiplier": 15.0,
      "description": "Satellite Network profit ×15",  "asset_path": None },
    { "biz_index": 1, "threshold": 2900, "type": "profit", "multiplier": 15.0,
      "description": "Satellite Network profit ×15",  "asset_path": None },
    { "biz_index": 1, "threshold": 3000, "type": "profit", "multiplier": 777.0,
      "description": "Satellite Network profit ×777",  "asset_path": None },
    { "biz_index": 1, "threshold": 3100, "type": "profit", "multiplier": 20.0,
      "description": "Satellite Network profit ×20",  "asset_path": None },
    { "biz_index": 1, "threshold": 3200, "type": "profit", "multiplier": 20.0,
      "description": "Satellite Network profit ×20",  "asset_path": None },
    { "biz_index": 1, "threshold": 3300, "type": "profit", "multiplier": 20.0,
      "description": "Satellite Network profit ×20",  "asset_path": None },
    { "biz_index": 1, "threshold": 3400, "type": "profit", "multiplier": 20.0,
      "description": "Satellite Network profit ×20",  "asset_path": None },
    { "biz_index": 1, "threshold": 3500, "type": "profit", "multiplier": 777.0,
      "description": "Satellite Network profit ×777",  "asset_path": None },
    { "biz_index": 1, "threshold": 3600, "type": "profit", "multiplier": 25.0,
      "description": "Satellite Network profit ×25",  "asset_path": None },
    { "biz_index": 1, "threshold": 3700, "type": "profit", "multiplier": 25.0,
      "description": "Satellite Network profit ×25",  "asset_path": None },
    { "biz_index": 1, "threshold": 3800, "type": "profit", "multiplier": 25.0,
      "description": "Satellite Network profit ×25",  "asset_path": None },
    { "biz_index": 1, "threshold": 3900, "type": "profit", "multiplier": 25.0,
      "description": "Satellite Network profit ×25",  "asset_path": None },
    { "biz_index": 1, "threshold": 4000, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 4100, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 4200, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 4300, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 4400, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 4500, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 4600, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 4700, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 4800, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 4900, "type": "profit", "multiplier": 30.0,
      "description": "Satellite Network profit ×30",  "asset_path": None },
    { "biz_index": 1, "threshold": 5000, "type": "profit", "multiplier": 50.0,
      "description": "Satellite Network profit ×50",  "asset_path": None },
    { "biz_index": 1, "threshold": 5100, "type": "profit", "multiplier": 50.0,
      "description": "Satellite Network profit ×50",  "asset_path": None },
    { "biz_index": 1, "threshold": 5200, "type": "profit", "multiplier": 50.0,
      "description": "Satellite Network profit ×50",  "asset_path": None },
    { "biz_index": 1, "threshold": 5300, "type": "profit", "multiplier": 50.0,
      "description": "Satellite Network profit ×50",  "asset_path": None },
    { "biz_index": 1, "threshold": 5400, "type": "profit", "multiplier": 50.0,
      "description": "Satellite Network profit ×50",  "asset_path": None },

    # -------------------
    # Rocket Yard (biz_index 2)
    # -------------------
    { "biz_index": 2, "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2",  "asset_path": None },
    { "biz_index": 2, "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2",  "asset_path": None },
    { "biz_index": 2, "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2",  "asset_path": None },
    { "biz_index": 2, "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2",  "asset_path": None },
    { "biz_index": 2, "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2",  "asset_path": None },
    { "biz_index": 2, "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2",  "asset_path": None },
    { "biz_index": 2, "threshold":  500, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold":  600, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold":  700, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold":  800, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold":  900, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 1000, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 1100, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 1200, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 1300, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 1400, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 1500, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 1600, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 1700, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 1800, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 1900, "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 2000, "type": "profit", "multiplier": 5.0,
      "description": "Rocket Yard profit ×5", "asset_path": None },
    { "biz_index": 2, "threshold": 2100, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 2200, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 2300, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 2400, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 2500, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 2600, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 2700, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 2800, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 2900, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3000, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3100, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3200, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3300, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3400, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3500, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3600, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3700, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3800, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 3900, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 4000, "type": "profit", "multiplier": 5.0,
      "description": "Rocket Yard profit ×5", "asset_path": None },
    { "biz_index": 2, "threshold": 4100, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 4200, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 4300, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 4400, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 4500, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 4600, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 4700, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 4800, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 4900, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 5000, "type": "profit", "multiplier": 5.0,
      "description": "Rocket Yard profit ×5", "asset_path": None },
    { "biz_index": 2, "threshold": 5250, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },
    { "biz_index": 2, "threshold": 5500, "type": "profit", "multiplier": 3.0,
      "description": "Rocket Yard profit ×3", "asset_path": None },

    # -------------------
    # Lunar Colony (biz_index 3)
    # -------------------
    { "biz_index": 3, "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2",  "asset_path": None },
    { "biz_index": 3, "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2",  "asset_path": None },
    { "biz_index": 3, "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2",  "asset_path": None },
    { "biz_index": 3, "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2",  "asset_path": None },
    { "biz_index": 3, "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2",  "asset_path": None },
    { "biz_index": 3, "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2",  "asset_path": None },
    { "biz_index": 3, "threshold":  500, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold":  600, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold":  700, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold":  800, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold":  900, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 1000, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 1100, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 1200, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 1300, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 1400, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 1500, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 1600, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 1700, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 1800, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 1900, "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 2000, "type": "profit", "multiplier": 5.0,
      "description": "Lunar Colony profit ×5", "asset_path": None },
    { "biz_index": 3, "threshold": 2100, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 2200, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 2300, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 2400, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 2500, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 2600, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 2700, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 2800, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 2900, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 3000, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 3100, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 3200, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 3300, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 3400, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 3500, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 3600, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 3700, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 3800, "type": "profit", "multiplier": 5.0,
      "description": "Lunar Colony profit ×5", "asset_path": None },
    { "biz_index": 3, "threshold": 3900, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 4000, "type": "profit", "multiplier": 5.0,
      "description": "Lunar Colony profit ×5", "asset_path": None },
    { "biz_index": 3, "threshold": 4100, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 4200, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 4300, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 4400, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 4500, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 4600, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 4700, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 4800, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 4900, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 5000, "type": "profit", "multiplier": 5.0,
      "description": "Lunar Colony profit ×5", "asset_path": None },
    { "biz_index": 3, "threshold": 5250, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 5500, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },
    { "biz_index": 3, "threshold": 5750, "type": "profit", "multiplier": 3.0,
      "description": "Lunar Colony profit ×3", "asset_path": None },

    # -------------------
    # Starlight Farm (biz_index 4)
    # -------------------
     { "biz_index": 4, "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2",  "asset_path": None },
    { "biz_index": 4, "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2",  "asset_path": None },
    { "biz_index": 4, "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2",  "asset_path": None },
    { "biz_index": 4, "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2",  "asset_path": None },
    { "biz_index": 4, "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2",  "asset_path": None },
    { "biz_index": 4, "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2",  "asset_path": None },
    { "biz_index": 4, "threshold":  500, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold":  600, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold":  700, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold":  800, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold":  900, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 1000, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 1100, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 1200, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 1300, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 1400, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 1500, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 1600, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 1700, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 1800, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 1900, "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 2000, "type": "profit", "multiplier": 5.0,
      "description": "Starlight Farm profit ×5", "asset_path": None },
    { "biz_index": 4, "threshold": 2100, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 2200, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 2300, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 2400, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 2500, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 2600, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 2700, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 2800, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 2900, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3000, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3100, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3200, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3300, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3400, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3500, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3600, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3700, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3800, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 3900, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4000, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4100, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4200, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4300, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4400, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4500, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4600, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4700, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4800, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 4900, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 5000, "type": "profit", "multiplier": 5.0,
      "description": "Starlight Farm profit ×5", "asset_path": None },
    { "biz_index": 4, "threshold": 5250, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 5500, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 5750, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 6000, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },
    { "biz_index": 4, "threshold": 6250, "type": "profit", "multiplier": 3.0,
      "description": "Starlight Farm profit ×3", "asset_path": None },

    # -------------------
    # Alien Outpost (biz_index 5)
    # -------------------
    { "biz_index": 5, "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2",  "asset_path": None },
    { "biz_index": 5, "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2",  "asset_path": None },
    { "biz_index": 5, "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2",  "asset_path": None },
    { "biz_index": 5, "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2",  "asset_path": None },
    { "biz_index": 5, "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2",  "asset_path": None },
    { "biz_index": 5, "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2",  "asset_path": None },
    { "biz_index": 5, "threshold":  500, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold":  600, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold":  700, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold":  800, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold":  900, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 1000, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 1100, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 1200, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 1300, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 1400, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 1500, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 1600, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 1700, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 1800, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 1900, "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 2000, "type": "profit", "multiplier": 5.0,
      "description": "Alien Outpost profit ×5", "asset_path": None },
    { "biz_index": 5, "threshold": 2100, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 2200, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 2300, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 2400, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 2500, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 2600, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 2700, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 2800, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 2900, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 3000, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 3250, "type": "profit", "multiplier": 5.0,
      "description": "Alien Outpost profit ×5", "asset_path": None },
    { "biz_index": 5, "threshold": 3500, "type": "profit", "multiplier": 5.0,
      "description": "Alien Outpost profit ×5", "asset_path": None },
    { "biz_index": 5, "threshold": 3750, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 4000, "type": "profit", "multiplier": 5.0,
      "description": "Alien Outpost profit ×5", "asset_path": None },
    { "biz_index": 5, "threshold": 4250, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 4500, "type": "profit", "multiplier": 5.0,
      "description": "Alien Outpost profit ×5", "asset_path": None },
    { "biz_index": 5, "threshold": 4750, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 5000, "type": "profit", "multiplier": 5.0,
      "description": "Alien Outpost profit ×5", "asset_path": None },
    { "biz_index": 5, "threshold": 5250, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 5500, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 5750, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 6000, "type": "profit", "multiplier": 5.0,
      "description": "Alien Outpost profit ×5", "asset_path": None },
    { "biz_index": 5, "threshold": 6250, "type": "profit", "multiplier": 3.0,
      "description": "Alien Outpost profit ×3", "asset_path": None },
    { "biz_index": 5, "threshold": 6500, "type": "profit", "multiplier": 5.0,
      "description": "Alien Outpost profit ×5", "asset_path": None },

    # -------------------
    # Solar Array (biz_index 6)
    # -------------------
    { "biz_index": 6, "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold":  500, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold":  600, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold":  700, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold":  800, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold":  900, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 1000, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 1100, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 1200, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 1300, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 1400, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 1500, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 1600, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 1700, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 1800, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 1900, "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 2000, "type": "profit", "multiplier": 5.0,
      "description": "Solar Array profit ×5", "asset_path": None },
    { "biz_index": 6, "threshold": 2100, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold": 2200, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 2300, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold": 2400, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 2500, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold": 2600, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 2700, "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2",  "asset_path": None },
    { "biz_index": 6, "threshold": 2800, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 2900, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 3000, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 3250, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 3500, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 3750, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 4000, "type": "profit", "multiplier": 5.0,
      "description": "Solar Array profit ×5", "asset_path": None },
    { "biz_index": 6, "threshold": 4250, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 4500, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 4750, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 5000, "type": "profit", "multiplier": 7.0,
      "description": "Solar Array profit ×7", "asset_path": None },
    { "biz_index": 6, "threshold": 5250, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 5500, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 5750, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 6000, "type": "profit", "multiplier": 7.0,
      "description": "Solar Array profit ×7", "asset_path": None },
    { "biz_index": 6, "threshold": 6250, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 6500, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 6750, "type": "profit", "multiplier": 3.0,
      "description": "Solar Array profit ×3", "asset_path": None },
    { "biz_index": 6, "threshold": 7000, "type": "profit", "multiplier": 7.0,
      "description": "Solar Array profit ×7", "asset_path": None },

    # -------------------
    # Black Hole Labs (biz_index 7)
    # -------------------
    { "biz_index": 7, "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold":  500, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold":  600, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold":  700, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold":  800, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold":  900, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 1000, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 1100, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 1200, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 1300, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 1400, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 1500, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 1600, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 1700, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 1800, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 1900, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 2000, "type": "profit", "multiplier": 5.0,
      "description": "Black Hole Labs profit ×5", "asset_path": None },
    { "biz_index": 7, "threshold": 2100, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold": 2200, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 2300, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold": 2400, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 2500, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold": 2600, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 2700, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold": 2800, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 2900, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 3000, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 3250, "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2",  "asset_path": None },
    { "biz_index": 7, "threshold": 3500, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 3750, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 4000, "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 4250, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 4500, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 4750, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 5000, "type": "profit", "multiplier": 5.0,
      "description": "Black Hole Labs profit ×5", "asset_path": None },
    { "biz_index": 7, "threshold": 5250, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 5500, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 5750, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 6000, "type": "profit", "multiplier": 9.0,
      "description": "Black Hole Labs profit ×9", "asset_path": None },
    { "biz_index": 7, "threshold": 6250, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 6500, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 6750, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 7000, "type": "profit", "multiplier": 9.0,
      "description": "Black Hole Labs profit ×9", "asset_path": None },
    { "biz_index": 7, "threshold": 7250, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 7500, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },
    { "biz_index": 7, "threshold": 7750, "type": "profit", "multiplier": 3.0,
      "description": "Black Hole Labs profit ×3", "asset_path": None },

    # -------------------
    # Wormhole Gate (biz_index 8)
    # -------------------
    { "biz_index": 8, "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold":  500, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold":  600, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold":  700, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold":  800, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold":  900, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 1000, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 1100, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 1200, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 1300, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 1400, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 1500, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 1600, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 1700, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 1800, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 1900, "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 2000, "type": "profit", "multiplier": 5.0,
      "description": "Wormhole Gate profit ×5", "asset_path": None },
    { "biz_index": 8, "threshold": 2250, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold": 2500, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold": 2750, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold": 3000, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold": 3250, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold": 3500, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold": 3750, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold": 4000, "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2",  "asset_path": None },
    { "biz_index": 8, "threshold": 4250, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 4500, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 4750, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 5000, "type": "profit", "multiplier": 5.0,
      "description": "Wormhole Gate profit ×5", "asset_path": None },
    { "biz_index": 8, "threshold": 5250, "type": "profit", "multiplier": 5.0,
      "description": "Wormhole Gate profit ×5", "asset_path": None },
    { "biz_index": 8, "threshold": 5500, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 5750, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 6000, "type": "profit", "multiplier": 5.0,
      "description": "Wormhole Gate profit ×5", "asset_path": None },
    { "biz_index": 8, "threshold": 6250, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 6500, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 6750, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 7000, "type": "profit", "multiplier": 5.0,
      "description": "Wormhole Gate profit ×5", "asset_path": None },
    { "biz_index": 8, "threshold": 7250, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 7500, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 7750, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 8000, "type": "profit", "multiplier": 5.0,
      "description": "Wormhole Gate profit ×5", "asset_path": None },
    { "biz_index": 8, "threshold": 8250, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },
    { "biz_index": 8, "threshold": 8500, "type": "profit", "multiplier": 3.0,
      "description": "Wormhole Gate profit ×3", "asset_path": None },

    # -------------------
    # Galactic Senate (biz_index 9)
    # -------------------
    { "biz_index": 9,  "threshold":   25, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold":   50, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold":  100, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold":  200, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold":  300, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold":  400, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold":  500, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold":  600, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold":  700, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold":  800, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold":  900, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 1000, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 1100, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 1200, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 1300, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 1400, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 1500, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 1600, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 1700, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 1800, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 1900, "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },
    { "biz_index": 9,  "threshold": 2000, "type": "profit", "multiplier": 5.0,
      "description": "Galactic Senate profit ×5", "asset_path": None },
    { "biz_index": 9,  "threshold": 2250, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 2500, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 2750, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 3000, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 3250, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 3500, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 3750, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 4000, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 4250, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 4500, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 4750, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 5000, "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2",  "asset_path": None },
    { "biz_index": 9,  "threshold": 5250, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 5500, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 5750, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 6000, "type": "profit", "multiplier": 5.0,
      "description": "Galactic Senate profit ×5", "asset_path": None },
    { "biz_index": 9,  "threshold": 6250, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 6500, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 6750, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 7000, "type": "profit", "multiplier": 7.0,
      "description": "Galactic Senate profit ×7", "asset_path": None },
    { "biz_index": 9,  "threshold": 7250, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 7500, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 7750, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 8000, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 8250, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    { "biz_index": 9,  "threshold": 8500, "type": "profit", "multiplier": 3.0,
      "description": "Galactic Senate profit ×3", "asset_path": None },
    # -------------------
    # Global (Capitalist) unlocks – biz_index=None
    # -------------------global_unlocks = [
    # Threshold 25: Speed ×2
    {
        "biz_index":   None,
        "threshold":   25,
        "type":         "global_speed",
        "multiplier":   2.0,
        "description": "All enterprises ×2 speed",
        "asset_path":   "assets/global.png"
    },
    # Threshold 25: Earnings ×2
    {
        "biz_index":   None,
        "threshold":   25,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 50: Speed ×2
    {
        "biz_index":   None,
        "threshold":   50,
        "type":         "global_speed",
        "multiplier":   2.0,
        "description": "All enterprises ×2 speed",
        "asset_path":   "assets/global.png"
    },
    # Threshold 50: Earnings ×2
    {
        "biz_index":   None,
        "threshold":   50,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 100: Speed ×2
    {
        "biz_index":   None,
        "threshold":  100,
        "type":         "global_speed",
        "multiplier":   2.0,
        "description": "All enterprises ×2 speed",
        "asset_path":   "assets/global.png"
    },
    # Threshold 100: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  100,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 200: Speed ×2
    {
        "biz_index":   None,
        "threshold":  200,
        "type":         "global_speed",
        "multiplier":   2.0,
        "description": "All enterprises ×2 speed",
        "asset_path":   "assets/global.png"
    },
    # Threshold 200: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  200,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 300: Speed ×2
    {
        "biz_index":   None,
        "threshold":  300,
        "type":         "global_speed",
        "multiplier":   2.0,
        "description": "All enterprises ×2 speed",
        "asset_path":   "assets/global.png"
    },
    # Threshold 300: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  300,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 400: Speed ×2
    {
        "biz_index":   None,
        "threshold":  400,
        "type":         "global_speed",
        "multiplier":   2.0,
        "description": "All enterprises ×2 speed",
        "asset_path":   "assets/global.png"
    },
    # Threshold 400: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  400,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 500: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  500,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 600: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  600,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 666: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  666,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 700: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  700,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 777: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  777,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 800: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  800,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 900: Earnings ×2
    {
        "biz_index":   None,
        "threshold":  900,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1000: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1000,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1100: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1100,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1111: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1111,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1200: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1200,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1300: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1300,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1400: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1400,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1500: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1500,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1600: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1600,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1700: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1700,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1800: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1800,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 1900: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 1900,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2000: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2000,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2100: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2100,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2200: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2200,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2222: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2222,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2300: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2300,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2400: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2400,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2500: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2500,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2600: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2600,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2700: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2700,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2800: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2800,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 2900: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 2900,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3000: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3000,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3100: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3100,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3200: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3200,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3300: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3300,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3333: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3333,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3400: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3400,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3500: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3500,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3600: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3600,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3700: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3700,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3800: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3800,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 3900: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 3900,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4000: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4000,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4100: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4100,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4200: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4200,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4300: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4300,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4400: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4400,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4500: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4500,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4600: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4600,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4700: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4700,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4800: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4800,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 4900: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 4900,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    },

    # Threshold 5000: Earnings ×2
    {
        "biz_index":   None,
        "threshold": 5000,
        "type":         "global_profit",
        "multiplier":   2.0,
        "description": "All enterprises ×2 earnings",
        "asset_path":   "assets/global.png"
    }
]


# 10. GALACTIC UPGRADES (Angel-style)
# -------------------------------------------------------------------------------
# ── (Somewhere near the top, after you’ve defined your business list) ──


galactic_upgrades = [
    # ───────────────────────────────────────────────────────────────────────────────
    {
        "name":        "Cosmic Sacrifice",
        "description": "All business profits ×3",
        "icon_image":  "assets/global.png",
        "biz_index":   None,
        "type":        "global",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        10_000,
        "purchased":   False
    },
    {
        "name":        "Stellar Archive",
        "description": "+10 Satellite Networks",
        "icon_image":  "assets/satellitenetwork.png",
        "biz_index":   1,            # Satellite Network
        "type":        "add_units",
        "multiplier":  0,
        "amount":      10,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "name":        "Rocket Reinforcements",
        "description": "+10 Rocket Yards",
        "icon_image":  "assets/rocketyard.png",
        "biz_index":   2,            # Rocket Yard
        "type":        "add_units",
        "multiplier":  0,
        "amount":      10,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "name":        "Lunar Land Bonus",
        "description": "+10 Lunar Colonies",
        "icon_image":  "assets/lunarcolony.png",
        "biz_index":   3,            # Lunar Colony
        "type":        "add_units",
        "multiplier":  0,
        "amount":      10,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "name":        "Starlight Seed Grant",
        "description": "+10 Starlight Farms",
        "icon_image":  "assets/starlightfarm.png",
        "biz_index":   4,            # Starlight Farm
        "type":        "add_units",
        "multiplier":  0,
        "amount":      10,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "name":        "Alien Assistance",
        "description": "+10 Alien Outposts",
        "icon_image":  "assets/alienoutpost.png",
        "biz_index":   5,            # Alien Outpost
        "type":        "add_units",
        "multiplier":  0,
        "amount":      10,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "name":        "Solar Surge",
        "description": "+10 Solar Arrays",
        "icon_image":  "assets/solararray.png",
        "biz_index":   6,            # Solar Array
        "type":        "add_units",
        "multiplier":  0,
        "amount":      10,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "name":        "Event Horizon Initiative",
        "description": "+10 Black Hole Labs",
        "icon_image":  "assets/blackholelabs.png",
        "biz_index":   7,            # Black Hole Labs
        "type":        "add_units",
        "multiplier":  0,
        "amount":      10,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "name":        "Wormhole Wealth Grant",
        "description": "+10 Wormhole Gates",
        "icon_image":  "assets/wormholegate.png",
        "biz_index":   8,            # Wormhole Gate
        "type":        "add_units",
        "multiplier":  0,
        "amount":      10,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "name":        "Senate Stimulus",
        "description": "+10 Galactic Senates",
        "icon_image":  "assets/galacticsenate.png",
        "biz_index":   9,            # Galactic Senate
        "type":        "add_units",
        "multiplier":  0,
        "amount":      10,
        "cost":        25_000_000,
        "purchased":   False
    },
    {
        "name":        "Galactic Triumph",
        "description": "All business profits ×9",
        "icon_image":  "assets/global.png",
        "biz_index":   None,
        "type":        "global",
        "multiplier":  9.0,
        "amount":      0,
        "cost":        100_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Satellite Supremacy",
        "description": "+50 Satellite Networks",
        "icon_image":  "assets/satellitenetwork.png",
        "biz_index":   1,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      50,
        "cost":        250_000_000,
        "purchased":   False
    },
    {
        "name":        "Rocket Ramp‐Up",
        "description": "+50 Rocket Yards",
        "icon_image":  "assets/rocketyard.png",
        "biz_index":   2,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      50,
        "cost":        250_000_000,
        "purchased":   False
    },
    {
        "name":        "Lunar Leap",
        "description": "+50 Lunar Colonies",
        "icon_image":  "assets/lunarcolony.png",
        "biz_index":   3,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      50,
        "cost":        250_000_000,
        "purchased":   False
    },
    {
        "name":        "Starlight Supercharge",
        "description": "+50 Starlight Farms",
        "icon_image":  "assets/starlightfarm.png",
        "biz_index":   4,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      50,
        "cost":        250_000_000,
        "purchased":   False
    },
    {
        "name":        "Alien Alliance",
        "description": "+50 Alien Outposts",
        "icon_image":  "assets/alienoutpost.png",
        "biz_index":   5,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      50,
        "cost":        250_000_000,
        "purchased":   False
    },
    {
        "name":        "Solar Core Boost",
        "description": "+50 Solar Arrays",
        "icon_image":  "assets/solararray.png",
        "biz_index":   6,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      50,
        "cost":        250_000_000,
        "purchased":   False
    },
    {
        "name":        "Black Hole Bonanza",
        "description": "+50 Black Hole Labs",
        "icon_image":  "assets/blackholelabs.png",
        "biz_index":   7,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      50,
        "cost":        250_000_000,
        "purchased":   False
    },
    {
        "name":        "Wormhole Windfall",
        "description": "+50 Wormhole Gates",
        "icon_image":  "assets/wormholegate.png",
        "biz_index":   8,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      50,
        "cost":        250_000_000,
        "purchased":   False
    },
    {
        "name":        "Senate Surge",
        "description": "+50 Galactic Senates",
        "icon_image":  "assets/galacticsenate.png",
        "biz_index":   9,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      50,
        "cost":        250_000_000,
        "purchased":   False
    },

    # ───────────────────────────────────────────────────────────────────────────────
    {
        "name":        "Celestial Convergence",
        "description": "All business profits ×11",
        "icon_image":  "assets/global.png",
        "biz_index":   None,
        "type":        "global",
        "multiplier":  11.0,
        "amount":      0,
        "cost":        1_000_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Astro‐Paper Swap",
        "description": "+25 Satellite Networks",
        "icon_image":  "assets/satellitenetwork.png",
        "biz_index":   1,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        250_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Rocket‐Fuel Remap",
        "description": "+25 Rocket Yards",
        "icon_image":  "assets/rocketyard.png",
        "biz_index":   2,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        250_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Lunar Lore",
        "description": "+25 Lunar Colonies",
        "icon_image":  "assets/lunarcolony.png",
        "biz_index":   3,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        250_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Starlight Stream",
        "description": "+25 Starlight Farms",
        "icon_image":  "assets/starlightfarm.png",
        "biz_index":   4,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        250_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Outpost Overdrive",
        "description": "+25 Alien Outposts",
        "icon_image":  "assets/alienoutpost.png",
        "biz_index":   5,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        250_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Solar‐Wind Sync",
        "description": "+25 Solar Arrays",
        "icon_image":  "assets/solararray.png",
        "biz_index":   6,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        250_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Gravity Glyph",
        "description": "+25 Black Hole Labs",
        "icon_image":  "assets/blackholelabs.png",
        "biz_index":   7,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        250_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Wormhole Wealth Transfer",
        "description": "+25 Wormhole Gates",
        "icon_image":  "assets/wormholegate.png",
        "biz_index":   8,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        250_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Senate Stimulus II",
        "description": "+25 Galactic Senates",
        "icon_image":  "assets/galacticsenate.png",
        "biz_index":   9,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        250_000_000_000,
        "purchased":   False
    },

    # ───────────────────────────────────────────────────────────────────────────────
    {
        "name":        "Unifying Umbra",
        "description": "All business profits ×15",
        "icon_image":  "assets/global.png",
        "biz_index":   None,
        "type":        "global",
        "multiplier":  15.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Sextillion
        "purchased":   False
    },
    {
        "name":        "Satellite Supremacy II",
        "description": "+75 Satellite Networks",
        "icon_image":  "assets/satellitenetwork.png",
        "biz_index":   1,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      75,
        "cost":        10_000_000_000_000_000,     # 10 Sextillion
        "purchased":   False
    },
    {
        "name":        "Rocket Resurgence II",
        "description": "+75 Rocket Yards",
        "icon_image":  "assets/rocketyard.png",
        "biz_index":   2,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      75,
        "cost":        10_000_000_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Lunar Legion II",
        "description": "+75 Lunar Colonies",
        "icon_image":  "assets/lunarcolony.png",
        "biz_index":   3,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      75,
        "cost":        10_000_000_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Starlight Surge II",
        "description": "+75 Starlight Farms",
        "icon_image":  "assets/starlightfarm.png",
        "biz_index":   4,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      75,
        "cost":        10_000_000_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Outpost Overload II",
        "description": "+75 Alien Outposts",
        "icon_image":  "assets/alienoutpost.png",
        "biz_index":   5,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      75,
        "cost":        10_000_000_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Solar‐Wing Amplifier",
        "description": "+75 Solar Arrays",
        "icon_image":  "assets/solararray.png",
        "biz_index":   6,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      75,
        "cost":        10_000_000_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Event Horizon Harvest",
        "description": "+75 Black Hole Labs",
        "icon_image":  "assets/blackholelabs.png",
        "biz_index":   7,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      75,
        "cost":        10_000_000_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Wormhole Warchest II",
        "description": "+75 Wormhole Gates",
        "icon_image":  "assets/wormholegate.png",
        "biz_index":   8,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      75,
        "cost":        10_000_000_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Senate Spartans II",
        "description": "+75 Galactic Senates",
        "icon_image":  "assets/galacticsenate.png",
        "biz_index":   9,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      75,
        "cost":        10_000_000_000_000_000,
        "purchased":   False
    },
    {
        "name":        "Infinite Incentive",
        "description": "All business profits ×3",
        "icon_image":  "assets/global.png",
        "biz_index":   None,
        "type":        "global",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        333_000_000_000_000_000_000,  # 333 Quintrigintillion
        "purchased":   False
    },
    {
        "name":        "Asteroid Accretion",
        "description": "+25 Asteroid Miners",
        "icon_image":  "assets/asteroidminer.png",
        "biz_index":   0,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      25,
        "cost":        700_000_000_000_000_000_000,  # 700 Quattuorvigintillion
        "purchased":   False
    },
    {
        "name":        "Satellite Supremacy III",
        "description": "+30 Satellite Networks",
        "icon_image":  "assets/satellitenetwork.png",
        "biz_index":   1,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      30,
        "cost":        30_000_000_000_000_000_000_000,  # 30 Novemdecillion
        "purchased":   False
    },
    {
        "name":        "Rocket Riddle",
        "description": "+30 Rocket Yards",
        "icon_image":  "assets/rocketyard.png",
        "biz_index":   2,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      30,
        "cost":        30_000_000_000_000_000_000_000,  # 30 Novemdecillion
        "purchased":   False
    },
    {
        "name":        "Lunar Luminance",
        "description": "+30 Lunar Colonies",
        "icon_image":  "assets/lunarcolony.png",
        "biz_index":   3,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      30,
        "cost":        30_000_000_000_000_000_000_000,  # 30 Novemdecillion
        "purchased":   False
    },
    {
        "name":        "Starlight Synchrotron",
        "description": "+30 Starlight Farms",
        "icon_image":  "assets/starlightfarm.png",
        "biz_index":   4,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      30,
        "cost":        30_000_000_000_000_000_000_000,  # 30 Novemdecillion
        "purchased":   False
    },
    {
        "name":        "Outpost Oasis",
        "description": "+30 Alien Outposts",
        "icon_image":  "assets/alienoutpost.png",
        "biz_index":   5,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      30,
        "cost":        30_000_000_000_000_000_000_000,  # 30 Novemdecillion
        "purchased":   False
    },
    {
        "name":        "Solar Skyforge",
        "description": "+30 Solar Arrays",
        "icon_image":  "assets/solararray.png",
        "biz_index":   6,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      30,
        "cost":        30_000_000_000_000_000_000_000,  # 30 Novemdecillion
        "purchased":   False
    },
    {
        "name":        "Black Hole Bonanza III",
        "description": "+30 Black Hole Labs",
        "icon_image":  "assets/blackholelabs.png",
        "biz_index":   7,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      30,
        "cost":        30_000_000_000_000_000_000_000,  # 30 Novemdecillion
        "purchased":   False
    },
    {
        "name":        "Wormhole Web",
        "description": "+30 Wormhole Gates",
        "icon_image":  "assets/wormholegate.png",
        "biz_index":   8,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      30,
        "cost":        30_000_000_000_000_000_000_000,  # 30 Novemdecillion
        "purchased":   False
    },
    {
        "name":        "Senate Supremacy III",
        "description": "+30 Galactic Senates",
        "icon_image":  "assets/galacticsenate.png",
        "biz_index":   9,
        "type":        "add_units",
        "multiplier":  0,
        "amount":      30,
        "cost":        30_000_000_000_000_000_000_000,  # 30 Novemdecillion
        "purchased":   False
    },
    {
        "name":        "Universal Uplift",
        "description": "All business profits ×7.777777",
        "icon_image":  "assets/global.png",
        "biz_index":   None,
        "type":        "global",
        "multiplier":  7.777777,
        "amount":      0,
        "cost":        777_000_000_000_000_000_000,  # 777 Unvigintillion
        "purchased":   False
    },
    {
        "name":        "Asteroid Amplifier",
        "description": "Asteroid Miner profit ×3",
        "icon_image":  "assets/asteroidminer.png",
        "biz_index":   0,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    },
    {
        "name":        "Satellite Surge",
        "description": "Satellite Network profit ×3",
        "icon_image":  "assets/satellitenetwork.png",
        "biz_index":   1,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    },
    {
        "name":        "Rocket Re‐Energizer",
        "description": "Rocket Yard profit ×3",
        "icon_image":  "assets/rocketyard.png",
        "biz_index":   2,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    },
    {
        "name":        "Lunar Luminosity",
        "description": "Lunar Colony profit ×3",
        "icon_image":  "assets/lunarcolony.png",
        "biz_index":   3,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    },
    {
        "name":        "Starlight Shine",
        "description": "Starlight Farm profit ×3",
        "icon_image":  "assets/starlightfarm.png",
        "biz_index":   4,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    },
    {  
        "name":        "Outpost Overdrive III",
        "description": "Alien Outpost profit ×3",
        "icon_image":  "assets/alienoutpost.png",
        "biz_index":   5,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    },
    {
        "name":        "Solar Supernova",
        "description": "Solar Array profit ×3",
        "icon_image":  "assets/solararray.png",
        "biz_index":   6,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    },
    {
        "name":        "Black Hole Bonanza IV",
        "description": "Black Hole Labs profit ×3",
        "icon_image":  "assets/blackholelabs.png",
        "biz_index":   7,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    },
    {
        "name":        "Wormhole Warchest III",
        "description": "Wormhole Gate profit ×3",
        "icon_image":  "assets/wormholegate.png",
        "biz_index":   8,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    },
    {
        "name":        "Senate Supremacy IV",
        "description": "Galactic Senate profit ×3",
        "icon_image":  "assets/galacticsenate.png",
        "biz_index":   9,
        "type":        "profit",
        "multiplier":  3.0,
        "amount":      0,
        "cost":        1_000_000_000_000_000_000,  # 1 Quintillion
        "purchased":   False
    }
  ]


    # ───────────────────────────────────────
    # “Capitalist” (global) unlocks (Earth)
    # ───────────────────────────────────────


# -------------------------------------------------------------------------------
# 11. LOAD ALL BUSINESS IMAGES & GLOBAL ICON & STATS ICON
# -------------------------------------------------------------------------------
def load_all_business_images():
    """
    Loads and scales images for each business, global unlocks, upgrades, and the stats icon.
    - Businesses use their own 'asset_path'.
    - Unlocks with biz_index=None use 'assets/global.png'.
    - Cash-upgrades with biz_index=None also use the global icon.
    - The stats button uses 'assets/stats.png'.
    """
    # ─── LOAD BUSINESS IMAGES (96×96) ───
    for biz in businesses:
        rel = biz.get("asset_path")
        if rel:
            abs_p = resource_path(rel)
            if os.path.isfile(abs_p):
                try:
                    img = pygame.image.load(abs_p).convert_alpha()
                    biz["image"] = pygame.transform.smoothscale(img, (96, 96))
                except Exception:
                    biz["image"] = None
            else:
                biz["image"] = None
        else:
            biz["image"] = None

    # ─── LOAD GLOBAL UNLOCK ICON (96×96) ───
    global_abs = resource_path("assets/global.png")
    if os.path.isfile(global_abs):
        try:
            gimg = pygame.image.load(global_abs).convert_alpha()
            gimg = pygame.transform.smoothscale(gimg, (96, 96))
            for u in unlocks:
                if u.get("biz_index") is None:
                    u["image"] = gimg
        except Exception:
            for u in unlocks:
                if u.get("biz_index") is None:
                    u["image"] = None
    else:
        for u in unlocks:
            if u.get("biz_index") is None:
                u["image"] = None

    # ─── ASSIGN GLOBAL ICON TO CASH-UPGRADES (biz_index=None) ───
    if 'gimg' in locals():
        for upg in upgrades:
            if upg.get("biz_index") is None:
                upg["image"] = gimg
    else:
        for upg in upgrades:
            if upg.get("biz_index") is None:
                upg["image"] = None

    # ─── LOAD STATS ICON (50×50) ───
    try:
        t_abs = resource_path("assets/stats.png")
        if os.path.isfile(t_abs):
            img_t = pygame.image.load(t_abs).convert_alpha()
            globals()["stats_icon"] = pygame.transform.smoothscale(img_t, (50, 50))
        else:
            globals()["stats_icon"] = None
    except Exception:
        globals()["stats_icon"] = None

load_all_business_images()

# -------------------------------------------------------------------------------
# 12. LOAD OR INITIALIZE STATE AT STARTUP
# -------------------------------------------------------------------------------
loaded = load_game()
if loaded is None:
    # No save found → first time playing
    game_state = default_game_state()
    game_state["businesses"] = []
    for biz in businesses:
        game_state["businesses"].append({
            "owned":       biz["owned"],
            "speed_mult":  biz["speed_mult"],
            "profit_mult": biz["profit_mult"],
            "base_time":   biz["base_time"],
            "base_payout": biz["base_payout"],
            "has_manager": biz["has_manager"],
            "unlocked":    biz["unlocked"],
            "timer":       biz["timer"],
            "in_progress": biz["in_progress"]
        })
    game_state["upgrades"] = []
    for upg in upgrades:
        game_state["upgrades"].append({"purchased": upg["purchased"]})
    game_state["unlocked_shown"] = []
    game_state["galactic_upgrades"] = []
    for gu in galactic_upgrades:
        game_state["galactic_upgrades"].append({"purchased": gu["purchased"]})

    # Initialize local variables from default state
    money                       = game_state["money"]
    space_lifetime_earnings     = game_state["space_lifetime_earnings"]
    global_speed_mult           = game_state["global_speed_mult"]
    global_profit_mult          = game_state["global_profit_mult"]
    galactic_investors_total    = game_state["galactic_investors_total"]
    galactic_investors_spent    = game_state["galactic_investors_spent"]
    unlocked_shown              = set(game_state["unlocked_shown"])

    # Prepare a persistent first‐time pop‐up (no auto‐dismiss)
    first_time_popup = True
    pw = int(WIDTH * 0.6)
    ph = int(HEIGHT * 0.7)
    px = (WIDTH - pw) // 2
    py = (HEIGHT - ph) // 2
    first_time_popup_rect = pygame.Rect(px, py, pw, ph)
    cb_size = 32
    cb_x = px + pw - cb_size - 12
    cb_y = py + 12
    first_time_popup_close = pygame.Rect(cb_x, cb_y, cb_size, cb_size)

    cycle_start_time  = time.time()
    cycle_start_money = money

    click_count = 0
    session_start_time = time.time()
    playtime_this_prestige = 0.0
    total_playtime = 0.0

else:
    game_state = loaded

    # Restore all per‐business fields (use defaults for missing keys)
    for idx, biz_saved in enumerate(game_state["businesses"]):
        biz = businesses[idx]
        biz["owned"]       = biz_saved.get("owned", 0)
        biz["speed_mult"]  = biz_saved.get("speed_mult", 1.0)
        biz["profit_mult"] = biz_saved.get("profit_mult", 1.0)
        biz["unlocked"]    = biz_saved.get("unlocked", False)
        biz["has_manager"] = biz_saved.get("has_manager", False)
        biz["timer"]       = biz_saved.get("timer", 0.0)
        biz["in_progress"] = biz_saved.get("in_progress", False)

    # Restore upgrades safely (guard against saved list being longer)
    for i, upg_saved in enumerate(game_state["upgrades"]):
        if i < len(upgrades):
            upgrades[i]["purchased"] = upg_saved.get("purchased", False)

    unlocked_shown = set(game_state.get("unlocked_shown", []))

    # Restore galactic_upgrades safely
    for i, gu_saved in enumerate(game_state.get("galactic_upgrades", [])):
        if i < len(galactic_upgrades):
            galactic_upgrades[i]["purchased"] = gu_saved.get("purchased", False)

    # Restore core numeric values
    money                       = game_state.get("money", 5.0)
    space_lifetime_earnings     = game_state.get("space_lifetime_earnings", 0)
    global_speed_mult           = game_state.get("global_speed_mult", 1.0)
    global_profit_mult          = game_state.get("global_profit_mult", 1.0)
    galactic_investors_total    = game_state.get("galactic_investors_total", 0)
    galactic_investors_spent    = game_state.get("galactic_investors_spent", 0)

    # Offline earnings & timer adjustments
    now_ts = time.time()
    offline_earned = calculate_offline_earnings(game_state, now_ts)
    if offline_earned > 0:
        money = game_state["money"]
        mant, suff = format_number_parts(int(offline_earned))
        popup_message = {
            "text": f"You earned ${mant}{suff} while away",
            "requirement": "Press X to close"
        }
        popup_end_time = pygame.time.get_ticks() + 3000

    load_all_business_images()

    cycle_start_time  = now_ts
    cycle_start_money = money

    click_count = game_state.get("click_count", 0)
    session_start_time = now_ts - game_state.get("total_playtime", 0.0)
    playtime_this_prestige = game_state.get("playtime_this_prestige", 0.0)
    total_playtime = game_state.get("total_playtime", 0.0)

if loaded is None:
    for idx, biz in enumerate(businesses):
        game_state["businesses"][idx] = {
            "owned":       biz["owned"],
            "speed_mult":  biz["speed_mult"],
            "profit_mult": biz["profit_mult"],
            "base_time":   biz["base_time"],
            "base_payout": biz["base_payout"],
            "has_manager": biz["has_manager"],
            "unlocked":    biz["unlocked"],
            "timer":       biz["timer"],
            "in_progress": biz["in_progress"]
        }
    for idx, upg in enumerate(upgrades):
        game_state["upgrades"][idx] = {"purchased": upg["purchased"]}
    game_state["unlocked_shown"] = list(unlocked_shown)
    for idx, gu in enumerate(galactic_upgrades):
        game_state["galactic_upgrades"][idx] = {"purchased": gu["purchased"]}

    game_state["click_count"] = click_count
    game_state["playtime_this_prestige"] = playtime_this_prestige
    game_state["total_playtime"] = total_playtime

# -------------------------------------------------------------------------------
# 13. APPLY UNLOCKS HELPER
# -------------------------------------------------------------------------------
def apply_single_unlock(idx):
    """
    idx is the index into `unlocks`. If u["type"] is "speed" or "profit", we
    multiply only that business. If u["type"] starts with "global_", we adjust
    global_speed_mult or global_profit_mult. Then we fire a popup.
    Finally, we add idx to unlocked_shown so it never triggers again.
    """
    global popup_message, popup_end_time, global_speed_mult, global_profit_mult

    u = unlocks[idx]
    descr = u["description"]

    if u["biz_index"] is not None:
        biz = businesses[u["biz_index"]]
        if u["type"] == "speed":
            biz["speed_mult"] *= u["multiplier"]
        elif u["type"] == "profit":
            biz["profit_mult"] *= u["multiplier"]
    else:
        if u["type"] == "global_speed":
            global_speed_mult *= u["multiplier"]
        elif u["type"] == "global_profit":
            global_profit_mult *= u["multiplier"]

    popup_message = {
        "text": descr,
        "requirement": "Press X to close"
    }
    popup_end_time = pygame.time.get_ticks() + 2000

    unlocked_shown.add(idx)

# -------------------------------------------------------------------------------
# 14. UI DRAW FUNCTIONS
# -------------------------------------------------------------------------------
def draw_sidebar(surface, mouse_pos, mouse_clicked):
    """
    Draw the left sidebar and detect clicks on: Managers, Upgrades, Unlocks, Investors,
    plus the Stats icon at the bottom-left. Return an integer index for which overlay to open:
      0 = Managers, 1 = Upgrades, 2 = Unlocks, 3 = Investors, 4 = Stats, or None.
    If there is any *new* affordable, unpurchased upgrade while the Upgrades tab is not open,
    draw a red notification dot on the Upgrades button.
    """
    pygame.draw.rect(surface, SIDEBAR_BG, (0, 0, SIDEBAR_WIDTH, HEIGHT))
    title_surf = font_big.render("SpaceRace", True, WHITE)
    surface.blit(title_surf, ((SIDEBAR_WIDTH // 2) - (title_surf.get_width() // 2), 20))

    btn_h = 50
    spacing = 20
    y_start = 100
    result = None

    # ────────────────────────────────────────────────────────
    # Determine which upgrades are currently affordable
    current_affordable = set(
        i for i, upg in enumerate(upgrades)
        if (not upg["purchased"]) and (money >= upg["cost"])
    )

    # The dot appears only if there's at least one index in current_affordable
    # that was not already in prev_affordable_upgrades, and we're not in the Upgrades tab
    upgrade_notification = False
    if overlay_mode != "Upgrades":
        if current_affordable - prev_affordable_upgrades:
            upgrade_notification = True

    # ────────────────────────────────────────────────────────
    # Top four menu items
    labels = ["Managers", "Upgrades", "Unlocks", "Investors"]
    for i, label_text in enumerate(labels):
        y = y_start + i * (btn_h + spacing)
        rect = pygame.Rect(20, y, SIDEBAR_WIDTH - 40, btn_h)
        hovered = rect.collidepoint(mouse_pos)
        color   = BTN_HOVER if hovered else PANEL_DARK
        pygame.draw.rect(surface, color, rect, border_radius=12)
        label = font_med.render(label_text, True, WHITE)
        surface.blit(
            label,
            (rect.x + (rect.w - label.get_width()) // 2,
             rect.y + (rect.h - label.get_height()) // 2)
        )

        # If this is the Upgrades button and we need a notification, draw a red dot
        if i == 1 and upgrade_notification:
            dot_radius = 6
            dot_x = rect.right - dot_radius - 8
            dot_y = rect.top + dot_radius + 8
            pygame.draw.circle(surface, RED_DOT, (dot_x, dot_y), dot_radius)

        if hovered and mouse_clicked:
            result = i  # 0..3

    # ─── bottom-left Stats icon (50×50) ───
    stats_size    = 50
    stats_x    = 20
    stats_y    = HEIGHT - 20 - stats_size
    stats_rect    = pygame.Rect(stats_x, stats_y, stats_size, stats_size)

    hovered_t = stats_rect.collidepoint(mouse_pos)
    bg_color_t = BTN_HOVER if hovered_t else PANEL_DARK
    pygame.draw.rect(surface, bg_color_t, stats_rect, border_radius=8)
    if globals().get("stats_icon"):
        surface.blit(globals()["stats_icon"], (stats_x, stats_y))
    else:
        t_txt = font_med.render("📊", True, WHITE)
        surface.blit(t_txt, (stats_x + (stats_size - t_txt.get_width()) // 2,
                             stats_y + (stats_size - t_txt.get_height()) // 2))
    if hovered_t and mouse_clicked:
        result = 4  # Stats

    return result

def draw_header(surface, money, mouse_pos, mouse_clicked):
    global purchase_index
    pygame.draw.rect(surface, PANEL_DARK, (SIDEBAR_WIDTH, 0, WIDTH - SIDEBAR_WIDTH, HEADER_HEIGHT))

    mant, suff = format_number_parts(money)
    money_label = font_big.render(f"${mant}{suff}", True, WHITE)
    surface.blit(money_label, (SIDEBAR_WIDTH + 20, (HEADER_HEIGHT - money_label.get_height()) // 2))

    # Now six buttons: x1, x5, x10, x50, x100, MAX
    labels = ["x1", "x5", "x10", "x50", "x100", "MAX"]
    total_w = 0
    btn_h   = 32
    gap     = 10
    btn_rects = []

    # Compute total width needed
    for lbl in labels:
        txt = font_small.render(lbl, True, WHITE)
        total_w += txt.get_width() + 20
    total_w += gap * (len(labels) - 1)

    x0 = SIDEBAR_WIDTH + (WIDTH - SIDEBAR_WIDTH) - total_w - 20
    y0 = (HEADER_HEIGHT - btn_h) // 2

    x = x0
    for i, lbl in enumerate(labels):
        txt = font_small.render(lbl, True, WHITE)
        w = txt.get_width() + 20
        rect = pygame.Rect(x, y0, w, btn_h)
        hovered = rect.collidepoint(mouse_pos)
        if i == purchase_index:
            color = ACCENT
        else:
            color = BTN_HOVER if hovered else PANEL_DARK
        pygame.draw.rect(surface, color, rect, border_radius=6)
        surface.blit(txt, (x + (w - txt.get_width()) // 2, y0 + (btn_h - txt.get_height()) // 2))
        btn_rects.append(rect)
        x += w + gap

    if mouse_clicked:
        for i, rect in enumerate(btn_rects):
            if rect.collidepoint(mouse_pos):
                purchase_index = i
                break

def draw_business_panel(surface, dt, mouse_pos, mouse_clicked):
    """
    Draw all businesses in two columns inside a scrollable panel.
    Return (unlock_clicked_index, buy_clicked_index).
    """
    global business_scroll, money, global_speed_mult, space_lifetime_earnings, global_profit_mult

    stripe_threshold = 0.7  # threshold (in seconds) for "fast-cycle" visual

    pygame.draw.rect(surface, BG_DARK, (PANEL_X - 10, PANEL_Y - 10, PANEL_WIDTH + 20, PANEL_HEIGHT + 20))

    n_total       = len(businesses)
    n_per_column  = math.ceil(n_total / 2)
    content_height = n_per_column * (ROW_HEIGHT + ROW_GAP) - ROW_GAP
    max_scroll    = max(0, content_height - PANEL_HEIGHT)
    business_scroll = max(0, min(business_scroll, max_scroll))

    unlock_clicked = None
    buy_clicked    = None

    for idx, biz in enumerate(businesses):
        col = 0 if idx < n_per_column else 1
        row = idx if col == 0 else idx - n_per_column

        x = PANEL_X + col * ((PANEL_WIDTH // 2) + ROW_GAP)
        y = PANEL_Y + row * (ROW_HEIGHT + ROW_GAP) - business_scroll
        biz_rect = pygame.Rect(x, y, (PANEL_WIDTH // 2) - ROW_GAP, ROW_HEIGHT)

        unlocked = biz["unlocked"]
        bg_col   = BUSINESS_BG if unlocked else BUSINESS_BG_LOCKED

        # Only draw if within visible panel bounds
        if y + ROW_HEIGHT < PANEL_Y or y > PANEL_Y + PANEL_HEIGHT:
            continue

        pygame.draw.rect(surface, bg_col, (x, y, biz_rect.w, biz_rect.h), border_radius=18)

        # ICON
        if biz.get("image"):
            icon_surf = biz["image"]
            icon_x = x
            icon_y = y + (ROW_HEIGHT - 96) // 2
            if not unlocked:
                locked_img = icon_surf.copy()
                locked_img.fill((100, 100, 100, 150), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(locked_img, (icon_x, icon_y))
            else:
                surface.blit(icon_surf, (icon_x, icon_y))
        else:
            icon_cx = x + 32
            icon_cy = y + 32
            col_icon = biz["icon_color"] if unlocked else GRAYED
            pygame.draw.circle(surface, col_icon, (icon_cx, icon_cy), 32)
            pygame.draw.circle(surface, PANEL_DARK if unlocked else BUSINESS_BG_LOCKED, (icon_cx, icon_cy), 26)
            pygame.draw.circle(surface, col_icon, (icon_cx, icon_cy), 21)
            icon_label = font_big.render(biz["icon"], True, WHITE if unlocked else GRAYED)
            surface.blit(icon_label, (x + 16, y + 16))

        txt_col   = WHITE if unlocked else GRAYED
        name_surf = font_med.render(biz["name"], True, txt_col)
        surface.blit(name_surf, (x + 100, y + 18))

        profit_mult = (1.0 + (0.02 * galactic_investors_total)) * global_profit_mult * biz["profit_mult"]
        earn_val    = int(biz["base_payout"] * biz["owned"] * profit_mult)
        earn_mant, earn_suff = format_number_parts(earn_val)
        earning_text = f"+${earn_mant}{earn_suff}"
        owned_text   = f"x{biz['owned']}"

        second_y = y + 52
        owned_surf = font_small.render(owned_text, True, txt_col)
        earn_surf  = font_small.render(earning_text, True, (ACCENT if unlocked else GRAYED))
        surface.blit(owned_surf, (x + 100, second_y))
        surface.blit(earn_surf, (x + 100 + owned_surf.get_width() + 20, second_y))

        # Determine how many to buy at once
        opt = purchase_options[purchase_index]
        if opt == -1:
            count = max_affordable(biz, money)
        else:
            count = opt
        if count < 0:
            count = 0

        total_cost = total_cost_for_next_N(biz, count)

        # BUY button is now moved above the progress bar
        btn_w = 140
        btn_h = 50
        btn_x = x + biz_rect.w - btn_w - 10
        btn_y = y + 80 - btn_h - 10
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        mant, suff = format_number_parts(total_cost)
        can_buy     = (money >= total_cost and count > 0 and unlocked)
        hovered_btn = btn_rect.collidepoint(mouse_pos)

        if can_buy:
            base_color = ACCENT
        else:
            base_color = PANEL_DARK
        btn_color = BTN_HOVER if (hovered_btn and can_buy) else base_color

        pygame.draw.rect(surface, btn_color, btn_rect, border_radius=10)

        line1_y = btn_y + 6
        line2_y = btn_y + btn_h // 2 + 2

        left1  = font_small.render("Buy", True, WHITE)
        left2  = font_small.render(f"x{count}", True, WHITE)
        right1 = font_small.render(f"{mant}", True, WHITE)
        right2 = font_small.render(f"{suff}", True, WHITE)

        surface.blit(left1,  (btn_x + 8, line1_y))
        surface.blit(right1, (btn_x + btn_w - right1.get_width() - 8, line1_y))
        surface.blit(left2,  (btn_x + 8, line2_y))
        surface.blit(right2, (btn_x + btn_w - right2.get_width() - 8, line2_y))

        # ── FIXED: Only signal the click, but do NOT apply money/owned here ──
        if hovered_btn and mouse_clicked and can_buy:
            buy_clicked = idx

        if not unlocked:
            # Instead of showing base_cost, show cost_for_count
            unlock_count = count if count > 0 else 1
            unlock_cost  = total_cost_for_next_N(biz, unlock_count)
            cost_mant_u, cost_suff_u = format_number_parts(unlock_cost)
            can_unlock = (money >= unlock_cost)
            cost_color = WHITE if can_unlock else GRAYED

            overlay_surf2 = pygame.Surface((biz_rect.w, biz_rect.h), pygame.SRCALPHA)
            overlay_surf2.fill((40, 42, 56, 180))
            surface.blit(overlay_surf2, (x, y))

            lock_label = font_small.render(f"Cost: ${cost_mant_u}{cost_suff_u}", True, cost_color)
            surface.blit(
                lock_label,
                (x + (biz_rect.w - lock_label.get_width()) // 2,
                 y + (biz_rect.h // 2) - 10)
            )

            # If you click on the locked rect and can afford "count" units, unlock+buy
            if biz_rect.collidepoint(mouse_pos) and mouse_clicked and can_unlock:
                money -= unlock_cost
                biz["owned"]    = unlock_count
                biz["unlocked"] = True
                biz["in_progress"] = False
                biz["timer"]    = 0.0
                unlock_clicked = idx
            continue

        # ICON CLICK TO START PRODUCTION (96×96 hitbox)
        if biz.get("image"):
            icon_hitbox = pygame.Rect(x, y + (ROW_HEIGHT - 96) // 2, 96, 96)
        else:
            icon_hitbox = pygame.Rect(x + 16, y + 16, 64, 64)

        if icon_hitbox.collidepoint(mouse_pos) and mouse_clicked and not biz["in_progress"] and biz["owned"] > 0:
            biz["in_progress"] = True
            effective_time = (biz["base_time"] / biz["speed_mult"]) / global_speed_mult
            biz["timer"] = effective_time

        # ─── PROGRESS BAR WITH FAST‐CYCLE OVERLAY LOGIC ───
        bar_x = x + 100
        bar_y = y + 80
        bar_w = biz_rect.w - 170
        bar_h = 18

        pygame.draw.rect(surface, PROGRESS_BG, (bar_x, bar_y, bar_w, bar_h), border_radius=7)

        if biz["in_progress"]:
            effective_time = (biz["base_time"] / biz["speed_mult"]) / global_speed_mult
            prev_timer = biz["timer"]
            biz["timer"] -= dt * biz["speed_mult"] * global_speed_mult
            reached_zero = False
            if biz["timer"] <= 0:
                biz["timer"] = 0.0
                reached_zero = True

            pct = max(0.0, min(1.0, 1.0 - (biz["timer"] / effective_time))) if effective_time > 0 else 0.0
            fill_w = int(bar_w * pct)

            if effective_time <= stripe_threshold:
                # FAST‐CYCLE: full fill + dark‐green stripes overlay
                pygame.draw.rect(surface, PROGRESS_FILL, (bar_x, bar_y, bar_w, bar_h), border_radius=7)
                clip_rect = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
                surface.set_clip(clip_rect)

                stripe_w = 20
                stripe_speed = 200
                offset = int((pygame.time.get_ticks() / 1000.0) * stripe_speed) % (stripe_w + 20)
                stripe_surf = pygame.Surface((stripe_w, bar_h), pygame.SRCALPHA)
                stripe_surf.fill(DARKER_GREEN)

                x_pos = bar_x - stripe_w + offset
                while x_pos < bar_x + bar_w:
                    surface.blit(stripe_surf, (x_pos, bar_y))
                    x_pos += stripe_w + 20
                surface.set_clip(None)
            else:
                if fill_w > 0:
                    pygame.draw.rect(surface, PROGRESS_FILL, (bar_x, bar_y, fill_w, bar_h), border_radius=7)

            if reached_zero:
                profit_mult = (
                    (1.0 + (0.02 * galactic_investors_total))
                    * global_profit_mult
                    * biz["profit_mult"]
                )
                payout_val = int(biz["base_payout"] * biz["owned"] * profit_mult)
                money += payout_val
                space_lifetime_earnings += payout_val

                if biz["has_manager"]:
                    biz["in_progress"] = True
                    effective_time = (biz["base_time"] / biz["speed_mult"]) / global_speed_mult
                    biz["timer"] = effective_time
                else:
                    biz["in_progress"] = False

            # ─── TIMER BOX just below Buy button and to the left of the progress bar ───
            timer_text = format_time(biz["timer"])
            tw_surf = font_small.render(timer_text, True, WHITE)
            tw_w, tw_h = tw_surf.get_size()
            box_w_t = tw_w + 12
            box_h_t = tw_h + 8
            box_x_t = bar_x - box_w_t - 8
            box_y_t = btn_y + btn_h + 2
            timer_box = pygame.Surface((box_w_t, box_h_t), pygame.SRCALPHA)
            timer_box.fill((40, 44, 55, 200))
            surface.blit(timer_box, (box_x_t, box_y_t))
            surface.blit(tw_surf, (box_x_t + 6, box_y_t + 4))

    # ←── Return must occur *after* the loop finishes, not inside it ──→
    return unlock_clicked, buy_clicked

def draw_managers_ui(surface, mouse_pos, mouse_clicked):
    global close_btn_rect, money, manager_scroll, manager_dragging, manager_drag_offset

    overlay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay_surf.fill((30, 30, 40, 210))
    surface.blit(overlay_surf, (0, 0))

    box_w = int(WIDTH * 0.6)
    box_h = int(HEIGHT * 0.7)
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2
    pygame.draw.rect(surface, PANEL_DARK, (box_x, box_y, box_w, box_h), border_radius=12)

    # TITLE + CLOSE BUTTON
    t_surf = font_big.render("Hire Managers", True, WHITE)
    surface.blit(t_surf, (box_x + (box_w - t_surf.get_width()) // 2, box_y + 20))

    close_size = 24
    close_x    = box_x + box_w - close_size - 12
    close_y    = box_y + 12
    close_btn_rect = pygame.Rect(close_x, close_y, close_size, close_size)
    pygame.draw.rect(surface, BTN_HOVER, close_btn_rect, border_radius=4)
    x_surf = font_small.render("X", True, WHITE)
    surface.blit(
        x_surf,
        (close_x + (close_size - x_surf.get_width()) // 2,
         close_y + (close_size - x_surf.get_height()) // 2)
    )

    header_y = box_y + 60
    col1_x = box_x + 20
    col2_x = box_x + 100
    col3_x = box_x + box_w - 280
    col4_x = box_x + box_w - 120

    mgr_list_y0  = header_y + 40
    scroll_top    = mgr_list_y0
    scroll_bottom = box_y + box_h - 20
    visible_h     = scroll_bottom - scroll_top
    clip_rect     = pygame.Rect(box_x + 10, scroll_top, box_w - 20, visible_h)
    surface.set_clip(clip_rect)

    mgr_entry_h = 60
    spacing     = 10

    total_content_h = len(businesses) * (mgr_entry_h + spacing)
    max_mgr_scroll  = max(0, total_content_h - visible_h)
    manager_scroll  = max(0, min(manager_scroll, max_mgr_scroll))

    y_offset = mgr_list_y0 - manager_scroll

    for biz in businesses:
        biz_unlocked = biz["unlocked"]
        biz_has_mgr  = biz["has_manager"]
        cost_val     = biz["manager_cost"]
        cost_mant, cost_suff = format_number_parts(cost_val)

        if (y_offset + mgr_entry_h < scroll_top) or (y_offset > scroll_bottom):
            y_offset += mgr_entry_h + spacing
            continue

        entry_rect = pygame.Rect(box_x + 10, y_offset, box_w - 20, mgr_entry_h)
        pygame.draw.rect(surface, (50, 50, 70), entry_rect, border_radius=8)

        # ICON
        icon_size = 60
        icon_y    = y_offset + (mgr_entry_h - icon_size) // 2
        if biz.get("image"):
            icon_surf = pygame.transform.smoothscale(biz["image"], (icon_size, icon_size))
            if not biz_unlocked:
                locked_img = icon_surf.copy()
                locked_img.fill((100, 100, 100, 150), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(locked_img, (col1_x, icon_y))
            else:
                surface.blit(icon_surf, (col1_x, icon_y))
        else:
            color = GRAYED if not biz_unlocked else WHITE
            icosurf = font_big.render(biz["icon"], True, color)
            surface.blit(icosurf, (col1_x, icon_y))

        # NAME
        name_color = GRAYED if not biz_unlocked else YELLOW
        name_surf  = font_med.render(biz["name"], True, name_color)
        surface.blit(name_surf, (col2_x, y_offset + 6))

        # DESCRIPTION or “Locked”
        if biz_unlocked:
            effect_text = "Automatically restarts production when idle"
        else:
            effect_text = "Locked until you unlock that business"
        effect_surf = font_small.render(effect_text, True, GRAYED)
        surface.blit(effect_surf, (col2_x, y_offset + 30))

        # COST
        cost_surf = font_small.render(f"${cost_mant}{cost_suff}", True, ACCENT)
        surface.blit(cost_surf, (col2_x, y_offset + 45))

        # HIRE BUTTON
        hire_rect = pygame.Rect(col4_x, y_offset + 15, 100, 30)
        if not biz_unlocked:
            btn_label  = "Locked"
            can_hire   = False
            base_color = PANEL_DARK
        elif biz_has_mgr:
            btn_label  = "Hired"
            can_hire   = False
            base_color = PANEL_DARK
        else:
            btn_label  = "Hire"
            can_hire   = (money >= cost_val)
            base_color = ACCENT if can_hire else PANEL_DARK

        if hire_rect.collidepoint(mouse_pos) and can_hire:
            hire_color = BTN_HOVER
        else:
            hire_color = base_color

        pygame.draw.rect(surface, hire_color, hire_rect, border_radius=6)
        hire_txt = font_small.render(btn_label, True, WHITE)
        surface.blit(
            hire_txt,
            (
                hire_rect.x + (hire_rect.w - hire_txt.get_width()) // 2,
                hire_rect.y + (hire_rect.h - hire_txt.get_height()) // 2
            )
        )

        if hire_rect.collidepoint(mouse_pos) and mouse_clicked and can_hire:
            money -= cost_val
            biz["has_manager"] = True
            if biz["owned"] > 0 and not biz["in_progress"]:
                biz["in_progress"] = True
                effective_time = (biz["base_time"] / biz["speed_mult"]) / global_speed_mult
                biz["timer"]     = effective_time

        y_offset += mgr_entry_h + spacing

    surface.set_clip(None)

    if total_content_h > visible_h:
        track_x = box_x + box_w - 12
        track_y = scroll_top
        track_w = 6
        track_h = visible_h
        pygame.draw.rect(surface, (60, 60, 80), (track_x, track_y, track_w, track_h), border_radius=3)

        thumb_h = max(20, int((visible_h / total_content_h) * visible_h))
        max_thumb_travel = visible_h - thumb_h
        if max_mgr_scroll > 0:
            thumb_y = scroll_top + int((manager_scroll / max_mgr_scroll) * max_thumb_travel)
        else:
            thumb_y = scroll_top

        thumb_rect = pygame.Rect(track_x, thumb_y, track_w, thumb_h)
        thumb_color = ACCENT if thumb_rect.collidepoint(mouse_pos) else BTN_HOVER
        pygame.draw.rect(surface, thumb_color, thumb_rect, border_radius=3)

        global manager_dragging, manager_drag_offset
        if mouse_clicked and thumb_rect.collidepoint(mouse_pos):
            manager_dragging = True
            manager_drag_offset = mouse_pos[1] - thumb_y

        if manager_dragging and pygame.mouse.get_pressed()[0]:
            new_y = mouse_pos[1] - manager_drag_offset
            new_y = max(scroll_top, min(scroll_top + max_thumb_travel, new_y))
            manager_scroll = int(((new_y - scroll_top) / max_thumb_travel) * max_mgr_scroll) if max_thumb_travel > 0 else 0
        elif not pygame.mouse.get_pressed()[0]:
            manager_dragging = False

    return close_btn_rect

def draw_upgrades_ui(surface, mouse_pos, mouse_clicked):
    global close_btn_rect, money, upgrade_scroll, upgrade_dragging, upgrade_drag_offset, prev_affordable_upgrades

    overlay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay_surf.fill((30, 30, 40, 210))
    surface.blit(overlay_surf, (0, 0))

    box_w = int(WIDTH * 0.6)
    box_h = int(HEIGHT * 0.7)
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2
    pygame.draw.rect(surface, PANEL_DARK, (box_x, box_y, box_w, box_h), border_radius=12)

    # “Buy All” button at top-left of the Upgrades box
    buyall_rect = pygame.Rect(box_x + 20, box_y + 20, 100, 30)
    buyall_hovered = buyall_rect.collidepoint(mouse_pos)
    buyall_color = BTN_HOVER if buyall_hovered else ACCENT
    pygame.draw.rect(surface, buyall_color, buyall_rect, border_radius=6)
    buyall_txt = font_small.render("Buy All", True, WHITE)
    surface.blit(
        buyall_txt,
        (buyall_rect.x + (buyall_rect.w - buyall_txt.get_width()) // 2,
         buyall_rect.y + (buyall_rect.h - buyall_txt.get_height()) // 2)
    )

    title_surf = font_big.render("Purchase Upgrades", True, WHITE)
    surface.blit(
        title_surf,
        (box_x + (box_w - title_surf.get_width()) // 2, box_y + 20 + buyall_rect.height + 10)
    )

    close_size = 24
    close_x    = box_x + box_w - close_size - 12
    close_y    = box_y + 12
    close_btn_rect = pygame.Rect(close_x, close_y, close_size, close_size)
    pygame.draw.rect(surface, BTN_HOVER, close_btn_rect, border_radius=4)
    x_surf = font_small.render("X", True, WHITE)
    surface.blit(
        x_surf,
        (close_x + (close_size - x_surf.get_width()) // 2,
         close_y + (close_size - x_surf.get_height()) // 2)
    )

    # As soon as we draw Upgrades UI, clear the notification
    current_affordable = set(
        i for i, upg in enumerate(upgrades)
        if (not upg["purchased"]) and (money >= upg["cost"])
    )
    prev_affordable_upgrades = set(current_affordable)

    header_y = box_y + 20 + buyall_rect.height + 10 + 40
    col1_x = box_x + 5
    col2_x = box_x + 60
    col3_x = box_x + box_w - 140

    surface.blit(font_med.render("Upgrade", True, WHITE), (col2_x, header_y))
    surface.blit(font_med.render("Cost", True, WHITE),    (col3_x, header_y))

    scroll_top    = header_y + 40
    scroll_bottom = box_y + box_h - 20
    visible_h     = scroll_bottom - scroll_top

    entry_h = 80
    spacing = 10

    unpurchased_upgs = [u for u in upgrades if not u["purchased"]]
    sorted_upgs      = sorted(unpurchased_upgs, key=lambda u: u["cost"])

    total_content_h = len(sorted_upgs) * (entry_h + spacing)
    max_scroll      = max(0, total_content_h - visible_h)
    upgrade_scroll  = max(0, min(upgrade_scroll, max_scroll))

    clip_rect = pygame.Rect(box_x + 10, scroll_top, box_w - 20, visible_h)
    surface.set_clip(clip_rect)
    y_offset = scroll_top - upgrade_scroll

    for upg in sorted_upgs:
        if upg["purchased"]:
            y_offset += entry_h + spacing
            continue

        if (y_offset + entry_h < scroll_top) or (y_offset > scroll_bottom):
            y_offset += entry_h + spacing
            continue

        entry_rect = pygame.Rect(box_x + 10, y_offset, box_w - 20, entry_h)
        pygame.draw.rect(surface, (50, 50, 70), entry_rect, border_radius=8)

        biz_index = upg.get("biz_index")

        icon_size = 60
        icon_y = y_offset + (entry_h - icon_size) // 2

        if biz_index is None:
            biz_name = "All Businesses"
            if upg.get("image"):
                gimg_surf = pygame.transform.smoothscale(upg["image"], (icon_size, icon_size))
                surface.blit(gimg_surf, (col1_x, icon_y))
            else:
                placeholder = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                pygame.draw.circle(
                    placeholder,
                    (150, 150, 150),
                    (icon_size // 2, icon_size // 2),
                    icon_size // 2
                )
                surface.blit(placeholder, (col1_x, icon_y))
        else:
            if not isinstance(biz_index, int) or not (0 <= biz_index < len(businesses)):
                y_offset += entry_h + spacing
                continue

            biz      = businesses[biz_index]
            biz_name = biz["name"]
            if biz.get("image"):
                small_img = pygame.transform.smoothscale(biz["image"], (icon_size, icon_size))
                surface.blit(small_img, (col1_x, icon_y))
            else:
                icon_surf = font_big.render(biz["icon"], True, WHITE)
                surface.blit(icon_surf, (col1_x, icon_y))

        name_surf = font_med.render(upg["name"], True, YELLOW)
        surface.blit(name_surf, (col2_x, y_offset + 8))

        desc_text = f"{biz_name} profit ×{upg['multiplier']}"
        desc_surf = font_small.render(desc_text, True, GRAYED)
        surface.blit(desc_surf, (col2_x, y_offset + 30))

        cost_val = upg["cost"]
        cost_mant, cost_suff = format_number_parts(cost_val)
        can_buy  = (money >= cost_val)
        cost_color = ACCENT if can_buy else GRAYED
        cost_surf = font_small.render(f"${cost_mant}{cost_suff}", True, cost_color)
        surface.blit(cost_surf, (col2_x, y_offset + 45))

        buy_rect = pygame.Rect(col3_x, y_offset + 15, 100, 30)
        base_color = ACCENT if can_buy else PANEL_DARK
        buy_color  = BTN_HOVER if (buy_rect.collidepoint(mouse_pos) and can_buy) else base_color
        pygame.draw.rect(surface, buy_color, buy_rect, border_radius=6)

        buy_txt = font_small.render("Buy!", True, WHITE)
        surface.blit(
            buy_txt,
            (buy_rect.x + (buy_rect.w - buy_txt.get_width()) // 2,
             buy_rect.y + (buy_rect.h - buy_txt.get_height()) // 2)
        )

        if buy_rect.collidepoint(mouse_pos) and mouse_clicked and can_buy:
            money -= cost_val
            if biz_index is None:
                for b in businesses:
                    b["profit_mult"] *= upg["multiplier"]
            else:
                businesses[biz_index]["profit_mult"] *= upg["multiplier"]
            upg["purchased"] = True

            remaining    = [u2 for u2 in upgrades if not u2["purchased"]]
            new_total_h  = len(remaining) * (entry_h + spacing)
            new_max_scroll = max(0, new_total_h - visible_h)
            upgrade_scroll = min(upgrade_scroll + (entry_h + spacing), new_max_scroll)

        y_offset += entry_h + spacing

    surface.set_clip(None)

    # ─── Scrollbar drawing ───
    if total_content_h > visible_h:
        track_x = box_x + box_w - 12
        track_y = scroll_top
        track_w = 6
        track_h = visible_h
        pygame.draw.rect(surface, (60, 60, 80), (track_x, track_y, track_w, track_h), border_radius=3)

        thumb_h = max(20, int((visible_h / total_content_h) * visible_h))
        max_thumb_travel = visible_h - thumb_h
        if max_scroll > 0:
            thumb_y = scroll_top + int((upgrade_scroll / max_scroll) * max_thumb_travel)
        else:
            thumb_y = scroll_top

        thumb_rect = pygame.Rect(track_x, thumb_y, track_w, thumb_h)
        thumb_color = ACCENT if thumb_rect.collidepoint(mouse_pos) else BTN_HOVER
        pygame.draw.rect(surface, thumb_color, thumb_rect, border_radius=3)

        global upgrade_dragging, upgrade_drag_offset
        if mouse_clicked and thumb_rect.collidepoint(mouse_pos):
            upgrade_dragging   = True
            upgrade_drag_offset = mouse_pos[1] - thumb_y

        if upgrade_dragging and pygame.mouse.get_pressed()[0]:
            new_y = mouse_pos[1] - upgrade_drag_offset
            new_y = max(scroll_top, min(scroll_top + max_thumb_travel, new_y))
            upgrade_scroll = int(((new_y - scroll_top) / max_thumb_travel) * max_scroll) if max_thumb_travel > 0 else 0
        elif not pygame.mouse.get_pressed()[0]:
            upgrade_dragging = False

    # ─── “Buy All” logic: if clicked, attempt to buy every affordable upgrade ───
    if buyall_rect.collidepoint(mouse_pos) and mouse_clicked:
        something_bought = True
        while something_bought:
            something_bought = False
            for upg2 in sorted_upgs:
                if upg2["purchased"]:
                    continue
                cost2 = upg2["cost"]
                if money >= cost2:
                    money -= cost2
                    if upg2.get("biz_index") is None:
                        for b2 in businesses:
                            b2["profit_mult"] *= upg2["multiplier"]
                    else:
                        businesses[upg2["biz_index"]]["profit_mult"] *= upg2["multiplier"]
                    upg2["purchased"] = True
                    something_bought = True
                    break  # restart scanning from top

    return close_btn_rect

def draw_unlocks_ui(surface, mouse_pos, mouse_clicked):
    global close_btn_rect, unlock_scroll, unlock_dragging, unlock_drag_offset

    overlay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay_surf.fill((30, 30, 40, 210))
    surface.blit(overlay_surf, (0, 0))

    box_w = int(WIDTH * 0.6)
    box_h = int(HEIGHT * 0.7)
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2
    pygame.draw.rect(surface, PANEL_DARK, (box_x, box_y, box_w, box_h), border_radius=12)

    title_surf = font_big.render("Unlocks", True, WHITE)
    surface.blit(title_surf, (box_x + (box_w - title_surf.get_width()) // 2, box_y + 20))

    close_size = 24
    close_x    = box_x + box_w - close_size - 12
    close_y    = box_y + 12
    close_btn_rect = pygame.Rect(close_x, close_y, close_size, close_size)
    pygame.draw.rect(surface, BTN_HOVER, close_btn_rect, border_radius=4)
    x_surf = font_small.render("X", True, WHITE)
    surface.blit(
        x_surf,
        (close_x + (close_size - x_surf.get_width()) // 2,
         close_y + (close_size - x_surf.get_height()) // 2)
    )

    header_y = box_y + 60
    col1_x = box_x + 5
    col2_x = box_x + 80
    col3_x = box_x + box_w - 140

    surface.blit(font_med.render("Unlock / Global", True, WHITE), (col2_x, header_y))
    surface.blit(font_med.render("Status", True, WHITE), (col3_x, header_y))

    scroll_top    = header_y + 40
    scroll_bottom = box_y + box_h - 20
    visible_h     = scroll_bottom - scroll_top

    entry_h = 60
    spacing = 10

    total_content_h = len(unlocks) * (entry_h + spacing)
    max_scroll  = max(0, total_content_h - visible_h)
    unlock_scroll = max(0, min(unlock_scroll, max_scroll))

    clip_rect = pygame.Rect(box_x + 10, scroll_top, box_w - 20, visible_h)
    surface.set_clip(clip_rect)

    y_offset = scroll_top - unlock_scroll

    for idx, u in enumerate(unlocks):
        if u["biz_index"] is not None:
            b = businesses[u["biz_index"]]
            is_unlocked = (b["owned"] >= u["threshold"])
        else:
            is_unlocked = all(bz["owned"] >= u["threshold"] for bz in businesses)

        if y_offset + entry_h < scroll_top or y_offset > scroll_bottom:
            y_offset += entry_h + spacing
            continue

        entry_rect = pygame.Rect(box_x + 10, y_offset, box_w - 20, entry_h)
        pygame.draw.rect(surface, (50, 50, 70), entry_rect, border_radius=8)

        icon_size = 60
        icon_y = y_offset + (entry_h - icon_size) // 2

        if u["biz_index"] is not None:
            biz = businesses[u["biz_index"]]
            if biz.get("image"):
                icon_img = pygame.transform.smoothscale(biz["image"], (icon_size, icon_size))
                surface.blit(icon_img, (col1_x, icon_y))
            else:
                icon_surf = font_big.render(biz["icon"], True, WHITE)
                surface.blit(icon_surf, (col1_x, icon_y))
        else:
            if u.get("image"):
                gimg_surf = pygame.transform.smoothscale(u["image"], (icon_size, icon_size))
                surface.blit(gimg_surf, (col1_x, icon_y))
            else:
                globe_surf = font_big.render("🌐", True, WHITE)
                surface.blit(globe_surf, (col1_x, icon_y))

        name_surf = font_med.render(u["description"], True, YELLOW)
        surface.blit(name_surf, (col2_x, y_offset + 8))

        if u["biz_index"] is not None:
            req_text = f"Own {u['threshold']} {businesses[u['biz_index']]['name']}"
        else:
            req_text = f"Own {u['threshold']} of every business"
        req_surf = font_small.render(req_text, True, GRAYED)
        surface.blit(req_surf, (col2_x, y_offset + 30))

        status_text = "Unlocked" if is_unlocked else "Locked"
        status_color = ACCENT if is_unlocked else GRAYED
        status_surf = font_small.render(status_text, True, status_color)
        surface.blit(status_surf, (col3_x, y_offset + 20))

        y_offset += entry_h + spacing

    surface.set_clip(None)

    if total_content_h > visible_h:
        track_x = box_x + box_w - 12
        track_y = scroll_top
        track_w = 6
        track_h = visible_h
        pygame.draw.rect(surface, (60, 60, 80), (track_x, track_y, track_w, track_h), border_radius=3)

        thumb_h = max(20, int((visible_h / total_content_h) * visible_h))
        max_thumb_travel = visible_h - thumb_h
        if max_scroll > 0:
            thumb_y = scroll_top + int((unlock_scroll / max_scroll) * max_thumb_travel)
        else:
            thumb_y = scroll_top

        thumb_rect = pygame.Rect(track_x, thumb_y, track_w, thumb_h)
        thumb_color = ACCENT if thumb_rect.collidepoint(mouse_pos) else BTN_HOVER
        pygame.draw.rect(surface, thumb_color, thumb_rect, border_radius=3)

        global unlock_dragging, unlock_drag_offset
        if mouse_clicked and thumb_rect.collidepoint(mouse_pos):
            unlock_dragging = True
            unlock_drag_offset = mouse_pos[1] - thumb_y

        if unlock_dragging and pygame.mouse.get_pressed()[0]:
            new_y = mouse_pos[1] - unlock_drag_offset
            new_y = max(scroll_top, min(scroll_top + max_thumb_travel, new_y))
            unlock_scroll = int(((new_y - scroll_top) / max_thumb_travel) * max_scroll) if max_thumb_travel > 0 else 0
        elif not pygame.mouse.get_pressed()[0]:
            unlock_dragging = False

    return close_btn_rect

def draw_investors_ui(surface, mouse_pos, mouse_clicked):
    global close_btn_rect, show_investor_shop, galactic_investors_total, galactic_investors_spent
    global investor_shop_scroll, global_speed_mult, global_profit_mult
    global money, space_lifetime_earnings, businesses, upgrades, unlocked_shown, session_start_time, playtime_this_prestige

    overlay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay_surf.fill((30, 30, 40, 210))
    surface.blit(overlay_surf, (0, 0))

    box_w = int(WIDTH * 0.6)
    box_h = int(HEIGHT * 0.7)
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2
    pygame.draw.rect(surface, PANEL_DARK, (box_x, box_y, box_w, box_h), border_radius=12)

    close_size = 24
    if not show_investor_shop:
        # ─── Main "Galactic Investors" view ───
        close_x = box_x + box_w - close_size - 12
        close_y = box_y + 12
        close_btn_rect = pygame.Rect(close_x, close_y, close_size, close_size)
        pygame.draw.rect(surface, BTN_HOVER, close_btn_rect, border_radius=4)
        x_surf = font_small.render("X", True, WHITE)
        surface.blit(
            x_surf,
            (close_x + (close_size - x_surf.get_width()) // 2,
             close_y + (close_size - x_surf.get_height()) // 2)
        )

        title_surf = font_big.render("Galactic Investors", True, WHITE)
        surface.blit(title_surf, (box_x + (box_w - title_surf.get_width()) // 2, box_y + 20))

        tagline = "Putting the ‘Galaxy’ back in ‘Galactic profits’!"
        tag_surf = font_small.render(tagline, True, GRAYED)
        surface.blit(tag_surf, (box_x + (box_w - tag_surf.get_width()) // 2, box_y + 60))

        info_y = box_y + 100
        line_spacing = 30

        # Total GIs
        gis_text = font_med.render(f"Total GIs: {galactic_investors_total}", True, WHITE)
        surface.blit(gis_text, (box_x + 40, info_y))

        # Bonus per GI
        bonus_text = font_med.render("Bonus per GI: 2%", True, WHITE)
        surface.blit(bonus_text, (box_x + 40, info_y + line_spacing))

        # GIs Spent
        spent_text = font_med.render(f"GIs Spent: {galactic_investors_spent}", True, WHITE)
        surface.blit(spent_text, (box_x + 40, info_y + 2 * line_spacing))

        # ─── Lifetime Earnings: format with format_number_parts ───
        mantissa, suffix = format_number_parts(int(space_lifetime_earnings))
        lte_text = font_med.render(f"Lifetime Earnings: {mantissa}{suffix}", True, WHITE)
        surface.blit(lte_text, (box_x + 40, info_y + 3 * line_spacing))

        # Calculate how many new GIs are available to collect
        # Use space_lifetime_earnings directly instead of undefined lf_q
        lf_q_value = space_lifetime_earnings / 1e15
        potential = int(150 * math.sqrt(lf_q_value)) if lf_q_value > 0 else 0
        new_gis = max(0, potential - galactic_investors_spent)

        # ─── Draw “Available Galactic Investors to collect: <new_gis>” text ───
        avail_text = f"Available Galactic Investors to collect: {new_gis}"
        avail_surf = font_med.render(avail_text, True, WHITE)
        surface.blit(avail_surf, (box_x + 40, box_y + box_h - 200))

        # ─── “Invest” button ───
        invest_btn_rect = pygame.Rect(box_x + 40, box_y + box_h - 160, box_w - 80, 40)
        if new_gis > 0:
            invest_color = ACCENT if not invest_btn_rect.collidepoint(mouse_pos) else BTN_HOVER
        else:
            invest_color = PANEL_DARK
        pygame.draw.rect(surface, invest_color, invest_btn_rect, border_radius=6)
        invest_surf = font_small.render("Invest", True, WHITE)
        surface.blit(
            invest_surf,
            (invest_btn_rect.x + (invest_btn_rect.w - invest_surf.get_width()) // 2,
             invest_btn_rect.y + (invest_btn_rect.h - invest_surf.get_height()) // 2)
        )
        if invest_btn_rect.collidepoint(mouse_pos) and mouse_clicked and new_gis > 0:
            # Collect all available GIs
            collect_amt = new_gis
            galactic_investors_total += collect_amt
            galactic_investors_spent += collect_amt

            # Reset everything except GIs and investor unlocks
            money = 0.0
            space_lifetime_earnings = 0.0
            for biz in businesses:
                biz["owned"] = 0
                biz["speed_mult"] = 1.0
                biz["profit_mult"] = 1.0
                biz["unlocked"] = False
                biz["has_manager"] = False
                biz["in_progress"] = False
                biz["timer"] = 0.0
            businesses[0]["unlocked"] = True
            businesses[0]["owned"]   = 1

            for upg in upgrades:
                upg["purchased"] = False
            unlocked_shown.clear()

            # Reset cycle timers
            global cycle_start_time, cycle_start_money, playtime_this_prestige
            cycle_start_time = time.time()
            cycle_start_money = money
            playtime_this_prestige = 0.0

        # ─── “Investor Shop” button ───
        shop_btn_rect = pygame.Rect(box_x + 40, box_y + box_h - 100, box_w - 80, 40)
        shop_color = ACCENT if not shop_btn_rect.collidepoint(mouse_pos) else BTN_HOVER
        pygame.draw.rect(surface, shop_color, shop_btn_rect, border_radius=6)
        shop_surf = font_small.render("Investor Shop", True, WHITE)
        surface.blit(
            shop_surf,
            (shop_btn_rect.x + (shop_btn_rect.w - shop_surf.get_width()) // 2,
             shop_btn_rect.y + (shop_btn_rect.h - shop_surf.get_height()) // 2)
        )
        if shop_btn_rect.collidepoint(mouse_pos) and mouse_clicked:
            show_investor_shop = True

        return close_btn_rect

    else:
        # ─── Investor Shop sub‐view ───
        title_surf = font_big.render("GALACTIC INVESTOR SHOP", True, WHITE)
        surface.blit(title_surf, (box_x + (box_w - title_surf.get_width()) // 2, box_y + 20))

        # Draw “X” close button instead of back arrow
        close_x = box_x + box_w - close_size - 12
        close_y = box_y + 12
        close_btn_rect = pygame.Rect(close_x, close_y, close_size, close_size)
        pygame.draw.rect(surface, BTN_HOVER, close_btn_rect, border_radius=4)
        x_surf = font_small.render("X", True, WHITE)
        surface.blit(
            x_surf,
            (close_x + (close_size - x_surf.get_width()) // 2,
             close_y + (close_size - x_surf.get_height()) // 2)
        )
        if close_btn_rect.collidepoint(mouse_pos) and mouse_clicked:
            show_investor_shop = False

        draw_investor_shop_list(surface, mouse_pos, mouse_clicked)
        return close_btn_rect


def draw_investor_shop_list(surface, mouse_pos, mouse_clicked):
    global investor_shop_scroll, galactic_investors_total, galactic_investors_spent
    global global_speed_mult, global_profit_mult
    global investor_shop_dragging, investor_shop_drag_offset

    box_w = int(WIDTH * 0.6)
    box_h = int(HEIGHT * 0.7)
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2

    line_y = box_y + 70
    pygame.draw.line(
        surface,
        GRAYED,
        (box_x + 20, line_y),
        (box_x + box_w - 20, line_y),
        1
    )

    list_top    = line_y + 20
    list_bottom = box_y + box_h - 20
    visible_h   = list_bottom - list_top
    entry_h = max(INVESTOR_ICON_SIZE + ENTRY_PADDING, 60)
    spacing     = 12

    # Clip to the scrolling region
    clip_rect = pygame.Rect(box_x + 10, list_top, box_w - 20, visible_h)
    surface.set_clip(clip_rect)

    unpurchased = [g for g in galactic_upgrades if not g.get("purchased", False)]
    total_h     = len(unpurchased) * (entry_h + spacing)
    max_scroll  = max(0, total_h - visible_h)
    investor_shop_scroll = max(0, min(investor_shop_scroll, max_scroll))

    y_offset = list_top - investor_shop_scroll
    col1_x = box_x + 20               # where the icon goes
    col2_x = box_x + 80               # text column
    col3_x = box_x + box_w - 140      # “Buy” button right‐edge

    for upgrade in unpurchased:
        # If this entry is off‐screen, skip
        if (y_offset + entry_h < list_top) or (y_offset > list_bottom):
            y_offset += entry_h + spacing
            continue

        entry_rect = pygame.Rect(box_x + 10, y_offset, box_w - 20, entry_h)
        pygame.draw.rect(surface, (50, 50, 70), entry_rect, border_radius=8)

        # ───── ICON ─────
        try:
            img = pygame.image.load(resource_path(upgrade["icon_image"])).convert_alpha()
            img = pygame.transform.smoothscale(img, (INVESTOR_ICON_SIZE, INVESTOR_ICON_SIZE))
            surface.blit(
                img,
                (col1_x, y_offset + (entry_h - INVESTOR_ICON_SIZE) // 2)
            )
        except Exception:
            # Fallback: draw a grey circle if asset not found
            placeholder = pygame.Surface((INVESTOR_ICON_SIZE, INVESTOR_ICON_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(
                placeholder,
                (150, 150, 150),
                (INVESTOR_ICON_SIZE // 2, INVESTOR_ICON_SIZE // 2),
                INVESTOR_ICON_SIZE // 2
            )
            surface.blit(
                placeholder,
                (col1_x, y_offset + (entry_h - INVESTOR_ICON_SIZE) // 2)
            )

        # ───── NAME & DESCRIPTION ─────
        name_surf = font_med.render(upgrade.get("name", ""), True, YELLOW)
        surface.blit(name_surf, (col2_x, y_offset + 8))

        desc_surf = font_small.render(upgrade.get("description", ""), True, GRAYED)
        surface.blit(desc_surf, (col2_x, y_offset + 30))

        # ───── PRICE BELOW DESCRIPTION ─────
        cost_val = upgrade.get("cost", 0)
        mant, suff = format_number_parts(cost_val)
        price_text = f"${mant}{suff}"
        price_surf = font_small.render(price_text, True, ACCENT)
        surface.blit(price_surf, (col2_x, y_offset + 50))

        # ───── “Buy” button ─────
        can_buy = (galactic_investors_total >= cost_val)
        buy_label = font_small.render("Buy", True, WHITE)
        padding = 20
        btn_w = buy_label.get_width() + padding
        btn_h = 32

        btn_x = col3_x
        if btn_x + btn_w > box_x + box_w - 10:
            btn_x = (box_x + box_w - 10) - btn_w

        buy_rect = pygame.Rect(col3_x, y_offset + (entry_h // 2) - 15, 100, 30)

        if can_buy:
            base_color = ACCENT
            btn_color  = BTN_HOVER if buy_rect.collidepoint(mouse_pos) else ACCENT
        else:
            base_color = PANEL_DARK
            btn_color  = PANEL_DARK

        pygame.draw.rect(surface, btn_color, buy_rect, border_radius=6)
        surface.blit(
            buy_label,
            (
                buy_rect.x + (buy_rect.w - buy_label.get_width())//2,
                buy_rect.y + (buy_rect.h - buy_label.get_height())//2
            )
        )

        # ───── HANDLE CLICK ─────
        if buy_rect.collidepoint(mouse_pos) and mouse_clicked and can_buy:
            galactic_investors_total -= cost_val
            upgrade["purchased"] = True

            upg_type = upgrade.get("type")
            biz_idx  = upgrade.get("biz_index")

            if upg_type == "profit":
                if biz_idx is not None:
                    businesses[biz_idx]["profit_mult"] *= upgrade.get("multiplier", 1.0)

            elif upg_type == "global_profit":
                for b in businesses:
                    b["profit_mult"] *= upgrade.get("multiplier", 1.0)

            elif upg_type == "add_units":
                amount = upgrade.get("amount", 0)
                if biz_idx is not None and amount > 0:
                    businesses[biz_idx]["owned"] += amount

        y_offset += entry_h + spacing

    surface.set_clip(None)

    # ─── Vertical scrollbar ───
    if total_h > visible_h:
        track_x = box_x + box_w - 12
        track_y = list_top
        track_w = 6
        track_h = visible_h
        pygame.draw.rect(
            surface,
            (60, 60, 80),
            (track_x, track_y, track_w, track_h),
            border_radius=3
        )

        thumb_h = max(20, int((visible_h / total_h) * visible_h))
        max_thumb_travel = visible_h - thumb_h
        if max_scroll > 0:
            thumb_y = list_top + int((investor_shop_scroll / max_scroll) * max_thumb_travel)
        else:
            thumb_y = list_top

        thumb_rect = pygame.Rect(track_x, thumb_y, track_w, thumb_h)
        thumb_color = ACCENT if thumb_rect.collidepoint(mouse_pos) else BTN_HOVER
        pygame.draw.rect(surface, thumb_color, thumb_rect, border_radius=3)

        if mouse_clicked and thumb_rect.collidepoint(mouse_pos):
            investor_shop_dragging = True
            investor_shop_drag_offset = mouse_pos[1] - thumb_y

        if 'investor_shop_dragging' in globals() and investor_shop_dragging and pygame.mouse.get_pressed()[0]:
            new_y = mouse_pos[1] - investor_shop_drag_offset
            new_y = max(list_top, min(list_top + max_thumb_travel, new_y))
            investor_shop_scroll = int(((new_y - list_top) / max_thumb_travel) * max_scroll) \
                                  if max_thumb_travel > 0 else 0
        elif not pygame.mouse.get_pressed()[0]:
            investor_shop_dragging = False


def draw_popup(surface):
    global popup_message, popup_end_time
    global first_time_popup, first_time_popup_rect, first_time_popup_close

    now_ms = pygame.time.get_ticks()

    # First-time pop-up (persistent until X clicked)
    if first_time_popup:
        pr = first_time_popup_rect
        pygame.draw.rect(surface, (40, 42, 56, 230), pr, border_radius=8)
        pygame.draw.rect(surface, PANEL_DARK, pr, 2, border_radius=8)

        # Close button in top-right
        cbr = first_time_popup_close
        pygame.draw.rect(surface, BTN_HOVER, cbr, border_radius=4)
        x_surf = font_big.render("X", True, WHITE)
        surface.blit(
            x_surf,
            (cbr.x + (cbr.w - x_surf.get_width()) // 2,
             cbr.y + (cbr.h - x_surf.get_height()) // 2)
        )

        # Centered, larger text
        lines = [
            "Good news, interstellar tycoon!",
            "Your eccentric uncle left you an out-of-this-world fortune!",
            "You saw an ad for an Asteroid Mining service today",
            "for 4 dollars—and opened the envelope to",
            "check the fortune you’ve been given so you",
            "can get started!",
            "",
            "At the bottom of the letter in bold letters,",
            "\"To my nephew I leave you the hefty sum of",
            "  5 dollars—don't spend it all in one place.\"",
            "",
            "I guess we will make the most out of it,",
            "         here goes nothing..."
        ]

        font_center = pygame.font.SysFont(None, 28)
        font_bold   = pygame.font.SysFont(None, 28, bold=True)

        total_text_height = 0
        rendered_lines = []
        for idx, line in enumerate(lines):
            if "5 dollars" in line:
                surf = font_bold.render(line, True, WHITE)
            else:
                surf = font_center.render(line, True, WHITE)
            rendered_lines.append(surf)
            total_text_height += surf.get_height()

        start_y = pr.y + (pr.h - total_text_height) // 2
        for surf in rendered_lines:
            x = pr.x + (pr.w - surf.get_width()) // 2
            surface.blit(surf, (x, start_y))
            start_y += surf.get_height() + 4

    # Standard pop-up (e.g., offline earnings or unlock)
    elif popup_message and now_ms < popup_end_time:
        text = popup_message["text"]
        req  = popup_message["requirement"]
        tw_surf = font_small.render(text, True, WHITE)
        rw_surf = font_small.render(req, True, GRAYED)

        pw = tw_surf.get_width() + 40
        ph = tw_surf.get_height() + rw_surf.get_height() + 30
        px = WIDTH - pw - 20
        py = HEIGHT - ph - 20

        pygame.draw.rect(surface, PANEL_DARK, (px, py, pw, ph), border_radius=8)
        surface.blit(tw_surf, (px + 20, py + 10))
        surface.blit(rw_surf, (px + 20, py + 10 + tw_surf.get_height()))

# -------------------------------------------------------------------------------
# 16. DRAW STATS MENU
# -------------------------------------------------------------------------------
def draw_stats_ui(surface, mouse_pos, mouse_clicked):
    global close_btn_rect, click_count, session_start_time, playtime_this_prestige, total_playtime
    global cycle_start_time, cycle_start_money, space_lifetime_earnings, galactic_investors_total, money

    overlay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay_surf.fill((30, 30, 40, 210))
    surface.blit(overlay_surf, (0, 0))

    box_w = int(WIDTH * 0.6)
    box_h = int(HEIGHT * 0.7)
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2
    pygame.draw.rect(surface, PANEL_DARK, (box_x, box_y, box_w, box_h), border_radius=12)

    title_surf = font_big.render("Stats", True, WHITE)
    surface.blit(
        title_surf,
        (box_x + (box_w - title_surf.get_width()) // 2, box_y + 20)
    )

    close_size = 24
    close_x    = box_x + box_w - close_size - 12
    close_y    = box_y + 12
    close_btn_rect = pygame.Rect(close_x, close_y, close_size, close_size)
    pygame.draw.rect(surface, BTN_HOVER, close_btn_rect, border_radius=4)
    x_surf = font_small.render("X", True, WHITE)
    surface.blit(
        x_surf,
        (close_x + (close_size - x_surf.get_width()) // 2,
         close_y + (close_size - x_surf.get_height()) // 2)
    )

    mant_c, suff_c = format_number_parts(int(money))
    cash_text = f"${mant_c}{suff_c}"

    cycle_cash = max(0, money - cycle_start_money)
    mant_cc, suff_cc = format_number_parts(int(cycle_cash))
    cycle_text = f"${mant_cc}{suff_cc}"

    mant_tca, suff_tca = format_number_parts(int(space_lifetime_earnings))
    total_cash_text = f"${mant_tca}{suff_tca}"

    pts = playtime_this_prestige
    pts_text = format_time(pts)

    elapsed_session = time.time() - session_start_time
    total_playtime = playtime_this_prestige + elapsed_session
    tpt_text = format_time(total_playtime)

    clicks_text = str(click_count)

    boost_pct = galactic_investors_total * 2
    boost_text = f"{boost_pct}%"

    x0 = box_x + 40
    y0 = box_y + 80
    line_gap = 40

    lines = [
        ("Cash:", cash_text),
        ("Cash this investment cycle:", cycle_text),
        ("Total cash earned all time:", total_cash_text),
        ("Playtime this prestige:", pts_text),
        ("Total playtime:", tpt_text),
        ("Total clicks all time:", clicks_text),
        ("Total boost from GIs:", boost_text),
    ]

    for i, (label, value) in enumerate(lines):
        y = y0 + i * line_gap
        label_surf = font_small.render(label, True, WHITE)
        value_surf = font_small.render(value, True, ACCENT)
        surface.blit(label_surf, (x0, y))
        surface.blit(value_surf, (x0 + 300, y))

    return close_btn_rect

# -------------------------------------------------------------------------------
# 17. EVENT LOOP & MAIN LOOP
# -------------------------------------------------------------------------------
running = True
mouse_down = False

while running:
    dt = clock.tick(FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    # Update playtime counters
    elapsed = dt
    playtime_this_prestige += elapsed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Before quitting, save game state
            save_data = {
                "money": money,
                "space_lifetime_earnings": space_lifetime_earnings,
                "global_speed_mult": global_speed_mult,
                "global_profit_mult": global_profit_mult,
                "last_timestamp": time.time(),
                "galactic_investors_total": galactic_investors_total,
                "galactic_investors_spent": galactic_investors_spent,
                "businesses": [], 
                "upgrades": [], 
                "unlocked_shown": list(unlocked_shown),
                "galactic_upgrades": []
            }
            for biz in businesses:
                save_data["businesses"].append({
                    "owned":       biz["owned"],
                    "speed_mult":  biz["speed_mult"],
                    "profit_mult": biz["profit_mult"],
                    "unlocked":    biz["unlocked"],
                    "has_manager": biz["has_manager"],
                    "timer":       biz["timer"],
                    "in_progress": biz["in_progress"],
                    "base_time":   biz["base_time"],
                    "base_payout": biz["base_payout"],
                })
            for upg in upgrades:
                save_data["upgrades"].append({"purchased": upg["purchased"]})
            for gu in galactic_upgrades:
                save_data["galactic_upgrades"].append({"purchased": gu["purchased"]})

            save_data["click_count"] = click_count
            save_data["playtime_this_prestige"] = playtime_this_prestige
            save_data["total_playtime"] = total_playtime

            save_game(save_data)
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            PANEL_WIDTH    = WIDTH - PANEL_X - 20
            PANEL_HEIGHT   = HEIGHT - PANEL_Y - 20

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            # ── FIX: Only treat left‐click (button=1) as a "click" ──
            if event.button == 1:
                mouse_clicked = True
                click_count += 1

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

        elif event.type == pygame.MOUSEWHEEL:
            # Scroll for manager, upgrades, unlocks, AND Investor Shop
            if overlay_mode == "Managers":
                manager_scroll -= event.y * 30
            elif overlay_mode == "Upgrades":
                upgrade_scroll -= event.y * 30
            elif overlay_mode == "Unlocks":
                unlock_scroll -= event.y * 30
            elif overlay_mode == "Investors" and show_investor_shop:
                investor_shop_scroll -= event.y * 30

    screen.fill(BG_DARK)

    # 0) HANDLE FIRST-TIME POPUP CLICK BLOCKING
    # If the first_time_popup is still open, we only let its "X" consume the click.
    # Otherwise, mouse clicks flow to the rest of the UI.
    if first_time_popup:
        bc = False
        sbc = False
    else:
        sbc = mouse_clicked
        bc  = mouse_clicked if overlay_mode is None else False

    # 1) UPDATE EACH BUSINESS (timers, payouts)
    for biz in businesses:
        if biz["in_progress"]:
            biz["timer"] -= dt * biz["speed_mult"] * global_speed_mult
            if biz["timer"] <= 0:
                biz["timer"] = 0.0
                biz["in_progress"] = False
                profit_mult = (1.0 + (0.02 * galactic_investors_total)) * global_profit_mult * biz["profit_mult"]
                payout_val = int(biz["base_payout"] * biz["owned"] * profit_mult)
                money += payout_val
                space_lifetime_earnings += payout_val

                if biz["has_manager"]:
                    biz["in_progress"] = True
                    effective_time = (biz["base_time"] / biz["speed_mult"]) / global_speed_mult
                    biz["timer"] = effective_time

    # 2) CHECK UNLOCKS
    for idx, u in enumerate(unlocks):
        if idx in unlocked_shown:
            continue
        if u["biz_index"] is not None:
            b = businesses[u["biz_index"]]
            if b["owned"] >= u["threshold"]:
                apply_single_unlock(idx)
        else:
            if all(bz["owned"] >= u["threshold"] for bz in businesses):
                apply_single_unlock(idx)

    # 3) UPDATE POPUP TIMER
    if popup_message and pygame.time.get_ticks() > popup_end_time:
        popup_message = None

    # 4) DRAW MAIN UI
    draw_header(screen, money, mouse_pos, sbc)

    unlock_result, buy_result = draw_business_panel(screen, dt, mouse_pos, bc)

    # Handle unlock & buy only when no overlay & no first-time popup
    if overlay_mode is None and not first_time_popup:
        # UNLOCK-BIZ click
        if unlock_result is not None:
            biz = businesses[unlock_result]
            # Already handled in draw_business_panel, so no extra action here

        # BUY-BIZ click (only apply once, here)
        if buy_result is not None:
            biz = businesses[buy_result]
            count = purchase_options[purchase_index]
            if count == -1:
                count = max_affordable(biz, money)
            total_cost = total_cost_for_next_N(biz, count)
            if money >= total_cost:
                money -= total_cost
                biz["owned"] += count

    # 5) DRAW SIDEBAR (only if no first-time pop-up)
    if not first_time_popup:
        sidebar_click = draw_sidebar(screen, mouse_pos, sbc)
        if sidebar_click == 0 and sbc:
            overlay_mode = "Managers"
        elif sidebar_click == 1 and sbc:
            overlay_mode = "Upgrades"
        elif sidebar_click == 2 and sbc:
            overlay_mode = "Unlocks"
        elif sidebar_click == 3 and sbc:
            overlay_mode = "Investors"
        elif sidebar_click == 4 and sbc:
            overlay_mode = "Stats"

    # 6) DRAW OVERLAY MENUS
    if not first_time_popup:
        if overlay_mode == "Managers":
            close_rect = draw_managers_ui(screen, mouse_pos, mouse_clicked)
            if close_rect and mouse_clicked and close_rect.collidepoint(mouse_pos):
                overlay_mode = None

        elif overlay_mode == "Upgrades":
            close_rect = draw_upgrades_ui(screen, mouse_pos, mouse_clicked)
            if close_rect and mouse_clicked and close_rect.collidepoint(mouse_pos):
                overlay_mode = None

        elif overlay_mode == "Unlocks":
            close_rect = draw_unlocks_ui(screen, mouse_pos, mouse_clicked)
            if close_rect and mouse_clicked and close_rect.collidepoint(mouse_pos):
                overlay_mode = None

        elif overlay_mode == "Investors":
            close_rect = draw_investors_ui(screen, mouse_pos, mouse_clicked)
            if close_rect and mouse_clicked and close_rect.collidepoint(mouse_pos):
                overlay_mode = None

        elif overlay_mode == "Stats":
            close_rect = draw_stats_ui(screen, mouse_pos, mouse_clicked)
            if close_rect and mouse_clicked and close_rect.collidepoint(mouse_pos):
                overlay_mode = None

    # 7) HANDLE CLICK ON FIRST-TIME POPUP CLOSE BUTTON
    if first_time_popup and mouse_clicked:
        if first_time_popup_close.collidepoint(mouse_pos):
            first_time_popup = False

    # 8) DRAW POPUP (first-time, offline earnings, or unlock)
    draw_popup(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
