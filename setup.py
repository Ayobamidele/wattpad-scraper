from setuptools import setup, find_packages

# requerments.txt path
req_file = 'requirements.txt'
with open(req_file) as f:
    requirements = f.read().splitlines()

readme_file = 'README.md'
with open(readme_file) as f:
    readme = f.read()

changes_log_file = 'CHANGELOG.md'
with open(changes_log_file) as f:
    changes_log = f.read()

recent_changes_file = 'RECENTCHANGELOG.md'
with open(recent_changes_file) as f:
    recent_changes = f.read()

long_description = readme + '\n\n' +"# RECENT CHANGES\n" + recent_changes + '\n\n' + changes_log

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Libraries :: Web Services',
    'Topic :: Utilities',
]

setup(
    name='wattpad-scraper',
    version='0.0.25',
    description='Get wattpad stories and chapters, and download them as ebook',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shhossain/wattpad-scraper',
    author='Shafayat Hossain Shifat',
    author_email='hossain0338@gmail.com',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=requirements,
)