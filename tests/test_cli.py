import pytest
from click.testing import CliRunner
from unittest.mock import patch
from edl.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestStatus:
    def test_not_logged_in(self, runner):
        with patch("edl.cli.is_logged_in", return_value=False):
            result = runner.invoke(cli, ["status"])
            assert result.exit_code == 0
            assert "not logged in" in result.output

    def test_logged_in(self, runner):
        with patch("edl.cli.is_logged_in", return_value=True), \
             patch("edl.cli.get_stored_username", return_value="testuser"):
            result = runner.invoke(cli, ["status"])
            assert result.exit_code == 0
            assert "testuser" in result.output


class TestLogout:
    def test_not_logged_in(self, runner):
        with patch("edl.cli.get_stored_username", return_value=None):
            result = runner.invoke(cli, ["logout"])
            assert "not logged in" in result.output

    def test_logout_success(self, runner):
        with patch("edl.cli.get_stored_username", return_value="testuser"), \
             patch("edl.cli.delete_credentials", return_value=True):
            result = runner.invoke(cli, ["logout"])
            assert "logged out" in result.output


class TestDl:
    def test_download_called(self, runner):
        with patch("edl.cli.download", return_value=True) as mock_dl, \
             patch("edl.cli.get_credentials", return_value=(None, None)):
            result = runner.invoke(cli, ["dl", "https://youtube.com/watch?v=test"])
            assert mock_dl.called
            assert result.exit_code == 0

    def test_download_failure_exits_1(self, runner):
        with patch("edl.cli.download", return_value=False), \
             patch("edl.cli.get_credentials", return_value=(None, None)):
            result = runner.invoke(cli, ["dl", "https://youtube.com/watch?v=test"])
            assert result.exit_code == 1
