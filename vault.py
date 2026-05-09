import argparse
import sys
import manager


def main():
    parser = argparse.ArgumentParser(
        prog="vault",
        description="A simple encrypted CLI password manager",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="Initialise a new vault")

    p_add = sub.add_parser("add", help="Add a new password")
    p_add.add_argument("site", help="Site name (e.g. github)")
    p_add.add_argument("username", help="Your username or email")

    p_get = sub.add_parser("get", help="Get a password")
    p_get.add_argument("site", help="Site name")
    p_get.add_argument("--show", action="store_true", help="Print password instead of copying")

    p_del = sub.add_parser("delete", help="Delete an entry")
    p_del.add_argument("site", help="Site name")

    sub.add_parser("list", help="List all saved sites")

    args = parser.parse_args()

    if args.command == "init":
        manager.initialise_vault()
    elif args.command == "add":
        manager.add_password(args.site, args.username)
    elif args.command == "get":
        manager.get_password(args.site, copy=not args.show)
    elif args.command == "delete":
        manager.delete_password(args.site)
    elif args.command == "list":
        manager.list_passwords()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()