"""
    IMPORTANT #1:
    Please change game settings to EXACTLY these numbers:
    desktop resolution: 1920x1080
    In-game Video settings:

    Resolution: 1920x1080
    Screen: Borderless
    Force 21:9 Aspect Ratio checked
    In-game Gameplay -> Controls and Display -> HUD size: 110%
    minimap transparency (at top right corner): 100%
    minimap zoom-in (at top right corner): 65%

    IMPORTANT #2: 
    config must be set up correctly in order for the bot to work properly on your machine.
    Refer to the inline comments below:

    For Lopang enjoyers: https://github.com/any-other-guy/LostArk-Endless-Chaos/issues/15
    Set your first bifrost point to be at lopang island.
    Exact location to be right in front of the NPC machine which stands farthest to the entrance.
    Then set your 2/4/5 (because i dont have no3 unlocked) bifrost location to be right in front of those three lopang quest hand-in NPCs.
    Set your lopang quests as your ONLY 3 favourite quests
"""

defaultStatesConfig = {
    "status": "inCity",
    "abilityScreenshots": [],
    "bossBarLocated": False,
    "clearCount": 0,
    "fullClearCount": 0,
    "moveTime": 0,
    "botStartTime": None,
    "instanceStartTime": None,
    "deathCount": 0,
    "healthPotCount": 0,
    "timeoutCount": 0,
    "goldPortalCount": 0,
    "purplePortalCount": 0,
    "badRunCount": 0,
    "gameRestartCount": 0,
    "gameCrashCount": 0,
    "gameOfflineCount": 0,
    "minTime": 450000,
    "maxTime": -1,
    "floor3Mode": False,
    "multiCharacterMode": True,
    "finishedCharacter": 0,
    "currentCharacter": 0,
    "multiCharacterModeState": 0,
    "numberOfCharacters":6,
    "doneEmojiTimes":0,
    "doneMusicTimes":0,
    "screenWidth":  1920,
    "screenHeight": 1080,
    "windowTopLeft":[0,0], #定位窗口的锚点
    "minimapRole":[148,126], #相对小地图的坐标
    # "windowTopLeft_y":0, #定位窗口的锚点

    "mainCharacter": 0,  # must be in between number 0 to len(characters) - 1 (0 is the first character)
    "GFN": True,  # set True for Geforce Now users
    "enableMultiCharacterMode": True,  # this is lit
    "enableLopang": True,  # NOTE: you need to setup bifrost locations properly for this, at very specific locations. Look up ^
    "enableGuildDonation": True,  # please make sure all your characters have a guild
    "enableRapport": True,  # NOTE: you need to setup bifrost no3 infront of a rapport NPC
    "enableBreakStone": True,
    "enableChaos": True,
    "floor3Mode": False,  # only enable if you ONLY want to run infinite floor3 clearing
    # Setup your characters below:
    # can setup UP TO 18(0 to 17) characters for daily chaos/lopang/guild stuff
    # however your main must be in character 0 to 5 (just for re-connect back after disconnection happens)
    # ilvl-endless is the dungeon which you want to run infinitely
    # ilvl-aor is the daily aura of resonance dungeon you only want to run TWICE per day
    # IMPORTANT: dungeon ilvl choices are only limited to 1475, 1445, 1370, 1110 for now. I will add more later when brel comes out
    # "characters": characters,
    "performance": False,  # set True for lower-end PCs
    "invisible": True,
    "healthPotAtPercent": 0.35,  # health threshold to trigger potion
    # "useAwakening": True, # not checking this for now
    # "useSpeciality1": True, # not checking this for now
    # "useSpeciality2": True, # not checking this for now
    "auraRepair": True,  # True if you have aura, if not then for non-aura users: MUST have your character parked near a repairer in city before starting the script
    "shortcutEnterChaos": True,  # you want to use True
    "useHealthPot": True,  # you want to use True
    # You might not want to touch anything below, because I assume you have your game setup same as mine :) otherwise something might not work properly!
    "confidenceForGFN": 0.9,
    "timeLimit": 450000,  # to prevent unexpected amount of time spent in a chaos dungeon, a tiem limit is set here, will quit after this amount of seconds
    "timeLimitAor": 720000,  # to prevent unexpected amount of time spent in a chaos dungeon, a tiem limit is set here, will quit after this amount of seconds
    "blackScreenTimeLimit": 30000,  # if stuck in nothing for this amount of time, alt f4 game, restart and resume.
    "delayedStart": 2500,
    "portalPause": 700,
    "gameLoadingTime": 10, #游戏读条时间，根据机器性能修改
    "picPath":"./res/pic/",
    "supportClass":["Wardancer","Artist","Arcanist"],   
}


