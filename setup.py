
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spekulatio",
    version="1.0.0",
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
        "Jinja2>=2.10",
        "libsass>=0.19.2",
        'pyyaml>=4.2b1',
        "rst2html5>=1.10.1",
        "markdown>=3.3.3",
        "coloredlogs>=15.0",
    ],
    extras_require={
        'dev': [
            'pytest',
            'black',
        ]
    },
    entry_points={
        'console_scripts': [
            'spekulatio=spekulatio.commands:spekulatio',
        ],
    }
)

