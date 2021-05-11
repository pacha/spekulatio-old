
==============
Spekulatio API
==============


Set values
==========

Special values that can be set in the front-matter section of content files or
in the ``_values.yaml`` file to configure the behavior of Spekulatio:

_template
---------

Type: ``string``. Default: ``spekulatio/default.html``

Jinja template to use. Eg::

    _template: foo/bar.html

    ---

    This is a title
    ---------------

    This is some content

In this case, the first template file to match ``foo/bar.html`` in the template
directories will be used. You can also set this variable in a ``_values.yaml``
file to alter the template to be used in an entire branch of the generated site.

_md
---

Type: ``dictionary``. Default: ``{}``

Set Markdown conversion parameters. For now it only accepts one key::

    _md:
      extra_extensions:
        - fenced_code

``extra_extensions`` is a list of strings as accepted by the
`Python-Markdown <https://github.com/Python-Markdown/markdown>`_ package. You
can find a list of available extensions at:

https://python-markdown.github.io/extensions/#officially-supported-extensions

Get Values
==========

Special values accessible in HTML templates.

``_content``: Content of a Markdown or RestructuredText file already converted to HTML.

``_raw_text``: Raw content of a Markdown or RestructuredText file (not including the front-matter if there's one).

``_toc``: Table of contents of the current Markdown or RestructuredText file. (TODO: explain structure)

``_title``: Top header of the current Markdown or RestructuredText file.

``_rst``
--------

Type: ``dictionary``

Extra information about a converted RestructuredText file. At the moment it only
provides information about the ``docinfo`` section of the document. For example,
for::

    :field1: foo
    :field2: bar

    This is a header
    ================

    This is just sample text

The value available in the HTML template is::

    _rst:
      docinfo:
        field1: foo
        field2: bar

