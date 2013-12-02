
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

def buildMetaData(articles):
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
	template = j2.get_template('article.html')
	raw_md = None

	for a in articles:
		with codecs.open("{0}/{1}".format(config['articles']['localPath'], a), encoding='utf-8') as fd:
			raw_md = ''.join([str(x) for x in fd.readlines()[articles[a]['meta_lines'] + 1:]])
			md = markdown.markdown(raw_md)

			with open("{0}/{1}".format(config['articles']['publishPath'], articles[a]['html']), 'w+') as fd:
				fd.write(template.render(site = config, content = md))

def buildAndWriteIndex(articles):
	template = j2.get_template('index.html')
	with open("{0}/{1}".format(config['articles']['indexPath'], 'index.html'), 'w+') as html_out:
		html_out.write(template.render(site = config['site'], articles = articles))

def copyTemplateAssests():
	template = "{0}/{1}".format(config['template']['localPath'], config['template']['name'])

	if os.path.exists(template):
		shutil.copytree(template, config['articles']['publishPath'], ignore=shutil.ignore_patterns("*.html"))

def cleanWebsite():
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
