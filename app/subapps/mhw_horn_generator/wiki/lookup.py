import os
import json
from functools import lru_cache
from app.utils import local_path
from .horns import get_horns,request_horn_info
from .melodies import get_melodies

HORNS={}
MELODIES={}

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

    for horn,horn_data in horns['horns'].items():
        valid=True
        if type(horn_data)!=dict:continue
        if horn=="Fate's Dirge":
            print()
        for effect in effects:
            if not any(can_play(horn_data['notes'],melody_option) for melody_option in melodies['melodies'][effect]['melodies']):
                valid=False

        if valid:valid_horns.append(horn_data)

   
        
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
    effects=[]
    
    for melody,melody_data in melodies['melodies'].items():
        if type(melody_data)!=dict:continue
        horn_notes=horn['notes']
        
        if any(can_play(horn_notes,melody_option) for melody_option in melodies['melodies'][melody]['melodies']):
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

def can_play(horn_notes:list,melody_notes:list):
    """
    Check if the given horn notes are enough to play the given melody
    """
    for note_group in melody_notes:
        intersect=set(note_group).intersection(horn_notes)
        if len(intersect)<1:return False
    return True


@lru_cache()
def get_horn_info(horn:str):
    """
    Look up basic info for the given horn. `horn` can be a link to the horn's wiki page, or the horn name.
    """
    #get name and link, one way or another
    link,name,='',''
    horns=get_horn_list()
    if 'fextralife' in horn:
        link=horn
        name=horn.split('/')[-1].replace('+',' ')
    else:
        name=horn
        link=horns['horns'].get(name,'')
    if not link or not name:
        return None
    
    info=horns['horn'].get(name,{})
    #if info not already cached, get
    if not info:
        info=request_horn_info(name)
        horns['horn']['info']=info
        save_data()
    return info

