import click
from click.testing import CliRunner
import imp
from devml import __version__

dml = imp.load_source("dml", "dml")

def test_cli():
    runner = CliRunner()
    result = runner.invoke(dml.cli, ['--version'])
    assert __version__ in result.output
