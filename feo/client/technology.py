from typing import ForwardRef, Optional

from feo.client import RecordCollection, api
from feo.client.api import schemas


class Technology(schemas.TechnologyBase):

    """
    <!--
    The Technology class enables access to technology data.
    Technologies are related hierarchically to one another via their parents / children properties.
    -->

    Technologies can be loaded directly with their id:

    ```python
    coal = Technology.from_id("coal")
    ```

    """

    _projections: Optional[ForwardRef("RecordCollection")] = None  # type: ignore[valid-type]
    _children: Optional[list["Technology"]] = None
    _parents: Optional[list["Technology"]] = None

    @classmethod
    def from_id(cls, id: str) -> "Technology":
        """
        Initialize the Technology object from an ID.

        Args:
            id (str): A technology ID, e.g. `coal`.

        Returns:
            Technology: A Technology object.
        """
        technology = api.technologies.get(slug=id)
        return cls(**technology.model_dump())

    @classmethod
    def search(
        cls,
        uuid: str | None = None,
        slug: str | None = None,
        name: str | None = None,
        owner_id: str | None = None,
        public: bool | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> list["Technology"]:
        """
        Search for technologies.

        Args:
            uuid (str | None): The target technology UUID to search.
            slug (str | None): The target technology slug to search.
            names (str | None): The target technology name to search.
            owner_id (str | None): The owner of the technologiess to filter.
            public (bool | None): Filter technologies by public status.
            limit (int): The maximum number of search results to return.
            page (int): The page number of search results to return.

        Returns:
            List[Technology]: A list of Technology objects.
        """

        search_results = api.technologies.search(
            uuid=uuid,
            slug=slug,
            name=name,
            owner_id=owner_id,
            public=public,
            limit=limit,
            page=page,
        )

        return [cls(**technology.model_dump()) for technology in search_results]

    @property
    def id(self) -> str:
        """The ID of the technology."""
        return self.slug

    @classmethod
    def _get_children(cls, slug):
        technology = api.technologies.get(slug=slug, includes="children")
        return [cls(**child.model_dump()) for child in technology.children]

    @classmethod
    def _get_parents(cls, slug):
        technology = api.technologies.get(slug=slug, includes="parents")
        return [cls(**parent.model_dump()) for parent in technology.parents]

    @property
    def children(self) -> list["Technology"]:
        """A set of technologies which are the heirarchical children of this technology."""
        if self._children is None:
            self._children = self._get_children(self.slug)
            return self._children
        return self._children

    @property
    def parents(self) -> list["Technology"]:
        """A set of technology which are the heirarchical ancestors of this technology."""
        if self._parents is None:
            self._parents = self._get_parents(self.slug)
            return self._parents
        return self._parents

    @property
    def projections(self):
        """The RecordCollection associated with the technoogy"""
        if self._projections is None:
            collection = RecordCollection()
            self._projections = collection.search(technology=self.slug)
        return self._projections

    def __str__(self) -> str:
        return f"Technology: {self.name} (id={self.id})"
