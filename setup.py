from distutils.core import setup

install_requires=[
    "httplib2 >= 0.7.0",
    "mwparserfromhell >= 0.1.1",
    "tornado >= 3.1",
],

setup(
    name = 'bwikibot',
    packages = [
        'bwikibot',
        'bwikibot.extensions',
        'bwikibot.spell',
    ],
    package_data = {
        'bwikibot.spell': ['*.txt'],
    },
    version = "1.0.0",
    description = "Simple mediawiki robot",
    author = "Taras Bunyk",
    author_email = "tbunyk@gmail.com",
    url = "https://github.com/bunyk/bwikibot",
    license='LICENSE.txt',
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Internet :: WWW/HTTP",
    ],
    long_description = open('README.md').read(),
    install_requires=install_requires,
    entry_points=dict(console_scripts=[
        'bwikibot=bwikibot.cli:main',
    ]),
)
