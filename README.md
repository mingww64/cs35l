# Assignment 5 for UCLA-CS35L

## How to setup 
To set up the project using pipenv:

1. **Install pipenv** (if you don't already have it):
   ```
   pip install pipenv
   ```

2. **Install dependencies**:
   ```
   pipenv install
   ```

3. **Activate the virtual environment**:
   ```
   pipenv shell
   ```

Now you are ready to run the project Python files inside the pipenv environment!

## Installation and Usage

### Install the project in editable mode

You can install the project in editable (`-e`) mode using pipenv. First, make sure you are in the project root directory (where `pyproject.toml` is located) and you have activated the pipenv shell (as described in the setup section above):

```
pipenv install -e .
```

Alternatively, if you're not in the pipenv shell, you can use:

```
pipenv run pip install -e .
```

### Running the main program

After installation, you can run the program in several ways:

#### Using the `user-profiles` command directly

Once installed, you can use the `user-profiles` command directly (inside the pipenv shell):

**Example 1: Sort by age and output to a file**
```
user-profiles --input input.json --output sorted_by_age.json --sort age
```

**Example 2: Sort by name and output to the screen (stdout)**
```
user-profiles --input input.json --sort name
```

If you're not in the pipenv shell, you can use:
```
pipenv run user-profiles --input input.json --output sorted_by_age.json --sort age
```

#### Using Python module syntax

Alternatively, you can execute the main script using the `-m` flag with Python. If you're inside the pipenv shell (activated with `pipenv shell`), you can run:

**Example 1: Sort by age and output to a file**
```
python -m app.main --input input.json --output sorted_by_age.json --sort age
```

**Example 2: Sort by name and output to the screen (stdout)**
```
python -m app.main --input input.json --sort name
```

Alternatively, if you're not in the pipenv shell, you can use `pipenv run`:

```
pipenv run python -m app.main --input input.json --output sorted_by_age.json --sort age
```

Replace `input.json` with the path to your input file. The `--sort` flag can be set to `age`, `name`, `email`, or `location`.

## Core Components

### UserProfile

The `UserProfile` class represents a user profile with validated information. Each profile contains:

- **name**: Full name (2-3 capitalized words)
- **email**: Email address (unique identifier)
- **password**: Secure password
- **dob**: Date of birth
- **location**: Geographic location (city, state, country)

#### Validation Requirements

All fields in a `UserProfile` must pass strict validation:

**Name Validation:**
- Must contain **exactly 2 or 3 words**
- Each word must start with an uppercase letter followed by lowercase letters
- No numbers, special characters, or extra spaces
- Examples:
  - ✅ Valid: `"John Smith"`, `"Alice Marie Johnson"`, `"Bob Williams"`
  - ❌ Invalid: `"SingleName"` (only one part), `"john Smith"` (not capitalized), `"John3 Smith"` (contains digit), `"Too Many Name Parts Extra"` (more than 3 parts)

**Email Validation:**
- Must match standard email format: `[local-part]@[domain].[tld]`
- Examples:
  - ✅ Valid: `"john.smith@example.com"`, `"user123@domain.co.uk"`
  - ❌ Invalid: `"invalid-email"`, `"user@domain"`

**Password Validation:**
- Must be **at least 8 characters long**
- Must contain one uppercase, one lowercase, one digit and one special character from: `@$!%*?&`
- Examples:
  - ✅ Valid: `"Secure123!"`, `"Password1@"`, `"A1@bcdefg"`
  - ❌ Invalid: `"weak"` (too short), `"password123"` (no uppercase, no special char), `"Password"` (no digit, no special char)

**Date of Birth (DOB) Validation:**
- Must be in one of two formats:
  - `YYYY-MM-DD` (e.g., `"1990-01-15"`)
  - `MM/DD/YYYY` (e.g., `"01/15/1990"`)
- Must be a valid calendar date
- Examples:
  - ✅ Valid: `"1990-01-15"`, `"01/15/1990"`
  - ❌ Invalid: `"15-01-1990"` (wrong format), `"1990-13-45"` (invalid date)

**Location Validation:**
- Format must be: `"City, ST, CC"` (e.g., `"LosAngeles, CA, US"`)
- City: alphabetic characters only (no spaces in city name)
- State: exactly 2 uppercase letters
- Country: exactly 2 uppercase letters
- Examples:
  - ✅ Valid: `"LosAngeles, CA, US"`, `"NewYork, NY, US"`, `"London, EN, GB"`
  - ❌ Invalid: `"Los Angeles, CA, US"` (space in city), `"LosAngeles, ca, US"` (state not uppercase), `"LosAngeles, CA, USA"` (country not 2 letters)

#### Methods

- `validate()`: Validates all fields and returns `True` if all validations pass, `False` otherwise
- `get_age(reference_date=None)`: Calculates age in years from date of birth (defaults to today)

### UserProfileManager

The `UserProfileManager` class manages a collection of user profiles. It stores profiles in a dictionary keyed by email address (ensuring uniqueness).

#### Methods

- `add_profile(profile)`: Adds a validated profile to the manager
  - Validates the profile before adding
  - Raises `ValueError` if profile is invalid or email already exists
- `get_profile(email)`: Retrieves a profile by email address
  - Returns `UserProfile` if found, `None` otherwise
- `remove_profile(email)`: Removes a profile by email address
  - Raises `ValueError` if profile with email does not exist
- `sort_profiles_by_age()`: Sorts profiles by age in **descending order** (oldest first)
- `sort_profiles_by_name()`: Sorts profiles by name alphabetically
- `sort_profiles_by_email()`: Sorts profiles by email alphabetically
- `sort_profiles_by_location()`: Sorts profiles by location (country → state → city)
- `load_profiles_from_json(json_file)`: Loads profiles from a JSON file
  - Accepts both single profile objects `{}` and arrays of profiles `[]`
  - Only loads profiles that pass validation
  - Silently skips invalid profiles with error messages
  - Handles missing fields gracefully
- `save_profiles_to_json(json_file)`: Saves all profiles to a JSON file as an array

#### JSON Input Format

The manager accepts JSON input in two formats:

**Single Profile (object):**
```json
{
    "name": "John Smith",
    "email": "john.smith@example.com",
    "password": "Secure123!",
    "dob": "01/15/1990",
    "location": {
        "city": "LosAngeles",
        "state": "CA",
        "country": "US"
    }
}
```

**Multiple Profiles (array):**
```json
[
    {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "password": "Secure123!",
        "dob": "01/15/1990",
        "location": {
            "city": "LosAngeles",
            "state": "CA",
            "country": "US"
        }
    },
    {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "password": "Password1@",
        "dob": "1995-06-20",
        "location": {
            "city": "NewYork",
            "state": "NY",
            "country": "US"
        }
    }
]
```

Invalid profiles are automatically filtered out during loading, and error messages are printed to help identify issues.


