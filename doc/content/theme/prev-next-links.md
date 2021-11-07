
Previous and Next Links
=======================

You can optionally have links to the previous and next pages displayed at the
bottom of the current one:

TODO: add image of 

This is particularly interesting for sequences of pages or tutorials with
multiple steps that are intended to be read one after another.

For a page to display the links, it is necessary that it has the variable
`prev_next_links` set to `true` (by default the value is `false`). Since you
usually want to set this value to `true` for a collection of pages, you can
add:

    prev_next_links: true

to the `_values.yaml` file inside the parent directory that contains all them.
This will set the value to `true` for all descendants, including the index page
of the directory. If you want to exclude that one, just set the value to `false`
in its front matter.

!!! Note

    The `prev_next_links` variable is also checked in the previous and next
    pages themselves to see if the links for them have to be displayed. For
    example, consider the following scenario:

        current page  →  prev_next_links: true
        previous page →  prev_next_links: true
        next page     →  prev_next_links: false

    In that case, the `prev_next_links` is shown in the current page, but only
    the link to the previous page will be shown. The link to the next one won't
    because the value is set to false there.

