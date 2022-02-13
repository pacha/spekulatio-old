---
_alias: template-functions
---

Template Functions
==================

Spekulatio offers some helper functions that you can use in your templates.
Here, you can find the full list of them together with their description.

» `get_node(url)`
-----------------

Get a node of the site given its URL. You can use it to access nodes that are
not direct relatives of the current node.

Example:

{% raw -%}
```
{% with some_node = get_node('/some/folder') %}
  <p>The child pages of {{ some_node.title }} are:</p>
  <ul>
    {% for child in some_node.children %}
    <li><a href="{{ child.url }}">{{ child.title }}</a></li>
    {% endfor %}
  </ul>
{% endwith %}
```
{%- endraw %}

It is possible to get a node using its alias too, using:

    get_node(alias='some-alias')

» `get_url(alias)`
------------------

Get the URL of a page given its alias.

Example:
{% raw -%}
```
<a href="{{ get_url('configuration-page') }}">Configuration</a>
```
{%- endraw %}

» `now_as(format)`
------------------

Write the current date (at build time) in the given format.

Example:
{% raw -%}
```
<p>Last updated: {{ now_as('%Y-%m-%d') }}</p>
```
{%- endraw %}


TODO

» `print_as_json(dictionary)`
-----------------------------

Dump the content of the given dictionary as JSON formatted output.

Example:
{% raw -%}
```
<pre>
<code>
{{ print_as_json(my_dictionary) }}</p>
</code>
</pre>
```
{%- endraw %}

This is mainly intended for debugging purposes. To get a full dump of all values
defined in one node you can use the [debug built-in template]({{
get_url('built-in-templates') ~ '#debughtml' }}) instead.


