[![CircleCI](https://circleci.com/gh/noahgift/devml.svg?style=svg)](https://circleci.com/gh/noahgift/devml)

# devml
Machine Learning, Statistics and Utilities around Developer Productivity

A few handy bits of functionality:

* Can checkout all repositories in Github
* Converts a tree of checked out repositories on disk into a pandas dataframe
* Statistics on combined DataFrames

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

```python
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

