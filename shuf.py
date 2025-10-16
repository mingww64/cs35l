#!/usr/bin/env python3

import random
import sys
import argparse

def main():

    usage_msg = """%(prog)s [OPTION]... [FILE]
or:  %(prog)s -e [ARG]...
or:  %(prog)s -i LO-HI [OPTION]..."""

    description_msg = """
Write a random permutation of the input lines to standard output.

With no FILE, or when FILE is -, read standard input."""

    parser = argparse.ArgumentParser(
        description=description_msg,
        usage=usage_msg,
        formatter_class=argparse.RawTextHelpFormatter
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        '-e', '--echo',
        action='store_true',
        help='treat each ARG as an input line'
    )
    input_group.add_argument(
        '-i', '--input-range',
        metavar='LO-HI',
        help='treat each number from LO to HI as an input line'
    )

    # Output modification options
    parser.add_argument(
        '-n', '--head-count',
        metavar='COUNT',
        type=int,
        help='output at most COUNT lines'
    )
    parser.add_argument(
        '-r', '--repeat',
        action='store_true',
        help='output lines can be repeated'
    )

    parser.add_argument(
        'operands',
        nargs='*',
        help=argparse.SUPPRESS
    )

    args = parser.parse_args()
    lines = []



    if args.head_count != None and args.head_count < 0:
        parser.error("invalid line count: '{0}'".format(args.head_count))

    try:
        if args.echo:
            lines = [op + '\n' for op in args.operands]
        elif args.input_range:
            if args.operands:
                parser.error("extra operand '{0}' not allowed with -i".format(args.operands[0]))
            try:
                low_str, high_str = args.input_range.split('-')
                low = int(low_str)
                high = int(high_str)
                if low > high:
                     parser.error("invalid input range: '{0}'".format(args.input_range))
                lines = [str(i) + '\n' for i in range(low, high + 1)]
            except ValueError:
                parser.error("invalid input range: '{0}'".format(args.input_range))
        else:
            # Input from a file or stdin
            if len(args.operands) > 1:
                parser.error("extra operand '{0}'".format(args.operands[1]))

            input_source = sys.stdin
            if len(args.operands) == 1 and args.operands[0] != '-':
                try:
                    input_source = open(args.operands[0], 'r')
                except IOError as e:
                    parser.error("cannot open '{0}': {1}".format(args.operands[0], e.strerror))

            with input_source:
                lines = input_source.readlines()

    except Exception as e:
        parser.error(str(e))


    if not lines:
        return

    try:
        if args.repeat:
            if args.head_count != None:
                for _ in range(args.head_count):
                    sys.stdout.write(random.choice(lines))
            else:
                while True:
                    sys.stdout.write(random.choice(lines))
        else:
            random.shuffle(lines)
            count = len(lines)
            if args.head_count != None:
                count = min(args.head_count, len(lines))

            for i in range(count):
                sys.stdout.write(lines[i])

    except KeyboardInterrupt:
        sys.exit(130)

if __name__ == "__main__":
    main()