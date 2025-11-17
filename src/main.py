import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from .user_manager import UserProfileManager


def _sort_profiles(manager: UserProfileManager, key: str):
    """Sort profiles by the specified key.
    
    Args:
        manager: UserProfileManager instance
        key: Sort key ("age", "name", "email", or "location")
        
    Returns:
        List of sorted UserProfile objects
        
    Raises:
        SystemExit: If sort key is invalid
    """
    if key == "age":
        return manager.sort_profiles_by_age()
    elif key == "name":
        return manager.sort_profiles_by_name()
    elif key == "email":
        return manager.sort_profiles_by_email()
    elif key == "location":
        return manager.sort_profiles_by_location()
    else:
        raise SystemExit(f"Unknown sort key: {key}")


def _write_output(obj, output_path: Optional[str]):
    """Write output to file or stdout.
    
    Args:
        obj: Object to serialize as JSON
        output_path: Optional path to output file (None = stdout)
    """
    if output_path:
        out_path = Path(output_path)
        with out_path.open("w") as f:
            json.dump(obj, f, indent=4)
    else:
        json.dump(obj, sys.stdout, indent=4)
        sys.stdout.write('\n')


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for user profile processing.
    
    Loads profiles from JSON, sorts them, and outputs results.
    
    Args:
        argv: Optional command-line arguments (defaults to sys.argv)
        
    Returns:
        Exit code (0 for success)
        
    Raises:
        SystemExit: If no valid profiles are loaded
    """
    parser = argparse.ArgumentParser(description="User profiles processor")
    parser.add_argument("--input", "-i", required=True, help="Path to input JSON (single user or list)")
    parser.add_argument("--output", "-o", help="Path to write output JSON (defaults to stdout)")
    parser.add_argument(
        "--sort",
        choices=["age", "name", "email", "location"],
        default="age",
        help="Sort key (default: age)",
    )
    args = parser.parse_args(argv)

    manager = UserProfileManager()
    manager.load_profiles_from_json(args.input)

    if len(manager.user_profiles) == 0:
        raise SystemExit("No valid profiles loaded from input file.")

    sorted_profiles = _sort_profiles(manager, args.sort)
    output_list = []
    for profile in sorted_profiles:
        profile_dict = profile.to_dict()
        output_list.append(profile_dict)
    _write_output(output_list, args.output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())