import abc
from enum import Enum

from pydantic import BaseModel, Field

from pydatalab.models.items import Item


class CellFormFactor(str, Enum):

    coin = "coin"
    pouch = "pouch"
    in_situ = "in situ (XRD)"
    cylindrical = "cylindrical"
    redox_flow = "redox flow"
    other = "other"


class ActiveIon(str, Enum):

    Li1 = "Li+"
    Na1 = "Na+"
    K1 = "K+"
    Mg2 = "Mg2+"
    Ca2 = "Ca2+"
    other = "other"


class Component(BaseModel):
    pass


class AnodicComponent(Component):
    pass


class CathodicComponent(Component):
    pass


class Separator(Component):
    pass


class Anolyte(AnodicComponent):
    pass


class Catholyte(CathodicComponent):
    pass


class Electrode(Component, abc.ABC):
    pass


class Cathode(CathodicComponent, Electrode):
    pass


class Anode(AnodicComponent, Electrode):
    pass


class Electrolyte(Component):
    pass


class SolidElectrolyte(Electrolyte):
    pass


class LiquidElectrolyte(Electrolyte):
    pass


class Cell(Item):
    """A model for representing electrochemical cells."""

    type: str = Field("cells", const="cells", pattern="^cells$")

    form_factor: CellFormFactor = Field(
        CellFormFactor.other,
        description="The form factor of the cell, e.g., coin, pouch, in situ or otherwise.",
    )

    form_factor_description: str = Field(
        description="Additional human-readable description of the cell form factor, e.g., 18650."
    )

    cathode: Cathode = Field()

    cathode_gravimetric_capacity: float = Field()

    anode: str = Field()

    anode_gravimetric_capacity: float = Field()

    separator: Separator = Field()

    electrolyte: str = Field()

    active_mass: float = Field()

    active_ion: ActiveIon = Field()
