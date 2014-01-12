Rita
====

Rita is a simple static website generator similar to Pelican, but a lot more simple in design, code and use.

The aim is to have a single script with no command line flags, making operation simple. You run it, and provided all the right files are in the right place, as documented below, your static website will be generated.

Dependencies
------------

* Jinja2
* Markdown
* PyYaml

These can be installed via pip.

Usage
-----

Execution is simple. There are no command line flags, just a configuration file:

$ python rita.py

Your Markdown articles (*.md) from your configured articles path will be taken, processed, and planted as HTML files in the publish path you've stated in the configuration.yaml file. It's really simple.

Rita can also generate pages from your pages path. These are processed in a similar fashion and output accordingly.

Metadata
--------

Articles support metadata. They're defined via a "key:value" pair on separate lines located at the start of an article or page. The colon (':') is not optional, but it can have a single space either side if this makes things easier to read.

Metadata is extracted and used to generate the article HTML files. It's also passed through to the Jinja2 templating engine, so you can re-use this metadata as and when you see fit.

License
-------
MIT.

The name: Rita
--------------
That's my cat's name. I'm not a very creative person ;-)