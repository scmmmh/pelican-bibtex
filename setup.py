from distutils.core import setup

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: Public Domain
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Software Development
Operating System :: POSIX
Operating System :: Unix

"""

LONG_DESCRIPTION = """\
Requirements
============

pelican\_bibtex requires pybtex.

This plugin reads a user-specified BibTeX file and populates the context with
a list of publications, ready to be used in your Jinja2 template.

If the file is present and readable, you will be able to find the 'publications'
variable in all templates.  See the README for details.
"""

setup(
    name='pelican_bibtex',
    description='Organize your scientific publications with BibTeX in Pelican',
    long_description=LONG_DESCRIPTION,
    version='0.4.0',
    author='Vlad Niculae',
    author_email='vlad@vene.ro',
    url='https://pypi.python.org/pypi/pelican_bibtex',
    py_modules=['pelican_bibtex'],
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    install_requires=['pybtex']
)
