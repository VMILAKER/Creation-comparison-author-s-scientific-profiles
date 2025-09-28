import json
import os
import re
import time
import pandas as pd
from functools import lru_cache
from Utilities import check_folder, open_file, save_file


def find_jinr(folderpath: str) -> json:
    list_of_authors_id = []
    for item_authors in os.listdir(os.path.join('JINR_data', 'authors')):
        data_authors = open_file(
            'JINR_data', os.path.join('authors', item_authors))
        authors_dict = dict.fromkeys(
            ['author_uuid', 'ORCID', 'ScopusID'], 0)
        authors_dict.update(
            author_uuid=data_authors['author_uuid'], ORCID=data_authors['ids']['ORCID'], ScopusID=data_authors['ids']['Scopus'])
        list_of_authors_id.append(authors_dict)
    # if folderpath == 'JINR_data':
    #     check_folder('Only_JINR_authors')
    #     for item_publications in os.listdir(os.path.join(folderpath, 'publications')):
    #         data_publications = open_file(
    #             folderpath,  os.path.join('publications', item_publications))
    #         keys = ['title', 'published', 'authors',
    #                 'number_authors', 'ScopusID']
    #         dict_data_authors = {}
    #         list_data_authors = []
    #         for keys in data_publications['published'].keys():
    #             if not data_publications['published'][keys]:
    #                 data_publications['published'][keys] = None

    #         for i in data_publications['authors']:
    #             for j in list_of_authors_id:
    #                 if i['author_uuid'] == j['author_uuid']:
    #                     # print(j['author_uuid'])
    #                     list_data_authors.append({'name': i['name'], 'author_uuid': j['author_uuid'], 'ORCID': j['ORCID'], 'ScopusID': j['ScopusID']})
    #         dict_data_authors.update(title=data_publications['title'], published=data_publications['published'], authors=list_data_authors, number_authors=len(
    #             data_publications['authors']) + len(data_publications['authors_external']))
    #         save_file(dict_data_authors,
    #                   'Only_JINR_authors', item_publications)
    if folderpath == 'JINR_data/publications_train':
        check_folder('Only_JINR_authors')
        for item_publications in os.listdir(folderpath):
            data_publications = open_file(
                folderpath, item_publications)
            keys = ['title', 'published', 'authors',
                    'number_authors', 'ScopusID']
            dict_data_authors = {}
            list_data_authors = []
            for keys in data_publications['published'].keys():
                if not data_publications['published'][keys]:
                    data_publications['published'][keys] = None

            for i in data_publications['authors']:
                for j in list_of_authors_id:
                    if i['author_uuid'] == j['author_uuid']:
                        list_data_authors.append({'name': i['name'], 'author_uuid': j['author_uuid'],
                                                  'ORCID': j['ORCID'], 'ScopusID': j['ScopusID']})
            dict_data_authors.update(title=data_publications['title'], published=data_publications['published'], authors=list_data_authors, number_authors=len(
                data_publications['authors']) + len(data_publications['authors_external']))
            save_file(dict_data_authors,
                      'Only_JINR_authors', item_publications)
    elif folderpath == 'JINR_data/publications_test':
        check_folder('Only_JINR_authors_new')
        for item_publications in os.listdir(folderpath):
            data_publications = open_file(
                folderpath, item_publications)
            keys = ['title', 'published', 'authors',
                    'number_authors', 'ScopusID']
            dict_data_authors = {}
            list_data_authors = []
            for keys in data_publications['published'].keys():
                if not data_publications['published'][keys]:
                    data_publications['published'][keys] = None

            for i in data_publications['authors']:
                for j in list_of_authors_id:
                    if i['author_uuid'] == j['author_uuid']:
                        # print(j['author_uuid'])
                        list_data_authors.append({'name': i['name'], 'author_uuid': j['author_uuid'],
                                                  'ORCID': j['ORCID'], 'ScopusID': j['ScopusID']})
            dict_data_authors.update(title=data_publications['title'], published=data_publications['published'], authors=list_data_authors, number_authors=len(
                data_publications['authors']) + len(data_publications['authors_external']))
            save_file(dict_data_authors,
                      'Only_JINR_authors_new', item_publications)


def cas(x):
    if len(x) < 8:
        return '0' + x
    else:
        return x


