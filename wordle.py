import os
import pandas as pd
import game as gm


class Wordle:

    def __init__(self, pool:str, pool_dir:str, pattern_dir:str) -> None:
        self.pool = pool
        self.patterns_pth = pattern_dir
        self.allowed_pth = pool_dir + '/' + pool + '/allowed-guesses.txt'
        self.answers_pth = pool_dir + '/' + pool + '/answers.txt'
        self.__set_patterns()
        self.__set_words()

    def __set_patterns(self) -> pd.DataFrame:
        pattern_dirs = [self.patterns_pth + '/' + x for x in next(os.walk(self.patterns_pth))[1]]
        patterns = []
        for p_dir in pattern_dirs:
            p_name = os.path.basename(p_dir)
            p_file = p_dir + '/pattern.txt'
            lines = []
            with open(p_file) as file:
                for idx,line in enumerate(file):
                    lines.append([idx, [int(l) for l in list(line.rstrip())]])
            patterns.append([p_name, lines])
        self.patterns = pd.DataFrame(patterns, columns=['name','pattern'])
    
    def __set_words(self) -> None:
        answers = []
        words = []

        with open(self.answers_pth) as file:
            for line in file:
                answers.append(line.rstrip())
                words.append(line.rstrip())

        with open(self.allowed_pth) as file:
            for line in file:
                words.append(line.rstrip())
        
        self.answers = answers
        self.words = words
    
    def play(self, pattern_name:str, attempts:int=1, repeat_pwd:bool=True, trace:bool=True) -> None:

        pattern_rows = self.patterns.loc[self.patterns['name'] == pattern_name]['pattern']
        if pattern_rows.empty:
            if trace: print('Pattern named ' + pattern_name + ' not found.')
            return
        
        pattern = pattern_rows.iloc[0]

        patternf_path = self.patterns_pth + '/' + pattern_name + '/' + self.pool + '_' + ('repeat' if repeat_pwd else 'distinct') + '.csv'

        if trace: print('Generating solutions...')
        for i in range(0, attempts):
            if trace: print('Attempt ' + str(i+1))

            possible_games = gm.playMultiple(self.answers, pattern, self.words)

            pgames_array = []

            for pg in possible_games:
                pgames_array.append([pg[0],tuple([x[1] for x in pg[1]])])

            pgames_df = pd.DataFrame(pgames_array, columns=['password','game'])

            os.makedirs(os.path.dirname(patternf_path), exist_ok=True)

            
            f = open(patternf_path, 'a')
            if os.stat(patternf_path).st_size <= 0:
                f.write('password,game')
            f.close()
                

            pgames_file = pd.read_csv(patternf_path)

            pgames_df = pd.concat([pgames_df,pgames_file])
            pgames_df = pgames_df[~pgames_df.duplicated(subset=['password','game'] if repeat_pwd else ['password']).values]
            pgames_df = pgames_df.sort_values(by='password')

            pgames_df.to_csv(patternf_path, index=False)

            if trace: print('File updated')
        if trace: print('Finished')