import sys
from os import path
from collections import OrderedDict
import pprint

_PATHSETS = [
    "casual-core",
    "casual-dboost",
    "standard-core",
    "standard-dboost",
    "standard-lure",
    "standard-abilities",
    "expert-core",
    "expert-dboost",
    "expert-lure",
    "expert-abilities",
    "dbash",
    "master-core",
    "master-dboost",
    "master-lure",
    "master-abilities",
    "gjump",
    "glitched",
    "timed-level",
    "insane"
]

def get_areas(verbose=False):
    dir_path = path.dirname(path.realpath(__file__))
    return ori_load_file("%s/areas.ori" % dir_path, verbose)

def ori_load_file(fn, verbose=False):
    with open(fn, 'r') as f:
        lines = f.readlines()

    return ori_load(lines, verbose)

  

def ori_load(lines, verbose=False):   
    
    errors = ""
       
    for i in range(len(lines)):
        line = lines[i]
        tokens = lines[i].split()
        if len(tokens) == 0:
            print(line, end="")
            continue
        
        if tokens[0] not in _PATHSETS:
            print(line, end="")
            continue
        
        if line.find("-abilities") != -1:
            if line.find("Ability=") == -1:
                errors += "Line {} is in -abilites but without an Ability=\n".format(i + 1)
        if line.find("-dboost") != -1:
            if line.find("Health=") == -1:
                errors += "Line {} is in -dboost but without a Health=\n".format(i + 1)
                tokens.append("Health=3")
        
        has_cflame = "ChargeFlame" in tokens
        has_dash = "Dash" in tokens
        has_dj = "DoubleJump" in tokens
        has_health = line.find("Health=") != -1
        ability = 0
        for token in tokens:
            if token.startswith("Ability="):
                ability = int(token.split("=")[1])
        
        if ability == 0:
            pass
        elif ability == 3:
            remove_ability = False
            if has_dash:
                dash_index = tokens.index("Dash")
                tokens[dash_index] = "AirDash"
                remove_ability = True
            if has_cflame and tokens[0].startswith("master"):
                cflame_index = tokens.index("ChargeFlame")
                tokens[cflame_index] = "ChargeFlameBurn"
                remove_ability = True
            if remove_ability:
                ability_index = tokens.index("Ability=3")
                tokens.pop(ability_index)
        elif ability == 6:
            remove_ability = False
            if has_dash:
                dash_index = tokens.index("Dash")
                tokens[dash_index] = "ChargeDash"
                remove_ability = True
            #if has_cflame and tokens[0].startswith("master"):
            #    cflame_index = tokens.index("ChargeFlame")
            #    tokens[cflame_index] = "ChargeFlameBurn"
            if remove_ability:
                ability_index = tokens.index("Ability=6")
                tokens.pop(ability_index)
        elif ability == 12:
            if has_dj:
                dj_index = tokens.index("DoubleJump")
                tokens[dj_index] = "TripleJump"
            ability_index = tokens.index("Ability=12")
            if has_health:
                tokens[ability_index] = "UltraDefense"
            else:
                tokens.pop(ability_index)
            if has_dash:
                dash_index = tokens.index("Dash")
                tokens[dash_index] = "ChargeDash"
            #if has_cflame and tokens[0].startswith("master"):
            #    cflame_index = tokens.index("ChargeFlame")
            #    tokens[cflame_index] = "ChargeFlameBurn"
        else:
            errors += "Line {} has Ability={}\n".format(i + 1, ability)

        if tokens[0] in ["casual-core", "casual-dboost"]:
            tokens[0] = "casual"
        elif tokens[0] in ["standard-core", "standard-dboost", "standard-abilities"]:
            tokens[0] = "standard"
        elif tokens[0] in ["standard-lure"]:
            tokens[0] = "standard Lure"
        elif tokens[0] in ["expert-core", "expert-dboost", "expert-abilities"]:
            tokens[0] = "expert"
        elif tokens[0] in ["expert-lure"]:
            tokens[0] = "expert Lure"  
        elif tokens[0] in ["dbash"]:
            tokens[0] = "expert"
            bash_index = tokens.index("Bash")
            tokens[bash_index] = "DoubleBash"
        elif tokens[0] in ["master-core", "master-dboost", "master-abilities"]:
            tokens[0] = "master"
        elif tokens[0] in ["master-lure"]:
            tokens[0] = "master Lure"
        elif tokens[0] in ["gjump"]:
            tokens[0] = "master"
            climb_index = tokens.index("Climb")
            tokens[climb_index] = "GrenadeJump"
            cjump_index = tokens.index("ChargeJump")
            tokens.pop(cjump_index)
            grenade_index = tokens.index("Grenade")
            tokens.pop(grenade_index)
        # glitched, timed-level, and insane don't change.        
     
        first_character = line.strip()[0]
        text_start = line.find(first_character)
        indentation = line[0:text_start]
        print(indentation + " ".join(tokens))

    #print(errors)


    
if __name__ == "__main__":
    import sys
    fn = sys.argv[1]
    contents = ori_load_file(fn, True)
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(contents)
