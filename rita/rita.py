
#
# Rita.py
# Simple, single-file, static site generator
#
# Michael Crilly <michael@mcrilly.me>

import sys
import os
import codecs
import re
import shutil
import errno

import markdown
import jinja2
import yaml

config = yaml.safe_load(open('./configuration.yaml'))

j2_l = jinja2.FileSystemLoader("{0}/{1}".format(config['template']['localPath'], config['template']['name']))
j2 	 = jinja2.Environment(loader=j2_l)

def buildMetaData(articles):
	'''
	Extracts metadata from the top of the file using a basic regular expresssion.
	The idea is simple: Look for a "Key: value" line and break when this criteria
	hasn't been met. This means terminating the metadata simply requires the author
	to use a new line.

	Returns a dictionary. Lower cases the key; the author can write the key:values
	as they	wish.
	'''

	metadata = {}
	metadata_re = re.compile('^(?P<key>[A-Za-z]+?\:)[ ](?P<value>.*)$')

	for a in articles:
		metadata[a] = {
			'html': "{0}".format(a.replace('md', 'html')),
			'meta_lines': 0,
		}
		with codecs.open("{0}/{1}".format(config['articles']['localPath'], a), encoding='utf-8') as raw_md:
			for line in raw_md:
				meta = metadata_re.search(line)
				if meta:
					metadata[a][meta.group('key').replace(':', '').lower()] = meta.group('value')
					metadata[a]['meta_lines'] += 1
				else:
					break

	return metadata

def buildAndWriteArticles(articles):
	'''
	Takes in the Markdown, after the metadata has been processed and the number of lines
	it takes noted, then returns the rendered template. Nothing fancy about this really,
	it just uses a a set of Jinja2 templates and applies the Markdown to them. Simple.

	Writes the HTML directly to disk in the correct location.
	'''

	template = j2.get_template('article.html')
	raw_md = None

	for a in articles:
		with codecs.open("{0}/{1}".format(config['articles']['localPath'], a), encoding='utf-8') as fd:
			raw_md = ''.join([str(x) for x in fd.readlines()[articles[a]['meta_lines'] + 1:]])
			md = markdown.markdown(raw_md)

			with open("{0}/{1}".format(config['articles']['publishPath'], articles[a]['html']), 'w+') as fd:
				fd.write(template.render(site = config, content = md))

def buildAndWriteIndex(articles):
	'''
	Produce an index HTML document from the list of articles in the article's directory
	'''

	template = j2.get_template('index.html')
	with open("{0}/{1}".format(config['articles']['indexPath'], 'index.html'), 'w+') as html_out:
		html_out.write(template.render(site = config['site'], articles = articles))

def copyTemplateAssests():
	template = "{0}/{1}".format(config['template']['localPath'], config['template']['name'])

	if os.path.exists(template):
		shutil.copytree(template, config['articles']['publishPath'], ignore=shutil.ignore_patterns("*.html"))

def cleanWebsite():
	'''
	cleanWebsite() deletes the existing content inside the output folder.
	'''
	if os.path.exists(config['articles']['publishPath']):
		shutil.rmtree(config['articles']['publishPath'])

	# os.makedirs(config['articles']['publishPath'])

if __name__ == "__main__":
	if config:
		cleanWebsite()

		article_list = os.listdir(config['articles']['localPath'])

		articles = {}
		articles = buildMetaData(article_list)

		copyTemplateAssests()
		buildAndWriteIndex(articles)
		buildAndWriteArticles(articles)





