---
_alias: built-in-templates
article_classes: reference-page
---

Built-in Templates
==================

Spekulatio includes some templates for you to use out of the box. This is the
complete list.

If you define a template yourself with the same name as any of these, the newly
defined one will override the built-in one.

» `content.html`
----------------

This template just renders the content of `_node.content` directly without
adding anything else to the page. For instance, if the source file for the page
is Markdown, the output will be the raw result of directly converting the
Markdown text to HTML (without any layout tags such as `head`, `body`,
`section`, ...).

That is, the template itself is just:

    {{ _node.content }}

It is mostly intended for debugging purposes.

Example:
```
---
_template: content.html
---

My Markdown File
================

This is just a bit of example content.
```

» `debug.html`
--------------

This template displays all values defined for this page. If you need to know if
a given value is defined for a given page or what's the structure of a nested
value, you can just switch the page template to `_template: debug.html`
temporarily and inspect the available values.

It looks something like this:

![debug.html template](/static/img/docs/debugging-template.png){.mid .shadow}

» `default.html`
----------------

This is a very minimal template that adds a HTML5 wrapper to the content of the
of the page being rendered. This is the template used by default when no
`_template` value is defined.

The whole template is:
{%- raw %}
```
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>{{ _node.title }}</title>
    </head>
    <body>
        {{ _node.content }}
    </body>
</html>

```
{%- endraw %}

