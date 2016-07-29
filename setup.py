from setuptools import setup, find_packages

version = '0.2'

setup(
    name='ever2text',
    version=version,
    description=(
        "Convert Evernote exports to text files"),
    long_description=(
        open("README.rst").read() +
        '\n\n' +
        open("HISTORY.rst").read()
    ),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords='note taking migration',
    author='Nicholas Kuechler',
    author_email='nicholaskuechler@nicholaskuechler.com',
    url='http://nicholaskuechler.com',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'lxml',
        'python-dateutil<2.0',
        'html2text',
        'beautifulsoup4',
    ],
    entry_points="""
    [console_scripts]
    ever2text = ever2text.core:main
    """,
    )
