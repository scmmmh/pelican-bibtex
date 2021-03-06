"""
Pelican BibTeX
==============

A Pelican plugin that populates the context with a list of formatted
citations, loaded from a BibTeX file at a configurable path.

The use case for now is to generate a ``Publications'' page for academic
websites.
"""
# Author: Vlad Niculae <vlad@vene.ro>
# Unlicense (see UNLICENSE for details)

import logging
import os

from pelican import signals

logger = logging.getLogger(__name__)


def add_publications(generator):
    """
    Populates context with a list of BibTeX publications.

    Configuration
    -------------
    generator.settings['PUBLICATIONS_SRC']:
        list of local paths to the BibTeX files to read.

    Output
    ------
    generator.context['publications']:
        Dictionary where the keys are the BibTeX filenames
        and the values list of Pybtex entries
    """
    if 'PUBLICATIONS_SRC' not in generator.settings:
        return
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
    try:
        from pybtex.database.input.bibtex import Parser
        from pybtex.database.output.bibtex import Writer
        from pybtex.database import BibliographyData, PybtexError
        from pybtex.backends import html
        from pybtex.style.formatting import unsrt
    except ImportError:
        logger.warn('`pelican_bibtex` failed to load dependency `pybtex`')
        return

    generator.context['publications'] = {}

    for refs_file in generator.settings['PUBLICATIONS_SRC']:
        try:
            bibdata_all = Parser().parse_file(refs_file)
        except PybtexError as e:
            logger.warn('`pelican_bibtex` failed to parse file %s: %s' % (
                refs_file,
                str(e)))
            return

        publications = []

        # format entries
        unsrt_style = unsrt.Style()
        html_backend = html.Backend()
        formatted_entries = unsrt_style.format_entries(bibdata_all.entries.values())

        for formatted_entry in formatted_entries:
            key = formatted_entry.key
            entry = bibdata_all.entries[key]

            #render the bibtex string for the entry
            bib_buf = StringIO()
            bibdata_this = BibliographyData(entries={key: entry})
            Writer().write_stream(bibdata_this, bib_buf)
            text = formatted_entry.text.render(html_backend)

            entry.fields['rendered'] = text
            publications.append(entry)

        generator.context['publications'][refs_file.replace(os.path.sep, '/').split('/')[-1]] = publications

def register():
    signals.generator_init.connect(add_publications)
