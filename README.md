[![CircleCI](https://circleci.com/gh/noahgift/devml.svg?style=svg)](https://circleci.com/gh/noahgift/devml)

# devml
Machine Learning, Statistics and Utilities around Developer Productivity

A few handy bits of functionality:

* Can checkout all repositories in Github
* Converts a tree of checked out repositories on disk into a pandas dataframe
* Statistics on combined DataFrames

## Explore Jupyter Notebooks on Github Organizations

You can explore combined datasets here using this example as a starter:

https://github.com/noahgift/devml/blob/master/notebooks/github_data_exploration.ipynb

![Pallets Project](https://user-images.githubusercontent.com/58792/31581904-66ee7fc0-b12a-11e7-804a-7b0f1728f30a.png)

## Explore Jupyter Notebooks on Repository Churn

#### All Files Churned by type:

You can explore File Metadata exploration example here: 

https://github.com/noahgift/devml/blob/master/notebooks/repo_file_exploration.ipynb

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

## Advanced CLI:  Get Activity Statistics for a Tree of Checkouts or a Checkout and sort

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





