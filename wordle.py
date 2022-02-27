import os
import pandas as pd
import game as gm

#This class manages the options and file input and output
class Wordle:

    def __init__(self, pool:str, pool_dir:str, pattern_dir:str) -> None:
        self.pool = pool
        self.patterns_pth = pattern_dir
        self.allowed_pth = pool_dir + '/' + pool + '/allowed-guesses.txt'
        self.answers_pth = pool_dir + '/' + pool + '/answers.txt'
        self.__set_patterns()
        self.__set_words()

    #Reads the patterns from the files
    def __set_patterns(self) -> pd.DataFrame:
        #Gets every child directory from the patterns dir
        pattern_dirs = [self.patterns_pth + '/' + x for x in next(os.walk(self.patterns_pth))[1]]
        
        patterns = []
        for p_dir in pattern_dirs:
            #Gets only the dir name
            p_name = os.path.basename(p_dir)
            p_file = p_dir + '/pattern.txt'
            
            lines = []
            with open(p_file) as file:
                for idx,line in enumerate(file):
                    #Creates an array for each line in the file with its index. Ex.: [0,[0,1,1,0,2]]
                    lines.append([idx, [int(l) for l in list(line.rstrip())]])
            
            #Array with the name of the pattern and the pattern itself
            patterns.append([p_name, lines])
        
        #Makes a DataFrame with named columns just to make things easier
        self.patterns = pd.DataFrame(patterns, columns=['name','pattern'])
    
    #Reads the words from the pools
    def __set_words(self) -> None:
        answers = []
        words = []

        #Possible answers are used in both answers(passwords) and words(guesses)
        with open(self.answers_pth) as file:
            for line in file:
                answers.append(line.rstrip())
                words.append(line.rstrip())

        #Allowed guesses populate only the words
        with open(self.allowed_pth) as file:
            for line in file:
                words.append(line.rstrip())
        
        self.answers = answers
        self.words = words
    
    #Generates solutions and writes them to a file
    def play(self, pattern_name:str, attempts:int=1, repeat_pwd:bool=True, trace:bool=True) -> None:

        #Finds the chosen pattern
        pattern_rows = self.patterns.loc[self.patterns['name'] == pattern_name]['pattern']
        if pattern_rows.empty:
            if trace: print('Pattern named ' + pattern_name + ' not found.')
            return
        pattern = pattern_rows.iloc[0]

        #Sets the solutions file path
        patternf_path = self.patterns_pth + '/' + pattern_name + '/' + self.pool + '_' + ('repeat' if repeat_pwd else 'distinct') + '.csv'

        if trace: print('Generating solutions...')
        for i in range(0, attempts):
            if trace: print('Attempt ' + str(i+1))

            #Generates the possible solutions
            possible_games = gm.playMultiple(self.answers, pattern, self.words)

            #Separates the pattern from the guesses and changes them into tuples for later
            pgames_array = []
            for pg in possible_games:
                pgames_array.append([pg[0], tuple([x[1] for x in pg[1]])])
            pgames_df = pd.DataFrame(pgames_array, columns=['password','game'])

            #Creates directories if something doesn't exist
            os.makedirs(os.path.dirname(patternf_path), exist_ok=True)

            #Creates the solutions file if it doesn't exist
            f = open(patternf_path, 'a')
            if os.stat(patternf_path).st_size <= 0:
                f.write('password,game')
            f.close()
                
            #Reads file to join the results and remove duplicates.
            pgames_file = pd.read_csv(patternf_path)
            pgames_df = pd.concat([pgames_df,pgames_file])
            #It normally checks both the password and the game to define duplicates, but can check the password alone if desired.
            pgames_df = pgames_df[~pgames_df.duplicated(subset=['password','game'] if repeat_pwd else ['password']).values]

            #Sorts alfabetically
            pgames_df = pgames_df.sort_values(by='password')

            #Writes to file
            pgames_df.to_csv(patternf_path, index=False)

            if trace: print('File updated')
        if trace: print('Finished')