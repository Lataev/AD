'''
Поиск в AD по строке поиска, сохранение атрибутов результатов в pandas dataframe.

'''

import pandas as pd
from ldap3 import Server, Connection
from secret import auth_data


def serverdata():
    return auth_data.ad().AD_SERVER, \
            auth_data.ad().AD_USER, \
            auth_data.ad().ad_username, \
            auth_data.ad().AD_PASSWORD, \
            auth_data.ad().AD_SEARCH_TREE

def ad_search(search_string: str, attributes: list = ['*'], search_scope: str = None) -> list[dict]: # Поиск в AD

    AD_SERVER, AD_USER, ad_username, AD_PASSWORD, AD_SEARCH_TREE = serverdata()

    server = Server(AD_SERVER)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD)
    conn.bind()

    if search_scope is None: search_scope = AD_SEARCH_TREE

    ad_entries = conn.extend.standard.paged_search(search_scope, search_string,
    get_operational_attributes=True,
    attributes = attributes,
        generator=True,
        )
    
    ad_entries_list = list(ad_entries)

    conn.unbind()

    if ad_entries_list:
        return ad_entries_list

if __name__ == '__main__':

    attributes = ['displayName', 'sAMAccountName']
    group_dn = 'OU=Users,OU=IT,OU=Departments,OU=Company,DC=domain,DC=com'
    search_string = f'(memberOf={group_dn})'

    ad_entries_list = ad_search(search_string=search_string, attributes=attributes)

    if ad_entries_list:
        df_ad = pd.DataFrame(ad_entry.get('attributes') for ad_entry in ad_entries_list)
    else:
        df_ad = None

    print(df_ad)