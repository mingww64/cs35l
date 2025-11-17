import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import UserProfileManager

class TestUserProfileManager:
    def test_load_valid_user_list(self):
        valid_list_path = Path(__file__).parent.parent / 'data' / 'valid' / 'input' / 'user_list.json'
        manager = UserProfileManager()
        manager.load_profiles_from_json(str(valid_list_path))
        assert len(manager.user_profiles) == 5, "Should load all 5 valid profiles"
    
    def test_load_invalid_user_list(self):
        invalid_list_path = Path(__file__).parent.parent / 'data' / 'invalid' / 'user_list.json'
        manager = UserProfileManager()
        manager.load_profiles_from_json(str(invalid_list_path))
        assert len(manager.user_profiles) == 0, "No invalid profiles should be loaded"
    
    def test_output_matches_expected(self):
        valid_input_path = Path(__file__).parent.parent / 'data' / 'valid' / 'input' / 'user_list.json'
        valid_output_path = Path(__file__).parent.parent / 'data' / 'valid' / 'output' / 'user_list.json'
        temp_output_path = Path(__file__).parent.parent / 'data' / 'temp_output.json'
        
        manager = UserProfileManager()
        manager.load_profiles_from_json(str(valid_input_path))
        sorted_profiles = manager.sort_profiles_by_age()
        
        manager_sorted = UserProfileManager()
        for profile in sorted_profiles:
            manager_sorted.add_profile(profile)
        manager_sorted.save_profiles_to_json(str(temp_output_path))
        
        with open(valid_output_path, 'r') as f:
            expected = json.load(f)
        with open(temp_output_path, 'r') as f:
            actual = json.load(f)
        assert len(actual) == len(expected), "Output should have same number of profiles"
        
        for i, (actual_profile, expected_profile) in enumerate(zip(actual, expected)):
            assert actual_profile['name'] == expected_profile['name'], f"Profile {i}: Name mismatch"
            assert actual_profile['email'] == expected_profile['email'], f"Profile {i}: Email mismatch"
            assert actual_profile['password'] == expected_profile['password'], f"Profile {i}: Password mismatch"
            assert actual_profile['dob'] == expected_profile['dob'], f"Profile {i}: DOB mismatch"
            assert actual_profile['location']['city'] == expected_profile['location']['city'], f"Profile {i}: City mismatch"
            assert actual_profile['location']['state'] == expected_profile['location']['state'], f"Profile {i}: State mismatch"
            assert actual_profile['location']['country'] == expected_profile['location']['country'], f"Profile {i}: Country mismatch"
        
        temp_output_path.unlink()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
