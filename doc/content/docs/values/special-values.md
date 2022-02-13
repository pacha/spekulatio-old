---
_alias: special-values
article_classes: reference-page
---

Special Values
==============

In Spekulatio, it is up to you to decide which values to define and how to use
them in your templates. However, there's a small number of reserved names for
variables that have a special meaning inside the tool. Those are the **special
values** and all them start with an underscore.

This is the list of all available special values. Note that they all have a
default scope that can't be modified.

» `_alias`
----------

> **Scope**: local <br> **Type**: string

It allows to give a name to a specific page so that it can be later be
referred using that name. For example, if you have a page like:

    ---
    _alias: configuration
    ---

    Configuration
    =============

    Some text.

Then you can create a link to it with:

    {% raw -%}
    <a href="{{ url('configuration') }}">Configuration Page</a>
    {% endraw %}

» `_template`
-------------

It sets the template to use by actions that require one. For example, if set
to `_template: my-dir/my-template.html`, actions that convert Markdown or
reStructuredText to HTML will use `my-dir/my-template.html` as their template.
The template filename must be specified relative to the input directory that
contains it, and that input directory has to have that filetype associated to
the `use_as_template` action. In the previous example, if `templates` is the
directory that contains the templates, the file must be located at
`templates/my-dir/my-template.html`.

» `_sort`
---------

This value is used to set the order of children pages in a directory. For
example, if you have the following directory:

    my-dir/
      _values.yaml
      bar.md
      baz.md
      foo.md
      another-dir/

then inside `_values.yaml` you can set any arbitrary order like:

    _sort:
      - foo
      - baz
      - another-dir
      - bar

Notice that the files are specified without extension. Having child nodes
sorted is useful when you
inspect the 

------

        "_skip": {"scope": "local", "operation": "replace", "type": bool},
        "_sort": {"scope": "local", "operation": "replace", "type": list},
        "_sort_options": {"scope": "default", "operation": "merge", "type": dict},


» `_content`
: It is set to the HTML version of the content of Markdown and reStructuredText
  files when they are being processed. You can use it in your templates to
  insert the content of the file at the appropriate place:

        <body>
          <article>
            {{ _content }}
          </article>
        </body>

  In non-template HTML files, `_content` is set to the same value as `_src_text`
  (ie. to the body of the file itself).

» `_title`
: It is set to the first header of the current Markdown or reStructuredText
  file. You can use it to insert the title of the page at the appropriate
  places:

        <head>
            <title>{{ _title }}</title>
        </head>

        "_jinja_options": {"scope": "default", "operation": "merge", "type": dict},
        "_md_options": {"scope": "default", "operation": "merge", "type": dict},
        "_rst_options": {"scope": "default", "operation": "merge", "type": dict},
        "_sass_options": {"scope": "default", "operation": "merge", "type": dict},
        "_src_text": {"scope": "local", "operation": "replace", "type": str},
        "_title": {"scope": "local", "operation": "replace", "type": str},
        "_toc": {"scope": "local", "operation": "replace", "type": list},
        "_url": {"scope": "local", "operation": "replace", "type": str},
