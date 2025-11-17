import pytest
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import UserProfile
from src.location import Location

class TestAgeRegression:
    
    def test_age_before_birthday_this_year(self):
        user = UserProfile(
            name="John Smith",
            email="john@example.com",
            password="Secure123!",
            dob="1990-12-31",  # Born Dec 31, 1990
            location=Location(city="LA", state="CA", country="US")
        )
        # Reference date: Jan 1, 2025 (birthday hasn't happened yet)
        ref_date = datetime(2025, 1, 1)
        age = user.get_age(ref_date)
        assert age == 34, f"Expected age 34 but got {age} for date before birthday"
    
    def test_age_on_birthday(self):
        user = UserProfile(
            name="John Smith",
            email="john@example.com",
            password="Secure123!",
            dob="1990-03-15",  # Born Mar 15, 1990
            location=Location(city="LA", state="CA", country="US")
        )
        # Reference date: Mar 15, 2025 (exactly on birthday)
        ref_date = datetime(2025, 3, 15)
        age = user.get_age(ref_date)
        assert age == 35, f"Expected age 35 on birthday but got {age}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
