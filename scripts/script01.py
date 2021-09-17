################################
# Create index in json format
################################

import utils
import json
import copy 

index_flat = utils.tsv2dictlist('master_data/index.txt')

root_url = '11'

def get_children(x):
    if x['hasChildren']:
        x['children'] = utils.unique_dicts(
                            utils.select_dict(
                                utils.subdict_list(
                                    index_flat,
                                    ['page','htmlTable'], 
                                    exclude=True
                                ), 
                                {'parent': x['url']}
                            )
                        )

def get_htmlTables(x):
    html_tables = utils.select_dict(
        utils.subdict_list(
            index_flat,
            ['url', 'htmlTable']
        ),
        {'url': x['url']}
    )

    html_tables_list = []
    for h in html_tables:
        html_tables_list.append(h['htmlTable'])

    x['html_tables'] = html_tables_list

level_0 = utils.unique_dicts(
            utils.select_dict(
                utils.subdict_list(
                    index_flat,
                    ['page','htmlTable'], 
                    exclude=True
                ),
                {'url': root_url}
            )   
        )

for i_1 in level_0:
    get_htmlTables(i_1)
    get_children(i_1)
    
    if 'children' in i_1.keys():
        for i_2 in i_1['children']:
            get_htmlTables(i_2)
            get_children(i_2)
            
            if 'children' in i_2.keys():
                for i_3 in i_2['children']:
                    get_htmlTables(i_3)
                    get_children(i_3)
                    
                    if 'children' in i_3.keys():
                        for i_4 in i_3['children']:
                            get_htmlTables(i_4)
                            get_children(i_4)
                            
                            if 'children' in i_4.keys():
                                for i_5 in i_4['children']:
                                    get_htmlTables(i_5)
                                    get_children(i_5)

# print(level_0)


with open('master_data/index.json', 'w') as fout:
    json.dump(level_0, fout,  indent=4)    


