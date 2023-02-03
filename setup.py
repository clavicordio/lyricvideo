import os, json
from urllib import parse
from urllib.request import urlopen
from os.path import join
from io import BytesIO
from zipfile import ZipFile



print('Retrieving data...')

data_yadisk_link = 'https://disk.yandex.ru/d/C4_X9w0_F8Rijw'

base_url = 'https://cloud-api.yandex.net:443/v1/disk/public/resources/download?public_key='
full_url = base_url + parse.quote_plus(parse.quote_plus(data_yadisk_link))

with urlopen(full_url) as u:
    data_json = json.loads(u.read())
href = data_json['href']

print('Url retreived.')
print('Downloading...')
with urlopen(href) as u:
    zip_data = u.read()
print('\nUnzipping...')
zip_obj = ZipFile(BytesIO(zip_data))
zip_obj.extractall(path='.')
print('Done.')
#
#
#
# res = os.popen('wget -qO - {}{}'.format(base_url, url)).read()
# json_res = json.loads(res)
# filename = ul.parse_qs(ul.urlparse(json_res['href']).query)['filename'][0]
# os.system("wget '{}' -P '{}' -O '{}'".format(json_res['href'], folder, filename))

