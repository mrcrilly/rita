Rita
====

Rita is a simple static website generator similar to Pelican, but a lot more simple in design, code and use.

The aim is to have a single script with no command line flags, making operation simple. You run it, and provided all the right files are in the right place, as documented below, your static website will be generated.

Dependencies
------------

* Jinja2
* Markdown

These can be installed via pip.

```
pip install Jinja2 Markdown
```

If you choose to use Meow, the basic CLI client, then you will also need YaML:

```
pip install PyYaml
```

Usage
-----

Rita is a library/class, so she requires a client to use. This repository has a bin/ directory which ships with "Meow", a simple CLI tool that will allow you to easily utilise Rita. If you write to your own, then she is really easy to utilise.

Taking the code from Meow:

```
from rita.rita import Rita

def meow(configuration_file):
    if configuration_file:
        config = yaml.load(open(configuration_file))

        site = Rita(config)
        site.build()
```

We simply read in a configuration file, which can come from anywhere or any format, convert it to a Python dictionary, and then pass this to Rita. At minimum, Rita expects to see a minimal amount of configuration inside of a hash called "core". More details to follow on this.

Configuration
-------------

There is a 'configuration.yaml' file located in the etc/ directory. This file is used as an example lto configure the location of various elements:

* Templates
* Content
* Dynamic information, such as site information
** This data is passed through to the templates
** It's ideal for contact information, site title, etc

This configuration must have, at minimum, a 'core' element:

```
---
core:
  templates:
    foundin: /Users/mcrilly/.rita/templates/
    use: development
  content:
    foundin: /Users/mcrilly/.rita/content/
  runtime:
    debug: true
```

Everything else included inside this file can be anything the user want. What's more, everything outside the 'core' section is passed through to the templates as and when articles and pages are being processed. This means you can include fixed information which you might want to be made available in your templates, such as contact details.

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
