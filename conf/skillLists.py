"""
    Make sure you have configed abilities for your specific class and spell position:
    key: keybind of the spell
    abilityType: do not change for now
    hold: if the spell is a hold spell, I DONT RECOMMENDED you to utilize hold spells
    holdTime: hold for x amount of milliseconds
    cast: if the spell is a cast spell
    castTime: cast time in milliseconds
    position: DO NOT CHANGE, they are fixed by HUD Size and Resolution
    directional: if the spell needs to be pointed at a direction where mobs are at

    My recommendations:
    Go to Trixion
    Find the spells/tripod combinations which does the LARGEST AoE around your character
    Try to avoid spells that moves your character a lot
    For instant spells that have long animations, Change the spell to cast mode and give it a proper cast time in milliseconds
    Trial and Error, until it works nicely
    Ideally how fast your chaos run should be:
    Floor 2 clear time should be around 100 - 160 seconds
    Floor 3 clear time could be anywhere around 200 - 300 seconds
"""

defaultSkillBarRegions={
    "Q":[682,978 ,45,45],
    "W":[729,978 ,45,45],
    "E":[776,978 ,45,45],
    "R":[823,978 ,45,45],
    "A":[704,1025,45,45],
    "S":[751,1025,45,45],
    "D":[798,1025,45,45],
    "F":[845,1025,45,45],
    "V":[623,999 ,52,52],
}


Wardancer = {
    "Q":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 1000,
        "directional": True,
    },
    "W":{
        "abilityType": "normal",
        "hold": True,
        "holdTime": 1200,
        "cast": False,
        "castTime": None,
        "directional": False,
    },
    "E":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 200,
        "directional": True,
    },
    "R":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": True,
        "castTime": 800,
        "directional": True,
    },
    "A":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 500,
        "directional": False,
    },
    "S":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 100,
        "directional": False,
    },
    "D": {
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 500,
        "directional": True,
    },
    "F":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 500,
        "directional": True,
    },
    "V":{
        "abilityType": "awakening",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 5000,
        "directional": False,
    },
    "combolist":["F","W","S","E","Q","R","A","D","V"],
}

Artist = {
    "Q":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 500,
        "directional": True,
    },
    "W":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 500,
        "directional": True,
    },
    "E":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 500,
        "directional": True,
    },
    "R":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 500,
        "directional": True,
    },
    "A":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "S":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "D": {
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "F":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "V":{
        "abilityType": "awakening",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 5000,
        "directional": False,
    },
    "combolist":["W","S","E","Q","R","A","D","F","V"],
}


Arcanist = {
    "Q":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "W":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "E":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "R":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 1500,
        "directional": True,
    },
    "A":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": True,
        "castTime": 1000,
        "directional": True,
    },
    "S":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "D": {
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": True,
        "castTime": 1000,
        "directional": True,
    },
    "F":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "V":{
        "abilityType": "awakening",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 5000,
        "directional": False,
    },
    "combolist":["R","F","S","D","Q","W","A","Q","V"],
}



Demonic = {
    "Q":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "W":{
        "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "E":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "R":{
       "abilityType": "normal",
        "hold": True,
        "holdTime": 1000,
        "cast": False,
        "castTime": None,
        "directional": True,
    },
    "A":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "S":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "D": {
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": False,
    },
    "F":{
       "abilityType": "normal",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 300,
        "directional": True,
    },
    "V":{
        "abilityType": "awakening",
        "hold": False,
        "holdTime": None,
        "cast": False,
        "castTime": 2000,
        "directional": False,
    },
    "combolist":["F","D","Q","R","S","E","A","W","V"],
}