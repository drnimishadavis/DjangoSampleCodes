from setuptools import setup, find_packages
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()
setup(
    name='django_page_hit_counter',
    version='0.1',
    description='Simple Django page hit counter',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/drnimishadavis/djangopagehitcounter',
    author='Nimisha Davis',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=['Django>=3.2'],
    classifiers=['Framework :: Django','Programming Language :: Python :: 3'],
)
