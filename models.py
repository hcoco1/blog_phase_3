from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Define the association table first
association_table = Table(
    "CityFacilityAssociation",
    Base.metadata,
    Column("city_id", Integer, ForeignKey("Cities.id")),
    Column("facility_id", Integer, ForeignKey("Facilities.id"))
)


class State(Base):
    __tablename__ = "States"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    abbreviation = Column(String(255))
    population = Column(Integer)
    capital = Column(String(255))
    area = Column(Float)
    
    # ORM relationship for Cities
    counties = relationship("County", back_populates="state")  # New relationship
    cities = relationship("City", back_populates="state")


    def __repr__(self):
        return f"<State(id={self.id}, name='{self.name}', abbreviation='{self.abbreviation}, population='{self.population}', area='{self.area}')>"


class County(Base):
    __tablename__ = "Counties"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    population = Column(Integer)
    area = Column(Float)
    state_id = Column(Integer, ForeignKey("States.id"))  # Foreign Key to States
    
    # ORM relationships
    state = relationship("State")  # Relationship to State
    cities = relationship("City", back_populates="county")

    def __repr__(self):
        return f"<County(id={self.id}, name='{self.name}', population='{self.population}', area='{self.area}'))>"



class City(Base):
    __tablename__ = "Cities"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    population = Column(Integer)
    area = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    state_id = Column(Integer, ForeignKey("States.id"))  # Foreign Key to States
    county_id = Column(Integer, ForeignKey("Counties.id"))  # Foreign Key to Counties

    # ORM relationships
    state = relationship("State", back_populates="cities")
    county = relationship("County", back_populates="cities")
    facilities = relationship(
        "Facilities", secondary=association_table, back_populates="cities"
    )


    def __repr__(self):
        return f"<City(id={self.id}, name='{self.name}', population='{self.population}', area='{self.area}'))>"


class Facilities(Base):
    __tablename__ = "Facilities"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    facility_type = Column(String(255))

    # ORM relationship
    cities = relationship(
        "City", secondary=association_table, back_populates="facilities"
    )

    def __repr__(self):
        return (
            f"<Facility(id={self.id}, name='{self.name}', type='{self.facility_type}')>"
        )
# Set up the database connection
DATABASE_URL = "sqlite:///./mydatabase.db"
engine = create_engine(DATABASE_URL)

# Create the tables
Base.metadata.create_all(engine)