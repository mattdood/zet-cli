"""Zet tool's main execution."""
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="zet", description="Zettlekasten command line tools"
    )

    parser.add_argument()

    parser.add_argument("-t", "--title", action="store", help="a zet title")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")


if __name__ == "__main__":
    main()
