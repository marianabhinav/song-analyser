import os
import zipfile
import requests


data_url = 'https://os.unil.cloud.switch.ch/fma/fma_small.zip'
data_name = 'fma_small.zip'

meta_url = 'https://os.unil.cloud.switch.ch/fma/fma_metadata.zip'
meta_name = 'fma_metadata.zip'

data_dir = os.path.join('..', 'data')


def download_file(url, name, data_dir):

    path = os.path.join(data_dir, name)
    if not os.path.exists(path):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
            }
        r = requests.get(url, headers=headers, allow_redirects=True, stream=True)
        length = int(r.headers.get('content-length'))

        with open(path, 'ab') as f:
            pos = f.tell()
            while pos <= length:

                for i, chunk in enumerate(r.iter_content(chunk_size=2391975)):
                    if chunk:
                        f.write(chunk)
                        print('\r', (i + 1) * 2391975, ' / ', length, end='')

                pos = f.tell()
                if pos <= length:
                    print('Download aborted - reconnecting')

                    headers['Range'] = f'bytes={pos}-'
                    r = requests.get(url, headers=headers, allow_redirects=True, stream=True)
                    length = int(r.headers.get('content-length'))

        print(name, 'done')
    else:
        print('File already exists', name)

    return path


data_file_path = download_file(data_url, data_name, data_dir)
meta_file_path = download_file(meta_url, meta_name, data_dir)


with zipfile.ZipFile(data_file_path, 'r') as zip:
    zip.printdir()
    zip.extractall(data_dir)

with zipfile.ZipFile(meta_file_path, 'r') as zip:
    zip.printdir()
    zip.extractall(data_dir)
