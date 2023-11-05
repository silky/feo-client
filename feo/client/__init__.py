"""
    `feo` stands for the Future Energy Outlook, by TransitionZero.
    The Future Energy Outlook gives users the ability to explore historic energy
    data, and to ask research questions about the energy future,
    using TransitionZero's 'batteries-included' systems modelling platform.
    This package, `feo-client`, allows users to interact with the platform via
    both a low-level api wrapper, and a set of higher-order class objects.

    To import the feo client library:
    ```python
    from feo import client
    ```

    Authenticate via the command line with
    ```
    feo auth login
    ```

    To use the lower-level api wrapper:
    ```python
    from feo.client import api
    ```

    To use the high-level objects:
    ```python
    from feo.client import Node, Model, Scenario
    ```
"""

from feo.client.asset import Asset, AssetCollection
from feo.client.node import Node

__all__ = ["Node", "Asset", "AssetCollection"]
__version__ = "0.0.1"