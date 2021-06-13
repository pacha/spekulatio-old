---

foobar: 67

---

Adding Data
===========

TODO

This is just a number: {{ foobar }}. And this is just text.

And this is another variable: {{ now_as('%Y') }}.

And this is a link to another node [{{ _node.next_sibling.title }}]({{ _node.next_sibling.url }}).
