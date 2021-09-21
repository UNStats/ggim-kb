####################################
# Extract list of documents
####################################

import utils
import json
import requests
from bs4 import BeautifulSoup
import markdownify


def parse_tables(x):
    x['links'] = []
    tables = x['html_tables']
    for t in tables:
        soup = BeautifulSoup(open('html_tables/' + t + '.html', encoding="utf8"), "html.parser") 
        links = []
        for a in soup.find_all("a", class_="primary"):
            d = dict()
            d['url'] = a['href']
            if a.has_attr('title'):
                d['title'] = a['title'].strip()
            else:
                d['title']= None
            d['label'] = a.text.replace('\n',' ').replace('  ', ' ').strip()
            d['file'] = parse_doc_page(d['url'] )
            links.append(d)
        x['links'].extend(links)

def parse_webpage(x):
    x['url'] = 'http://ggim.un.org/knowledgebase/KnowledgebaseCategory'+x['url']+'.aspx'
    page = requests.get(x['url'])
    soup = BeautifulSoup(page.content, "html.parser")
    x['title'] =  soup.find("head").title.text.strip()
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
    related_links = soup.find_all("a", id="ctl00_ctlContentPlaceHolder_ctl00_ctl00_ctl00_ctl00_ctlPanelBar_ctlViewArticleRelatedLinks_ctl00_ctlDataList_ctl00_hypRelatedLink2")
    document['related_links'] = []

    for rl in related_links:
        d = dict()
        d['url'] = rl['href']
        d['label'] = rl.text
        document['related_links'].append(d)

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
    
for index_file in ['global', 'regional', 'national']:

    index = utils.open_json('master_data/index_'+index_file+'.json')

    # print(index[0].keys())

    index_links = []

    for i_0 in index:    
        parse_webpage(i_0)
        parse_tables(i_0)

        for idx_1, i_1 in enumerate(i_0['children']):

            # if idx_1 != 0:
            #     continue

            parse_webpage(i_1)
            
            parse_tables(i_1)
                
            for idx_2, i_2 in enumerate(i_1['children']):
                
                # if idx_2 != 0:
                #     continue

                parse_webpage(i_2)
                
                parse_tables(i_2)

                for i_3 in i_2['children']:
                    parse_webpage(i_3)
                    
                    parse_tables(i_3)

                    for i_4 in i_3['children']:
                        parse_webpage(i_4)
                        
                        parse_tables(i_4)
                        
                        i_4.pop('html_tables')

                    i_3.pop('html_tables')
                
                i_2.pop('html_tables')

            i_1.pop('html_tables')

    with open('output/index_links_'+index_file+'.json', 'w') as fout:
        json.dump(index, fout,  indent=4)    

