units = [
    " ",                      # 10^0
    " Thousand",              # 10^3
    " Million",               # 10^6
    " Billion",               # 10^9
    " Trillion",              # 10^12
    " Quadrillion",           # 10^15
    " Quintillion",           # 10^18
    " Sextillion",            # 10^21
    " Septillion",            # 10^24
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


import pygame
import sys
import os
import json
from pygame.locals import *

pygame.init()

# -----------------------------------
# Constants
# -----------------------------------
WIDTH, HEIGHT = 1200, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Galactic Capitalist")

FPS = 60
clock = pygame.time.Clock()

# --- Colors ---
WHITE        = (235, 235, 245)
ACCENT       = (82, 130, 255)
ACCENT_LIGHT = (130, 180, 255)
BG_DARK      = (30, 32, 41)
PANEL_DARK   = (42, 44, 58)
SIDEBAR_BG   = (36, 37, 50)
BUSINESS_BG  = (48, 52, 70)
BUSINESS_BG_LOCKED = (38, 40, 50)
PROGRESS_BG  = (40, 44, 55)
PROGRESS_FILL= (90, 200, 150)
BTN_HOVER    = (90, 110, 200)
COIN_COLOR   = (244, 201, 66)
GRAYED       = (110, 110, 120)
OVERLAY      = (40, 42, 56, 200)
POPUP_BG     = (50, 52, 70)
POPUP_TEXT   = (235, 235, 245)

font_big    = pygame.font.SysFont(None, 44)
font_med    = pygame.font.SysFont(None, 32)
font_small  = pygame.font.SysFont(None, 20)
font_popup  = pygame.font.SysFont(None, 36)

SAVE_FILE = "save_state.json"

# -----------------------------------
# Units for number formatting
# -----------------------------------
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
capitalist_upgrades = [
    {
        "name":        "Mogul",
        "description": "Profit Speed Doubled once you have 25 of every business",
        "icon":        "🏦",
        "cost":        25,
        "purchased":   False
    },
    {
        "name":        "Oligarch",
        "description": "Profit Speed Doubled once you have 50 of every business",
        "icon":        "💵",
        "cost":        50,
        "purchased":   False
    },
    {
        "name":        "Tycoon",
        "description": "Profit Speed Doubled once you have 100 of every business",
        "icon":        "👑",
        "cost":        100,
        "purchased":   False
    },
    {
        "name":        "Adam Smith Award",
        "description": "Profit Speed Doubled once you have 200 of every business",
        "icon":        "📜",
        "cost":        200,
        "purchased":   False
    },
    {
        "name":        "Universal Capitalist",
        "description": "Profit Speed Doubled once you have 300 of every business",
        "icon":        "🌐",
        "cost":        300,
        "purchased":   False
    },
    {
        "name":        "Theoretical Economist",
        "description": "Profit Speed Doubled once you have 400 of every business",
        "icon":        "📈",
        "cost":        400,
        "purchased":   False
    }
]
