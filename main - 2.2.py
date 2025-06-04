import pygame
import sys
import os
import json
import math
import time

pygame.init()

# -------------------------------------------------------------------------------
# 1. RESOURCE PATH HELPER
# -------------------------------------------------------------------------------
def resource_path(relative_path):
    """
    Return absolute path to resource, works for development and for PyInstaller EXE.
    """
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)

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
    Split a number into a mantissa and suffix (e.g., 1,234,000 → ("1.234", "M")).
    """
    units = ["", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No"]
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

    total_offline_earned = 0
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

        # How many full cycles could have run
        cycles = math.floor(offline_seconds / effective_time)

        one_cycle_value = biz_saved["base_payout"] * owned * biz_saved["profit_mult"] * global_profit_mult * (1.0 + 0.02 * galactic_investors_total)

        if cycles > 0:
            # Pay for all full cycles
            earned = one_cycle_value * cycles
            total_offline_earned += earned

            # Calculate remainder time after those cycles
            remainder = offline_seconds - (cycles * effective_time)

            if biz_saved.get("has_manager", False):
                # Keep it in progress with leftover time
                if remainder >= effective_time:
                    # Could complete one more cycle if remainder large (rare)
                    total_offline_earned += one_cycle_value
                    biz_saved["in_progress"] = True
                    biz_saved["timer"] = effective_time - (remainder - effective_time)
                else:
                    biz_saved["in_progress"] = True
                    biz_saved["timer"] = effective_time - remainder
            else:
                # Without manager, it just finishes and idles
                if remainder >= effective_time:
                    total_offline_earned += one_cycle_value
                    biz_saved["in_progress"] = False
                    biz_saved["timer"] = 0.0
                else:
                    biz_saved["in_progress"] = True
                    biz_saved["timer"] = effective_time - remainder

            continue  # Done handling cycles

        # If no full cycles fit, but there may have been a partial cycle
        saved_timer = biz_saved.get("timer", 0.0)
        if saved_timer > 0:
            new_timer = saved_timer - offline_seconds
            if new_timer <= 0:
                # It finished exactly one cycle while offline
                total_offline_earned += one_cycle_value
                biz_saved["in_progress"] = False
                biz_saved["timer"] = 0.0
            else:
                biz_saved["in_progress"] = True
                biz_saved["timer"] = new_timer

    # Add offline earnings into the saved state
    data_loaded["money"] += total_offline_earned
    data_loaded["space_lifetime_earnings"] += total_offline_earned
    data_loaded["last_timestamp"] = now_ts

    return total_offline_earned

# -------------------------------------------------------------------------------
# 5. DEFAULT GAME STATE
# -------------------------------------------------------------------------------
def default_game_state():
    """
    Returns a fresh initial game state dictionary with all needed fields.
    """
    return {
        "money": 5000000.0,
        "space_lifetime_earnings": 0.0,
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
# 6. PYGAME SETUP & CUSTOM WINDOW ICON
# -------------------------------------------------------------------------------
WIDTH, HEIGHT = 1200, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("SpaceRace")

# Load and set window icon using starlightfarm.png, scaled to 96×96
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

font_big   = pygame.font.SysFont(None, 44)
font_med   = pygame.font.SysFont(None, 32)
font_small = pygame.font.SysFont(None, 20)

business_scroll      = 0
manager_scroll       = 0
upgrade_scroll       = 0
unlock_scroll        = 0
investor_shop_scroll = 0

# -------------------------------------------------------------------------------
# NEW GLOBAL DRAGGING STATE VARIABLES
# -------------------------------------------------------------------------------
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

overlay_mode        = None
last_overlay_mode   = None
show_investor_shop  = False

purchase_options = [1, 5, 10, -1]
purchase_index   = 0

popup_message          = None
popup_end_time         = 0
first_time_popup       = False
first_time_popup_rect  = None
first_time_popup_close = None

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
]

# -------------------------------------------------------------------------------
# 9. UNLOCKS (per-business + global)
# -------------------------------------------------------------------------------
unlocks = [
    # -------------------
    # Asteroid Miner (biz_index 0)
    # -------------------
    { "biz_index": 0, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2", "asset_path": None },
    { "biz_index": 0, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2", "asset_path": None },
    { "biz_index": 0, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2", "asset_path": None },
    { "biz_index": 0, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2", "asset_path": None },
    { "biz_index": 0, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2", "asset_path": None },
    { "biz_index": 0, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Asteroid Miner speed ×2", "asset_path": None },
    { "biz_index": 0, "threshold": 500,  "type": "profit", "multiplier": 4.0,
      "description": "Asteroid Miner profit ×4", "asset_path": None },

    # -------------------
    # Satellite Network (biz_index 1)
    # -------------------
    { "biz_index": 1, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2", "asset_path": None },
    { "biz_index": 1, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2", "asset_path": None },
    { "biz_index": 1, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2", "asset_path": None },
    { "biz_index": 1, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2", "asset_path": None },
    { "biz_index": 1, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2", "asset_path": None },
    { "biz_index": 1, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Satellite Network speed ×2", "asset_path": None },
    { "biz_index": 1, "threshold": 500,  "type": "profit", "multiplier": 2.0,
      "description": "Satellite Network profit ×2", "asset_path": None },

    # -------------------
    # Rocket Yard (biz_index 2)
    # -------------------
    { "biz_index": 2, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2", "asset_path": None },
    { "biz_index": 2, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Rocket Yard speed ×2", "asset_path": None },
    { "biz_index": 2, "threshold": 500,  "type": "profit", "multiplier": 2.0,
      "description": "Rocket Yard profit ×2", "asset_path": None },

    # -------------------
    # Lunar Colony (biz_index 3)
    # -------------------
    { "biz_index": 3, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2", "asset_path": None },
    { "biz_index": 3, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Lunar Colony speed ×2", "asset_path": None },
    { "biz_index": 3, "threshold": 500,  "type": "profit", "multiplier": 2.0,
      "description": "Lunar Colony profit ×2", "asset_path": None },

    # -------------------
    # Starlight Farm (biz_index 4)
    # -------------------
    { "biz_index": 4, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2", "asset_path": None },
    { "biz_index": 4, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Starlight Farm speed ×2", "asset_path": None },
    { "biz_index": 4, "threshold": 500,  "type": "profit", "multiplier": 2.0,
      "description": "Starlight Farm profit ×2", "asset_path": None },

    # -------------------
    # Alien Outpost (biz_index 5)
    # -------------------
    { "biz_index": 5, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2", "asset_path": None },
    { "biz_index": 5, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Alien Outpost speed ×2", "asset_path": None },
    { "biz_index": 5, "threshold": 500,  "type": "profit", "multiplier": 2.0,
      "description": "Alien Outpost profit ×2", "asset_path": None },

    # -------------------
    # Solar Array (biz_index 6)
    # -------------------
    { "biz_index": 6, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2", "asset_path": None },
    { "biz_index": 6, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Solar Array speed ×2", "asset_path": None },
    { "biz_index": 6, "threshold": 500,  "type": "profit", "multiplier": 2.0,
      "description": "Solar Array profit ×2", "asset_path": None },

    # -------------------
    # Black Hole Labs (biz_index 7)
    # -------------------
    { "biz_index": 7, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2", "asset_path": None },
    { "biz_index": 7, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Black Hole Labs speed ×2", "asset_path": None },
    { "biz_index": 7, "threshold": 500,  "type": "profit", "multiplier": 2.0,
      "description": "Black Hole Labs profit ×2", "asset_path": None },

    # -------------------
    # Wormhole Gate (biz_index 8)
    # -------------------
    { "biz_index": 8, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2", "asset_path": None },
    { "biz_index": 8, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Wormhole Gate speed ×2", "asset_path": None },
    { "biz_index": 8, "threshold": 500,  "type": "profit", "multiplier": 2.0,
      "description": "Wormhole Gate profit ×2", "asset_path": None },

    # -------------------
    # Galactic Senate (biz_index 9)
    # -------------------
    { "biz_index": 9, "threshold":  25,  "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2", "asset_path": None },
    { "biz_index": 9, "threshold":  50,  "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2", "asset_path": None },
    { "biz_index": 9, "threshold": 100,  "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2", "asset_path": None },
    { "biz_index": 9, "threshold": 200,  "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2", "asset_path": None },
    { "biz_index": 9, "threshold": 300,  "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2", "asset_path": None },
    { "biz_index": 9, "threshold": 400,  "type": "speed",  "multiplier": 2.0,
      "description": "Galactic Senate speed ×2", "asset_path": None },
    { "biz_index": 9, "threshold": 500,  "type": "profit", "multiplier": 2.0,
      "description": "Galactic Senate profit ×2", "asset_path": None },

    # -------------------
    # Global (Capitalist) unlocks – biz_index=None
    # -------------------
    { "biz_index": None, "threshold":  25,   "type": "global_speed",  "multiplier": 2.0,
      "description": "All businesses speed ×2",  "asset_path": "assets/global.png" },
    { "biz_index": None, "threshold":  50,   "type": "global_speed",  "multiplier": 2.0,
      "description": "All businesses speed ×2",  "asset_path": "assets/global.png" },
    { "biz_index": None, "threshold": 100,   "type": "global_speed",  "multiplier": 2.0,
      "description": "All businesses speed ×2",  "asset_path": "assets/global.png" },
    { "biz_index": None, "threshold": 200,   "type": "global_speed",  "multiplier": 2.0,
      "description": "All businesses speed ×2",  "asset_path": "assets/global.png" },
    { "biz_index": None, "threshold": 300,   "type": "global_speed",  "multiplier": 2.0,
      "description": "All businesses speed ×2",  "asset_path": "assets/global.png" },
    { "biz_index": None, "threshold": 400,   "type": "global_speed",  "multiplier": 2.0,
      "description": "All businesses speed ×2",  "asset_path": "assets/global.png" },
    { "biz_index": None, "threshold": 500,   "type": "global_profit", "multiplier": 2.0,
      "description": "All businesses profit ×2", "asset_path": "assets/global.png" },
]

# -------------------------------------------------------------------------------
# 10. GALACTIC UPGRADES (Angel-style)
# -------------------------------------------------------------------------------
galactic_upgrades = [
    {
        "name":        "Heavenly Harvest",
        "description": "All business profits ×2",
        "icon":        "✨",
        "cost":        5,
        "purchased":   False
    },
    {
        "name":        "Divine Acceleration",
        "description": "All business speeds ×2",
        "icon":        "🚀",
        "cost":        10,
        "purchased":   False
    },
    {
        "name":        "Cosmic Fortune",
        "description": "All profits ×3",
        "icon":        "🪐",
        "cost":        20,
        "purchased":   False
    },
    {
        "name":        "Temporal Warp",
        "description": "All speeds ×3",
        "icon":        "🕳️",
        "cost":        50,
        "purchased":   False
    },
    {
        "name":        "Astral Dividend",
        "description": "Earn +0.5% GI per second",
        "icon":        "💰",
        "cost":        100,
        "purchased":   False
    },
    {
        "name":        "Galactic Beacon",
        "description": "Unlock all businesses automatically",
        "icon":        "🛰️",
        "cost":        200,
        "purchased":   False
    },
]

# -------------------------------------------------------------------------------
# 11. LOAD ALL BUSINESS IMAGES & GLOBAL ICON (scale to 96×96)
# -------------------------------------------------------------------------------
def load_all_business_images():
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

    # Also load the global unlock icon (global.png)
    global_abs = resource_path("assets/global.png")
    if os.path.isfile(global_abs):
        try:
            gimg = pygame.image.load(global_abs).convert_alpha()
            gimg = pygame.transform.smoothscale(gimg, (96, 96))
            for u in unlocks:
                if u["biz_index"] is None:
                    u["image"] = gimg
        except Exception:
            for u in unlocks:
                if u["biz_index"] is None:
                    u["image"] = None
    else:
        for u in unlocks:
            if u["biz_index"] is None:
                u["image"] = None

# Call once at startup so that every biz["image"] and each global-unlock’s "image" is set.
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

    # Prepare a persistent first-time pop-up (no auto-dismiss)
    first_time_popup = True
    # Match manager-window dimensions (60%×70% of the screen)
    pw = int(WIDTH * 0.6)
    ph = int(HEIGHT * 0.7)
    px = (WIDTH - pw) // 2
    py = (HEIGHT - ph) // 2
    first_time_popup_rect = pygame.Rect(px, py, pw, ph)
    # Close button in top-right of the popup
    cb_size = 32
    cb_x = px + pw - cb_size - 12
    cb_y = py + 12
    first_time_popup_close = pygame.Rect(cb_x, cb_y, cb_size, cb_size)

else:
    game_state = loaded

    # Restore all per-business fields (use get defaults for old saves)
    for idx, biz_saved in enumerate(game_state["businesses"]):
        biz = businesses[idx]
        biz["owned"]       = biz_saved.get("owned", 0)
        biz["speed_mult"]  = biz_saved.get("speed_mult", 1.0)
        biz["profit_mult"] = biz_saved.get("profit_mult", 1.0)
        biz["unlocked"]    = biz_saved.get("unlocked", False)
        biz["has_manager"] = biz_saved.get("has_manager", False)
        biz["timer"]       = biz_saved.get("timer", 0.0)
        biz["in_progress"] = biz_saved.get("in_progress", False)

    # Restore all cash-upgrades
    for i, upg_saved in enumerate(game_state["upgrades"]):
        upgrades[i]["purchased"] = upg_saved.get("purchased", False)

    unlocked_shown = set(game_state.get("unlocked_shown", []))

    # Restore all Angel-style (galactic) upgrades
    for i, gu_saved in enumerate(game_state.get("galactic_upgrades", [])):
        galactic_upgrades[i]["purchased"] = gu_saved.get("purchased", False)

    # Restore core numeric values
    money                       = game_state.get("money", 5000000.0)
    space_lifetime_earnings     = game_state.get("space_lifetime_earnings", 0.0)
    global_speed_mult           = game_state.get("global_speed_mult", 1.0)
    global_profit_mult          = game_state.get("global_profit_mult", 1.0)
    galactic_investors_total    = game_state.get("galactic_investors_total", 0)
    galactic_investors_spent    = game_state.get("galactic_investors_spent", 0)

    # Calculate offline earnings, adjusting saved timers accordingly
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

    # Reload images so biz["image"] and global unlock images are present
    load_all_business_images()

# -------------------------------------------------------------------------------
# 13. RESTORE STATE FOR FIRST-TIME LOAD
# -------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------
# 14. UI DRAW FUNCTIONS
# -------------------------------------------------------------------------------
def draw_sidebar(surface, mouse_pos, mouse_clicked):
    pygame.draw.rect(surface, SIDEBAR_BG, (0, 0, SIDEBAR_WIDTH, HEIGHT))
    title_surf = font_big.render("SpaceRace", True, WHITE)
    surface.blit(title_surf, ((SIDEBAR_WIDTH // 2) - (title_surf.get_width() // 2), 20))
    btn_h = 50
    spacing = 20
    y_start = 100
    for i, label_text in enumerate(["Managers", "Upgrades", "Unlocks", "Investors"]):
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
        if hovered and mouse_clicked:
            return i
    return None

def draw_header(surface, money, mouse_pos, mouse_clicked):
    global purchase_index
    pygame.draw.rect(surface, PANEL_DARK, (SIDEBAR_WIDTH, 0, WIDTH - SIDEBAR_WIDTH, HEADER_HEIGHT))

    mant, suff = format_number_parts(money)
    money_label = font_big.render(f"${mant}{suff}", True, WHITE)
    surface.blit(money_label, (SIDEBAR_WIDTH + 20, (HEADER_HEIGHT - money_label.get_height()) // 2))

    labels = ["x1", "x5", "x10", "MAX"]
    total_w = 0
    btn_h   = 32
    gap     = 10
    btn_rects = []

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
    global business_scroll, money, global_speed_mult, space_lifetime_earnings, global_profit_mult

    stripe_threshold = 0.2

    pygame.draw.rect(surface, BG_DARK, (PANEL_X - 10, PANEL_Y - 10, PANEL_WIDTH + 20, PANEL_HEIGHT + 20))

    n_total      = len(businesses)
    n_per_column = math.ceil(n_total / 2)
    content_height = n_per_column * (ROW_HEIGHT + ROW_GAP) - ROW_GAP
    max_scroll = max(0, content_height - PANEL_HEIGHT)
    business_scroll = max(0, min(business_scroll, max_scroll))

    for idx, biz in enumerate(businesses):
        col = 0 if idx < n_per_column else 1
        row = idx if col == 0 else idx - n_per_column

        x = PANEL_X + col * ((PANEL_WIDTH // 2) + ROW_GAP)
        y = PANEL_Y + row * (ROW_HEIGHT + ROW_GAP) - business_scroll
        biz_rect = pygame.Rect(x, y, (PANEL_WIDTH // 2) - ROW_GAP, ROW_HEIGHT)

        unlocked = biz["unlocked"]
        bg_col   = BUSINESS_BG if unlocked else BUSINESS_BG_LOCKED

        # Only draw if visible within panel bounds
        if y + ROW_HEIGHT < PANEL_Y or y > PANEL_Y + PANEL_HEIGHT:
            continue

        pygame.draw.rect(surface, bg_col, biz_rect, border_radius=18)

        # ICON: draw scaled 96×96 image if available; else fallback to emoji
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
            icon_surf = font_big.render(biz["icon"], True, WHITE if unlocked else GRAYED)
            surface.blit(icon_surf, (x + 16, y + 16))

        txt_col    = WHITE if unlocked else GRAYED
        name_surf  = font_med.render(biz["name"], True, txt_col)
        surface.blit(name_surf, (x + 100, y + 18))

        profit_mult = (1.0 + (0.02 * galactic_investors_total)) * global_profit_mult * biz["profit_mult"]
        earn_val = int(biz["base_payout"] * biz["owned"] * profit_mult)
        earn_mant, earn_suff = format_number_parts(earn_val)
        earning_text = f"+${earn_mant}{earn_suff}"
        owned_text   = f"x{biz['owned']}"

        second_y = y + 52
        owned_surf   = font_small.render(owned_text, True, txt_col)
        earn_surf    = font_small.render(earning_text, True, ACCENT if unlocked else GRAYED)
        surface.blit(owned_surf, (x + 100, second_y))
        surface.blit(earn_surf, (x + 100 + owned_surf.get_width() + 20, second_y))

        opt = purchase_options[purchase_index]
        if opt == -1:
            count = max_affordable(biz, money)
        else:
            count = opt
        if count < 0:
            count = 0

        total_cost = total_cost_for_next_N(biz, count)

        btn_w = 140
        btn_h = 50
        btn_x = x + biz_rect.w - btn_w - 10
        btn_y = y + 80 - btn_h - 10
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        mant, suff = format_number_parts(total_cost)
        can_buy = money >= total_cost and count > 0
        hovered_btn = btn_rect.collidepoint(mouse_pos)

        if can_buy:
            base_color = ACCENT
        else:
            base_color = PANEL_DARK
        btn_color = BTN_HOVER if (hovered_btn and can_buy) else base_color

        pygame.draw.rect(surface, btn_color, btn_rect, border_radius=10)

        line1_y = btn_y + 6
        line2_y = btn_y + btn_h // 2 + 2

        left1 = font_small.render("Buy", True, WHITE)
        left2 = font_small.render(f"x{count}", True, WHITE)
        right1 = font_small.render(f"{mant}", True, WHITE)
        right2 = font_small.render(f"{suff}", True, WHITE)

        surface.blit(left1, (btn_x + 8, line1_y))
        surface.blit(right1, (btn_x + btn_w - right1.get_width() - 8, line1_y))
        surface.blit(left2, (btn_x + 8, line2_y))
        surface.blit(right2, (btn_x + btn_w - right2.get_width() - 8, line2_y))

        if hovered_btn and mouse_clicked and can_buy and unlocked:
            money -= total_cost
            biz["owned"] += count

        if not unlocked:
            overlay_surf = pygame.Surface((biz_rect.w, biz_rect.h), pygame.SRCALPHA)
            overlay_surf.fill((40, 42, 56, 180))
            surface.blit(overlay_surf, (x, y))

            lock_mant, lock_suff = format_number_parts(biz["base_cost"])
            lock_label = font_small.render(f"Cost: ${lock_mant}{lock_suff}", True, WHITE)
            surface.blit(
                lock_label,
                (x + (biz_rect.w - lock_label.get_width()) // 2,
                 y + (biz_rect.h // 2) - 10)
            )

            if biz_rect.collidepoint(mouse_pos) and mouse_clicked and money >= biz["base_cost"]:
                money -= biz["base_cost"]
                biz["owned"] = 1
                biz["unlocked"] = True
                biz["in_progress"] = False
                biz["timer"] = 0.0
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

        # ----------------------
        # DRAW TIMER (if active) WITH SMALL OPAQUE BOX
        # ----------------------
        if biz["in_progress"]:
            time_text = format_time(biz["timer"])
            timer_surf = font_small.render(time_text, True, WHITE)
            # Calculate position: left of progress bar, just under the buy button
            bar_x = x + 100
            btn_h_local = btn_h
            timer_x = bar_x - timer_surf.get_width() - 10
            timer_y = btn_y + btn_h_local + 5

            # Draw small opaque background box
            bg_w = timer_surf.get_width() + 8
            bg_h = timer_surf.get_height() + 4
            bg_surf = pygame.Surface((bg_w, bg_h), pygame.SRCALPHA)
            # Adjust this RGBA for desired opacity
            bg_surf.fill((40, 44, 55, 200))
            surface.blit(bg_surf, (timer_x - 4, timer_y - 2))
            # Draw the timer text on top
            surface.blit(timer_surf, (timer_x, timer_y))

        # DRAW PROGRESS BAR
        bar_x = x + 100
        bar_y = y + 80
        bar_w = biz_rect.w - 170
        bar_h = 18
        pygame.draw.rect(surface, PROGRESS_BG, (bar_x, bar_y, bar_w, bar_h), border_radius=7)

        if biz["in_progress"]:
            effective_time = (biz["base_time"] / biz["speed_mult"]) / global_speed_mult
            biz["timer"] -= dt
            if biz["timer"] <= 0:
                biz["timer"] = 0.0
                biz["in_progress"] = False
                profit_mult = (1.0 + (0.02 * galactic_investors_total)) * global_profit_mult * biz["profit_mult"]
                payout_val = int(biz["base_payout"] * biz["owned"] * profit_mult)
                money += payout_val
                space_lifetime_earnings += payout_val

                if biz["has_manager"]:
                    biz["in_progress"] = True
                    biz["timer"] = effective_time

            if effective_time <= stripe_threshold:
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
                pct = max(0.0, min(1.0, 1.0 - (biz["timer"] / effective_time)))
                fill_w = int(bar_w * pct)
                pygame.draw.rect(surface, PROGRESS_FILL, (bar_x, bar_y, fill_w, bar_h), border_radius=7)

    return None

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

    header_icon   = font_med.render("Icon", True, WHITE)
    header_build  = font_med.render("Building", True, WHITE)
    header_effect = font_med.render("Effect", True, WHITE)
    header_cost   = font_med.render("Cost", True, WHITE)
    #surface.blit(header_icon,   (col1_x, header_y))
    surface.blit(header_build,  (col2_x, header_y))
    surface.blit(header_effect, (col3_x, header_y))
    surface.blit(header_cost,   (col4_x, header_y))

    mgr_list_y0 = header_y + 40
    scroll_top    = mgr_list_y0
    scroll_bottom = box_y + box_h - 20
    visible_h     = scroll_bottom - scroll_top
    clip_rect = pygame.Rect(box_x + 10, scroll_top, box_w - 20, visible_h)
    surface.set_clip(clip_rect)

    mgr_entry_h  = 60
    spacing      = 10
    unpurchased_count = sum(1 for b in businesses if not b["has_manager"])
    total_content_h = unpurchased_count * (mgr_entry_h + spacing)
    max_mgr_scroll  = max(0, total_content_h - visible_h)
    manager_scroll  = max(0, min(manager_scroll, max_mgr_scroll))

    y_offset = mgr_list_y0 - manager_scroll

    for biz in businesses:
        if biz["has_manager"]:
            continue

        if y_offset + mgr_entry_h < scroll_top or y_offset > scroll_bottom:
            y_offset += mgr_entry_h + spacing
            continue

        entry_rect = pygame.Rect(box_x + 10, y_offset, box_w - 20, mgr_entry_h)
        pygame.draw.rect(surface, (50, 50, 70), entry_rect, border_radius=8)

        if biz.get("image"):
            icon_surf = pygame.transform.smoothscale(biz["image"], (40, 40))
            surface.blit(icon_surf, (col1_x, y_offset + 10))
        else:
            icosurf = font_big.render(biz["icon"], True, WHITE)
            surface.blit(icosurf, (col1_x, y_offset + 10))

        name_surf = font_med.render(biz["name"], True, YELLOW)
        surface.blit(name_surf, (col2_x, y_offset + 6))

        effect_text = "Automatically restarts production when idle"
        effect_surf = font_small.render(effect_text, True, GRAYED)
        surface.blit(effect_surf, (col2_x, y_offset + 30))

        cost_val = biz["manager_cost"]
        cost_mant, cost_suff = format_number_parts(cost_val)
        can_hire  = money >= cost_val
        hire_rect = pygame.Rect(col4_x, y_offset + 15, 100, 30)
        if can_hire:
            base_color = ACCENT
        else:
            base_color = PANEL_DARK
        hire_color = BTN_HOVER if (hire_rect.collidepoint(mouse_pos) and can_hire) else base_color
        pygame.draw.rect(surface, hire_color, hire_rect, border_radius=6)
        hire_txt = font_small.render(f"Hire ${cost_mant}{cost_suff}", True, WHITE)
        surface.blit(hire_txt, (hire_rect.x + (hire_rect.w - hire_txt.get_width()) // 2, hire_rect.y + 6))

        if hire_rect.collidepoint(mouse_pos) and mouse_clicked and can_hire:
            money                 -= cost_val
            biz["has_manager"]     = True
            if not biz["in_progress"] and biz["owned"] > 0:
                biz["in_progress"] = True
                effective_time = (biz["base_time"] / biz["speed_mult"]) / global_speed_mult
                biz["timer"]     = effective_time

        y_offset += mgr_entry_h + spacing

    surface.set_clip(None)

    # ------------------------
    # DRAW VERTICAL SCROLLBAR
    # ------------------------
    if total_content_h > visible_h:
        track_x = box_x + box_w - 12
        track_y = scroll_top
        track_w = 6
        track_h = visible_h
        pygame.draw.rect(surface, (60, 60, 80), (track_x, track_y, track_w, track_h), border_radius=3)

        # Thumb height based on ratio
        thumb_h = max(20, int((visible_h / total_content_h) * visible_h))
        max_thumb_travel = visible_h - thumb_h
        if max_mgr_scroll > 0:
            thumb_y = scroll_top + int((manager_scroll / max_mgr_scroll) * max_thumb_travel)
        else:
            thumb_y = scroll_top

        thumb_rect = pygame.Rect(track_x, thumb_y, track_w, thumb_h)
        thumb_color = ACCENT if thumb_rect.collidepoint(mouse_pos) else BTN_HOVER
        pygame.draw.rect(surface, thumb_color, thumb_rect, border_radius=3)

        # HANDLE DRAGGING
        global manager_dragging, manager_drag_offset
        if mouse_clicked and thumb_rect.collidepoint(mouse_pos):
            manager_dragging = True
            manager_drag_offset = mouse_pos[1] - thumb_y

        if manager_dragging and pygame.mouse.get_pressed()[0]:
            new_y = mouse_pos[1] - manager_drag_offset
            new_y = max(scroll_top, min(scroll_top + max_thumb_travel, new_y))
            manager_scroll = int(((new_y - scroll_top) / max_thumb_travel) * max_mgr_scroll) if max_thumb_travel > 0 else 0

    return close_btn_rect

def draw_upgrades_ui(surface, mouse_pos, mouse_clicked):
    global close_btn_rect, money, upgrade_scroll, upgrade_dragging, upgrade_drag_offset

    overlay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay_surf.fill((30, 30, 40, 210))
    surface.blit(overlay_surf, (0, 0))

    box_w = int(WIDTH * 0.6)
    box_h = int(HEIGHT * 0.7)
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2
    pygame.draw.rect(surface, PANEL_DARK, (box_x, box_y, box_w, box_h), border_radius=12)

    title_surf = font_big.render("Purchase Upgrades", True, WHITE)
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
    col1_x = box_x + 20
    col2_x = box_x + 60
    col3_x = box_x + box_w - 140

    icon_header = font_med.render("Icon", True, WHITE)
    name_header = font_med.render("Upgrade", True, WHITE)
    cost_header = font_med.render("Cost", True, WHITE)
    #surface.blit(icon_header, (col1_x, header_y))
    surface.blit(name_header, (col2_x, header_y))
    surface.blit(cost_header, (col3_x, header_y))

    scroll_top    = header_y + 40
    scroll_bottom = box_y + box_h - 20
    visible_h     = scroll_bottom - scroll_top

    entry_h = 60
    spacing = 10

    total_content_h = len([u for u in upgrades if not u["purchased"]]) * (entry_h + spacing)
    max_scroll  = max(0, total_content_h - visible_h)
    upgrade_scroll = max(0, min(upgrade_scroll, max_scroll))

    clip_rect = pygame.Rect(box_x + 10, scroll_top, box_w - 20, visible_h)
    surface.set_clip(clip_rect)

    y_offset = scroll_top - upgrade_scroll

    for upg in upgrades:
        if upg["purchased"]:
            continue

        if y_offset + entry_h < scroll_top or y_offset > scroll_bottom:
            y_offset += entry_h + spacing
            continue

        entry_rect = pygame.Rect(box_x + 10, y_offset, box_w - 20, entry_h)
        pygame.draw.rect(surface, (50, 50, 70), entry_rect, border_radius=8)

        biz = businesses[upg["biz_index"]]
        if biz.get("image"):
            small_img = pygame.transform.smoothscale(biz["image"], (40, 40))
            surface.blit(small_img, (col1_x, y_offset + 10))
        else:
            icon_surf = font_big.render(biz["icon"], True, WHITE)
            surface.blit(icon_surf, (col1_x, y_offset + 10))

        name_surf = font_med.render(upg["name"], True, YELLOW)
        surface.blit(name_surf, (col2_x, y_offset + 8))

        biz_name = businesses[upg["biz_index"]]["name"]
        desc_text = f"{biz_name} profit ×{upg['multiplier']}"
        desc_surf = font_small.render(desc_text, True, GRAYED)
        surface.blit(desc_surf, (col2_x, y_offset + 30))

        cost_mant, cost_suff = format_number_parts(upg["cost"])
        cost_surf = font_small.render(f"${cost_mant}{cost_suff}", True, ACCENT)
        surface.blit(cost_surf, (col2_x, y_offset + 45))

        can_buy = (money >= upg["cost"])
        buy_rect = pygame.Rect(col3_x, y_offset + 15, 100, 30)
        if can_buy:
            base_color = ACCENT
        else:
            base_color = PANEL_DARK
        if buy_rect.collidepoint(mouse_pos) and can_buy:
            buy_color = BTN_HOVER
        else:
            buy_color = base_color
        pygame.draw.rect(surface, buy_color, buy_rect, border_radius=6)
        buy_txt = font_small.render("Buy!", True, WHITE)
        surface.blit(
            buy_txt,
            (buy_rect.x + (buy_rect.w - buy_txt.get_width()) // 2,
             buy_rect.y + (buy_rect.h - buy_txt.get_height()) // 2)
        )

        if buy_rect.collidepoint(mouse_pos) and mouse_clicked and can_buy:
            money -= upg["cost"]
            biz_ref = businesses[upg["biz_index"]]
            biz_ref["profit_mult"] *= upg["multiplier"]
            upg["purchased"] = True

            # Shift the remaining list up by one entry-height
            unpurchased_count = sum(1 for u2 in upgrades if not u2["purchased"])
            new_total_h       = unpurchased_count * (entry_h + spacing)
            new_max_scroll    = max(0, new_total_h - visible_h)
            upgrade_scroll    = min(upgrade_scroll + (entry_h + spacing), new_max_scroll)

        y_offset += entry_h + spacing

    surface.set_clip(None)

    # ------------------------
    # DRAW VERTICAL SCROLLBAR
    # ------------------------
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

        # HANDLE DRAGGING
        global upgrade_dragging, upgrade_drag_offset
        if mouse_clicked and thumb_rect.collidepoint(mouse_pos):
            upgrade_dragging = True
            upgrade_drag_offset = mouse_pos[1] - thumb_y

        if upgrade_dragging and pygame.mouse.get_pressed()[0]:
            new_y = mouse_pos[1] - upgrade_drag_offset
            new_y = max(scroll_top, min(scroll_top + max_thumb_travel, new_y))
            upgrade_scroll = int(((new_y - scroll_top) / max_thumb_travel) * max_scroll) if max_thumb_travel > 0 else 0

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
    col1_x = box_x + 20
    col2_x = box_x + 80
    col3_x = box_x + box_w - 140

    icon_header   = font_med.render("Icon", True, WHITE)
    name_header   = font_med.render("Unlock / Global", True, WHITE)
    status_header = font_med.render("Status", True, WHITE)
    #surface.blit(icon_header,   (col1_x, header_y))
    surface.blit(name_header,   (col2_x, header_y))
    surface.blit(status_header, (col3_x, header_y))

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
            biz = businesses[u["biz_index"]]
            is_unlocked = (biz["owned"] >= u["threshold"])
        else:
            # Global unlock: check if every single business meets that threshold
            is_unlocked = all(b["owned"] >= u["threshold"] for b in businesses)

        if y_offset + entry_h < scroll_top or y_offset > scroll_bottom:
            y_offset += entry_h + spacing
            continue

        entry_rect = pygame.Rect(box_x + 10, y_offset, box_w - 20, entry_h)
        pygame.draw.rect(surface, (50, 50, 70), entry_rect, border_radius=8)

        # If biz_index is None, use the global image; else use biz image/emoji
        if u["biz_index"] is not None:
            biz = businesses[u["biz_index"]]
            if biz.get("image"):
                icon_img = pygame.transform.smoothscale(biz["image"], (40, 40))
                surface.blit(icon_img, (col1_x, y_offset + 10))
            else:
                icon_surf = font_big.render(biz["icon"], True, WHITE)
                surface.blit(icon_surf, (col1_x, y_offset + 10))
        else:
            # Global unlock: draw global.png if available
            if u.get("image"):
                gimg_surf = pygame.transform.smoothscale(u["image"], (40, 40))
                surface.blit(gimg_surf, (col1_x, y_offset + 10))
            else:
                # fallback: draw a simple globe emoji
                globe_surf = font_big.render("🌐", True, WHITE)
                surface.blit(globe_surf, (col1_x, y_offset + 10))

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

    # ------------------------
    # DRAW VERTICAL SCROLLBAR
    # ------------------------
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

        # HANDLE DRAGGING
        global unlock_dragging, unlock_drag_offset
        if mouse_clicked and thumb_rect.collidepoint(mouse_pos):
            unlock_dragging = True
            unlock_drag_offset = mouse_pos[1] - thumb_y

        if unlock_dragging and pygame.mouse.get_pressed()[0]:
            new_y = mouse_pos[1] - unlock_drag_offset
            new_y = max(scroll_top, min(scroll_top + max_thumb_travel, new_y))
            unlock_scroll = int(((new_y - scroll_top) / max_thumb_travel) * max_scroll) if max_thumb_travel > 0 else 0

    return close_btn_rect

def draw_investors_ui(surface, mouse_pos, mouse_clicked):
    global close_btn_rect
    global show_investor_shop, galactic_investors_total, galactic_investors_spent, space_lifetime_earnings
    global investor_shop_scroll, global_speed_mult, global_profit_mult

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
    else:
        back_x = box_x + 12
        back_y = box_y + 12
        back_btn_rect = pygame.Rect(back_x, back_y, close_size, close_size)
        pygame.draw.rect(surface, BTN_HOVER, back_btn_rect, border_radius=4)
        arrow_surf = font_small.render("<", True, WHITE)
        surface.blit(
            arrow_surf,
            (back_x + (close_size - arrow_surf.get_width()) // 2,
             back_y + (close_size - arrow_surf.get_height()) // 2)
        )

    if not show_investor_shop:
        title_surf = font_big.render("Galactic Investors", True, WHITE)
        surface.blit(title_surf, (box_x + (box_w - title_surf.get_width()) // 2, box_y + 20))

        tagline = "Putting the ‘Galaxy’ back in ‘Galactic profits’! Look at those boosts!"
        tag_surf = font_small.render(tagline, True, GRAYED)
        surface.blit(tag_surf, (box_x + (box_w - tag_surf.get_width()) // 2, box_y + 60))

        info_y = box_y + 100
        line_spacing = 30

        gis_text = font_med.render(f"Total GIs: {galactic_investors_total}", True, WHITE)
        surface.blit(gis_text, (box_x + 40, info_y))

        bonus_text = font_med.render("Bonus per GI: 2%", True, WHITE)
        surface.blit(bonus_text, (box_x + 40, info_y + line_spacing))

        spent_text = font_med.render(f"GIs Spent: {galactic_investors_spent}", True, WHITE)
        surface.blit(spent_text, (box_x + 40, info_y + 2 * line_spacing))

        lf_q = space_lifetime_earnings / 1e15
        if lf_q < 0.01:
            lte_str = "0.00"
        else:
            lte_str = f"{lf_q:.2f}"
        lte_text = font_med.render(f"Lifetime Earnings: {lte_str} Q", True, WHITE)
        surface.blit(lte_text, (box_x + 40, info_y + 3 * line_spacing))

        potential = int(150 * math.sqrt(lf_q)) if lf_q > 0 else 0
        new_gis   = max(0, potential - galactic_investors_spent)
        claim_btn_rect = pygame.Rect(box_x + 40, box_y + box_h - 140, box_w - 80, 40)
        claim_color = BTN_HOVER if (new_gis > 0 and claim_btn_rect.collidepoint(mouse_pos)) else PANEL_DARK
        pygame.draw.rect(surface, claim_color, claim_btn_rect, border_radius=6)
        claim_txt = "Claim GIs" if new_gis > 0 else "No GIs Available"
        claim_surf = font_small.render(claim_txt, True, WHITE)
        surface.blit(
            claim_surf,
            (claim_btn_rect.x + (claim_btn_rect.w - claim_surf.get_width()) // 2,
             claim_btn_rect.y + (claim_btn_rect.h - claim_surf.get_height()) // 2)
        )
        if claim_btn_rect.collidepoint(mouse_pos) and mouse_clicked and new_gis > 0:
            lifetime_q = space_lifetime_earnings / 1e15
            potential_amt = int(150 * math.sqrt(lifetime_q)) if lifetime_q > 0 else 0
            new_amt = max(0, potential_amt - galactic_investors_spent)
            galactic_investors_total += new_amt
            galactic_investors_spent += new_amt
            # Reset all businesses etc.
            STARTING_MONEY = 50000000000000.0
            money = STARTING_MONEY
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
            for upg in upgrades:
                upg["purchased"] = False
            unlocked_shown.clear()

        shop_btn_rect = pygame.Rect(box_x + 40, box_y + box_h - 80, box_w - 80, 40)
        shop_color = BTN_HOVER if shop_btn_rect.collidepoint(mouse_pos) else PANEL_DARK
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
        title_surf = font_big.render("GALACTIC INVESTOR SHOP", True, WHITE)
        surface.blit(title_surf, (box_x + (box_w - title_surf.get_width()) // 2, box_y + 20))

        back_x = box_x + 12
        back_y = box_y + 12
        back_btn_rect = pygame.Rect(back_x, back_y, close_size, close_size)
        pygame.draw.rect(surface, BTN_HOVER, back_btn_rect, border_radius=4)
        arrow_surf = font_small.render("<", True, WHITE)
        surface.blit(
            arrow_surf,
            (back_x + (close_size - arrow_surf.get_width()) // 2,
             back_y + (close_size - arrow_surf.get_height()) // 2)
        )
        if back_btn_rect.collidepoint(mouse_pos) and mouse_clicked:
            show_investor_shop = False

        draw_investor_shop_list(surface, mouse_pos, mouse_clicked)
        return back_btn_rect

def draw_investor_shop_list(surface, mouse_pos, mouse_clicked):
    global investor_shop_scroll, galactic_investors_total, galactic_investors_spent

    box_w = int(WIDTH * 0.6)
    box_h = int(HEIGHT * 0.7)
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2

    line_y = box_y + 70
    pygame.draw.line(surface, GRAYED, (box_x + 20, line_y), (box_x + box_w - 20, line_y), 1)

    list_top    = line_y + 20
    list_bottom = box_y + box_h - 20
    visible_h   = list_bottom - list_top
    entry_h     = 60
    spacing     = 10

    clip_rect = pygame.Rect(box_x + 10, list_top, box_w - 20, visible_h)
    surface.set_clip(clip_rect)

    unpurchased = [g for g in galactic_upgrades if not g["purchased"]]
    total_h     = len(unpurchased) * (entry_h + spacing)
    max_scroll  = max(0, total_h - visible_h)
    investor_shop_scroll = max(0, min(investor_shop_scroll, max_scroll))

    y_offset = list_top - investor_shop_scroll
    col1_x = box_x + 20
    col2_x = box_x + 80
    col3_x = box_x + box_w - 140

    for upgrade in galactic_upgrades:
        if upgrade["purchased"]:
            continue

        if y_offset + entry_h < list_top or y_offset > list_bottom:
            y_offset += entry_h + spacing
            continue

        entry_rect = pygame.Rect(box_x + 10, y_offset, box_w - 20, entry_h)
        pygame.draw.rect(surface, (50, 50, 70), entry_rect, border_radius=8)

        icon_surf = font_big.render(upgrade["icon"], True, WHITE)
        surface.blit(icon_surf, (col1_x, y_offset + 10))

        name_surf = font_med.render(upgrade["name"], True, YELLOW)
        surface.blit(name_surf, (col2_x, y_offset + 8))
        desc_surf = font_small.render(upgrade["description"], True, GRAYED)
        surface.blit(desc_surf, (col2_x, y_offset + 30))

        cost_val = upgrade["cost"]
        mant, suff = format_number_parts(cost_val)
        can_buy  = galactic_investors_total >= cost_val
        buy_rect = pygame.Rect(col3_x, y_offset + 15, 100, 30)
        if can_buy:
            base_color = ACCENT
        else:
            base_color = PANEL_DARK
        if buy_rect.collidepoint(mouse_pos) and can_buy:
            buy_color = BTN_HOVER
        else:
            buy_color = base_color
        pygame.draw.rect(surface, buy_color, buy_rect, border_radius=6)
        buy_txt = font_small.render(f"Spend {mant}{suff} GIs", True, WHITE)
        surface.blit(
            buy_txt,
            (buy_rect.x + (buy_rect.w - buy_txt.get_width()) // 2,
             y_offset + 15 + (30 - buy_txt.get_height()) // 2)
        )

        if buy_rect.collidepoint(mouse_pos) and mouse_clicked and can_buy:
            galactic_investors_total -= cost_val
            galactic_investors_spent  += cost_val
            upgrade["purchased"] = True
            name = upgrade["name"]
            if name == "Heavenly Harvest":
                global_profit_mult *= 2
            elif name == "Divine Acceleration":
                global_speed_mult *= 2
            elif name == "Cosmic Fortune":
                global_profit_mult *= 3
            elif name == "Temporal Warp":
                global_speed_mult *= 3
            elif name == "Astral Dividend":
                pass
            elif name == "Galactic Beacon":
                for b in businesses:
                    b["unlocked"] = True

        y_offset += entry_h + spacing

    surface.set_clip(None)

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

    # Standard pop-up (e.g., offline earnings) auto-dismiss
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
# 15. EVENT LOOP & MAIN LOOP
# -------------------------------------------------------------------------------
running = True
mouse_down = False

while running:
    dt = clock.tick(FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

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

            save_game(save_data)
            running = False

        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            PANEL_WIDTH    = WIDTH - PANEL_X - 20
            PANEL_HEIGHT   = HEIGHT - PANEL_Y - 20

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            mouse_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

    screen.fill(BG_DARK)

    # Draw header and business panel first (always visible)
    draw_header(screen, money, mouse_pos, mouse_clicked)
    draw_business_panel(screen, dt, mouse_pos, mouse_clicked)

    # Draw sidebar and detect which button is clicked
    sidebar_click = draw_sidebar(screen, mouse_pos, mouse_clicked)
    if sidebar_click == 0 and mouse_clicked:
        overlay_mode = "Managers"
    elif sidebar_click == 1 and mouse_clicked:
        overlay_mode = "Upgrades"
    elif sidebar_click == 2 and mouse_clicked:
        overlay_mode = "Unlocks"
    elif sidebar_click == 3 and mouse_clicked:
        overlay_mode = "Investors"

    # Draw overlay UI if in a menu
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

    # Handle click on first-time popup close button
    if first_time_popup and mouse_clicked:
        if first_time_popup_close.collidepoint(mouse_pos):
            first_time_popup = False

    # Draw the pop-up (either first-time or offline earnings)
    draw_popup(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
