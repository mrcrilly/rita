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

Execution is simple. There are no command line flags:

$ python rita.py

Configuration is read from a single file.

Configuration
-------------

There is a 'configuration.yaml' file located in the same directory as 'rita.py'. This file is used to configure the location of various elements:

* Templates
* Articles
* Pages
* Generated static content: where it's published

This configuration must have, at minimum:

```
template:
    localPath: templates
    name: development

index:
    publishPath: website

articles:
    localPath: articles
    publishPath: website

pages:
    localPath: pages
    publishPath: website
```

The paths here are relative, but they can be absolute, also.

Everything else included inside this file can be anything the user want. What's more, this entire configuration is passed through to the templates as and when articles and pages are being processed. This means you can include fixed information which you might want to be made available in your templates, such as contact details.

Process
-------

Your Markdown articles and pages (*.md) from your configured paths will be taken, processed, and planted as HTML files in the publish path you've stated in the configuration.yaml file. It's really simple.

Rita...

1. Cleans up the existing website publish path;
1. Produces a list of articles and pages from the respective directories;
1. Processes metadata in articles and pages;
1. Copies all of the directories and files, except HTML files, from the template to the publish path;
1. Builds and writes out the index.html index using the 'index.html' template;
1. Builds and writes out your articles and pages;

Metadata
--------

Articles support metadata. They're defined via a "key:value" pair on separate lines located at the start of an article or page. The colon (':') is not optional, but it can have a single space either side if this makes things easier to read. No blank lines are permitted and the moment the regular expressions used fails to find a match is the moment Rita assumes all metadata has been consumed.

Metadata is extracted and used to generate the article HTML files. It's also passed through to the Jinja2 templating engine, so you can re-use this metadata as and when you see fit, right there in your templates.

Templates
---------

The templates can be called or arranged in anyway you see fit. The only requirement is that there is an 'index.html' template. This is "hard coded" (for now) into Rita, is assumed to exist and is consumed and used as the index for your static content.

Any files inside the template directory are copied to the publish path, except the HTML template files themselves. This allows you to include anything you want inside your template directory, such as images, CSS, JavaScript, etc - it will all be copied over.

License
-------
MIT.

The name: Rita
--------------
That's my cat's name. I'm not a very creative person ;-)
