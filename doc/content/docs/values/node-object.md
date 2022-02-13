---
_alias: node-object
article_classes: reference-page
---

Node Object
===========

Inside Spekulatio, a site is represented as a tree of nodes in memory. Every
time a page is rendered, the template receives a `_node` reference pointing to
the node associated to that page. Using that node object gives you access to the
entire site tree. For example, you can access the root of the site with
`_node.root` or all the children of the current node with `_node.children`. You
can then use Jinja loops and conditionals to traverse the tree and generate
sitemaps, menus or sets of links at the sidebar.

For example, to list the links to the pages at the same level as the
current one, you could use something like:
{% raw %}
```
<ul>
    {% for child in _node.parent.children %}
    <li><a href="{{ child.url }}">{{ child.title }}</a></li>
    {% endfor %}
</ul>
```
{% endraw %}

The following is a list of the available attributes and functions of a node
object grouped by category.

Basic Properties
----------------

» `title`
---------

> String

Title of the page. Set by defining the `_title` special value. If that value is
not defined, the title will be extracted for the first header in the file in
case of Markdown and reStructuredText files. If there is no header or the file
is of a different format the title will be the same as `relative_dst_path`.

» `name`
--------

> String

Basename of the destination file. For example, if the file associated to the
current node is `some/folder/file.html` then `name` is `file.html`.

» `alias`
--------

> String

Identifier of the page and set using the `_alias` special value.

» `url`
-------

> String

URL of the page. By default, the URL of the page is the same as `default_url`
but it can be overridden using the `_url` special value.

» `default_url`
---------------

> String

URL of the page unless it has been overridden using the `_url` special value. It
is the same as `relative_dst_path` but appending a slash in front of it. For
example, if the file associated to the current page is `some/folder/file.html`
the value of `default_url` will be `/some/folder/file.html`.

» `skip`
--------

> Boolean

Flag that tells if this node will be skipped during tree traversal operations.
For instance, a folder full of static content such as CSS or image files can be
marked to be skipped and then it won't appear within the children of the parent
node or when calling `traverse()` (see below). To mark a node to be skipped, the
`_skip` special value is used. `index.html` pages are skipped by default,
although it is possible to not to skip them by setting `_skip: False`.

» `is_dir`
----------

> Boolean

True if the current node is associated to a directory in disk and False if it is
associated to a file.

» `is_index`
------------

> Boolean

`index.html` pages inside the site are special as they represent the HTML
content of the folder that contains them. By default, index pages are skipped
during any tree traversal operation, but you can mark them to not to be skipped
using `_skip: False` and you can use this property to know if a given node is
associated or not with an index page.

Data
----

» `data`
--------

> Dictionary

All the values defined or inherited by this node. For example, if a node defines
a variable `foobar`, then you can access it with `some_node.data["foobar"]`. For
the current node being rendered in a template (`_node`), you can access the data
directly without having to access this dictionary. For example, if it defines a
variable `foobar`, you can access it with either `{{ foobar }}` or 
`_node.data["foobar"]`.

» `user_data`
-------------

> Dictionary

Same as `data` but the dictionary doesn't include special values starting with
an underscore (`_`).

Content
-------

!!! note

    Content attributes are only available once a node has been fully processed
    since they are populated using the node's Markdown, reStructuredText or HTML
    body. In practice, this is usually not a problem since these attributes are
    most frequently used within templates. When templates are rendered all nodes
    have been completely processed already. However, if you access these
    attributes from the Markdown, reStructuredText or HTML body of another node,
    there's no guarantee that the attribute will be available. For example, if
    you have {% raw %}`{{ some_other_node.content }}`{% endraw %} included in
    the Markdown body of a node, you'll get an error if `some_other_node` hasn't
    been processed yet.

» `content`
-----------

> String

Content of the page represented by the node. This attribute is populated in
different ways depending on the format of its associated file:

* For **Markdown** and **reStructuredText** files, `content` holds the result of
  converting these formats to HTML. Take into account that this HTML doesn't
  contain any layout related HTML such as including `<html>`, `<head>` or
  `<body>` —which should be part of the template used to generate the final
  page. Any Jinja constructs in the body of the file are resolved before
  `content` is populated.

* For **HTML** files, `content` holds the raw HTML as is present in the file.
  Any Jinja constructs in the body of the file are resolved before `content` is
  populated.

* For **JSON** and **YAML** files, the value of `content` can be set by using
  the `_content` special variable.

`content` is an important attribute of the node object. In most cases,
generating a page of the site implies inserting `_node.content` in the layout
set by the template that is being used.

» `src_text`
------------

> String

Raw text of the file associated to this node. For example, if this node
represents a Markdown file, `src_text` will contain the Markdown body itself
(if the file contains a front-matter, that is *not* included).

» `toc`
-------

> List of dictionaries

Table of contents of the `content` of the current node. This attributed is
generated for nodes associated to Markdown, reStructuredText and HTML files.
The table of contents is represented by a list of dictionaries with a structure
similar to this:

    [
      {
        "level": 1,
        "id": "title-1",
        "name": "Title 1",
        "children": [
          {
            "level": 2,
            "id": "title-2",
            "name": "Title 2",
            "children": []
          },
          …
      },
      …
    ]

Paths
-----

» `src_path`
------------

> String

Absolute path of the input file associated to this node.

» `relative_src_path`
---------------------

> String

Path of the input file associated from this node relative to its input
directory. For example, if the input file is
`~/projects/project/content/a-folder/a-file.md` (and `content/` is the input
directory), `relative_src_path` will be `a-folder/a-file.md`.

» `relative_dst_path`
---------------------

> String

Path of the output file associated from this node relative to the output
directory. For example, if the input file is
`~/projects/project/content/a-folder/a-file.md` (and `content/` is the input
directory and the action is to convert Markdown to HTML), `relative_dst_path`
will be `a-folder/a-file.html`.


Relationships
-------------

» `root`
--------

> Node

Root node of the site. Represents both the output directory and the `/` URL.

» `parent`
----------

> Node

Parent node of current one. A parent node is always a directory.

» `children`
------------

> List of nodes

Sorted list with the children of current node.

» `prev`
--------

> Node

Previous node to current one according to preorder traversal of the site tree.

» `next`
--------

> Node

Next node to current one according to preorder traversal of the site tree.

» `prev_sibling`
----------------

> Node

Previous sibling. Children of a node are always sorted.

» `next_sibling`
----------------

> Node

Next sibling. Children of a node are always sorted.


Traversing functions
--------------------

» `is_descendant_of(node)`
--------------------------

> Boolean

Returns whether a node is a descendant than a given one.

For example, if a site defines its sections by the first level of nodes below
the root, to highlight the section that the current page belongs to, you can do
something like:
{%- raw %}
```
{% for top_menu_node in _node.root.children %}
  {% with link_class = 'active' if _node.is_descendant_of(top_menu_node) else 'normal' %}
    <a class="{{ link_class }}" href="{{ top_menu_node.url }}">
      {{ top_menu_node.title }}
    </a>
  {% endwidth %}
{% endfor %}
```
{%- endraw %}

» `traverse()`
--------------

> Iterable of nodes

Allows to iterate through all the descendant nodes to the current one in
preorder traversal.

To iterate through all the nodes of the site, use:
{%- raw %}
```
{% for node in _node.root.traverse() %}
…
{% endfor %}
```
{%- endraw %}

`traverse()` skips all index nodes (`index.html`) and nodes marked with `_skip:
true`.

» `traverse_all()`
--------------

> Iterable of nodes

Like `traverse()` but it doesn't skip index nodes or nodes marked with `_skip:
true`.