defaultUiRegions = {
    "minimap": [1595,40,294,254],  # (1700, 200, 125, 120)
    "abilities": [625, 779, 300, 155],
    "leaveMenu": [0, 154, 250, 300],
    "buffs":  [625, 780, 300, 60],
    "center": [685, 280, 600, 600],
    "portal": [228, 230, 1370, 570],
    "inTownCheck":[1848, 4, 40, 40],
    "inChaosCheck":[106, 110, 80, 30],
    "researchCheck":[964,330, 400,200],
    "supportResearchCheck":[705,520, 250, 200],
    "quickCharacterCheck":[384,650,100,100],
    "EvnaTaskPanel":[329,281,300,600],
    "EvnaTaskStatuePanel":[1226,281,200,600],
    "fullScreen":[0,0,1920,1080],
    "loadingUiRegion":[876,912,200,100],
    "rapportRegion":[29,822,200,260],
    "EvnaTaskFinishedCheck":[1556,411,300,460],
    "hpBarRegion":[612,949,259,28],
    "specialClassRegion":[853,841,222,225],
    "chaosStateRegion":[14,34,251,300],
}
    
defaultUiCoordi = {
    "charPositionsAtCharSelect": [
        [500, 827],
        [681, 827],
        [874, 827],
        [1050, 827],
        [1237, 827],
        [1425, 827],
    ],
    "charPositions": [
        [760, 440],
        [960, 440],
        [1160, 440],
        [760, 530],
        [960, 530],
        [1160, 530],
        [760, 620],
        [960, 620],
        [1160, 620],
        [760, 530],
        [960, 530],
        [1160, 530],
        [760, 620],
        [960, 620],
        [1160, 620],
    ],
    "screenCenter":[960,540],
    # "screenCenterX": 960,
    # "screenCenterY": 540,
    "minimapCenter":[1772,272],
    # "minimapRole":[148,126],
    # "minimapCenterX": 1772,
    # "minimapCenterY": 272,
    "healthCheck":[690,854],
    # "healthCheckX": 690,
    # "healthCheckY": 854,
    "charSwitch": [540,683],
    # "charSwitchX": 540,
    # "charSwitchY": 683,
    "charPositionsAtCharSelect": [
        [500, 827],
        [681, 827],
        [874, 827],
        [1050, 827],
        [1237, 827],
        [1425, 827],
    ],
    "charPositions": [
        [760, 440],
        [960, 440],
        [1160, 440],
        [760, 530],
        [960, 530],
        [1160, 530],
        [760, 620],
        [960, 620],
        [1160, 620],
        [760, 530],
        [960, 530],
        [1160, 530],
        [760, 620],
        [960, 620],
        [1160, 620],
    ],
    "charSelectConnect":[1030,684],
    # "charSelectConnectX": 1030,
    # "charSelectConnectY": 684,
    "charSelectOk":[920,590],
    # "charSelectOkX": 920,
    # "charSelectOkY": 590,
    "guildDono":[1580,945],
    "donoTap":[686,140],
    "donoSilver":[708,567],
    "researchTap":[1304,140],
    "supportConf":[910,760],
    "fastLoginOtherCharc":[397,727],
    "login":[1054,734],
    "bifrost":[1696,313],
    "roleInMiniMap":[1742,166.5],
    "dailyTasks":[563,301],
    "moveBoundary_TopLeft":[400,120],
    "moveBoundary_BottomRigth":[1500,950],
    "folderChatWindow":[366,739],
    "lowHp":[685,959],
    "midHp":[747,959],
    "highHp":[823,959],
}


defaultCharacters = {
    "charc0":{
        "index": 0,
        "class": "Wardancer", #斗魂
        "ilvl-endless": 1540,
        "ilvl-aor": 1540,
        "chaos":True,
        "lopang": False,
        "guildDonation": True,
        "rapport": True,
        "breakStone": True,
        "abilities": [],
    },
    "charc1":{
        "index": 1,
        "class": "Artist", #墨灵
        "ilvl-endless": 1477,
        "ilvl-aor": 1477,
        "chaos":True,
        "lopang": False,
        "guildDonation": True,
        "rapport": False,
        "breakStone": True,
        "abilities": [],
        "combolist":["Q","E","W","R","A","S","D","F"]
    },
    "charc2":{
        "index": 2,
        "class": "Arcanist", #卡牌
        "ilvl-endless": 1430,
        "ilvl-aor": 1430,
        "chaos":True,
        "lopang": True,
        "guildDonation": True,
        "rapport": True,
        "breakStone": False,
        "abilities": [],
    },         
    "charc3":{
        "index": 3,
        "class": "Shadowhunter", #半魔
        "ilvl-endless": 1430,
        "ilvl-aor": 1430,
        "chaos":False,
        "lopang": True,
        "guildDonation": True,
        "rapport": False,
        "breakStone": False,
        "abilities": [],
    },
    "charc4":{
        "index": 4,
        "class": "fighter",
        "ilvl-endless": 1430,
        "ilvl-aor": 1430,
        "chaos":False,
        "lopang": True,
        "guildDonation": True,
        "rapport": False,
        "breakStone": False,
        "abilities": [],
    },    
    "charc5":{
        "index":5,
        "class": "Soulfist",
        "ilvl-endless": 800,
        "ilvl-aor": 800,
        "chaos":False,
        "lopang": False,
        "guildDonation": True,
        "rapport": True,
        "breakStone": False,
        "abilities": [],
    },

    
}

