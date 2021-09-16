####################################
# Extract list of documents
####################################

import utils
import json
import requests
from bs4 import BeautifulSoup

index = utils.open_json('master_data/index.json')

# print(index[0].keys())

index_links = []

def parse_table(x):
    soup = BeautifulSoup(open('html_tables/' + x['htmlTable'] + '.html', encoding="utf8"), "html.parser") 
    x['links'] = []
    for a in soup.find_all("a", class_="primary"):
        d = dict()
        d['url'] = a['href']
        if a.has_attr('title'):
            d['title'] = a['title'].strip()
        else:
            d['title']= None
        d['label'] = a.text.replace('\n',' ').replace('  ', ' ').strip()
        x['links'].append(d)

def parse_webpage(x):
    page = requests.get('http://ggim.un.org/knowledgebase/KnowledgebaseCategory'+x['url']+'.aspx')
    soup = BeautifulSoup(page.content, "html.parser")
    description = soup.find("span", id="ctl00_ctlContentPlaceHolder_ctl00_ctl00_ctl00_ctl00_lblCategoryDesc")
    print(f"{description=}")
    if description:
        x['blurb'] = description.text
    else:
        x['blurb'] = None

for i_0 in index:    
    if i_0['htmlTable']:
        parse_webpage(i_0)
        parse_table(i_0)
    for i_1 in i_0['children']:
        if i_1['htmlTable']:
            parse_webpage(i_1)
            parse_table(i_1)
        for i_2 in i_1['children']:
            if i_2['htmlTable']:
                parse_webpage(i_2)
                parse_table(i_2)
            for i_3 in i_2['children']:
                if i_3['htmlTable']:
                    parse_webpage(i_3)
                    parse_table(i_3)



with open('master_data/index_links.json', 'w') as fout:
    json.dump(index, fout,  indent=4)    

