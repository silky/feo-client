import pandas as pd
from pydantic import root_validator

from feo.client import api
from feo.client.api import schemas


class Asset(schemas.NodeBase):
    def __init__(self, id: str, **kwargs):
        """Initialise Asset from `id` as a positional argument"""
        super(self.__class__, self).__init__(id=id, **kwargs)

    @classmethod
    def search(
        cls,
        alias: str,
        threshold: float = 0.5,
        node_type: str | None = None,
        sector: str | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> list["schemas.Node"]:
        """
        Search for nodes using an alias.

        Args:
            alias (str): The target alias to search.
            threshold (float): The desired confidence in the search result.
            node_type (str): filter search to a specific node type.
            sector (str): the industrial sector to filter assets for

        Returns:
            list[schemas.Node]: A list of Node objects.
        """

        search_results = api.aliases.get(
            alias=alias,
            threshold=threshold,
            node_type=node_type,
            sector=sector,
            includes="power_unit",
            page=page,
            limit=limit,
        )

        return [
            cls(**alias.node.model_dump())  # type: ignore[union-attr, misc]
            for alias in search_results.aliases
        ]

    @root_validator(pre=True)
    def maybe_initialise_from_api(cls, values):
        id = values.get("id")
        node_type = values.get("node_type")
        type_alias = values.get("type_alias")

        if id is not None and any([(node_type is None), (type_alias is None)]):
            # call from API
            node = api.assets.get(ids=id)[0]

            for key, val in node.model_dump().items():
                values[key] = val

            return values

        return values


class AssetCollection(pd.DataFrame):
    @classmethod
    def from_parent_node(cls, node_id: str):
        pass

    def next_page(self):
        pass
