import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.tools import Base
from models.band import Band
from models.venue import Venue
from models.concert import Concert

class TestConcertApp(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")  # Use in-memory SQLite for testing
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Add initial data for testing
        self.band_1 = Band(name="The Rolling Stones", hometown="London")
        self.band_2 = Band(name="The Beatles", hometown="Liverpool")
        self.venue_1 = Venue(title="Madison Square Garden", city="New York")
        self.venue_2 = Venue(title="Wembley Stadium", city="London")
        self.session.add_all([self.band_1, self.band_2, self.venue_1, self.venue_2])
        self.session.commit()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_concert_creation(self):
        concert = Concert(date="2024-09-25", band=self.band_1, venue=self.venue_1)
        self.session.add(concert)
        self.session.commit()
        self.assertEqual(concert.band, self.band_1)
        self.assertEqual(concert.venue, self.venue_1)

if __name__ == "__main__":
    unittest.main()
