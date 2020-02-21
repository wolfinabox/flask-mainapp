import requests
from bs4 import BeautifulSoup
import bs4
import json
import datetime
import re


DEFAULT_MELODIES_URL = r'https://monsterhunter.fandom.com/wiki/MHWI:_Horn_Melodies'


# @lru_cache()
# def fmt_melody_effects(effect:str)->str:
#     """
#     Split and format a raw effect(s) string, to be more friendly\n
#     and usable to look up on the wiki
#     """
#     table={'Atk':'Attack','Def':'Defense','Rec':'Recovery','Envir':'Environmental'}
#     effects=re.split('\([a-zA-Z]\)|and|And',effect)
#     ret=[]
#     for eff in effects:
#         if not eff:continue
#         eff=eff.replace('.','').replace('\u00a0','')\
#             .replace('And','').replace('and','').replace('+','')
#         eff=eff.translate(table)
#         ret.append(eff.strip())
#     if len(ret)>1 and any(s.endswith('up') for s in ret) and not all(s.endswith('up') for s in ret):
#         for i,eff in enumerate(ret):
#             if not eff.endswith('up'):
#                 ret[i]+=' up'


#     return ret

# @lru_cache()
# def get_effect_wiki_page(effect:str,url:str=r'https://monsterhunterworld.wiki.fextralife.com'):
#     """
#     Get the wiki page url for an effect.\n
#     Returns the url if found, otherwise None
#     """
#     response=requests.get(f'{url}/{"+".join(effect.split())}')
#     if response.status_code==200:
#         return response.url
#     else: return None

def get_melodies(url: str = DEFAULT_MELODIES_URL) -> dict:
    """
    Get melodies and their note info from wiki.\n
    Returns a dictionary
    """
    timefmt = '%m-%d-%Y:%H:%M:%S'
    data = {'melodies': {}}
    currtime = datetime.datetime.now()
    data['parse_time'] = currtime.strftime(timefmt)
    # Get page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables: bs4.ResultSet = soup.findAll(attrs={'class': 'wikitable hover'})
    melody_table = ([table for table in tables if 'horn melodies' in table.find(
        'th').text.lower()] or [None])[0]
    if not melody_table:
        raise LookupError('Couldn\'t find melodies table')
    # go through rows
    for row in melody_table.findAll('tr', recursive=False):
        if isinstance(row, (bs4.NavigableString, str)):
            continue
        cols = [td for td in row.findAll('td', recursive=False)]
        if len(cols) == 0:
            continue
        if 'rowspan' in cols[0].attrs.keys():
            cols = cols[1:]

        notes = [n for n in cols[0].findAll('a', recursive=False)]
        note_names = [n.attrs['title'].strip() for n in notes]
        if '-'.join(note_names) in data['melodies']:
            continue

        # save note img links
        if 'note_img_urls' not in data:
            data['note_img_urls'] = {}
        for i, name in enumerate(note_names):
            if name in data['note_img_urls']:
                continue
            img = notes[i]
            data['note_img_urls'][name] = img.attrs['href']

        effects = [c.text.strip()
                   for c in cols[1:3] if c.text.strip() not in ('?', 'N/A')]
        duration = cols[3].text.strip()
        if duration not in ('?', 'N/A'):
            duration = None
        extension = cols[4].text.strip()
        if extension not in ('?', 'N/A'):
            extension = None
        data['melodies']['-'.join(note_names)] = {
            'effects': effects, 'duration': duration, 'extension': extension,'melody':'-'.join(note_names)}

    return data
