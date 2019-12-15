import os
from getpass import getpass
from functools import partial

import requests
import asyncio


base_url = 'https://raw.githubusercontent.com/madmaze/pytesseract/master/tests/data/'

github_user = os.environ.get('GITHUB_USER') or input('Enter github user')
github_pwd = getpass(f'Enter pwd for {github_user}')

images = [
    'test' + '.' + ext
    for ext in ('jpg', 'png', 'gif', 'ppm', 'tiff', 'bmp', 'pgm')
]


def make_data_directory(dirname='data'):
    curdir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(curdir, dirname)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)


@asyncio.coroutine
def download_image(filename):
    url = base_url + filename
    data_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'data',
        filename
    ))
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None,
            partial(requests.get, auth=(github_user, github_pwd)), url)
    res = yield from future
    with open(data_dir, 'wb') as f:
        f.write(res.content)


async def main():
    make_data_directory()
    for image in images:
        await download_image(image)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(e)
        loop.close()

    loop.close()
