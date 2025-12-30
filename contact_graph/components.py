# components.py

from dataclasses import dataclass, field 
from datetime import datetime
from enum import StrEnum


@dataclass
class FirstName:
    value: str

    def __repr__(self) -> str:
        return self.value

@dataclass
class LastName:
    value: str

    def __repr__(self) -> str:
        return self.value

@dataclass
class MiddleName:
    value: str

    def __repr__(self) -> str:
        return self.value

@dataclass
class Prefix:
    value: str

    def __repr__(self) -> str:
        return self.value

@dataclass
class Suffix:
    value: str

    def __repr__(self) -> str:
        return self.value

@dataclass
class Nickname:
    value: str

    def __repr__(self) -> str:
        return self.value

@dataclass
class Nicknames:
    values: list[Nickname] = field(default_factory=list)

    @classmethod
    def from_strings(cls, *names: str) -> "Nicknames":
        return cls([Nickname(name) for name in names])

class PhoneTag(StrEnum):
    MOBILE = "mobile"
    WORK = "work"
    HOME = "home"

class PhoneNumber:
    def __init__(
        self, number: int,
        country_code: int | None = None,
        tag: PhoneTag | None = None
    ) -> None:
        self.country_code: int | None = country_code
        self.tag: PhoneTag | None = tag

        n = str(number)
        if len(n) == 10:
            self.number = number
        elif len(n) > 10 and country_code is None:
            self.country_code = int(n[:-10])
            self.number = int(n[-10:])
        else:
            raise ValueError("Invalid phone number.")

    def __str__(self) -> str:
        n = str(self.number)
        s = f"({n[:3]}) {n[3:6]}-{n[6:]}"
        if self.country_code is not None:
            s = f"+{self.country_code} {s}"
        return s

    def __repr__(self) -> str:
        s = str(self)
        if self.tag is not None:
            s = f"{s} ({str(self.tag)})"
        return s

@dataclass
class PhoneNumbers:
    values: list[PhoneNumber] = field(default_factory=list)

    def __repr__(self) -> str:
        return ", ".join(repr(v) for v in self.values)

@dataclass
class Email:
    value: str
    tag: str | None = None

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        s = str(self)
        if self.tag is not None:
            s = f"{s} ({self.tag})"
        return s

@dataclass
class Emails:
    values: list[Email] = field(default_factory=list)

    def __repr__(self) -> str:
        return ", ".join(repr(v) for v in self.values)

@dataclass
class Address:
    country: str
    state: str
    city: str
    address: str
    zipcode: int
    unit: int | str | None = None
    tag: str | None = None

    def __str__(self) -> str:
        s = f"{self.address}"

        if self.unit is not None:
            s = f"{s} Un. {self.unit}"

        s = f"{s}, {self.city}, {self.state} {self.country} {self.zipcode}"

        return s


    def __repr__(self) -> str:
        s = str(self)
        if self.tag is not None:
            s = f"{s} ({self.tag})"
        return s

@dataclass
class Addresses:
    values: list[Address] = field(default_factory=list)

    def __repr__(self) -> str:
        return ", ".join(repr(v) for v in self.values)

@dataclass
class Company:
    name: str
    address: Address | None = None

    def __str__(self) -> str:
        return self.name

@dataclass
class Birthday:
    date: datetime


@dataclass
class Groups:
    names: set[str] = field(default_factory=set)

    @classmethod
    def from_strings(cls, *names:str) -> "Groups":
        return cls(set(names))