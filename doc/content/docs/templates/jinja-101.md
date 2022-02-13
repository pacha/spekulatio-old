---
_alias: jinja-101
---

Jinja 101
=========

Spekulatio uses the [Jinja library](https://jinja.palletsprojects.com/) to power
its templates. It is very flexible and mature and offers a great deal of
features. The most basic one is interpolating a variable:

{% raw %}
```html
<div class="author">{{ author }}</div>
```
{% endraw %}

That will be rendered, in our example, as:
```html
<div class="author">me</div>
```

However, Jinja offers much more including conditional statements, loops over
values, definition of reusable blocks and so on. You can find the documentation
of the possibilities it offers at:

[https://jinja.palletsprojects.com/en/3.0.x/templates/](https://jinja.palletsprojects.com/en/3.0.x/templates/)

The documentation is very complete and easy to follow, but let's cover here some
basic elements.

Delimiters
----------

To use Jinja constructs, use the following delimiters:

{% raw %}
* `{{ … }}` for expressions (eg. like interpolating the value of a variable)
* `{% … %}` for statements (eg. `if` or `for` loops)
* `{# … #}` for comments. These, unlike HTML comments, won't appear in the final
  rendered pages.
{% endraw %}

Variable interpolation
----------------------

Consider a set of variables of different kinds:
```
a_scalar: foo
a_list:
  - one
  - two
a_dictionary:
  one:
    two: true
```
You can show their values with the double curly brace notation we saw before
{% raw %}`{{ … }}`{% endraw %}:
{% raw %}
```html
<span>This is a scalar: {{ a_scalar }}</span>
<span>This is an element in a list {{ a_list[2] }}</span>
<span>This is an element in a dictionary {{ a_dictionary.one.two }}</span>
```
{% endraw %}
Also, you can apply _filters_ to the values using pipes:
{% raw %}
```html
<span>This is a scalar: {{ a_scalar|upper }}</span>
```
{% endraw %}
The list of all available built-in filters is available
[here](https://jinja.palletsprojects.com/en/3.0.x/templates/#list-of-builtin-filters).

If Statements
-------------

You can conditionally render parts of your HTML with `if` statements:
{% raw %}
```
{% if <expresion> %} … {% endif %}
```
{% endraw %}

For example, if you have values defined as:
```
category: foo
show_banner: true
```
Then you can use them as follows:
{% raw %}
```html
<!DOCTYPE html>
<html>
    <head>
        {% if category == 'foo' %}
        <link rel="stylesheet" href="static/css/special-styles.css">
        {% endif %}
    </head>
    <body>
        {% if show_banner %}
        <div class="banner">
            …
        </div>
        {% endif %}
    </body>
</html>
```
{% endraw %}

For Loops
---------

If you define lists, you can iterate through them using:
{% raw %}
```
{% for <variable> in <iterable> %} … {% endfor %}
```
{% endraw %}
For example, giving this list:
```
authors:
  - Mary
  - John
  - Sam
```
Then you can iterate over it like this:
{% raw %}
```html
<!DOCTYPE html>
<html>
    <body>
        <ul class="authors">
            {% for author in authors %}
            <li>{{ author }}</li>
            {% endfor %}
        </ul>
    </body>
</html>
```
{% endraw %}

Template Inheritance and Includes
---------------------------------

In almost every site, there are parts of the layout that are reused across
different pages. Headers, sidebars or footers are the most common usual cases.
If your site uses one single template for every page then reusing those
components is very straightforward. You add them to the template and every page
will show them. However, if you have a more complex site, you may want to have
different layouts that still share some components. For instance, you may want
to have some pages displaying an one-column layout and others a two-column one,
while still keeping the same header and footer.

To solve that problem you can use **template inheritance** in Jinja, which
allows you to specify that one template has to be based in another one but
replacing only parts of it.

To illustrate it, imagine that we have the following `templates` folder:

    templates/
    ├── base.html
    ├── one-column.html
    └── two-columns.html

Then `base.html` can contain all the common elements to every page:
{% raw -%}
```
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="static/css/styles.css">
        <title>My Site</title>
    </head>
    <body>
        <header> … </header>

        {% block main %}
        {% endblock %}

        <footer> … </footer>
    </body>
</html>
```
{%- endraw %}

And the other two templates may just define how the `main` block should look
like. For example, `two-columns.html` could be:
{% raw -%}
```
{% extends "base.html" %}

{% block main %}
<main class="two-cols">
    <article>
      ...
    </article>

    <aside>
      ...
    </aside>
</main>
{% endblock main %}
```
{%- endraw %}

Child templates can define more than a single block like we did in this example.
To know more about the possibilities, check the [Template
Inheritance](https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance)
section of Jinja's documentation.

