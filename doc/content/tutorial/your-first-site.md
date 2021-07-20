
Quick Start
===========

A Minimal Site
--------------

Let's set up a new site just to get a feeling on how Spekulatio
works. Create a directory for your new project with two
subdirectories: `content` and `build`.

    my-site/
    ├── build/    # your site will be generated here
    └── content/  # here's where you'll put your content files

Now, let's add the first page of the site. Create a `content/index.md` file with
any Markdown content that you want:

    Hello World
    ===========

    A new site with some **incredible** content.

And this is all we need for now. We can now generate the first version of the
site. To do so, execute:

    spekulatio build

at the root of the project folder (eg. inside `my-site` in this case).

Then, to see the result, you can start a HTTP development server by executing:

    spekulatio serve

Now, your site should be available at
[http://localhost:8000](http://localhost:8000). So if you open that address in a
browser you'll see something like:

![My first site](/static/img/tutorial/first-site.png){.mid .shadow}

Well the site doesn't look super sophisticated, but it is a start. Let's add now
some HTML and styles.

Adding Templates
----------------

Add a new subdirectory `templates` to your project:

    my-site/
    ├── build/
    ├── content/
    └── templates/  # difficult to believe... but template files go here

Now, add a new HTML file inside it. We'll call it `layout.html`, but you can use any
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

You can create any HTML that you want. As you can see, there are two
placeholders being used. Once you use this template to render a content file (a
Markdown or Restructured Text one for example) they will be replaced by:

  * `{{ _title }}`: top level title of your content file (eg. "Hello World" for
    the Markdown file we used above).

  * `{{ _content }}`: the content of the file already converted to HTML.

