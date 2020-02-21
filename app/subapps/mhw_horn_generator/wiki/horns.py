import requests
from bs4 import BeautifulSoup
import bs4
import json
import datetime
import re
DEFAULT_HORN_URL = r'https://monsterhunter.fandom.com/wiki/MHWI:_Hunting_Horn_Weapon_Tree'
BASE_URL = r'https://monsterhunter.fandom.com'


def get_horns(url: str = DEFAULT_HORN_URL):
    """
    Get hunting horn info from weapon tree page
    """

    timefmt = '%m-%d-%Y:%H:%M:%S'
    data = {'horns': {}}
    currtime = datetime.datetime.now()
    data['parse_time'] = currtime.strftime(timefmt)
    # Get page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables: bs4.ResultSet = soup.findAll(attrs={'class': 'wikitable hover'})
    horn_table = ([table for table in tables if 'horn path' in table.find(
        'th').text.lower()] or [None])[0]
    if not horn_table:
        raise LookupError('Couldn\'t find horns table')

    # iterate through rows
    curr_tree = ''
    for row in horn_table.findAll('tr', recursive=False):
        if isinstance(row, (bs4.NavigableString, str)):
            continue

        # if a path header
        th = row.find('th', recursive=False)
        if th and 'path' in th.text.lower():
            curr_tree = th.text.replace('Path', '').strip()
            continue

        # if a horn info row
        cols = row.findAll('td', recursive=False)
        if not cols:
            continue
        # get info
        horn_name = cols[0].findAll('a')[-1].text.strip()
        horn_data = {}
        horn_data['name']=horn_name
        horn_data['tree']=curr_tree
        horn_data['horn_url']=(BASE_URL+cols[0].findAll('a')[-1].attrs['href']) if 'href' in cols[0].findAll('a')[-1].attrs else None
        horn_data['attack'] = cols[1].text.strip()
        if cols[2].text.strip() == 'N/A':
            horn_data['element'] = None
        else:
            horn_data['element'] = cols[2].text.strip(
            )+' '+cols[2].find('a').attrs['title'].strip()
        horn_data['sharpness'] = cols[3].text.strip()
        horn_data['slots'] = list(cols[4].text.strip().replace('-', ''))
        if not horn_data['slots']:
            horn_data['slots'] = None
        horn_data['affinity'] = cols[5].text.strip()
        if cols[6].text.strip() == 'N/A':
            horn_data['misc'] = None
        else:
            horn_data['misc'] = cols[6].text.strip()

        # notes
        notes = [n for n in cols[7].findAll(
            'a', recursive=False)]  # echo is a workaround
        note_names = [n.find('img').attrs['alt'].split('.')[1].title().strip() for n in notes]+['Echo']
        #get note img urls
        if 'note_img_urls' not in data:
            # echo is a workaround
            data['note_img_urls'] = {
                'Echo': r'https://vignette.wikia.nocookie.net/monsterhunter/images/2/2d/MHWI-Note_Echo.png/revision/latest?cb=20190918182007'}
        for i, name in enumerate(note_names):
            if name in data['note_img_urls']:
                continue
            img = notes[i]
            data['note_img_urls'][name] = img.attrs['href']
        
        horn_data['notes']='-'.join(note_names)
        data['horns'][horn_name]=horn_data
    return data


# def request_horn_info(url: str):
#     """
#     Get info from horn link and compile into dict
#     """
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     base_url = url[::-1].split('/', 1)[-1][::-1]
#     data = {}

#     data_table: bs4.PageElement = soup.find('table', {'class': 'wiki_table'})
#     # go through rows of table
#     row_gen = (t for t in data_table.findChild(
#         'tbody').findChildren('tr', recursive=False))
#     # name
#     row = next(row_gen)
#     data['name'] = row.findChild('h2').text
#     # img
#     row = next(row_gen)
#     data['img_url'] = base_url+(row.findChild('img').attrs['src'])
#     # rarity
#     row = next(row_gen)
#     data['rarity'] = row.findChild('div').text.split()[-1]
#     # decorations
#     row = next(row_gen)
#     data['decorations'] = [base_url+d.attrs['src']
#                            for d in row.findChildren('img') if 'gem' in d.attrs['src']]
#     # damage
#     row = next(row_gen)
#     data['attack'] = row.findChildren('td')[-1].text
#     # sharpness
#     row = next(row_gen)
#     data['sharpness'] = [s.attrs['style'].split(
#         ':')[-1][1:-1] for s in row.findChildren('div', {'class': 'progress-bar'})]
#     # affinity
#     row = next(row_gen)
#     data['affinity'] = row.findChildren('td')[-1].text
#     # element
#     row = next(row_gen)
#     el_child = row.findChildren('td')[-1]
#     # try to get element from text, otherwise icon
#     el_type = ''
#     el_num = ''
#     if len(el_child.text.split()) > 1:
#         el_type, el_num = el_child.text.split()
#     else:
#         el_num = el_child.text
#         el_type = el_child.findChild('img').attrs['src'].split(
#             '/')[-1].replace('mhw-', '').split('-')[0]

#     # dragonseal

#     data['element'] = f'{el_type} {el_num}'
#     row = next(row_gen)
#     if 'elderseal' in row.findChild('img').attrs['title']:
#         data['elderseal'] = row.findChildren('td')[-1].text
#     else:
#         data['elderseal'] = None

#     return data


# horns = get_horns()
# json.dump(horns, open('horns.json', 'w'), indent=4,
#           separators=(',', ':'), sort_keys=True)
