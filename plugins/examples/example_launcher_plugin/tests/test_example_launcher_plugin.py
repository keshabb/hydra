# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest

from hydra.core.plugins import Plugins
from hydra.plugins.launcher import Launcher
from hydra.test_utils.launcher_common_tests import (
    IntegrationTestSuite,
    LauncherTestSuite,
)

# This has to be included here for the LauncherTestSuite to work.
# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401
from hydra_plugins.example_launcher_plugin import ExampleLauncher


def test_discovery() -> None:
    # Tests that this plugin can be discovered via the plugins subsystem when looking for Launchers
    assert ExampleLauncher.__name__ in [x.__name__ for x in Plugins.discover(Launcher)]


@pytest.mark.parametrize("launcher_name, overrides", [("example", [])])
class TestExampleLauncher(LauncherTestSuite):
    """
    Run the Launcher test suite on this launcher.
    Note that hydra/launcher/example.yaml should be provided by this launcher.
    """

    pass


@pytest.mark.parametrize(
    "task_launcher_cfg, extra_flags, plugin_module",
    [
        (
            {
                "defaults": [
                    {"hydra/launcher": None},
                    {"hydra/hydra_logging": "hydra_debug"},
                    {"hydra/job_logging": "disabled"},
                ],
                "hydra": {
                    "launcher": {
                        "class": "hydra_plugins.example_launcher_plugin.ExampleLauncher",
                        "params": {"foo": 10, "bar": "abcde"},
                    }
                },
            },
            ["-m"],
            "hydra_plugins.example_launcher",
        )
    ],
)
class TestExampleLauncherIntegration(IntegrationTestSuite):
    """
    Run this launcher through the integration test suite.
    """

    pass
