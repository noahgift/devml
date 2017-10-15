[![CircleCI](https://circleci.com/gh/noahgift/devml.svg?style=svg)](https://circleci.com/gh/noahgift/devml)

# devml
Machine Learning, Statistics and Utilities around Developer Productivity

A few handy bits of functionality:

* Can checkout all repositories in Github
* Converts a tree of checked out repositories on disk into a pandas dataframe
* Statistics on combined DataFrames

## Get environment setup

#### An easy way to run the project locally is to check the repo out and in the root of the repo run:

```bash
make setup
```
This create a virtualenv in  ~/.devml

#### Next, source that virtualenv:

```bash
source ~/.devml/bin/activate
```

#### Run Make All (installs, lints and tests)
```bash
make all

# #Example output
#(.devml) ➜  devml git:(master) make all                    
#pip install -r requirements.txt
#Requirement already satisfied: pytest in /Users/noahgift/.devml/lib/python3.6/site-packages (from -r requirements.txt (line #1)
---------- coverage: platform darwin, python 3.6.2-final-0 -----------
Name                       Stmts   Miss  Cover
----------------------------------------------
devml/__init__.py              1      0   100%
devml/author_stats.py          6      6     0%
devml/fetch_repo.py           54     42    22%
devml/mkdata.py               84     21    75%
devml/org_stats.py            76     55    28%
devml/post_processing.py      50     35    30%
devml/state.py                29      9    69%
devml/stats.py                55     43    22%
devml/ts.py                   29     14    52%
devml/util.py                 12      4    67%
dml.py                       111     66    41%
----------------------------------------------
TOTAL                        507    295    42%
....
```

You don't use virtualenv or don't want to use it.  No problem, just run `make all` it should probably work if you have python 3.6 installed.

```bash

make all
```


## Explore Jupyter Notebooks on Github Organizations

You can explore combined datasets here using this example as a starter:

https://github.com/noahgift/devml/blob/master/notebooks/github_data_exploration.ipynb

![Pallets Project](https://user-images.githubusercontent.com/58792/31581904-66ee7fc0-b12a-11e7-804a-7b0f1728f30a.png)

## Explore Jupyter Notebooks on Repository Churn

You can explore File Metadata exploration example here: 

https://github.com/noahgift/devml/blob/master/notebooks/repo_file_exploration.ipynb

#### All Files Churned by type:
![Pallets Project Relative Churn by file type](https://user-images.githubusercontent.com/58792/31587879-59d9724e-b19e-11e7-942e-999c02d7b566.png)

#### Summary Churn Statistics by type:

![Pallets Project by file type Churn statistics](https://user-images.githubusercontent.com/58792/31587931-5d79199e-b19f-11e7-89c2-98185fdef909.png)

## Expected Configuration

The command-line tools expects for you to create a project directory with a config.json file.
Inside the config.json file, you will need to provide an oath token.  You can find information about how to do that here:  https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/.

Alternately, you can pass these values in via the python API or via the command-line as options.
They stand for the following:

* org:  Github Organization (To clone entire tree of repos)
* checkout_dir:  place to checkout 
* oath:  personal oath token generated from Github

```bash
➜  devml git:(master) ✗ cat project/config.json 
{
    "project" : 
        {
            "org":"pallets",
            "checkout_dir": "/tmp/checkout",
            "oath": "<keygenerated from Github>"
        }
    
}
```

## Basic command-line Usage

You can find out stats for a checkout or a directory full of checkout as follows

```bash

python dml.py gstats author --path ~/src/mycompanyrepo(s)
Top Commits By Author:                     author_name  commits
0                     John Smith     3059
1                      Sally Joe     2995
2                   Greg Mathews     2194
3                 Jim Mayflower      1448
```

## Basic API Usage (Converting a tree of repo(s) into a pandas DataFrame)

```python
In [1]: from devml import (mkdata, stats)

In [2]: org_df = mkdata.create_org_df(path=/src/mycompanyrepo(s)")
In [3]: author_counts = stats.author_commit_count(org_df)

In [4]: author_counts.head()
Out[4]: 
      author_name  commits
0       John Smith     3059
1        Sally Joe     2995
2     Greg Mathews     2194
3    Jim Mayflower     1448
4   Truck Pritter      1441

```

## Clone all repos in Github using API

```ipython
In [1]: from devml import (mkdata, stats, state, fetch_repo)

In [2]: dest, token, org = state.get_project_metadata("../project/config.json")
In [3]: fetch_repo.clone_org_repos(token, org, 
        dest, branch="master")
017-10-14 17:11:36,590 - devml - INFO - Creating Checkout Root:  /tmp/checkout
2017-10-14 17:11:37,346 - devml - INFO - Found Repo # 1 REPO NAME: flask , URL: git@github.com:pallets/flask.git 
2017-10-14 17:11:37,347 - devml - INFO - Found Repo # 2 REPO NAME: pallets-sphinx-themes , URL: git@github.com:pallets/pallets-sphinx-themes.git 
2017-10-14 17:11:37,347 - devml - INFO - Found Repo # 3 REPO NAME: markupsafe , URL: git@github.com:pallets/markupsafe.git 
2017-10-14 17:11:37,348 - devml - INFO - Found Repo # 4 REPO NAME: jinja , URL: git@github.com:pallets/jinja.git 
2017-10-14 17:11:37,349 - devml - INFO - Found Repo # 5 REPO NAME: werkzeug , URL: git@githu
In [4]: !ls -l /tmp/checkout
total 0
drwxr-xr-x  21 noahgift  wheel  672 Oct 14 17:11 click
drwxr-xr-x  25 noahgift  wheel  800 Oct 14 17:11 flask
drwxr-xr-x  11 noahgift  wheel  352 Oct 14 17:11 flask-docs
drwxr-xr-x  12 noahgift  wheel  384 Oct 14 17:11 flask-ext-migrate
drwxr-xr-x   8 noahgift  wheel  256 Oct 14 17:11 flask-snippets
drwxr-xr-x  14 noahgift  wheel  448 Oct 14 17:11 flask-website
drwxr-xr-x  18 noahgift  wheel  576 Oct 14 17:11 itsdangerous
drwxr-xr-x  23 noahgift  wheel  736 Oct 14 17:11 jinja
drwxr-xr-x  18 noahgift  wheel  576 Oct 14 17:11 markupsafe
drwxr-xr-x   4 noahgift  wheel  128 Oct 14 17:11 meta
drwxr-xr-x  10 noahgift  wheel  320 Oct 14 17:11 pallets-sphinx-themes
drwxr-xr-x   9 noahgift  wheel  288 Oct 14 17:11 pocoo-sphinx-themes
drwxr-xr-x  15 noahgift  wheel  480 Oct 14 17:11 website
drwxr-xr-x  25 noahgift  wheel  800 Oct 14 17:11 werkzeug
```

## Advanced CLI-Author:  Get Activity Statistics for a Tree of Checkouts or a Checkout and sort

```base
 ➜  devml git:(master) ✗ python dml.py gstats activity --path /tmp/checkout --sort active_days 

Top Unique Active Days:               author_name  active_days active_duration  active_ratio
86         Armin Ronacher          989       3817 days      0.260000
501  Markus Unterwaditzer          342       1820 days      0.190000
216            David Lord          129        712 days      0.180000
664           Ron DuPlain           78        854 days      0.090000
444         Kenneth Reitz           68       2566 days      0.030000
197      Daniel Neuhäuser           42       1457 days      0.030000
297          Georg Brandl           41       1337 days      0.030000
196     Daniel Neuhäuser           36        435 days      0.080000
450      Keyan Pishdadian           28        885 days      0.030000
169     Christopher Grebs           28       1515 days      0.020000
666    Ronny Pfannschmidt           27       3060 days      0.010000
712           Simon Sapin           22        793 days      0.030000
372           Jeff Widman           19        840 days      0.020000
427    Julen Ruiz Aizpuru           16         36 days      0.440000
21                 Adrian           16       1935 days      0.010000
569        Nicholas Wiles           14        197 days      0.070000
912                lord63           14        692 days      0.020000
756           ThiefMaster           12       1287 days      0.010000
763       Thomas Waldmann           11       1560 days      0.010000
628            Priit Laes           10       1567 days      0.010000
23        Adrian Moennich           10        521 days      0.020000
391  Jochen Kupperschmidt           10       3060 days      0.000000
```

## Advanced CLI-Churn:  Get churn by file type

#### Get the top ten files sorted by churn count with the extension .py: 

```bash
✗ python dml.py gstats churn --path /Users/noahgift/src/flask --limit 10 --ext .py
2017-10-15 12:10:55,783 - devml.post_processing - INFO - Running churn cmd: [git log --name-only --pretty=format:] at path [/Users/noahgift/src/flask]
                       files  churn_count  line_count extension  \
1            b'flask/app.py'          316      2183.0       .py   
3        b'flask/helpers.py'          176      1019.0       .py   
5    b'tests/flask_tests.py'          127         NaN       .py   
7                b'flask.py'          104         NaN       .py   
8                b'setup.py'           80       112.0       .py   
10           b'flask/cli.py'           75       759.0       .py   
11      b'flask/wrappers.py'           70       194.0       .py   
12      b'flask/__init__.py'           65        49.0       .py   
13           b'flask/ctx.py'           62       415.0       .py   
14  b'tests/test_helpers.py'           62       888.0       .py   

    relative_churn  
1             0.14  
3             0.17  
5              NaN  
7              NaN  
8             0.71  
10            0.10  
11            0.36  
12            1.33  
13            0.15  
14            0.07  
```
#### Get descriptive statistics for extension .py and compare to another repository

```bash
(.devml) ➜  devml git:(master) ✗ python dml.py gstats metachurn --path /Users/noahgift/src/flask --ext .py --statistic describe
2017-10-15 12:30:18,563 - devml.post_processing - INFO - Running churn cmd: [git log --name-only --pretty=format:] at path [/Users/noahgift/src/flask]
DESCRIPTIVE STATISTICS:

          churn_count                                                    \
                count       mean        std  min  25%  50%   75%    max   
extension                                                                 
.py             204.0  12.509804  30.449423  1.0  1.0  2.0  11.0  316.0   

          line_count            ...                 relative_churn           \
               count       mean ...     75%     max          count     mean   
extension                       ...                                           
.py             77.0  204.12987 ...   227.0  2183.0           77.0  0.23987   

                                                  
                std   min   25%   50%   75%  max  
extension                                         
.py        0.398271  0.01  0.06  0.13  0.24  2.5  

[1 rows x 24 columns]
(.devml) ➜  devml git:(master) ✗ python dml.py gstats metachurn --path /Users/noahgift/src/devml --ext .py --statistic describe
2017-10-15 12:30:47,543 - devml.post_processing - INFO - Running churn cmd: [git log --name-only --pretty=format:] at path [/Users/noahgift/src/devml]
DESCRIPTIVE STATISTICS:

          churn_count                                              line_count  \
                count      mean       std  min  25%  50%  75%  max      count   
extension                                                                       
.py              17.0  1.529412  0.799816  1.0  1.0  1.0  2.0  4.0       16.0   

                     ...                  relative_churn                       \
               mean  ...      75%     max          count     mean    std  min   
extension            ...                                                        
.py        158.8125  ...   122.25  1490.0           16.0  0.04125  0.045  0.0   

                                   
            25%   50%   75%   max  
extension                          
.py        0.02  0.02  0.06  0.18  

[1 rows x 24 columns]

```


