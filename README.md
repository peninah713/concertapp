Project Overview
This project manages concerts played by different bands at various venues. The three main models are:

Band: Represents musical bands.
Venue: Represents venues where concerts are held.
Concert: Junction table representing concerts that connect a band and a venue.

Available Methods
Concert
band(): Returns the band playing in this concert.
venue(): Returns the venue where the concert is happening.
hometown_show(): Returns True if the concert is in the band's hometown.
introduction(): Returns an introduction string for the band at this concert.
Band
concerts(): Returns all concerts for the band.
venues(): Returns all venues the band has played at.
play_in_venue(venue, date): Creates a concert for the band in the specified venue.
all_introductions(): Returns a list of all concert introductions for the band.
most_performances(): Class method that returns the band with the most concerts.
Venue
concerts(): Returns all concerts held at the venue.
bands(): Returns all bands that have performed at the venue.
concert_on(date): Finds and returns the concert on a specific date.
most_frequent_band(): Returns the band that performed most frequently at this venue.
Set Up the Project
First, make sure you have set up the project properly by following these steps:

Clone the repository
Create a virtual environment:




Install dependencies:
pip install sqarchmy and alembic

Set Up the Database You need to set up your database, apply migrations, and seed data.
Initialize the database:


alembic upgrade head
Seed the database with test data: test_app.py
