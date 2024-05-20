import ast


class Scorer:
    scores = {}

    def __init__(self):
        self.get_from_file()

    def get_from_file(self):
        with open("scores", 'r', encoding='utf-8') as file:
            self.scores = ast.literal_eval(file.read())

    def put_in_file(self):
        with open("scores", 'a', encoding='utf-8') as file:
            file.truncate(0)
            file.write(str(self.scores))

    def get_score_from_id(self, id):
        if id not in self.scores:
            self.scores[id] = 100.0
        self.put_in_file()
        return float(self.scores[id])

    def win(self, id1, id2):
        r1 = self.get_score_from_id(id1)
        r2 = self.get_score_from_id(id2)
        e1 = 1 / (1 + pow(10, (r2 - r1) / 400))
        e2 = 1 / (1 + pow(10, (r1 - r2) / 400))
        r1, r2 = r1 + 10 * (1 - e1), r2 + 10 * (0 - e2)
        self.scores[id1] = r1
        self.scores[id2] = r2
        self.put_in_file()

    def draw(self, id1, id2):
        r1 = self.get_score_from_id(id1)
        r2 = self.get_score_from_id(id2)
        e1 = 1 / (1 + pow(10, (r2 - r1) / 400))
        e2 = 1 / (1 + pow(10, (r1 - r2) / 400))
        r1, r2 = r1 + 10 * (0.5 - e1), r2 + 10 * (0.5 - e2)
        self.scores[id1] = r1
        self.scores[id2] = r2
        self.put_in_file()
