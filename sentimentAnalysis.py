import pandas as pd



class SentimentAnalyzer():

    def __init__(self):
        URL = 'http://www.plosone.org/article/fetchSingleRepresentation.action?uri=info:doi/10.1371/journal.pone.0026752.s001'
        self.labmt = pd.read_csv(URL, skiprows=2, sep='\t', index_col=0, engine='python')

    def averageScore(self, text):
        average = self.labmt.happiness_average.mean()
        happiness = (self.labmt.happiness_average - average).to_dict()
        words = text.split()
        return sum([happiness.get(word.lower(), 0.0) for word in words]) / len(words)



if __name__ == '__main__':

    sa = SentimentAnalyzer()

    print sa.averageScore('amazing the amazing')
    print sa.averageScore('amazing')
    print sa.averageScore('amazing amazing amazing')
