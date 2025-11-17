import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import UserProfile

class TestUserProfile:
    def test_valid_user_profile(self):
        valid_user_path = Path(__file__).parent.parent / 'data' / 'valid' / 'input' / 'user.json'
        user = UserProfile.from_json(str(valid_user_path))
        assert user.validate() == True, "Valid user profile should pass validation"
    
    def test_invalid_user_profile(self):
        invalid_user_path = Path(__file__).parent.parent / 'data' / 'invalid' / 'user.json'
        user = UserProfile.from_json(str(invalid_user_path))
        assert user.validate() == False, "Invalid user profile should fail validation"
    
    def test_valid_name(self):
        assert UserProfile.valid_name("John Smith") == True
        assert UserProfile.valid_name("Alice Marie Johnson") == True
        assert UserProfile.valid_name("Bob Williams") == True
        assert UserProfile.valid_name("A B") == True  # Single uppercase letters are valid

        assert UserProfile.valid_name("SingleName") == False  # Only one part
        assert UserProfile.valid_name("john Smith") == False  # First name doesn't start with uppercase
        assert UserProfile.valid_name("John smith") == False  # Last name doesn't start with uppercase
        assert UserProfile.valid_name("John3 Smith") == False  # Contains digit
        assert UserProfile.valid_name("Too Many Name Parts Extra") == False  # More than 3 parts
    
    def test_user_serialization(self):
        valid_input_path = Path(__file__).parent.parent / 'data' / 'valid' / 'input' / 'user.json'
        valid_output_path = Path(__file__).parent.parent / 'data' / 'valid' / 'output' / 'user.json'
        temp_output_path = Path(__file__).parent.parent / 'data' / 'temp_user_output.json'
        user = UserProfile.from_json(str(valid_input_path))
        user.to_json(str(temp_output_path))
        with open(valid_output_path, 'r') as f:
            expected = json.load(f)
        with open(temp_output_path, 'r') as f:
            actual = json.load(f)
        assert actual['name'] == expected['name']
        assert actual['email'] == expected['email']
        assert actual['password'] == expected['password']
        assert actual['dob'] == expected['dob']
        assert actual['location']['city'] == expected['location']['city']
        assert actual['location']['state'] == expected['location']['state']
        assert actual['location']['country'] == expected['location']['country']
        temp_output_path.unlink()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
