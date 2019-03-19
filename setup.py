
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spekulatio",
    version="0.9.0",
    author="Andrés Sopeña Pérez",
    author_email="asopena@ehmm.org",
    description="A simple but flexible static site generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pacha/spekulatio",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Click>=7.0",
        "frontmatter>=3.0.5",
        "Jinja2>=2.10",
        "pyScss>=1.3.5",
        "PyYAML>=3.13",
        "rst2html5>=1.10.1",
    ],
    entry_points={
        'console_scripts': ['spekulatio=spekulatio.commands:create_site'],
    }
)

