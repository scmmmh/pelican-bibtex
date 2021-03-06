Pelican BibTeX
==============

Organize your scientific publications with BibTeX in Pelican

Author          | Vlad Niculae
----------------|-----
Author Email    | vlad@vene.ro
Author Homepage | http://vene.ro
Github Account  | https://github.com/vene

*Note*: This code is unlicensed. It was not submitted to the `pelican-plugins`
official repository because of the license constraint imposed there.


Requirements
============

`pelican_bibtex` requires `pybtex`.

```bash
pip install pybtex
```

How to Use
==========

This plugin reads a user-specified BibTeX file and populates the context with
a list of publications, ready to be used in your Jinja2 template.

Configuration is simply:

```python
PUBLICATIONS_SRC = ['content/pubs.bib']
```

If the file is present and readable, you will be able to find the `publications`
variable in all templates.  It is a dictionary of the filenames specified in
`PUBLICATIONS_SRC`. Each key maps to a list of Pybtex Entry objects loaded from
the given BibTeX file. Each Entry has an additional key `rendered` that holds
the generated reference for that Entry.

Template Example
================

You probably want to define a 'publications.html' direct template.  Don't forget
to add it to the `DIRECT\_TEMPLATES` configuration key.  Note that we are escaping
the BibTeX string twice in order to properly display it.  This can be achieved
using `forceescape`.

```python
{% extends "base.html" %}
{% block title %}Publications{% endblock %}
{% block content %}

<script type="text/javascript">
    function disp(s) {
        var win;
        var doc;
        win = window.open("", "WINDOWID");
        doc = win.document;
        doc.open("text/plain");
        doc.write("<pre>" + s + "</pre>");
        doc.close();
    }
</script>
<section id="content" class="body">
    <h1 class="entry-title">Publications</h1>
    <ul>
      {% for group in publications['pubs.bib']|groupby('fields.year')|reverse %}
      <li> {{group.grouper}}
        <ul>
        {% for publication in group.list %}
          <li id="{{ publication.fields.get('key') }}">{{ publication.fields.get('rendered') }}
          [&nbsp;<a href="javascript:disp('{{ publication.fields.get('bibtex')|replace('\n', '\\n')|escape|forceescape }}');">Bibtex</a>&nbsp;]
          {% for label, target in [('PDF', publication.fields.get('pdf')), ('Slides', publication.fields.get('slides')), ('Poster', publication.fields.get('poster'))] %}
            {{ "[&nbsp;<a href=\"%s\">%s</a>&nbsp;]" % (target, label) if target }}
          {% endfor %}
          </li>
        {% endfor %}
        </ul></li>
      {% endfor %}
    </ul>
</section>
{% endblock %}
```

Extending this plugin
=====================

A relatively simple but possibly useful extension is to make it possible to
write internal links in Pelican pages and blog posts that would point to the
corresponding paper in the Publications page.

A slightly more complicated idea is to support general referencing in articles
and pages, by having some BibTeX entries local to the page, and rendering the
bibliography at the end of the article, with anchor links pointing to the right
place.
