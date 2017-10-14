import click
from click.testing import CliRunner

from dml import cli
from devml import __version__

def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert __version__ in result.output
