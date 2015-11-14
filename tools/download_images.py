import re
import os
import codecs
import requests
import shutil
from urlparse import urlparse

class DownloadImages:
  def __init__(self, path, assets):
    self.path = path
    self.assets = assets
    self.files = [
      f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path,f))
    ]

  def download(self):
    download_images = []
    for f in self.files:
      source = '%s/%s' % (self.path, f)
      # target = '%s/%s.md' % (self.path, os.path.splitext(f)[0])
      with codecs.open(source, encoding="utf-8") as content_file:
        content = content_file.read()
        for image in re.findall(r'(https?://\S+\.(?:jpg|gif|png))', content):
          filename = os.path.basename(urlparse(image).path)
          if not os.path.isfile(filename):
            r = requests.get(image, stream=True)
            if r.status_code == 200:
              with open('%s/%s' % (self.assets, filename), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
          content = content.replace(image, '/assets/images/%s' % filename)
      with codecs.open(source, "w", encoding="utf-8") as target:
        target.write(content)

import click, logging
@click.command()
@click.option('--path', help='Path to Blogger -> Jekyll migrated _posts folder')
@click.option('--assets', help='Path to Assets Folder')
def run(path, assets):
  if os.path.isdir(path):
    downloader = DownloadImages(path, assets)
    downloader.download()

if __name__ == '__main__':
  run()
