import json
import os
import re

import pandas as pd
from joblib import Memory

from Utilities import check_folder, open_file, save_file
cachedir = 'Cache_main'
memory = Memory(cachedir, verbose=0)


def find_jinr(folderpath: str) -> json:
    list_of_authors_id = []
    check_folder('Authors_JINR_0')
    for item_authors in os.listdir(os.path.join(folderpath, 'authors')):
        data_authors = open_file(
            folderpath, os.path.join('authors', item_authors))
        authors_dict = dict.fromkeys(['author_uuid', 'ORCID', 'ScopusID'], 0)
        authors_dict.update(
            author_uuid=data_authors['author_uuid'], ORCID=data_authors['ids']['ORCID'], ScopusID=data_authors['ids']['Scopus'])
        list_of_authors_id.append(authors_dict)

    for item_publications in os.listdir(os.path.join(folderpath, 'publications')):
        data_publications = open_file(
            folderpath,  os.path.join('publications', item_publications))
        keys = ['title', 'published', 'authors', 'number_authors', 'ScopusID']
        d = {}
        l = []
        for keys in data_publications['published'].keys():
            if not data_publications['published'][keys]:
                data_publications['published'][keys] = None

        for i in data_publications["authors"]:
            for j in list_of_authors_id:
                if i['author_uuid'] == j['author_uuid']:
                    print(j['author_uuid'])
                    l.append({'name': i['name'], 'author_uuid': j['author_uuid'],
                             'ORCID': j['ORCID'], 'ScopusID': j['ScopusID']})
        c = d.fromkeys(keys, None)
        d.update(title=data_publications['title'], published=data_publications['published'], authors=l, number_authors=len(
            data_publications['authors']) + len(data_publications['authors_external']))
        save_file(d, 'Authors_JINR_0', item_publications)


def cas(x):
    if len(x) < 8:
        return '0' + x
    else:
        return x


class Match_SCIMAGO_data:
    def __init__(self, sci_csv: str, path_to_folder: str, path_check_folder: str):
        self.sci = sci_csv
        self.data_folder = path_to_folder
        self.check = path_check_folder

    def match_scimago(self) -> json:
        df = pd.read_csv(self.sci, sep=';')
        df['Issn'] = df['Issn'].apply(cas)
        check_folder(self.check)

        for i in os.listdir(self.data_folder):
            data = open_file(self.data_folder, i)
            if data['published']['journal']['ISSN']:
                df_1 = df[(df['Issn'].str.contains(
                    data['published']['journal']['ISSN']))]
                if not df_1.empty:
                    data.update(
                        {'quartile': list(df_1['SJR Best Quartile'])[0], 'Categories': str(list(df_1['Categories'])).replace("['", '').replace("']", '')})
                    save_file(data, self.check, i)
                else:
                    data.update(
                        {'quartile': None, 'Categories': None})
                    save_file(data, self.check, i)
            else:
                data.update(
                    {'quartile': None, 'Categories': None})
                save_file(data, self.check, i)
            print(i)


def conto(path_to_folder) -> None:
    l = []
    uuid_list = []
    data_cat = []
    quartile_dict = {'Q1': 4, 'Q2': 3, 'Q3': 2, 'Q4': 1}
    for i in os.listdir(path_to_folder):
        data = open_file(path_to_folder, i)
        pattern = r"\((Q\d+)\)"
        if data['Categories']:
            data['Categories'] = [re.sub(pattern, '', io).strip()
                                  for io in data['Categories'].split(';')]
            if data['quartile'] and data['quartile'] != '-':
                for j in range(len(data['authors'])):
                    keyss = ['author_uuid']
                    d = {}
                    k = {}

                    d = dict.fromkeys(keyss, 0)
                    k = dict.fromkeys(data['Categories'], 0)
                    if not data['authors'][j]['author_uuid'] in uuid_list:
                        d.update({'author_name': data['authors'][j]['name'], 'author_uuid': data['authors'][j]
                                 ['author_uuid'], 'ORCID': data['authors'][j]['ORCID'], 'ScopusID': data['authors'][j]['ScopusID']})
                        for numero in data['Categories']:
                            if data['number_authors'] < 20:
                                # d.update({'categories':quartile_dict[data['quartile']]*(1/(j+1))})
                                k[numero] += quartile_dict[data['quartile']] * \
                                    (1/(j+1))
                                d['Categories'] = k
                            else:
                                # d.update({'count':quartile_dict[data['quartile']]*(1/(data['number_authors']))})
                                k[numero] += quartile_dict[data['quartile']] * \
                                    (1/(data['number_authors']))
                                d['Categories'] = k
                            uuid_list.append(data['authors'][j]['author_uuid'])
                        l.append(d)
                    else:
                        for item in l:
                            nn = item['Categories']
                            if data['authors'][j]['author_uuid'] in item['author_uuid']:
                                for numeri in list(nn):
                                    for z in data['Categories']:
                                        if z == numeri:
                                            if data['number_authors'] < 20:
                                                nn[numeri] += quartile_dict[data['quartile']
                                                                            ]*(1/(j+1))
                                            else:
                                                nn[numeri] += quartile_dict[data['quartile']
                                                                            ]*(1/(data['number_authors']))
                                        else:
                                            nn.update({z: 0})
                                            if data['number_authors'] < 20:
                                                nn[z] += quartile_dict[data['quartile']
                                                                       ]*(1/(j+1))
                                            else:
                                                nn[z] += quartile_dict[data['quartile']
                                                                       ]*(1/(data['number_authors']))
                            item['Categories'] = nn
    save_file(l, '', 'gol_0_2.json')

