###  Flatten json

import utils
import urllib.request


def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open('docs/'+filename, 'wb')
    file.write(response.read())
    file.close()

def get_node_details(node, breadcrumbs):
    d = dict()
    d['parent'] = 'http://ggim.un.org/knowledgebase/KnowledgebaseCategory'+node['parent']+'.aspx'
    d['category_url'] = node['url']
    d['hasChildren'] = node['hasChildren']
    d['breadcrumbs'] = breadcrumbs + ' >> ' + node['title']
    d['category_title'] = node['title']
    d['category_blurb'] = node['blurb']
    return d

def get_node_articles(node, level):
    node_articles = []
    for idx, i in enumerate(node['links']):
        d = dict()
        d['level'] = level
        d['category_url'] = node['url']
        d['category_title'] = node['title']
        d['article_no'] = idx
        d['article_url'] = i['url']
        d['article_title'] = i['title']
        d['article_label'] = i['label']
        d['article_desc'] = i['file']['article']
        if len(i['file']['related_links'])>0:
            d['article_weblink_url'] = i['file']['related_links'][0]['url']
            d['article_weblink_label'] = i['file']['related_links'][0]['label']
        else:
            d['article_weblink_url'] = None
            d['article_weblink_label'] = None
        d['article_file_url'] = i['file']['file_url']
        d['article_file_title'] = i['file']['file_name']
        if d['article_file_url']:
            download_file(d['article_file_url'], d['article_file_title'])
        d['article_dateModified'] = i['file']['dateModified']
        d['article_modifiedBy'] = i['file']['modifiedBy']
        d['article_type'] = i['file']['type']
        node_articles.append(d)
    return node_articles


for index_file in ['global', 'regional', 'national']:

    index = utils.open_json('output/index_links_'+index_file+'.json')

    print(f"{index[0].keys()=}")

    categories_list = []

    for idx_1, i_1 in enumerate(index):
        d1 = get_node_details(i_1, '')
        categories_list.append(d1)

        for idx_2, i_2 in enumerate(i_1['children']):
            d2 = get_node_details(i_2, d1['breadcrumbs'])
            categories_list.append(d2)

            for idx_3, i_3 in enumerate(i_2['children']):
                d3 = get_node_details(i_3, d2['breadcrumbs'])
                categories_list.append(d3)

                for idx_4, i_4 in enumerate(i_3['children']):
                    d4 = get_node_details(i_4, d3['breadcrumbs'])
                    categories_list.append(d4)

    utils.dictList2tsv(categories_list, 'output/categories_'+index_file+'.txt')

    article_list = []

    for idx, i_1 in enumerate(index):
        article_list.extend(get_node_articles(i_1, 1))

        for idx_2, i_2 in enumerate(i_1['children']):
            article_list.extend(get_node_articles(i_2, 2))

            for idx_3, i_3 in enumerate(i_2['children']):
                article_list.extend(get_node_articles(i_3, 3))

                for idx_4, i_4 in enumerate(i_3['children']):
                    article_list.extend(get_node_articles(i_4, 4))


    utils.dictList2tsv(article_list, 'output/articles_'+index_file+'.txt')
    