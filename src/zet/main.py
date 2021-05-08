"""Zet tool's main execution."""
import optparse


def main():
    p = optparse.OptionParser()
    p.add_option("--name", "-n")

    options, arguments = p.parse_args()


if __name__ == "__main__":
    main()
