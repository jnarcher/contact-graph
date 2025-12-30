from graph import Graph
from components import (
    FirstName,
    LastName,
    MiddleName,
    Nicknames,
    Groups,
)
from collections import defaultdict
from typing import TypeVar, Any

T = TypeVar("T")

Contact = int
LinkMetadata = dict[str, Any]

class ContactManager:
    def __init__(self) -> None:
        self._graph = Graph()
        self._components = defaultdict(dict) # component_type -> id -> component

    def contacts(self):
        for c in self._graph._nodes.keys():
            yield c

    def add_component(self, contact: Contact, component: object) -> None:
        """Attach a component to a contact."""
        self._components[type(component)][contact] = component

    def get_component(self, contact: Contact, component_type: type[T]) -> T | None:
        """Retrieve a component for a contact id, or None."""
        return self._components.get(component_type, {}).get(contact)
    
    def all_components(self, contact: Contact) -> dict:
        """Return all components attached to a contact."""
        return {ctype: comps[contact] for ctype, comps in self._components.items() if contact in comps}

    def new(self) -> Contact:
        return self._graph.create_node()
    
    def new_with_name(
        self,
        first: str,
        last: str | None = None,
        middle: str | None = None,
        nicknames: list[str] | None = None
    ) -> Contact:
        c = self.new()

        self.add_component(c, FirstName(first))

        if last is not None:
            self.add_component(c, LastName(last))

        if middle is not None:
            self.add_component(c, MiddleName(middle))
        
        if nicknames:
            self.add_component(c, Nicknames.from_strings(*nicknames))

        return c

    def link_contacts(
        self,
        a: Contact,
        b: Contact,
        weight: float = 1.0,
        a_to_b_meta: LinkMetadata | None = None,
        b_to_a_meta: LinkMetadata | None = None,
        overwrite: bool = False
    ) -> bool:
        return self._graph.connect(a, b, weight, a_to_b_meta, b_to_a_meta, overwrite)

    def contacts_in_group(self, group_name: str):
        for contact in self.contacts():
            groups = self.get_component(contact, Groups)
            if groups and group_name in groups.names:
                yield contact

    def get_display_name(self, contact: Contact) -> str:
        first = self.get_component(contact, FirstName)
        last = self.get_component(contact, LastName)

        s = ""
        
        if first is not None:
            s = first.value

        if last is not None:
            s = f"{s} {last.value}"

        return s