# @memory.cache


def norma():
    data = open_file('', 'gol.json')
    l = []
    for i in data:
        for keys in i['Categories'].keys():
            if not keys in l:
                l.append(keys)

    max_min_dict = dict.fromkeys(l, 0)
    dd = dict.fromkeys(l, 0)
    for item in data:
        for keyss in item['Categories'].keys():
            if item['Categories'][keyss] > max_min_dict[keyss]:
                max_min_dict[keyss] = item['Categories'][keyss]
            # elif d[keyss] > item['Categories'][keyss]:
            dd[keyss] += 1

    dd = dict(list(sorted(dd.items(), key=lambda x: x[1], reverse=True))[:5])
    d = dict(sorted(max_min_dict.items(), key=lambda x: x[1], reverse=True))
    for kq in list(d):
        if not kq in dd.keys():
            del d[kq]

    for it in data:
        nn = it['Categories']
        z = dict.fromkeys(d.keys(), 0)
        for ke in list(nn):
            if ke in d.keys():
                z[ke] = (nn[ke])/(d[ke])

        it['Categories'] = z
        for q in z.keys():
            if z[q] > 1:
                print(it)
    save_file(data, '', 'gol_0_2.json')
    return d


def numero():
    l = []
    author_list = []
    nk = []
    for i in os.listdir('Authors_1'):
        data = open_file('Authors_1', i)
        local_author = []
        for authors in data['authors']:
            if not authors['author_uuid'] in local_author:
                local_author.append(
                    [authors['author_uuid'], authors['ScopusID'], authors['ORCID']])
            if authors['author_uuid'] not in author_list:
                d = dict.fromkeys(
                    ['author_uuid', 'ScopusID', 'ORCID', 'Connected'], [])

                author_list.append(authors['author_uuid'])
                d.update(author_uuid=authors['author_uuid'],
                         ScopusID=authors['ScopusID'], ORCID=authors['ORCID'])
                l.append(d)
        nk.append(local_author)

    for item in l:
        for z in nk:
            # if len(z) == 1:
            #     pass
            ze = [gol[0] for gol in z]
            if item['author_uuid'] in ze:
                zk = [goll for goll in z if goll[0] != item['author_uuid']]
                for n in zk:
                    if not item['Connected']:
                        item['Connected'].append(
                            {f'author_uuid': n[0], 'ScopusID': n[1], 'ORCID': n[2], 'common': 1})
                    else:
                        es = [hi['author_uuid'] for hi in item['Connected']]
                        for j in item['Connected']:
                            if not n[0] in es:
                                item['Connected'].append(
                                    {f'author_uuid': n[0],  'ScopusID': n[1], 'ORCID': n[2], 'common': 1})
                                break
                            elif n[0] == j['author_uuid']:
                                j['common'] += 1
        # item['Connected'] = list(sorted([dy[dy in item['Connected']], lambda x: x[1], reverse = True))
    # with open('Output_2.json', 'w', encoding='utf-8') as f:
    #     json.dump(l, f, indent=2, ensure_ascii=False)
    save_file(l, '', 'Output_2.json')


def add_new(path_to_folder_new):
    old_one = main()
    find_jinr(path_to_folder_new)
    cl = Match_SCIMAGO_data(r'scimagojr 2023.csv',
                            'Authors_JINR_0', path_to_folder_new)
    cl.match_scimago()
    conto(path_to_folder_new)


@memory.cache
def main():
    PATH_TO_FOLDER = 'Authors_2'
    find_jinr('JINR_data')
    cl = Match_SCIMAGO_data(r'scimagojr 2023.csv',
                            'Authors_JINR', PATH_TO_FOLDER)
    cl.match_scimago()
    conto(PATH_TO_FOLDER)
    max_list = norma()
    data = open_file('gol_0_2.json')


if __name__ == '__main__':
    # find_jinr('JINR_data')
    # # match_scimago()
    # conto()
    # norma()
    # list_of_authors_id = []
    # for item_authors in os.listdir(os.path.join('JINR_data', 'authors')):
    #     data_authors = open_file('JINR_data', os.path.join('authors', item_authors))
    #     if not data_authors['author_uuid'] in list_of_authors_id:
    #         list_of_authors_id.append(data_authors['author_uuid'])
    # print(list_of_authors_id, len(list_of_authors_id))
    # l = []
    # for i in os.listdir('Authors'):
    #     data = open_file('Authors', i)
    #     for j in data['authors']:
    #         if j['author_uuid'] == "15342f96-558c-4891-a3b7-9ac301d11251":
    #             l.append(i)
    # print(set(l))
    # {'Nuclear and High Energy Physics': 42.0, 'Physics and Astronomy (miscellaneous)': 14.0, 'Software': 12.0, 'Engineering (miscellaneous)': 8.0, 'Mathematical Physics': 8.0}
    # data = open_file('', 'gol_4.json')
    # for i in data:
    #     if i['ORCID']:
    #         print(i['ScopusID'])
    # numero()
    # n = []
    # for i in os.listdir('Authors_1'):
    #     data = open_file('Authors_1', i)
    #     for at in data['authors']:
    #         if at['author_uuid'] == "c87115cd-4fa9-4912-af9f-dad253f73d3f":
    #             n.append(i)
    # print(n, len(n))
    add_new('JINR_data/publications_test')
