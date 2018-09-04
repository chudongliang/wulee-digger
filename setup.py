"""
setup
"""
import setuptools

setuptools.setup(
    name='wulee-digger',
    packages=['wulee-digger'], # this must be the same as the name above
    version='1.1',
    description='A random test lib',
    author='chudongliang',
    author_email='chudongliang@gmail.com',
    url='https://github.com/peterldowns/mypackage', # use the URL to the github repo
    download_url='https://github.com/peterldowns/mypackage/archive/0.1.tar.gz', # I'll explain this in a second
    keywords=['testing', 'logging', 'example'], # arbitrary keywords
    include_package_data=True,
    install_requires=[
        'jinja2',
        'requests_oauth',
    ],
    classifiers=[],
)
