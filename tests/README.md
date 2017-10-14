#Tests and Linting

##Overview

##Pytest
The testing framework used [pytest](http://docs.pytest.org/en/latest/).  It has quite a few cool features I am using.  Here are a few:

* Support for annotating tests to divide them up.  An example of this in action is [here](https://github.com/noahgift/meta_machine_intelligence/blob/master/tests/test_dynamo.py).  I mark these as integration so I can exclude them for regular test runs.

* xml coverage reporting so jenkins can see output:
  
    `@cd tests; PYTHONPATH=.. pytest -vv --cov=dml --cov=devml --cov=aws --cov=ctl --cov=mworker *.py --cov-report xml`

##Linting
The linting framework used is pylint.  It is a PITA unless you configure it to only show you warning and errors.  This is accomplished as follows:

    pylint --disable=R,C devml dml aws ctl mworker

Note, each new library or script has to be added to the pylint output.

##Running everything (linting and testing all in one go):
    
    make all

This first lints, and if there are no warnings or errors, then it runs unit tests and/or integration tests.  Almost never have I regretted not being able to checkin code with warnings.
