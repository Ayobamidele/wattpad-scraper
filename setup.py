from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
]

setup(
    name='wattpad-scraper',
    version='0.0.5',
    description='Easy to use wattpad scraper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shhossain/wattpad-scraper',
    author='Shafayat Hossain Shifat',
    author_email='hossain0338@gmail.com',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=[
        'cloudscraper',
        'bs4',
    ]
)