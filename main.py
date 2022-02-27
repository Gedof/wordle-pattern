from ast import pattern
from wordle import Wordle


pool_dir = './word_pools'
pattern_dir = './patterns'

wordle = Wordle('wordle', pool_dir, pattern_dir)
wordle.play('diagonal', attempts=2, repeat_pwd=True, trace=True)