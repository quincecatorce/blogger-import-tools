import os
import codecs
import html2text

class ConsolidateMarkdown:
  def __init__(self, path):
    self.path = path
    self.files = [
      f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path,f))
    ]

  def consolidate(self):
    for f in self.files:
      source = '%s/%s' % (self.path, f)
      target = '%s/%s.md' % (self.path, os.path.splitext(f)[0])
      with codecs.open(source, encoding='utf-8') as content_file:
        content = content_file.read()
        header_limit = content.rfind('---') + 3
        header = content[0:header_limit]
        content = content[header_limit:]
        h = html2text.HTML2Text()
        h.body_width = 0
        content = h.handle(content)
        with codecs.open(target, "w", encoding='utf-8') as target:
          target.write(header)
          target.write('\n\n')
          target.write(content)

import click, logging
@click.command()
@click.option('--path', help='Path to Blogger -> Jekyll migrated _posts folder')
@click.option('--delete_sources', is_flag=True, default=False, help='Delete Sources?')
def run(path, delete_sources):
  if os.path.isdir(path):
    consolidator = ConsolidateMarkdown(path)
    consolidator.consolidate()

if __name__ == '__main__':
  run()
