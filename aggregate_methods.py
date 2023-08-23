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


@click.command(help="Count the number of cities in a given state.")
def count_cities_in_state():
    # Prompt the user for the state name using click's prompt function with added color
    state_name = click.prompt(click.style('Please enter the name of the state', fg='blue'), type=str)

    # Use SQLAlchemy's session to construct a query
    count = session.query(func.count(City.id)).join(State).filter(State.name == state_name).scalar()        

    # Display the result using click's echo function with added color
    click.echo(click.style(f"The number of cities in {state_name} is: {count}", fg='green'))


@click.command(help="Calculate the average population of cities in a given state.")
@click.argument('state_name')
def average_city_population_in_state(state_name):
    average = session.query(func.avg(City.population)).join(State).filter(State.name == state_name).scalar()
    click.echo(f"The average population of cities in {state_name} is: {average:.2f}")
    

@click.command(help="Find the total area of all cities in a given county.")
@click.argument('county_name')
def total_area_in_county(county_name):
    area = session.query(func.sum(City.area)).join(County).filter(County.name == county_name).scalar()
    click.echo(f"The total area of cities in {county_name} county is: {area:.2f}")  


@click.command(help="Count the number of facilities in a given city.")
@click.argument('city_name')
def count_facilities_in_city(city_name):
    count = session.query(func.count(Facilities.id)).join(association_table).join(City).filter(City.name == city_name).scalar()
    click.echo(f"The number of facilities in {city_name} is: {count}")

cli.add_command(count_facilities_in_city)

session.close()

cli.add_command(count_cities_in_state)
cli.add_command(average_city_population_in_state)
cli.add_command(total_area_in_county)
cli.add_command(count_facilities_in_city)

if __name__ == '__main__':
    cli()
   
    
# python aggregate_methods.py count-cities-in-state "state_name"   
# python aggregate_methods.py count-cities-in-state "Connecticut"
# ==> The number of cities in Connecticut is: 4

"""
SELECT COUNT(*) FROM Cities c 
JOIN States s ON c.state_id = s.id 
WHERE s.name = "Connecticut";

"""


# python aggregate_methods.py average-city-population-in-state "state_name"   
# python aggregate_methods.py average-city-population-in-state "Connecticut"
# ==> The average population of cities in Connecticut is: 17192.75

"""
SELECT AVG(c.population) 
FROM Cities c
JOIN States s ON c.state_id = s.id
WHERE s.name = "Connecticut";

"""


# python aggregate_methods.py total-area-in-county "county_name"   
# python aggregate_methods.py total-area-in-county "Susanside"
# ==> The total area of cities in Susanside county is: 1537.00

"""
SELECT SUM(c.area) 
FROM Cities c
JOIN Counties co ON c.county_id = co.id
WHERE co.name = "Susanside";

"""


# python aggregate_methods.py count-facilities-in-city "city_name"   
# python aggregate_methods.py count-facilities-in-city "Lake Hunter"
# ==> The number of facilities in Lake Hunter is: 8

"""
SELECT COUNT(DISTINCT f.id)
FROM Facilities f
JOIN CityFacilityAssociation cfa ON f.id = cfa.facility_id
JOIN Cities c ON cfa.city_id = c.id
WHERE c.name = "Lake Hunter";


"""












