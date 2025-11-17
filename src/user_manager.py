from __future__ import annotations

import json
from .location import Location
from .user_profile import UserProfile

class UserProfileManager:
    """Manages a collection of user profiles with CRUD operations and sorting.
    
    Provides methods to add, remove, retrieve, and sort user profiles.
    Profiles are stored in a dictionary keyed by email address.
    """
    def __init__(self):
        """Initialize an empty UserProfileManager."""
        self.user_profiles = {}
        
    def add_profile(self, profile: UserProfile) -> None:
        """Add a validated profile to the manager.
        
        Args:
            profile: UserProfile instance to add
            
        Raises:
            ValueError: If profile is invalid or email already exists
        """
        if profile.validate():
            if profile.email in self.user_profiles:
                raise ValueError(f"Profile with email {profile.email} already exists")
            self.user_profiles[profile.email] = profile
            return
        raise ValueError(f"Failed to add profile for '{profile.email}'")

    def get_profile(self, email: str) -> UserProfile | None:
        """Retrieve a profile by email address.
        
        Args:
            email: Email address of the profile to retrieve
            
        Returns:
            UserProfile if found, None otherwise
        """
        return self.user_profiles.get(email, None)

    def remove_profile(self, email: str) -> None:
        """Remove a profile by email address.
        
        Args:
            email: Email address of the profile to remove
            
        Raises:
            ValueError: If profile with email does not exist
        """
        if email in self.user_profiles:
            del self.user_profiles[email]
            return
        raise ValueError(f"Failed to remove profile for '{email}'")

    def sort_profiles_by_age(self):
        """Sort profiles by age in descending order (oldest first).
        
        Returns:
            List of UserProfile objects sorted by age
        """
        return sorted(self.user_profiles.values(), key=lambda p: p.get_age(), reverse=True)
    
    def sort_profiles_by_name(self):
        """Sort profiles by name alphabetically.
        
        Returns:
            List of UserProfile objects sorted by name
        """
        return sorted(self.user_profiles.values(), key=lambda p: p.name)
    
    def sort_profiles_by_email(self):
        """Sort profiles by email alphabetically.
        
        Returns:
            List of UserProfile objects sorted by email
        """
        return sorted(self.user_profiles.values(), key=lambda p: p.email)
    
    def sort_profiles_by_location(self):
        """Sort profiles by location (country, state, city).
        
        Returns:
            List of UserProfile objects sorted by location
        """
        return sorted(self.user_profiles.values(), key=lambda p: (p.location.country, p.location.state, p.location.city))
    
    def save_profiles_to_json(self, json_file: str):
        """Save all profiles to a JSON file.
        
        Args:
            json_file: Path to output JSON file
        """
        profile_list = []
        for user_profile in self.user_profiles.values():
            profile_data = {
                'name': user_profile.name,
                'email': user_profile.email,
                'password': user_profile.password,
                'dob': user_profile.dob,
                'location': {
                    'city': user_profile.location.city,
                    'state': user_profile.location.state,
                    'country': user_profile.location.country
                }
            }
            profile_list.append(profile_data)
        with open(json_file, mode='w') as f:
            json.dump(profile_list, f, indent=4)
    
    def load_profiles_from_json(self, json_file: str):
        """Load profiles from a JSON file.
        
        Args:
            json_file: Path to JSON file containing profile(s)
        """
        with open(json_file, mode='r') as input_file:
            loaded_data = json.load(input_file)
        if isinstance(loaded_data, dict):
            profile_items = [loaded_data]
        elif isinstance(loaded_data, list):
            profile_items = loaded_data
        else:
            print(f"ERROR: JSON file must contain a dictionary or list")
            return
        for profile_item in profile_items:
            try:
                user_profile = UserProfile(
                    name=profile_item['name'],
                    email=profile_item['email'],
                    password=profile_item['password'],
                    dob=profile_item['dob'],
                    location=Location(**profile_item['location'])
                )
                try:
                    self.add_profile(user_profile)
                except ValueError:
                    pass
            except KeyError as e:
                print(f"error loading profile: missing field {e}")
            except Exception as e:
                print(f"error loading profile: {e}")