class Match_SCIMAGO_ISBN:
    def __init__(self, sci_csv: str, path_to_folder: str):
        self.sci = sci_csv
        self.data_folder = path_to_folder

    def match_scimago(self) -> json:
        df = pd.read_csv(self.sci, sep=';')
        df['Issn'] = df['Issn'].apply(cas)
        check_folder(self.data_folder)

        for i in os.listdir(self.data_folder):
            data = open_file(self.data_folder, i)
            if data['published']['journal']['ISSN']:
                df_1 = df[(df['Issn'].str.contains(
                    data['published']['journal']['ISSN']))]
                if not df_1.empty:
                    data.update(
                        {'quartile': list(df_1['SJR Best Quartile'])[0], 'Categories': str(list(df_1['Categories'])).replace("['", '').replace("']", '')})
                    save_file(data, self.data_folder, i)
                else:
                    data.update(
                        {'quartile': None, 'Categories': None})
                    save_file(data, self.data_folder, i)
            else:
                data.update(
                    {'quartile': None, 'Categories': None})
                save_file(data, self.data_folder, i)
            # print(i)


@lru_cache
def counting_total_score(path_to_folder, path_to_new_data) -> None:
    list_data = []
    uuid_list = []
    quartile_dict = {'Q1': 4, 'Q2': 3, 'Q3': 2, 'Q4': 1}
    for i in os.listdir(path_to_folder):
        data = open_file(path_to_folder, i)
        pattern = r"\((Q\d+)\)"

        if data['Categories']:
            data['Categories'] = [(re.sub(pattern, '', i).strip(), i.split()[-1].replace('(', '').replace(')', ''))
                                  for i in data['Categories'].split(';')]
            print(data['Categories'])
            if data['quartile'] and data['quartile'] != '-':
                for j in range(len(data['authors'])):
                    dict_keys = {}
                    dict_category = {}
                    dict_keys = dict.fromkeys(['author_uuid'], 0)
                    dict_category = dict.fromkeys(
                        [j for j, nn in data['Categories']], 0)
                    if not data['authors'][j]['author_uuid'] in uuid_list:
                        dict_keys.update({'author_name': data['authors'][j]['name'], 'author_uuid': data['authors'][j]
                                          ['author_uuid'], 'ORCID': data['authors'][j]['ORCID'], 'ScopusID': data['authors'][j]['ScopusID']})
                        for numero, q in data['Categories']:
                            if data['number_authors'] > 20:
                                # d.update({'categories'quartile_dict[data['quartile']](1(j+1))})
                                dict_category[numero] += quartile_dict[q] * \
                                    (1/(j+1))
                                dict_keys['Categories'] = dict_category
                            else:
                                # d.update({'count'quartile_dict[data['quartile']](1(data['number_authors']))})
                                dict_category[numero] += quartile_dict[q] * \
                                    (1/(data['number_authors']))
                                dict_keys['Categories'] = dict_category
                            uuid_list.append(data['authors'][j]['author_uuid'])
                        list_data.append(dict_keys)
                    else:
                        for item in list_data:
                            nn = item['Categories']
                            if data['authors'][j]['author_uuid'] in item['author_uuid']:
                                for numeri in list(nn):
                                    for z, r in data['Categories']:
                                        if z == numeri:
                                            if data['number_authors'] < 20:
                                                nn[numeri] += quartile_dict[r] * \
                                                    (1/(j+1))
                                            else:
                                                nn[numeri] += quartile_dict[r] * \
                                                    (1/(data['number_authors']))
                                        else:
                                            nn.update({z: 0})
                                            if data['number_authors'] < 20:
                                                nn[z] += quartile_dict[r] * \
                                                    (1/(j+1))
                                            else:
                                                nn[z] += quartile_dict[r] * \
                                                    (1/(data['number_authors']))
                            item['Categories'] = nn
    save_file(list_data, '', path_to_new_data)


def normalization(path_to_file):
    data = open_file('', path_to_file)
    list_keys = []
    for i in data:
        for keys in i['Categories'].keys():
            if not keys in list_keys:
                list_keys.append(keys)

    max_min_dict = dict.fromkeys(list_keys, 0)
    dict_count_number_keys = dict.fromkeys(list_keys, 0)
    for item in data:
        for keyss in item['Categories'].keys():
            if item['Categories'][keyss] > max_min_dict[keyss]:
                max_min_dict[keyss] = item['Categories'][keyss]
            dict_count_number_keys[keyss] += 1

    dict_count_number_keys = dict(list(
        sorted(dict_count_number_keys.items(), key=lambda x: x[1], reverse=True))[:5])
    d = dict(sorted(max_min_dict.items(), key=lambda x: x[1], reverse=True))
    for kq in list(d):
        if not kq in dict_count_number_keys.keys():
            del d[kq]

    for it in data:
        nn = it['Categories']
        z = dict.fromkeys(d.keys(), 0)
        for ke in list(nn):
            if ke in d.keys():
                z[ke] = (nn[ke])/(d[ke])
        it['Categories'] = z
        # for q in z.keys()
        #     if z[q]  1
        #         print(it)
    save_file(data, '', 'Output_normalization3.json')
    return d, dict_count_number_keys


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
        # item['Connected'] = list(sorted([dy[dy in item['Connected']], lambda x x[1], reverse = True))
    # with open('Output_2.json', 'w', encoding='utf-8') as f
    #     json.dump(l, f, indent=2, ensure_ascii=False)
    save_file(l, '', 'Output_2.json')


