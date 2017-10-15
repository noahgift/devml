[![CircleCI](https://circleci.com/gh/noahgift/devml.svg?style=svg)](https://circleci.com/gh/noahgift/devml)

# devml
Machine Learning around Developer Productivity and Github Utilities

A few handy bits of functionality:

* Can checkout all repositories in Github
* Converts a tree of checked out repositories on disk into a pandas dataframe
* Statistics on combined DataFrames

## Expected Configuration

The command-line tools expects for you to create a project directory with a config.json file.
Inside the config.json file, you will need to provide an oath token.  You can find information about how to do that here:  https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/.

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

```bash

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
