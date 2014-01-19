
#
# Rita.py
# Simple static site generator
#
# Michael Crilly <michael@mcrilly.me>
# @mrmcrilly

import sys, os, codecs, re, shutil, errno, markdown, jinja2, yaml

class Rita:

    def __init__(self, config=None):
        if not config:
            self.config = yaml.safe_load(open('./configuration.yaml'))
        else:
            if 'core' in config:
                self.config = config
            else:
                self.log("Your provided configuration is invalid.", "error")
                sys.exit(1)

        self.debugging = self.config['core']['runtime']['debug']
        self.site = { 'content': { 'raw': {}, 'processed': {} } }

    def build(self):
        self.template_environment()
        self.gather_content()
        self.process_content()
        self.write_html()
        self.write_index()

    def template_environment(self):
        template = self.config['core']['templates']
        loader   = jinja2.FileSystemLoader("{0}/{1}".format(template['foundin'], template['use']))

        self.jinja = jinja2.Environment(loader=loader)

    def log(self, message, severity="debug"): print "{0}: {1}".format(severity, message)

    def gather_content(self):
        if self.config:
            contentpath = self.config['core']['content']['foundin']

            for item in os.walk(contentpath):
                self.site['content']['raw'][item[0]] = item[2]

            if self.debugging:
                self.log("contentpath: {0}".format(contentpath))
                self.log("raw content: {0}".format(self.site['content']['raw']))
        else:
            self.log("no configuration found/defined.", "error")
            sys.exit(1)

    def process_content(self):
        if self.config:
            content = self.site['content']['raw']
            if self.debugging: self.log("content: {}".format([i for i in content]))

            md_file_pattern = re.compile('^.*\.md$')

            for path in content:    
                if self.debugging: self.log("path: {}".format(path))

                if len(content[path]) > 0:
                    if self.debugging: self.log("path: {0}: has files".format(content[path]))

                    for file in content[path]:
                        if md_file_pattern.search(file):
                            if self.debugging: self.log("file matched: {}".format(file))
                            self.process_markdown(os.path.abspath(path), file)
        else:
            self.log("no configuration or raw content.", "error")
            sys.exit(1)

    def process_markdown(self, path, file):
        if self.config and self.site['content']:
            meta_re = re.compile('^(?P<key>[A-Za-z0-9_-]+?)[ ]?\:[ ]?(?P<value>.*)$')

            with codecs.open("{0}/{1}".format(path, file), encoding='utf-8') as fd:
                target = self.site['content']['processed']["{0}/{1}".format(path, file)] = {
                    'metadata': {}, 'html': ""
                    }

                for line in fd:
                    regex = meta_re.search(line)
                    if regex:
                        target['metadata'][regex.group('key').lower()] = regex.group('value')
                    else:
                        break

                # reset the file pointer so we can work the file again
                fd.seek(0)

                raw_md = ''.join([str(x) for x in fd.readlines()[ len(target['metadata']) + 1: ]])
                target['html'] = markdown.markdown(raw_md)

    def write_html(self):
        if self.config and self.site['content']['processed']:
            for content in self.site['content']['processed']:
                target = self.site['content']['processed'][content]
                template = self.jinja.get_template('content.html')

                with open(re.sub('\.md$', '.html', content), 'w+') as fd:
                    fd.write(template.render(config=self.config, content=target))

    def write_index(self):
        if self.config and self.site['content']['processed']:
            template = self.jinja.get_template('index.html')

            with open("{}/index.html".format(self.config['core']['content']['foundin']), 'w+') as fd:
                fd.write(template.render(config=self.config, content=self.site['content']['processed']))


if __name__ == "__main__":
    site = Rita()
    site.build()
