from posixpath import split
from numpy import mat
from sys import argv
import requests
import re


def get_wp_updates(url, login, password):

    login_url = 'http://' + domain_name + '/wp-login.php'
    plugins_url = f'http://{domain_name}/wp-admin/plugins.php'
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    session = requests.Session()
    r = session.get(login_url, headers = {
        'User-Agent': user_agent_val
    })
    session.headers.update({'Referer':login_url})
    session.headers.update({'User-Agent':user_agent_val})

    login_request = session.post(login_url, {
        'log': login,
        'pwd': password,
        'remember':'yes',
    })

#    post_request = session.get('http://poltorakota.ru/wp-admin/update-core.php')
    post_request = session.get(plugins_url)
    
    #print(post_request.text)
    updates_dict = {}
    text = post_request.text.split('\n')
    for line in text:
        match = re.search(r"Доступна свежая версия (?P<PluginName>\D+?)\..+(?:версии )(?P<version>.+?)<", line)
        if match:
#                print(match.groups())
#                print(match.group('PluginName'))
            updates_dict[match.group('PluginName')] = match.group('version')
            print("Доступны обновления для следующих плагинов: \n", updates_dict)


if __name__ == '__main__':
    script_name, domain_name, log, passwd = argv
    get_wp_updates(domain_name, log, passwd)
