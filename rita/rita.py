
#
# Rita.py
# Simple static site generator
#
# Michael Crilly <michael@mcrilly.me>
# @mrmcrilly
# movedx/Freenode/#puppet
# 
import sys, os, codecs, re, shutil, errno
import markdown, jinja2, yaml

class Rita:
	"""
	Meow.
	"""

	def __init__(self, debug=False):
		self.config = yaml.safe_load(open('./configuration.yaml'))
		self.j2_l 	= jinja2.FileSystemLoader("{0}/{1}".format(self.config['template']['localPath'], self.config['template']['name']))
		self.j2 	= jinja2.Environment(loader=self.j2_l)

		self.debugging = debug

		if not self.config:
			print "Configuration failure"

	def _debug(self, message, severity="DEBUG"):
		"""
		Debug function for printing debug messages.

		Arguments:
		message -- the mesage to print
		"""
		print "{0}: {1}".format(severity, message)

	def findArticles(self):
		"""
		OS walk the articles local path and construct files list 

		Returns:
		dictionary -- dictionary of files found
		"""

		return {
			'type': 'articles',
			'files': [i[2] for i in os.walk(self.config['articles']['localPath'])][0]
		}

	def findPages(self):
		"""
		OS walk the pages local path and construct files list 

		Returns:
		dictionary -- dictionary of files found
		"""

		return {
			'type': 'pages',
			'files': [i[2] for i in os.walk(self.config['pages']['localPath'])][0]
		}

	def go(self):
		self.articles 	= self.findArticles()
		self.pages 		= self.findPages()			

		if self.debugging:
			self._debug(self.articles)
			self._debug(self.pages)

		if self.debugging:
			self._debug('clearPublishPath()')

		self.clearPublishPath()

		self.articles['content'] 	= self.buildMetadata(self.articles)
		self.pages['content'] 		= self.buildMetadata(self.pages)

		if self.debugging:
			self._debug(self.articles)
			self._debug(self.pages)

		self.convertMarkdown(self.articles)
		self.convertMarkdown(self.pages)

		self.copyTemplateAssests()
		self.buildAndWriteIndex()

	def buildMetadata(self, items):
		"""
		Read the header of the Markdown file and extract the metadata.

		Arguments:
		items -- a tuple as returned by os.walk()

		Returns:
		metadata -- dictionary of metadata for each article/page
		"""

		metadata = {}
		metadata_re = re.compile('^(?P<key>[A-Za-z0-9]+?)[ ]?\:[ ]?(?P<value>.*)$')

		if self.debugging:
			self._debug(items)

		for i in items['files']:

			metadata[i] = {
				'meta': {
				}
			}

			with codecs.open("{0}/{1}".format(self.config[items['type']]['localPath'], i), encoding='utf-8') as raw_md:
				for line in raw_md:
					meta = metadata_re.search(line)
					if meta:
						metadata[i]['meta'][meta.group('key').lower()] = meta.group('value')
					else:
						# If there is no match, we assume the metadata "header" has finished
						break


			if not 'htmlfile' in metadata[i]['meta']:
				metadata[i]['meta']['htmlfile'] = "{0}".format(i.replace('md', 'html'))

			if not 'template' in metadata[i]['meta']:
				metadata[i]['meta']['template'] = self.config[items['type']]['template']

		if self.debugging:
			self._debug("buildMetaData(): metadata: {}".format(metadata))

		return metadata

	def convertMarkdown(self, contentItems):
		for i in contentItems['content']:
			template = self.j2.get_template(i['meta']['htmlfile'])

	def buildAndWriteContent(self, contentItems):
		"""
		Reads a metadata hash and builds the HTML from the Markdown. Uses templating.

		Arguments:
		contentItems -- dictionary containing the items and their metadata
		"""

		for i in contentItems:
			template = self.j2.get_template(contentItems[i]['template'])
			owner = contentItems[x]['owner']
			write_path = "{0}/{1}".format(self.config[owner]['localPath'], x)

			with codecs.open(write_path, encoding='utf-8') as fd:
				raw_md = ''.join([str(y) for y in fd.readlines()[ contentItems[x]['meta_lines'] + 1: ]])
				md = markdown.markdown(raw_md)

			with open("{0}/{1}".format(self.config[owner]['publishPath'], contentItems[x]['html_file']), 'w+') as fd:
				fd.write(template.render(site = self.config, content = md))

	def buildAndWriteIndex(self):
		"""
		Passes an articles object to a template and writes out the resulting HTML

		Arguments:
		articles -- dictionary object for articles to be indexed.
		"""

		template = self.j2.get_template('index.html')
		with open("{0}/{1}".format(self.config['index']['publishPath'], 'index.html'), 'w+') as html_out:
			html_out.write(template.render(site = self.config['site'], articles = articles))

	def copyTemplateAssests(self):
		""" Copy into place everything the template includes, such as static files """

		template = "{0}/{1}".format(self.config['template']['localPath'], self.config['template']['name'])

		if os.path.exists(template):
			shutil.copytree(template, self.config['articles']['publishPath'], ignore=shutil.ignore_patterns("*.html"))

	def clearPublishPath(self):
		""" Clean up the publish path """
		if os.path.exists(self.config['index']['publishPath']):
			shutil.rmtree(self.config['index']['publishPath'])

if __name__ == "__main__":
	site = Rita(True)
	site.go()
