##############################
# Order
##############################

import utils
import json

data = utils.open_json('master_data/index_links.json')

print(data[0].keys())

print(data[0]['links'][0].keys())

print(data[0]['links'][0]['file'].keys())

category_keys = ['parent', 'url', 'title','blurb', 'Multipage', 'hasChildren']

for i in data:
    category = dict()
    for k in category_keys:
        if k == 'url':
            category[k] = 'http://ggim.un.org/knowledgebase/KnowledgebaseCategory'+i[k]+'.aspx'
        else:
            category[k] = i[k]
    print(category)
        
