import requests
from bs4 import BeautifulSoup
import bs4
import json
import datetime
import re
from functools import lru_cache


def get_horns(url:str=r'https://monsterhunterworld.wiki.fextralife.com/Hunting+Horn+Weapon+Tree'):
    """
    Get hunting horn info from weapon tree page
    """

    timefmt='%m-%d-%Y:%H:%M:%S'
    data={'horns':{}}
    currtime=datetime.datetime.now()
    data['parse_time']=currtime.strftime(timefmt)
    #Get page
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    trees:bs4.ResultSet=[t for t in soup.findAll(name='div') if ('id' in t.attrs and 'embedded' in t.attrs['id'])]
    for tree in trees:
        for horn in tree.findChildren(name='li'):
            horn_link=horn.findChild(attrs={'class':'wiki_link'},recursive=False)

            link=r'https://monsterhunterworld.wiki.fextralife.com'+horn_link.attrs['href']
            name=horn_link.text
            data['horns'][name]={'horn_link':link,'name':name}
            #get notes
            note_nums=[]
            notes=horn.findChildren(name='img',recursive=False)
            for note in notes:
                src=''
                num=''         
                if 'data-src' in note.attrs and 'note' in note.attrs['data-src']:
                    src=note.attrs['data-src']
                    num=note.attrs['data-src'].split('mhw-note')[1].replace('-icon.png','')
                elif 'note' in note.attrs['src']:
                    src=note.attrs['src']
                    num=note.attrs['src'].split('mhw-note')[1].replace('-icon.png','')
                if num:
                    note_nums.append(num)
                    if 'note_icon_url' not in data:
                            data['note_icon_url']=url.replace(r'/Hunting+Horn+Weapon+Tree','')+src.replace(num,'{0}')

            data['horns'][name]['notes']=note_nums            


                #print(f'{name}: {link}')

    return data

@lru_cache()
def request_horn_info(url:str):
    """
    Get info from horn link and compile into dict
    """
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    base_url=url[::-1].split('/',1)[-1][::-1]
    data={}


    data_table:bs4.PageElement=soup.find('table',{'class':'wiki_table'})
    #go through rows of table
    row_gen=(t for t in data_table.findChild('tbody').findChildren('tr',recursive=False))
    #name
    row=next(row_gen)
    data['name']=row.findChild('h2').text
    #img
    row=next(row_gen)
    data['img_url']=base_url+(row.findChild('img').attrs['src'])
    #rarity
    row=next(row_gen)
    data['rarity']=row.findChild('div').text.split()[-1]
    #decorations
    row=next(row_gen)
    data['decorations']=[base_url+d.attrs['src'] for d in row.findChildren('img') if 'gem' in d.attrs['src']]
    #damage
    row=next(row_gen)
    data['attack']=row.findChildren('td')[-1].text
    #sharpness
    row=next(row_gen)
    data['sharpness']=[s.attrs['style'].split(':')[-1][1:-1] for s in row.findChildren('div',{'class':'progress-bar'}) ]
    #affinity
    row=next(row_gen)
    data['affinity']=row.findChildren('td')[-1].text
    #element
    row=next(row_gen)
    el_child=row.findChildren('td')[-1]
    #try to get element from text, otherwise icon
    el_type=''
    el_num=''
    if len(el_child.text.split())>1:
        el_type,el_num=el_child.text.split()
    else:
        el_num=el_child.text
        el_type=el_child.findChild('img').attrs['src'].split('/')[-1].replace('mhw-','').split('-')[0]
    
    #dragonseal

    data['element']=f'{el_type} {el_num}'
    row=next(row_gen)
    if 'elderseal' in row.findChild('img').attrs['title']:
            data['elderseal']=row.findChildren('td')[-1].text
    else:
        data['elderseal']=None


    return data