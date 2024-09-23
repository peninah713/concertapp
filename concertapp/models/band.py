from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from utils.tools import Base
from models.concert import Concert
from models.venue import Venue
from utils.tools import SessionLocal

class Band(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String, nullable=False)

    concerts = relationship('Concert', back_populates='band')

    def get_all_concerts(self):
        """Returns all concerts associated with this band."""
        return self.concerts

    def get_venues(self, session):
        """Returns a list of venues where the band has performed."""
        return session.query(Venue).join(Concert).filter(Concert.band_id == self.id).all()

    def play_in_venue(self, venue, date):
        """Creates a concert for the band in the venue on a given date."""
        session = SessionLocal()

        # Check if a concert on that date for that band already exists
        existing_concert = session.query(Concert).filter_by(band_id=self.id, venue_id=venue.id, date=date).first()

        if existing_concert:
            print(f"Concert on {date} at {venue.title} already exists for this band")
            return existing_concert

        # Create a new concert if it doesn't exist
        new_concert = Concert(band_id=self.id, venue_id=venue.id, date=date)
        session.add(new_concert)
        session.commit()
        print("Concert added successfully")
        return new_concert

    def all_introductions(self):
        """Returns a list of all introductions for the band."""
        introductions = []

        for concert in self.concerts:
            venue = concert.venue  # Assuming Concert has a relationship with Venue
            introduction = f"Hello {venue.city}!!! We are {self.name} and we're from {self.hometown}"
            introductions.append(introduction)

        return introductions

    @classmethod
    def most_performances(cls, session):
        """Returns details of the band that has played the most concerts."""
        # Subquery to count the number of concerts for each band
        subquery = session.query(
            Concert.band_id, 
            func.count(Concert.id).label('performance_count')
        ).group_by(Concert.band_id).subquery()

        # Find the band with the maximum performance count
        most_performances_by_band = session.query(
            subquery.c.band_id
        ).order_by(subquery.c.performance_count.desc()).first()

        # If no band is found
        if not most_performances_by_band:
            return 'No bands found'

        # Retrieve band details if found
        band = session.query(cls).filter_by(id=most_performances_by_band[0]).first()

        if band:
            # Count the number of concerts performed by the band
            performance_count = session.query(Concert).filter_by(band_id=band.id).count()

            # Return a formatted string with band details
            return (f"Band with the most performances:\n"
                    f"Name: {band.name}\n"
                    f"Hometown: {band.hometown}\n"
                    f"Number of Concerts: {performance_count}")
        else:
            return 'Band not found'