def add_new(path_to_folder_new):
    main()
    find_jinr(path_to_folder_new)
    cl = Match_SCIMAGO_ISBN(r'scimagojr 2023.csv', 'Only_JINR_authors_new')
    cl.match_scimago()
    counting_total_score('Only_JINR_authors_new', 'count_file_test.json')
    data = open_file('', 'count_file_test.json')
    data_main = open_file('', 'count_file.json')
    # for autho in data:
    #     for i in autho['Categories']:
    #         if not i in p:
    #             p.append(i)
    # for a in data_main
    #     for ii in a['Categories']
    #         if not ii in p
    #             p.append(ii)
    ct = [j for i in data for j in i['Categories']]
    ct_main = [jj for ii in data_main for jj in ii['Categories']]
    ct_main.extend(ct)
    ct_main = list(set(ct_main))
    authors_main_list = [avtor['author_uuid'] for avtor in data_main]
    # for author in data:
    #     for au in data_main:
    #         if author['author_uuid'] == au['author_uuid']:
    #             for keys in ct_main:
    #                 if keys in author['Categories'].keys() and keys in au['Categories'].keys():
    #                     au['Categories'][keys] = au['Categories'][keys] + author['Categories'][keys]
    for author in data:
        for au in data_main:
            if author['author_uuid'] == au['author_uuid']:
                for keys in ct_main:
                    if keys in author['Categories'].keys() and keys in au['Categories'].keys():
                        au['Categories'][keys] = au['Categories'][keys] + \
                            author['Categories'][keys]
        if not author['author_uuid'] in authors_main_list:
            data_main.append(author)
    save_file(data_main, '', 'count_file.json')
    # for i in os.listdir('Only_JINR_authors_new')
    #     if os.path.exists(os.path.join('JINR_datapublications_train', i))
    #         pass
    #     else
    #         os.rename(os.path.join('Only_JINR_authors_new', i),
    #                   os.path.join('JINR_datapublications_train', i))
    print(normalization('count_file.json'))
    # os.remove('count_file_test.json')
    # os.remove('count_file.json')


def main():
    start = time.time()
    find_jinr('JINR_data/publications_train')
    cl = Match_SCIMAGO_ISBN(r'scimagojr 2023.csv', 'Only_JINR_authors')
    cl.match_scimago()
    counting_total_score('Only_JINR_authors', 'count_file.json')
    normalization('count_file.json')
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    # find_jinr('JINR_data')
    # # match_scimago()
    # conto()
    # norma()
    # list_of_authors_id = []
    # for item_authors in os.listdir(os.path.join('JINR_data', 'authors'))
    #     data_authors = open_file('JINR_data', os.path.join('authors', item_authors))
    #     if not data_authors['author_uuid'] in list_of_authors_id
    #         list_of_authors_id.append(data_authors['author_uuid'])
    # print(list_of_authors_id, len(list_of_authors_id))
    # l = []
    # for i in os.listdir('Authors')
    #     data = open_file('Authors', i)
    #     for j in data['authors']
    #         if j['author_uuid'] == 15342f96-558c-4891-a3b7-9ac301d11251
    #             l.append(i)
    # print(set(l))
    # {'Nuclear and High Energy Physics' 42.0, 'Physics and Astronomy (miscellaneous)' 14.0, 'Software' 12.0, 'Engineering (miscellaneous)' 8.0, 'Mathematical Physics' 8.0}
    # data = open_file('', 'gol_4.json')
    # for i in data
    #     if i['ORCID']
    #         print(i['ScopusID'])
    # numero()
    # n = []
    # for i in os.listdir('Only_JINR_authors'):
    #     data = open_file('Only_JINR_authors', i)
    #     for at in data['authors']:
    #         if at['author_uuid'] == "15342f96-558c-4891-a3b7-9ac301d11251":
    #             n.append(i)
    # print(n, len(n))
    add_new('JINR_data/publications_test')
    # counting_total_score('JINR_data/publications_test', '')
    # for author, au in zip(data['authors'], data_main['authors'])
    #     if author['author_uuid'] == au['author_uuid']
    #         data_main['Categories'][keys] += data['Categories'][keys]
    #         if data['Categories'][keys] = old_one[keys]
    #             data['Categories'][keys] = (
    #                 data['Categories'][keys])(old_one[keys])
    #         else
    #             old_one[keys] = data['Categories'][keys]
    #             data['Categories'][keys] = (
    #                 data['Categories'][keys])(data['Categories'][keys])
    #             data_main['Categories'][keys] = (
    #                 data_main['Categories'][keys])(old_one[keys])
