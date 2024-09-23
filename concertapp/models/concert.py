from sqlalchemy import ForeignKey, Column, String, Integer
from sqlalchemy.orm import relationship
from utils.tools import Base, SessionLocal

class Concert(Base):
    __tablename__ = 'concerts'

    # Attributes
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey('bands.id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)
    date = Column(String, nullable=False)  # Added date attribute

    # Relationships
    band = relationship("Band", back_populates="concerts")
    venue = relationship("Venue", back_populates="concerts")

    # Object relationship methods
    def get_band(self):
        """Returns the band associated with this concert."""
        return self.band

    def get_venue(self):
        """Returns the venue associated with this concert."""
        return self.venue

    # Aggregate relationship methods
    @classmethod
    def play_in_venue(cls, band, venue, date):
        """Creates a concert for the band in the venue on a given date."""
        with SessionLocal() as session:
            # Check if a concert on that date for that band already exists
            existing_concert = session.query(cls).filter_by(
                band_id=band.id,
                venue_id=venue.id,
                date=date
            ).first()

            if existing_concert:
                print(f"Concert on {date} at {venue.title} already exists for this band.")
                return existing_concert

            # Create a new concert if it doesn't exist
            new_concert = cls(band_id=band.id, venue_id=venue.id, date=date)
            session.add(new_concert)
            session.commit()
            print("Concert added successfully.")
            return new_concert

    def introduction(self):
        """Returns a string introducing the band and venue of a concert."""
        return f"Welcome to {self.venue.title} in {self.venue.city}! This evening: {self.band.name}!"

    def hometown_show(self):
        """Returns True if the concert is in the band's hometown, False otherwise."""
        return self.venue.city.lower() == self.band.hometown.lower()
