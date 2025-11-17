import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import UserProfile
from src.location import Location

class TestPasswordRegression:
    """
    Regression tests for password validation bug.
    The bug was in the regex pattern that incorrectly rejected valid passwords.
    """
    
    def test_valid_password_basic(self):
        password = "Secure123!"
        assert UserProfile.valid_password(password), f"Password '{password}' should be valid"
    
    def test_valid_password_uppercase_start(self):
        password = "MyPassword1@"
        assert UserProfile.valid_password(password), f"Password '{password}' should be valid"
    
    def test_valid_password_lowercase_start(self):
        password = "myPassword1@"
        assert UserProfile.valid_password(password), f"Password '{password}' should be valid"
    


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
