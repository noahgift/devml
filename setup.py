import sys
if sys.version_info < (3,6):
    sys.exit('Sorry, Python < 3.6 is not supported')

from setuptools import setup

from devml import __version__

setup(
    name='devml',
    version=__version__,
    url='https://github.com/pallets/flask/',
    license='MIT',
    author='Noah Gift',
    author_email='consulting@noahgift.com',
    description="""Machine Learning, Statistics and Utilities around Developer Productivity, 
        Company Productivity and Project Productivity""",
    long_description="""
    Machine Learning, Statistics and Utilities around Developer Productivity

    A few handy bits of functionality:

    Can checkout all repositories in Github
    Converts a tree of checked out repositories on disk into a pandas dataframe
    Statistics on combined DataFrames
    """,
    packages=['devml'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'pandas',
        'click',
        'PyGithub',
        'gitpython',
        'sensible',
        'scipy',
        'numpy',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points='''
        [console_scripts]
        dml=dml:cli
    '''
)