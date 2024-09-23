from sqlalchemy import ForeignKey, Column, String, Integer, func
from sqlalchemy.orm import relationship
from utils.tools import Base

class Venue(Base):
    __tablename__ = 'venues'

    # Attributes (columns)
    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    title = Column(String, nullable=False, unique=True)

    # One-to-many relationship with concerts
    concerts = relationship('Concert', back_populates='venue')

    def concert_on(self, date, session):
        """Returns the first concert on the given date at this venue."""
        from models.concert import Concert

        # Query to find the concert at this venue on a specific date
        concert = session.query(Concert).filter_by(venue_id=self.id, date=date).first()

        if concert:
            band_name = concert.band.name if concert.band else 'unknown'
            return (f"Concert details: Band: {band_name}, "
                    f"Date: {concert.date}, "
                    f"Location: {self.title} ({self.city})")
        else:
            return f"No concert found on {date} at {self.title} ({self.city})"

    def most_frequent_band(self, session):
        """Returns the band that has played the most concerts at this venue."""
        from models.concert import Concert
        from models.band import Band

        # Query to find the most frequent band at the venue
        most_frequent_band = session.query(Band).join(Concert).filter(
            Concert.venue_id == self.id
        ).group_by(Band.id).order_by(func.count(Concert.id).desc()).first()

        if most_frequent_band:
            return f"The most frequent band at {self.title} is {most_frequent_band.name}"
        else:
            return f"No band found for {self.title}"

    def most_frequent_band_name(self, session):
        """Returns the name of the band that has played the most concerts at this venue."""
        return self.most_frequent_band(session)  # Reusing existing method to avoid redundancy
