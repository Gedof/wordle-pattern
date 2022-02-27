import argparse
import textwrap

from wordle import Wordle

class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):
    def _get_help_string(self, action):
        return textwrap.dedent(action.help)

def start():
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--pool', '-pl', required=True, help='Name of the directory containing the pool of words to use. (Required)')
    parser.add_argument('--pattern', '-pt', required=True, help='Name of the directory containing the pattern to run. (Required)')
    parser.add_argument('--attempts', '-at', type=int, default=1, help='Number of times the program will run on each pattern. This matters because the possible solutions use random generations, so running a pattern a second time will probably create different solutions. If --distinct, new solutions to the same password will be discarded.(Default: 1)')
    parser.add_argument('--pools_dir', '-pld', default='./word_pools', help='Path to the directory containing all the word pools. (Default: ./word_pools)')
    parser.add_argument('--patterns_dir', '-ptd', default='./patterns', help='Path to the directory containing all the patterns. (Default: ./patterns)')
    parser.add_argument('--distinct', '-d', action='store_true', default=False, help='Keep only one solution for each password. Only matters if using --attempts greater than 1 or if running the pattern a second time.')
    parser.add_argument('--trace', '-t', action='store_true', default=False, help='Show execution text.')
    
    args = parser.parse_args()

    pool = args.pool
    pattern = args.pattern
    attempts = args.attempts
    pools_dir = args.pools_dir
    patterns_dir = args.patterns_dir
    repeat = not args.distinct
    trace = args.trace


    wordle = Wordle(pool, pools_dir, patterns_dir)
    wordle.play(pattern, attempts=attempts, repeat_pwd=repeat, trace=trace)

if __name__ == '__main__':
    start()