import requests
from bs4 import BeautifulSoup
import bs4
import json
import datetime
import re
from functools import lru_cache

@lru_cache()
def fmt_melody_effects(effect:str)->str:
    """
    Split and format a raw effect(s) string, to be more friendly\n
    and usable to look up on the wiki
    """
    table={'Atk':'Attack','Def':'Defense','Rec':'Recovery','Envir':'Environmental'}
    effects=re.split('\([a-zA-Z]\)|and|And',effect)
    ret=[]
    for eff in effects:
        if not eff:continue
        eff=eff.replace('.','').replace('\u00a0','')\
            .replace('And','').replace('and','').replace('+','')
        eff=eff.translate(table)
        ret.append(eff.strip())
    if len(ret)>1 and any(s.endswith('up') for s in ret) and not all(s.endswith('up') for s in ret):
        for i,eff in enumerate(ret):
            if not eff.endswith('up'):
                ret[i]+=' up'



    

    return ret

@lru_cache()
def get_effect_wiki_page(effect:str,url:str=r'https://monsterhunterworld.wiki.fextralife.com'):
    """
    Get the wiki page url for an effect.\n
    Returns the url if found, otherwise None
    """
    response=requests.get(f'{url}/{"+".join(effect.split())}')
    if response.status_code==200:
        return response.url
    else: return None

def get_melodies(url:str=r'https://monsterhunterworld.wiki.fextralife.com/Hunting+Horn')->dict:
    """
    Get melodies and their note info from wiki.\n
    Returns a dictionary
    """
    timefmt='%m-%d-%Y:%H:%M:%S'
    data={'melodies':{}}
    currtime=datetime.datetime.now()
    data['parse_time']=currtime.strftime(timefmt)
    #Get page
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")

    tables:bs4.ResultSet=soup.findAll(attrs={'class':'wiki_table'})
    melodies_table:bs4.Tag=tables[1]

    body:bs4.Tag=melodies_table.findChild('tbody')
    #Go through each row
    for row in body.findChildren(recursive=False):
        note1,note2,note3,note4,effect=[c for c in row.findChildren(recursive=False)]
        
        if effect.text not in data['melodies']:
            data['melodies'][effect.text]={'melodies':[],'name':effect.text}

        #Try to get a link to effect from wiki
        effects=fmt_melody_effects(effect.text)
        for eff in effects:
            eff_url=get_effect_wiki_page(eff)
            if eff_url:
                if 'effect_urls' not in data['melodies'][effect.text]:
                    data['melodies'][effect.text]['effect_urls']=[]
                data['melodies'][effect.text]['effect_urls'].append(eff_url)

        #Go through each note
        melody=[]
        for note in (note1,note2,note3,note4):
            tmp=[]
            for content in note.contents:
                if not isinstance(content,str) and 'src' in content.attrs:
                    src=content.attrs['src']
                    num=src.split('mhw-note')[1].replace('-icon.png','')
                    tmp.append(num)
                    
                    
                    #get note icon url
                    if 'note_icon_url' not in data:
                        data['note_icon_url']=url.replace(r'/Hunting+Horn','')+src.replace(num,'{0}')
                        
            if tmp:
                 melody.append(tmp)
        data['melodies'][effect.text]['melodies'].append(melody)

    return data


# melodies=get_melodies()
# json.dump(melodies,open('melodies.json','w'),indent=4,separators=(',',':'),sort_keys=True)

# eff=fmt_melody_effects('Attack and Defense up (S)')
# print(eff)
# print([get_effect_wiki_page(e) for e in eff])
