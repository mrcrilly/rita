
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
			self.config = config

		self.template_environment()

		# We start of with an empty site until we populate it
		self.site = {
			'content': {
				'raw': {},
				'processed': {}
			}
		}

	def build(self):
		"""
		This method does it all. It's the only method that needs to be called.
		"""

		self.gather_content()
		self.process_content()
		self.write_html()


	def template_environment(self):
		template 	= self.config['core']['templates']
		loader 		= jinja2.FileSystemLoader("{0}/{1}".format(template['foundin'], template['use']))

		self.jinja 	= jinja2.Environment(loader=loader)

	def abort(self, message):
		print "Abort: {0}".format(message)
		sys.exit(1)

	def gather_content(self):
		if self.config:
			contentpath = self.config['core']['content']['foundin']
			self.site['content']['raw'] = os.walk(contentpath)
		else:
			self.abort("No configuration found/defined.")

	def process_content(self):
		if self.config and self.site['content']['raw']:
			content = self.site['content']['raw']
			md_file_pattern = re.compile('^.*\.md$')

			for path in content:
				if len(path[2]) > 0:
					for file in path[2]:
						if md_file_pattern.search(file):
							self.process_markdown(os.path.abspath(path[0]), file)

	def process_markdown(self, path, file):
		if self.config and self.site['content']:
			meta_re = re.compile('^(?P<key>[A-Za-z0-9_-]+?)[ ]?\:[ ]?(?P<value>.*)$')

			with codecs.open("{0}/{1}".format(path, file), encoding='utf-8') as fd:
				target = self.site['content']['processed']["{0}/{1}".format(path, file)] = {
					'metadata': {},
					'html': ""
				}

				for line in fd:
					regex = meta_re.search(line)
					if regex:
						target['metadata'][regex.group('key').lower()] = regex.group('value')

				# reset the file pointer so we can work the file again
				fd.seek(0)

				raw_md = ''.join([str(x) for x in fd.readlines()[ len(target['metadata']) + 1: ]])
				target['html'] = markdown.markdown(raw_md)

	def write_html(self):
		if self.config and self.site['content']:
			for content in self.site['content']['processed']:
				pass


	# def buildAndWriteContent(contentItems):
	# 	"""
	# 	Reads a metadata hash and builds the HTML from the Markdown. Uses templating.

	# 	Arguments:
	# 	contentItems -- dictionary containing the items and their metadata
	# 	"""

	# 	for x in contentItems:
	# 		template = j2.get_template(contentItems[x]['template'])
	# 		owner = contentItems[x]['owner']
	# 		write_path = "{0}/{1}".format(config[owner]['localPath'], x)

	# 		with codecs.open(write_path, encoding='utf-8') as fd:
	# 			raw_md = ''.join([str(y) for y in fd.readlines()[ contentItems[x]['meta_lines'] + 1: ]])
	# 			md = markdown.markdown(raw_md)

	# 		with open("{0}/{1}".format(config[owner]['publishPath'], contentItems[x]['html_file']), 'w+') as fd:
	# 			fd.write(template.render(site = config, content = md))

	# def buildAndWriteIndex(articles):
	# 	"""
	# 	Passes an articles object to a template and writes out the resulting HTML

	# 	Arguments:
	# 	articles -- dictionary object for articles to be indexed.
	# 	"""

	# 	template = j2.get_template('index.html')
	# 	with open("{0}/{1}".format(config['index']['publishPath'], 'index.html'), 'w+') as html_out:
	# 		html_out.write(template.render(site = config['site'], articles = articles))

	# def copyTemplateAssests():
	# 	""" Copy into place everything the template includes, such as static files """

	# 	template = "{0}/{1}".format(config['template']['localPath'], config['template']['name'])

	# 	if os.path.exists(template):
	# 		shutil.copytree(template, config['articles']['publishPath'], ignore=shutil.ignore_patterns("*.html"))

	# def cleanWebsite():
	# 	""" Clean up the publish path """
	# 	if os.path.exists(config['index']['publishPath']):
	# 		shutil.rmtree(config['index']['publishPath'])

if __name__ == "__main__":
	site = Rita()
	site.build()
