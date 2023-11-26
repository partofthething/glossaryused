==========================
sphinxcontrib-glossaryused
==========================

Glossaryused is a Sphinx extension that limits glossary printouts to the terms used.

Overview
--------
This  allows you to have glossary listings that only include terms you referred
to with ``:term:``. This allows you, for example, to have a huge ``..
glossary::`` listing shared across different organizations or institutions that
you bring into different projects and just print out the glossary terms that
were actually relevant.

This is partially motivated by https://github.com/sphinx-doc/sphinx/issues/3559

Installation
------------
Install by cloning this repository and running ``pip install -e .`` from the main directory.
Will attempt to get it uploaded to PyPI soon.

Then activate it in ``conf.py`` with::

    extensions = ["sphinxcontrib.glossaryused"]

If it's activated in there, then it will be in use.

Limitations
-----------
As of the first version, any ``:term:`` that's used in a different definition
will always be included. In other words, it's not yet capable of recursively
adding new follow-on terms that were part of the definition of one you included.
We'd like to add this but just haven't yet.

Links
-----

- Source: https://github.com/partofthething/sphinxcontrib-glossaryused
- Bugs: https://github.com/partofthething/sphinxcontrib-glossaryused/issues
