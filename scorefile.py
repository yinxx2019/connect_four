class ScoreFile:
    def __init__(self):
        self.score_dict = {}
        self.count = 0

    def process_file(self):
        score_file = open('scores.txt', 'r')
        for line in score_file:
            line = line.rstrip().rsplit(' ', 1)
            name = line[0].strip().capitalize()
            score = int(line[1])
            if name in self.score_dict.keys():
                self.score_dict[name] += score
            else:
                self.score_dict[name] = score
        dic_list = sorted(self.score_dict.items(),
                          key=lambda x: x[1], reverse=True)
        score_file.close()
        score_file = open('scores.txt', 'w')
        for i in dic_list:
            score_file.write(i[0]+' ' + str(i[1]) + '\n')
        score_file.close()
        self.count += 1
