
#
# Rita.py
# Simple static site generator
#
# Michael Crilly <michael@mcrilly.me>
# @mrmcrilly

import sys, os, codecs, re, shutil, errno
import markdown, jinja2, yaml

config = yaml.safe_load(open('./configuration.yaml'))

j2_l = jinja2.FileSystemLoader("{0}/{1}".format(config['template']['localPath'], config['template']['name']))
j2 	 = jinja2.Environment(loader=j2_l)

def buildMetaData(items):
	metadata = {}
	metadata_re = re.compile('^(?P<key>[A-Za-z0-9]+?\:)[ ](?P<value>.*)$')

	for i in items:
		for x in i[2]: 
			metadata[x] = {
				'html_file': "{0}".format(x.replace('md', 'html')),
				'meta_lines': 0,
				'template': "{0}.html".format(i[0][:-1]),
				'owner': i[0]
			}

			with codecs.open("{0}/{1}".format(config[i[0]]['localPath'], x), encoding='utf-8') as raw_md:
				for line in raw_md:
					meta = metadata_re.search(line)
					if meta:
						metadata[x][meta.group('key').replace(':', '').lower()] = meta.group('value')
						metadata[x]['meta_lines'] += 1
					else:
						break

	return metadata

def buildAndWriteArticles(articles):
	template = j2.get_template('article.html')
	raw_md = None

	for a in articles:
		with codecs.open("{0}/{1}".format(config['articles']['localPath'], a), encoding='utf-8') as fd:
			# Not so obvious, but we're using a join to take an array and make a string from it.
			# We're also using a for-loop comprehension to read the lines, in one go, and then
			# slicing the array to skip over the meta data in the document.
			raw_md = ''.join([str(x) for x in fd.readlines()[ articles[a]['meta_lines'] + 1: ]])
			md = markdown.markdown(raw_md)

			with open("{0}/{1}".format(config['articles']['publishPath'], articles[a]['html']), 'w+') as fd:
				fd.write(template.render(site = config, content = md))

def buildAndWriteContent(contentItems):
	for x in contentItems:
		template = j2.get_template(contentItems[x]['template'])
		owner = contentItems[x]['owner']
		write_path = "{0}/{1}".format(config[owner]['localPath'], x)

		with codecs.open(write_path, encoding='utf-8') as fd:
			raw_md = ''.join([str(y) for y in fd.readlines()[ contentItems[x]['meta_lines'] + 1: ]])
			md = markdown.markdown(raw_md)

		with open("{0}/{1}".format(config[owner]['publishPath'], contentItems[x]['html_file']), 'w+') as fd:
			fd.write(template.render(site = config, content = md))

def buildAndWriteIndex(articles):
	template = j2.get_template('index.html')
	with open("{0}/{1}".format(config['index']['publishPath'], 'index.html'), 'w+') as html_out:
		html_out.write(template.render(site = config['site'], articles = articles))

def copyTemplateAssests():
	template = "{0}/{1}".format(config['template']['localPath'], config['template']['name'])

	if os.path.exists(template):
		shutil.copytree(template, config['articles']['publishPath'], ignore=shutil.ignore_patterns("*.html"))

def cleanWebsite():
	if os.path.exists(config['index']['publishPath']):
		shutil.rmtree(config['index']['publishPath'])

if __name__ == "__main__":
	if config:
		cleanWebsite()

		article_list = os.walk(config['articles']['localPath'])
		page_list	 = os.walk(config['pages']['localPath'])

		articles 	= buildMetaData(article_list)
		pages 		= buildMetaData(page_list)

		copyTemplateAssests()

		buildAndWriteIndex(articles)

		buildAndWriteContent(articles)
		buildAndWriteContent(pages)

