import click
from models import State, County, City, Facilities, association_table
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from seed import Session, session

session = Session()
session.query(State).delete()

@click.group()
def cli():
    pass


@click.command(help="Add a city to a state")
@click.argument('city_name')
@click.argument('state_name')
def add_city_to_state(city_name, state_name):
    state = session.query(State).filter_by(name=state_name).first()
    if not state:
        click.echo(f"State {state_name} not found!")
        return
    
    new_city = City(name=city_name)
    state.cities.append(new_city)
    session.add(new_city)
    session.commit()
    click.echo(f"City {city_name} added to State {state_name}!")


@click.command(help="Link a city to a facility")
@click.argument('city_name')
@click.argument('facility_name')
def link_city_to_facility(city_name, facility_name):
    city = session.query(City).filter_by(name=city_name).first()
    facility = session.query(Facilities).filter_by(name=facility_name).first()
    
    if not city or not facility:
        click.echo(f"City {city_name} or Facility {facility_name} not found!")
        return

    city.facilities.append(facility)
    session.commit()
    click.echo(f"Linked City {city_name} to Facility {facility_name}!")


@click.command(help="Move a city to a different county")
@click.argument('city_name')
@click.argument('new_county_name')
def move_city_to_county(city_name, new_county_name):
    city = session.query(City).filter_by(name=city_name).first()
    new_county = session.query(County).filter_by(name=new_county_name).first()
    
    if not city or not new_county:
        click.echo(f"City {city_name} or County {new_county_name} not found!")
        return

    city.county = new_county
    session.commit()
    click.echo(f"Moved City {city_name} to County {new_county_name}!")

cli.add_command(add_city_to_state)
cli.add_command(link_city_to_facility)
cli.add_command(move_city_to_county)

if __name__ == '__main__':
    cli()
    
    
# python associate_methods.py add-city-to-state 'Pleasantville' 'Nevada'

"""
SELECT c.name AS City, s.name AS State
FROM Cities c
JOIN States s ON c.state_id = s.id
WHERE c.name = 'Pleasantville' AND s.name = 'Nevada';

"""

# python associate_methods.py link-city-to-facility 'Pleasantville' 'Ross LLC'

"""
    
SELECT c.name AS City, f.name AS Facility
FROM Cities c
JOIN CityFacilityAssociation cfa ON c.id = cfa.city_id
JOIN Facilities f ON cfa.facility_id = f.id;

SELECT c.name AS City, f.name AS Facility
FROM Cities c
JOIN CityFacilityAssociation cfa ON c.id = cfa.city_id
JOIN Facilities f ON cfa.facility_id = f.id
WHERE c.name = 'Pleasantville';


    """

# python associate_methods.py move-city-to-county 'Pleasantville' 'Susanside'

"""
SELECT c.name AS City, co.name AS County
FROM Cities c
JOIN Counties co ON c.county_id = co.id
WHERE c.name = 'Pleasantville' AND co.name = 'Susanside';

"""
