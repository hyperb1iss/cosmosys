import pytest
from colorama import Fore, Style

from cosmosys.color_schemes import ColorManager
from cosmosys.config import ColorScheme, CosmosysConfig, ProjectConfig


@pytest.fixture
def default_config():
    return CosmosysConfig(
        project=ProjectConfig(name="TestProject", repo_name="test/repo", version="1.0.0"),
        color_scheme="default",
    )


@pytest.fixture
def custom_config():
    return CosmosysConfig(
        project=ProjectConfig(name="TestProject", repo_name="test/repo", version="1.0.0"),
        color_scheme="custom",
        custom_color_schemes={
            "custom": ColorScheme(
                primary="blue",
                secondary="green",
                success="cyan",
                error="red",
                warning="yellow",
                info="magenta",
            )
        },
    )


def test_default_color_scheme(default_config):
    color_manager = ColorManager(default_config)
    assert color_manager.current_scheme == ColorManager.DEFAULT_SCHEME


def test_custom_color_scheme(custom_config):
    color_manager = ColorManager(custom_config)
    assert color_manager.current_scheme == custom_config.custom_color_schemes["custom"]


def test_colorize(default_config):
    color_manager = ColorManager(default_config)
    colored_text = color_manager.primary("Test")
    assert colored_text == f"{Fore.CYAN}Test{Style.RESET_ALL}"


def test_set_scheme(default_config):
    color_manager = ColorManager(default_config)
    color_manager.set_scheme("monochrome")
    assert color_manager.current_scheme == color_manager.COLOR_SCHEMES["monochrome"]


def test_color_methods(default_config):
    color_manager = ColorManager(default_config)
    assert color_manager.primary("Test") == f"{Fore.CYAN}Test{Style.RESET_ALL}"
    assert color_manager.secondary("Test") == f"{Fore.MAGENTA}Test{Style.RESET_ALL}"
    assert color_manager.success("Test") == f"{Fore.GREEN}Test{Style.RESET_ALL}"
    assert color_manager.error("Test") == f"{Fore.RED}Test{Style.RESET_ALL}"
    assert color_manager.warning("Test") == f"{Fore.YELLOW}Test{Style.RESET_ALL}"
    assert color_manager.info("Test") == f"{Fore.BLUE}Test{Style.RESET_ALL}"
