####################################
# Extract list of documents
####################################

import utils
import json
import requests
from bs4 import BeautifulSoup
import markdownify

index = utils.open_json('master_data/index.json')

# print(index[0].keys())

index_links = []

def parse_table(x):
    soup = BeautifulSoup(open('html_tables/' + x['htmlTable'] + '.html', encoding="utf8"), "html.parser") 

    page = requests.get('http://ggim.un.org/knowledgebase/KnowledgebaseCategory'+x['url']+'.aspx')
    soup2 = BeautifulSoup(page.content, "html.parser")

    x['title'] =  soup2.find("head").title.text.strip()
    x['links'] = []
    for a in soup.find_all("a", class_="primary"):
        d = dict()
        d['url'] = a['href']
        if a.has_attr('title'):
            d['title'] = a['title'].strip()
        else:
            d['title']= None
        d['label'] = a.text.replace('\n',' ').replace('  ', ' ').strip()
        d['file'] = parse_doc_page(d['url'] )
        x['links'].append(d)

def parse_webpage(x):
    page = requests.get('http://ggim.un.org/knowledgebase/KnowledgebaseCategory'+x['url']+'.aspx')
    soup = BeautifulSoup(page.content, "html.parser")
    description = soup.find("span", id="ctl00_ctlContentPlaceHolder_ctl00_ctl00_ctl00_ctl00_lblCategoryDesc")
    if description:
        x['blurb'] = description.text
    else:
        x['blurb'] = None


def parse_doc_page(url):
    print(url)
    document = dict()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    doc_title = soup.find("h1")
    a = soup.find("a", id="ctl00_ctlContentPlaceHolder_ctl00_ctl00_ctl00_ctl00_ctlPanelBar_ctlViewArticleAttachments_ctl00_ctlViewAttachments_ctl00_ctlDataList_ctl00_hypAttachment")
    article = soup.find("div", class_="i-row ikb-article")
    doc_info = soup.find("div", id="ctlDataList")
    r = doc_info.find_all("div", class_="row")

    document['title'] = doc_title.text

    if a:
        document['file_url'] = a['href']
        document['file_name'] = a.text
    else:
        document['file_url'] = None
        document['file_name'] = None    

    if article:
        article_md = markdownify.markdownify(str(article), heading_style="ATX").strip()
        document['article'] = article_md
    else:
        document['article'] = None

    document['dateModified'] = r[0].span.find_all('span', recursive=False)[1]['title']
    document['modifiedBy'] = r[1].span.find_all('span', recursive=False)[1].text
    document['type'] = r[2].span.find_all('span', recursive=False)[1].text 

    return document
    

for i_0 in index:    
    if i_0['htmlTable']:
        parse_webpage(i_0)
        parse_table(i_0)
        print(i_0['htmlTable'])
    for idx_1, i_1 in enumerate(i_0['children']):

        # if idx_1 != 0:
        #     continue

        if i_1['htmlTable']:
            parse_webpage(i_1)
            parse_table(i_1)
            print(i_1['htmlTable'])
            
        for idx_2, i_2 in enumerate(i_1['children']):
            
            # if idx_2 != 0:
            #     continue

            if i_2['htmlTable']:
                parse_webpage(i_2)
                parse_table(i_2)
                print(i_2['htmlTable'])

            for i_3 in i_2['children']:
                if i_3['htmlTable']:
                    parse_webpage(i_3)
                    parse_table(i_3)
                    print(i_3['htmlTable'])



with open('master_data/index_links.json', 'w') as fout:
    json.dump(index, fout,  indent=4)    

