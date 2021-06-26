
Your First Site
===============

Hello World
-----------

To create a new project, you only need to create a root directory and two
subdirectories: `content` and `build`.

    my-site/
    ├── build/    # your site will be generated here
    └── content/  # here's where you'll put your content files

Now, let's add a page to the site. Create a `content/index.md` file with any
Markdown content that you want:

    Hello World
    ===========

    A new site with some **incredible** content.

And we are ready to go. At the root of your project (in this case, inside
`my-site/`), generate your site by executing the `build` subcommand:

    spekulatio build

Then, to see the result, you can start a HTTP development server by executing:

    spekulatio serve

Now, your site should be available at
[http://localhost:8000](http://localhost:8000). So if you open that address in a
browser you'll see something like:

![My first site](/static/img/tutorial/first-site.png){.mid .shadow}

Granted, the site looks rather modest, so let's add some HTML and styles.

!!! Note

    foooo bar

Adding a template
-----------------

Add a new subdirectory `templates` to your project:

    my-site/
    ├── build/
    ├── content/
    └── templates/  # I know, difficult to believe, but template files go here

Now, add a new HTML file inside. We'll call it `layout.html`, but you can use any
name you want:

    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>{{ _title }}</title>
        </head>
        <body>
            {{ _content }}
        </body>
    </html>

There are no restrictions on how the HTML must look like
