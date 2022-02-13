---
_alias: adding-code-blocks
---

Adding Code Blocks
==================

You can add code examples or code blocks to your pages using the standard syntax
according to the file you're editing:

_Markdown_

    ```
    <!DOCTYPE html>
    <html>
      <body>
        <h1>Some HTML</h1>
      </body>
    </html>
    ```

_reStructuredText_

    .. code-block::

        <!DOCTYPE html>
        <html>
          <body>
            <h1>Some HTML</h1>
          </body>
        </html>

Syntax Highlighting
-------------------

Spekulatio also support syntax highlighting in code blocks out of the box
thanks to the [Pygments](https://pygments.org/) library. To enable it,
you only have to specify the programming or markup language of the code block.
You can check the [complete list of supported languages][supported-languages]
in the Pygments site.

[supported-languages]: https://pygments.org/languages/

_Markdown_

Add the language name after the triple quotes:

    ``` html
    <!DOCTYPE html>
    <html>
      <body>
        <h1>Some HTML</h1>
      </body>
    </html>
    ```

_reStructuredText_

Add the language name after `code-block` and add the `codehilite` class too:

    .. code-block:: html
        :class: codehilite

        <!DOCTYPE html>
        <html>
          <body>
            <h1>Some HTML</h1>
          </body>
        </html>

