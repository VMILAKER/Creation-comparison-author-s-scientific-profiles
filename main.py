import json
import os
import pandas as pd
from Utilities import open_file, save_file, check_folder
import pprint


def find_jinr(folderpath: str):
    list_of_authors_id = []
    for item_authors in os.listdir(os.path.join(folderpath, 'authors')):
        data_authors = open_file(
            folderpath, os.path.join('authors', item_authors))
        if not data_authors['author_uuid'] in list_of_authors_id:
            list_of_authors_id.append(data_authors['author_uuid'])

    for item_publications in os.listdir(os.path.join(folderpath, 'publications')):
        data_publications = open_file(
            folderpath,  os.path.join('publications', item_publications))
        keys = ['title', 'published', 'authors']
        d = {}
        l = []
        for i in data_publications["authors"]:
            if i['author_uuid'] in list_of_authors_id:
                l.append({'name': i['name'], 'author_uuid': i['author_uuid']})
        check_folder('Authors_JINR')
        c = d.fromkeys(keys, None)
        d.update(title=data_publications['title'],
                 published=data_publications['published'], authors=l)
        save_file(d, 'Authors_JINR', item_publications)


def cas(x):
    if len(x) < 8:
        return '0' + x
    else:
        return x


def match_scimago():
    sci_csv = r'scimagojr 2023.csv'
    df = pd.read_csv(sci_csv, sep=';')
    df['Issn'] = df['Issn'].apply(cas)
    for i in os.listdir('Authors'):
        data = open_file('Authors', i)
        df_1 = df[(df['Issn'].str.contains(
            data['published']['journal']['ISSN']))]
        if not df_1.empty:
            data.update(
                {'Quartile': list(df_1['SJR Best Quartile'])[0], 'Categories': list(df_1['Categories'])})
            save_file(data, 'Authors', i)


def numero():
    l = []
    author_list = []
    nk = []
    for i in os.listdir('Authors_JINR_1'):
        data = open_file('Authors_JINR_1', i)
        nn = []
        local_author = []
        for authors in data['authors']:
            if not authors['author_uuid'] in local_author:
                local_author.append(authors['author_uuid'])
            if authors['author_uuid'] not in author_list:
                d = dict.fromkeys(['author_uuid', 'Connected'], [])
                # dd = dict.fromkeys(['author_uuid', 'common'], 0)

                author_list.append(authors['author_uuid'])
                d.update(author_uuid=authors['author_uuid'])
                # d['Connected'].append(dd)
                l.append(d)
        nk.append(local_author)
    for item in l:
        for z in nk:
            # if len(z) == 1:
            #     pass
            if item['author_uuid'] in z:
                z = [gol for gol in z if gol != item['author_uuid']]
                for n in z:
                    if not item['Connected']:
                        item['Connected'].append(
                            {f'author_uuid': n, 'common': 1})
                    else:
                        es = [hi['author_uuid'] for hi in item['Connected']]
                        for j in item['Connected']:
                            if not n in es:
                                item['Connected'].append(
                                    {f'author_uuid': n, 'common': 1})
                                break
                            elif n == j['author_uuid']:
                                j['common'] += 1
    with open('Output_1.json', 'w', encoding='utf-8') as f:
        json.dump(l, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # find_jinr('JINR_data')
    # match_scimago()
    # numero()
    n = []
    for i in os.listdir('Authors_JINR_1'):
        data = open_file('Authors_JINR_1', i)
        for at in data['authors']:
            if at['author_uuid'] == "c87115cd-4fa9-4912-af9f-dad253f73d3f":
                n.append(i)
    print(n, len(n))
