Rita
====
Rita is a simple static website generator similar to Pelican, but a lot more simple in design, code and use.

I just wanted something I provided a template and a set of Markdown files to, which it then used to produce a flat (in directory structure), static website consistenting of the template's requirements (any JavaScript files, etc) and pure HTML.

Usage
-----
$ python rita.py

Your Markdown articles (*.md) from 'articles' will be taken, processed, and planted as HTML files in whatever publish path you stated in the configuration.yaml file. It's really simple.

Metadata
--------
Articles support metadata. Simply put, they're a "Key: value" pair on separate lines. The 'key' is a proper-noun and there is a space between the ':' and the value. A regular expression looks for this exact format at the top of the file. The moment the regular expression starts finding this matter is the moment the metadata has come to and end. Therefore a new line or some other pattern that doesn't match stops the metadata search.

Example Markdown articles are provided with example data. 

License
-------
MIT.

The name: Rita
--------------
That's my cat's name. I'm not a very creative person ;-)