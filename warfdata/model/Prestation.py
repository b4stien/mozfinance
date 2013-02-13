from sqlalchemy import Column, Integer, Date, Enum, Unicode, Float

from . import Base


PRESTATION_CATEGORY_FOO = 'foo'  # eg: sale / rental
PRESTATION_CATEGORIES = [PRESTATION_CATEGORY_FOO]
PRESTATION_SECTOR_BAR = 'bar'  # eg: bank / industry
PRESTATION_SECTORS = [PRESTATION_SECTOR_BAR]


class Prestation(Base):
    __tablename__ = "prestations"
    id = Column(Integer, primary_key=True)

    date = Column(Date, index=True)
    client = Column(Unicode(length=30))
    selling_price = Column(Float)

    category = Column(Enum(
        *PRESTATION_CATEGORIES,
        name="prestation_categories"), index=True)
    sector = Column(Enum(
        *PRESTATION_SECTORS,
        name="prestation_sectors"), index=True)
