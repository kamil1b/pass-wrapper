import subprocess
import pytest
from pass_wrapper.wrapper import pass_wrapper


@pytest.fixture
def mock_subprocess(monkeypatch, subprocess_config):
    def mock_run(*args, **kwargs):
        subprocess_config["args"] = args[0]
        subprocess_config["kwargs"] = kwargs
        return subprocess.CompletedProcess(
            args=args, returncode=0, stdout=subprocess_config["stdout"]
        )

    monkeypatch.setattr(subprocess, "run", mock_run)


@pytest.mark.parametrize("subprocess_config", [{"stdout": ""}])
def test_wrapper_wrapp_parameter_of_pass(mock_subprocess, subprocess_config):
    pass_wrapper("find")
    assert subprocess_config["args"] == ["pass", "find"]


@pytest.mark.parametrize("subprocess_config", [{"stdout": ""}])
def test_wrapper_wrap_parameters_of_pass(mock_subprocess, subprocess_config):
    pass_wrapper("www.web.com", "-q")
    assert subprocess_config["args"] == ["pass", "www.web.com", "-q"]


@pytest.mark.parametrize("subprocess_config", [{"stdout": "something_result"}])
def test_wrapper_wrap_capture_output(mock_subprocess, subprocess_config):
    result = pass_wrapper("something")
    assert "stdout" in subprocess_config["kwargs"]
    assert subprocess_config["kwargs"]["stdout"] == subprocess.PIPE
    assert ["something_result"] == result


@pytest.mark.parametrize("subprocess_config", [{"stdout": "something\nresult"}])
def test_extract_output_should_split_by_split_newline(
    mock_subprocess, subprocess_config
):
    result = pass_wrapper("something")
    assert ["something", "result"] == result


@pytest.mark.parametrize(
    "subprocess_config", [{"stdout": "   something   \n   result   "}]
)
def test_extract_output_should_contain_only_text(mock_subprocess, subprocess_config):
    result = pass_wrapper("something")
    assert ["something", "result"] == result
