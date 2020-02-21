import os
import json
from functools import lru_cache
from app.utils import local_path
from .horns import get_horns
from .melodies import get_melodies

HORNS={}
MELODIES={}

def reset_data(horns_path:str=local_path('horns.json'),melodies_path:str=local_path('melodies.json')):
    get_horns_from_effects.cache_clear()
    get_effects_from_horn.cache_clear()
    # get_horn_info.cache_clear()
    
    HORNS=None
    MELODIES=None
    if os.path.exists( horns_path):os.remove(horns_path)
    if os.path.exists( melodies_path):os.remove(melodies_path)
    load_data()

def load_data(horns_path:str=local_path('horns.json'),melodies_path:str=local_path('melodies.json')):
    """
    Load data, either from already stored variable, file, or request from serever
    """
    #horns
    global HORNS
    #if horns not already loaded
    if not HORNS:
        if not os.path.exists(horns_path):
            HORNS=get_horns()
            json.dump(HORNS,open(horns_path,'w'),indent=4,separators=(',',':'),sort_keys=True)
        else:
            with open(horns_path,'r') as f:
                HORNS=json.load(f)

    #melodies
    global MELODIES
    #if melodies not already loaded
    if not MELODIES:
        if not os.path.exists(melodies_path):
            MELODIES=get_melodies()
            json.dump(MELODIES,open(melodies_path,'w'),indent=4,separators=(',',':'),sort_keys=True)
        else:
            with open(melodies_path,'r') as f:
                MELODIES=json.load(f)
    
    return HORNS,MELODIES

def save_data(horns_path:str=local_path('horns.json'),melodies_path:str=local_path('melodies.json')):
    """
    Save data to json files (do this whenever modifying the data in memory)
    """
    json.dump(HORNS,open(horns_path,'w'),indent=4,separators=(',',':'),sort_keys=True)
    json.dump(MELODIES,open(melodies_path,'w'),indent=4,separators=(',',':'),sort_keys=True)

@lru_cache()
def get_horns_from_effects(effects:list):
    """
    Get horns that can produce the request effects\n
    Effects must be VALID effect names, matching those in the list on the\n
    wiki EXACTLY
    """
    if type(effects)==str:
        effects=[effects]
    horns,melodies=load_data()
    valid_horns=[]
    effects=[effect.strip() for effect in effects]
    notes_required={e:set() for e in effects}
    for melody,melody_data in melodies['melodies'].items():
       for effect in effects:
           if effect in melody_data['effects']:
               notes=[m for m in melody.split('-')]
               if sorted(notes) not in [sorted(n) for n in notes_required[effect]]:
                notes_required[effect].add(tuple(notes))


    
    for horn,horn_data in horns['horns'].items():
        valid=True
        #get horn notes
        horn_notes=[n for n in horn_data['notes'].split('-')]
        #check it can play every effect
        for effect,combinations in notes_required.items():
            #check every combination that makes this effect
            if not any(all(cn in horn_notes for cn in combination) for combination in combinations):
                #it can't play this effect, so isn't valid
                valid=False
                break
        if valid: valid_horns.append(horn_data)





    
    return valid_horns

@lru_cache()
def get_effects_from_horn(horn:dict):
    """
    Get effects from horn
    """
    horns,melodies=load_data()
    if type(horn)==str:
        if horn not in horns['horns']:return None
        horn=horns['horns'][horn]

    horn_notes=set(horn['notes'].split('-'))

    effects=[]

    for melody,melody_data in melodies['melodies'].items():
        melody_notes=set(melody.split('-'))
        if all(n in horn_notes for n in melody_notes):
            effects.append(melody_data)


    
   
    return effects

# @lru_cache()
# def recommend_effect_names(part:str):
#     horns,melodies=load_data()
#     return [e for e in melodies.keys() if part.lower() in e.lower()]

# @lru_cache()
# def recommend_horn_names(part:str):
#     horns,melodies=load_data()
#     return [h for h in horns.keys() if part.lower() in h.lower()]


def get_horn_list():
    horns,melodies=load_data()
    return horns

def get_melody_list():
    horns,melodies=load_data()
    return melodies

def get_horn_names():
    horns,melodies=load_data()
    return sorted(horns['horns'].keys)

def get_melody_names():
    horns,melodies=load_data()
    melody_names=set()
    for melody,data in melodies['melodies'].items():
        for effect in data['effects']:
            melody_names.add(effect)
    return sorted(list(melody_names))

