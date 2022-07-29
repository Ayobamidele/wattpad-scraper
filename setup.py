from setuptools import setup, find_packages

# requerments.txt path
req_file = 'requerments.txt'
with open(req_file) as f:
    requirements = f.read().splitlines()


classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
]

setup(
    name='wattpad-scraper',
    version='0.0.11',
    description='Easy to use wattpad scraper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/shhossain/wattpad-scraper',
    author='Shafayat Hossain Shifat',
    author_email='hossain0338@gmail.com',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=requirements,
)