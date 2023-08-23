import click
from  models import State, County, City, Facilities, association_table as CityFacilityAssociation, Base
from sqlalchemy.orm import sessionmaker
from data import states_to_add, counties_to_add, cities_to_add, facilities_to_add, association_to_add
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./mydatabase.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    """Manage the database records."""
    pass



@cli.command()
def create_tables():
    """Create all tables."""
    Base.metadata.create_all(engine)
    click.echo("✅ Done creating tables!")
    
    
@cli.command()
def seed_states():
    """Seed states."""
    session.query(State).delete()
    session.commit()
    session.add_all(states_to_add)
    session.commit()       
    click.echo("✅ Done seeding states!")

@cli.command()
def seed_counties():
    """Seed counties."""
    session.query(County).delete()
    session.commit()
    session.add_all(counties_to_add)
    session.commit()
    click.echo("✅ Done seeding counties!")

@cli.command()
def seed_cities():
    """Seed cities."""
    session.query(City).delete()
    session.commit()
    session.add_all(cities_to_add)
    session.commit()  
    click.echo("✅ Done seeding cities!")

@cli.command()
def seed_facilities():
    """Seed facilities."""
    session.query(Facilities).delete()
    session.commit()
    session.add_all(facilities_to_add)
    session.commit()
    click.echo("✅ Done seeding facilities!")
    
@cli.command()
def seed_associations():
    """Seed associations."""
    session.execute(CityFacilityAssociation.delete())  # Delete existing associations
    for association in association_to_add:
        session.execute(CityFacilityAssociation.insert().values(**association))
    session.commit()
    click.echo("✅ Done seeding associations!")

    
    

if __name__ == '__main__':
    print("🌱 Seeding DB...")
    cli()

# To create Tables: python seed.py create-tables
# To seed states: python seed.py seed-states
# To seed counties: python seed.py seed-counties
# To seed cities: python seed.py seed-cities
# To seed facilities: python seed.py seed-facilities
# To seed associations: python seed.py seed-associations
