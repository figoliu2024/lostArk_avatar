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
    "v":[623,999 ,51,51],
}


# Wardancer = {
#     {
#         "key": "q",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "w",
#         "abilityType": "normal",
#         "hold": True,
#         "holdTime": 800,
#         "cast": False,
#         "castTime": None,
#         "directional": True,
#     },
#     {
#         "key": "e",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": True,
#     },
#     {
#         "key": "r",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": True,
#         "castTime": 2500,
#         "directional": False,
#     },
#     {
#         "key": "a",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "s",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "d",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "f",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": True,
#     },
#     {
#         "key": "v",
#         "abilityType": "awakening",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "z",
#         "abilityType": "specialty1",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
# }

# Artist = {
#     {
#         "key": "q",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "w",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": True,
#     },
#     {
#         "key": "e",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": True,
#     },
#     {
#         "key": "r",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": True,
#         "castTime": 2500,
#         "directional": False,
#     },
#     {
#         "key": "a",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "s",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "d",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "f",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": True,
#     },
#     {
#         "key": "v",
#         "abilityType": "awakening",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "z",
#         "abilityType": "specialty1",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
# }


# Arcanist = {
#     {
#         "key": "q",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "w",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": True,
#     },
#     {
#         "key": "e",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": True,
#     },
#     {
#         "key": "r",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": True,
#         "castTime": 2500,
#         "directional": False,
#     },
#     {
#         "key": "a",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "s",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "d",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "f",
#         "abilityType": "normal",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": True,
#     },
#     {
#         "key": "v",
#         "abilityType": "awakening",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
#     {
#         "key": "z",
#         "abilityType": "specialty1",
#         "hold": False,
#         "holdTime": None,
#         "cast": False,
#         "castTime": None,
#         "directional": False,
#     },
# }