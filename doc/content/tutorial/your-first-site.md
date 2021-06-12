
Your First Site
===============

The folder structure of a Spekulatio project is very simple, just create a
folder for your new site and add two directories: `content` and `build`:

    my-site/
    ├── build/    # your site will be generated here
    └── content/  # here's where you'll put your content files

Now, let's add a page to the site. Create a `content/index.md` file with any
Markdown content that you want. For example, something like:

    My New Site
    ===========

    With some **incredible** content.

And we are ready to go. Execute the following commands in your terminal at the
root of your project (eg. inside `my-site/`):

    spekulatio build
    spekulatio serve

As you can imagine, the first one generates your site and the second one
launches a HTTP server that serves your files at [http://localhost:8000](http://localhost:8000).

If you open a browser at that address, you'll get something like:

![My first site](/static/img/tutorial/first-site.png){.mid .shadow}

!!! note

    There's no `init` command to initialize a project in Spekulatio since all it
    is necessary are those two folders.

