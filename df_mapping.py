"""Map between element names, object names, and object URNs."""

from copy import deepcopy

import pandas as pd


class Gem:
    """Look up element and object identifiers in a mapping table."""

    def __init__(self):
        """Initialize the mapping cache."""
        self._element_object_urn = None

    def get_map_element_object_urn(self):
        """Get the element, object, and URN mapping tables.

        Returns:
            dict[str, pd.DataFrame]: Mapping tables keyed by ``element``,
            ``urn``, or ``object``.
        """
        if self._element_object_urn is None:
            self._map_element_object_urn()
        return deepcopy(self._element_object_urn)

    def _map_element_object_urn(self):
        """Create and cache the mapping tables."""
        df = pd.DataFrame(
            {
                "element": ["IDT_A", "GLM_B", "SBX_C"],
                "object": ["Blue.A", "Blue.B", "Blue.C"],
                "urn": ["101", "102", "103"],
            }
        )
        self._element_object_urn = {
            col: df.set_index(col) for col in df.columns
        }

    def objmap0(
        self,
        element: str | None = None,
        urn: str | None = None,
        object: str | None = None,
    ):
        """Look up element, object, or URN using exactly one identifier.

        Args:
            element: Element name to look up.
            urn: URN to look up.
            object: Object name to look up.

        Returns:
            pd.Series: The matching row indexed by the other identifier
            names.

        Raises:
            ValueError: If non-unity identifier is supplied.
            KeyError: If the supplied identifier is not in the mapping.

        Examples:
            >>> gem = Gem()
            >>> # Look up object name or urn from the element name.
            >>> gem.objmap(element="IDT_A").object
            >>> gem.objmap(element="IDT_A").urn
            >>> # Look up an element name or object name from its URN.
            >>> gem.objmap(urn=102).element
            >>> gem.objmap(urn=102).object
            >>> # Look up an element name or urn from its object name.
            >>> gem.objmap(object="Blue.C").element
            >>> gem.objmap(object="Blue.C").urn
        """
        urn = str(urn) if urn else None
        lookup = self.get_map_element_object_urn()
        if sum(x is not None for x in (element, urn, object)) != 1:
            raise ValueError(
                f"Must specify exactly one of `element`, `urn`, or `object`."
            )
        if element:
            key = "element"
        elif urn:
            key = "urn"
        elif object:
            key = "object"
        val = element or urn or object
        try:
            result = lookup[key].loc[val]
        except KeyError:
            entries = list(lookup[key].index)
            raise KeyError(
                f"{key} '{val}' not found. Expecting one of: "
                f"{', '.join(entries)}."
            )
        return result

    def objmap(
        self,
        element: str | None = None,
        urn: str | int | None = None,
        object: str | None = None,
    ) -> pd.Series:
        """Look up element, object, or URN using exactly one identifier.

        Args:
            element: Element name to look up.
            urn: URN to look up.
            object: Object name to look up.

        Returns:
            The matching row indexed by the other identifier names.

        Raises:
            ValueError: If non-unity identifier is supplied.
            KeyError: If the supplied identifier is not in the mapping.

        Examples:
            >>> gem = Gem()
            >>> # Look up object name or urn from the element name.
            >>> gem.objmap(element="IDT_A").object
            >>> gem.objmap(element="IDT_A").urn
            >>> # Look up an element name or object name from its URN.
            >>> gem.objmap(urn=102).element
            >>> gem.objmap(urn=102).object
            >>> # Look up an element name or urn from its object name.
            >>> gem.objmap(object="Blue.C").element
            >>> gem.objmap(object="Blue.C").urn
        """
        identifiers = {
            "element": element,
            "urn": str(urn) if urn is not None else None,
            "object": object,
        }
        provided = {
            key: value
            for key, value in identifiers.items()
            if value is not None
        }
        if len(provided) != 1:
            raise ValueError(
                "Must specify exactly one of `element`, `urn`, or `object`."
            )
        key, value = next(iter(provided.items()))
        lookup = self.get_map_element_object_urn()[key]
        try:
            return lookup.loc[value]
        except KeyError:
            raise KeyError(
                f"{key} '{value}' not found. "
                f"Expecting one of: {', '.join(map(str, lookup.index))}."
            ) from None


gem = Gem()
df = gem.get_map_element_object_urn()
df["element"].loc["IDT_A", "urn"] = "1"
print(gem.get_map_element_object_urn())
breakpoint()
