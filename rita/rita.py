
#
# Rita.py
# Simple static site generator
#
# Michael Crilly <michael@mcrilly.me>

import sys, os, codecs, re, shutil, errno
import markdown, jinja2, yaml

config = yaml.safe_load(open('./configuration.yaml'))

j2_l = jinja2.FileSystemLoader("{0}/{1}".format(config['template']['localPath'], config['template']['name']))
j2 	 = jinja2.Environment(loader=j2_l)

def buildMetaData(items):
	metadata = {}
	metadata_re = re.compile('^(?P<key>[A-Za-z]+?\:)[ ](?P<value>.*)$')

	for i in items:
		for x in i[2]: 
			print i[0][:-1]
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
	template = j2.get_template(contentItems['template'])
	raw_md = None

	# for x in contentItems:
	# 	with codecs.open("{0}/{1}".format(config[x['owner']]['localPath']), x)

# def buildAndWritePages(pages):
# 	template = j2.get_template('page.html')
# 	raw_md = None

# 	for p in pages:
# 		with codecs.open("{0}/{1}".format(config['pages']['localPath'], p), encoding='utf-8') as fd:
# 			raw_md = ''.join([str(x) for x in fd.readlines()[ pages[p]['meta_lines'] + 1: ]])
# 			md = markdown.markdown(raw_md)

def buildAndWriteIndex(articles):
	template = j2.get_template('index.html')
	with open("{0}/{1}".format(config['articles']['indexPath'], 'index.html'), 'w+') as html_out:
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

		print articles

		sys.exit()

		copyTemplateAssests()
		buildAndWriteIndex(articles)
		buildAndWriteArticles(articles)
		buildAndWritePages(pages)

