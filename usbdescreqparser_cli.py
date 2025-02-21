from argparse import ArgumentParser

from usbdescreqparser import Parser


def main():
    aparser = ArgumentParser()
    aparser.add_argument("INPUT", nargs=1)
    aparser.add_argument("--stddesc", action="store_true")

    args = aparser.parse_args()

    input_filepath = args.INPUT[0]
    with open(input_filepath, "r", encoding="ascii") as file:
        s = file.read()

    parser = Parser()

    if args.stddesc:
        t = parser.parse_stddesc(s)
        print(t)
    else:
        t = parser.best_guess(s)
        print(t)


if __name__ == "__main__":
    main()
