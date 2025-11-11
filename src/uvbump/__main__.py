import argparse
import sys
from ._core import update_version, UvbumpError


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="uvbump",
        description="Version bumping tool for Python projects using pyproject.toml",
    )
    parser.add_argument(
        "version",
        nargs="?",
        default="bump",
        help="Version to set or bump type (major|minor|patch|bump)",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Use test- prefix for tag instead of v",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    try:
        version_info = update_version(args.version, args.test, args.dry_run)

        # Display results
        print(f"Updated: {version_info.path}")
        print(f"Version: {version_info.old_version} → {version_info.new_version}")
        print(f"Commit: {version_info.commit_message}")
        print(f"Tag: {version_info.tag}")

        if args.dry_run:
            print("(dry run - no changes made)")

    except UvbumpError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
