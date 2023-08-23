import click
from models import State, County, City, Facilities, association_table
from data import CityFacilityAssociation
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
    """Seed city-facility associations."""
    # Clear the table first
    session.execute(association_table.delete())
    session.commit()

    # Add the associations
    for association in association_to_add:
        session.execute(association_table.insert().values(city_id=association.city_id, facility_id=association.facility_id))
    session.commit()
    
    click.echo("✅ Done seeding city-facility associations!")


if __name__ == '__main__':
    print("🌱 Seeding DB...")
    cli()


# To seed states: python seed.py seed-states
# To seed counties: python seed.py seed-counties
# To seed cities: python seed.py seed-cities
# To seed facilities: python seed.py seed-facilities
# To seed city-facility associations: python seed.py seed-associations
