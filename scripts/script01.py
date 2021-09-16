################################
# Create index in json format
################################

import utils
import json

index_flat = utils.tsv2dictlist('master_data/index.txt')

root_url = '11'

def get_children(x):
    if x['hasChildren']:
        x['children'] = utils.select_dict(index_flat, {'parent': x['url']})


level_0 = utils.select_dict(index_flat, {'url': root_url})

for i_1 in level_0:
    get_children(i_1)

    if 'children' in i_1.keys():
        for i_2 in i_1['children']:
            get_children(i_2)
            
            if 'children' in i_2.keys():
                for i_3 in i_2['children']:
                    get_children(i_3)
                    
                    if 'children' in i_3.keys():
                        for i_4 in i_3['children']:
                            get_children(i_4)
                            
                            if 'children' in i_4.keys():
                                for i_5 in i_4['children']:
                                    get_children(i_5)

print(level_0)


with open('master_data/index.json', 'w') as fout:
    json.dump(level_0, fout,  indent=4)    


