import csv


def read_scores(filename):
  all_scores = []
  with open(filename, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
      assert len(row) == 3, row
      name = row[0]
      highest = int(row[1])
      score = int(row[2])
      all_scores.append((name, highest, score))
  return all_scores


def write_all(rows, filename):
  with open(filename, 'w') as file:
    writer = csv.writer(file)
    for row in rows:
      writer.writerow(row)


class HighScore:
  def __init__(self):
    self.filename = 'data/score.csv'
    self.all_scores = read_scores(self.filename)
    self.last = None

  def add_score(self, name, highest_level, score):
    self.last = (name, highest_level, score)
    self.all_scores.append(self.last)
    # Sort on score.
    self.all_scores.sort(key=lambda t: -t[2])

  def get_unique_scores(self):
    # already sorted
    uniqued = []
    seen = set()
    for t in self.all_scores:
      name = t[0]
      if not name in seen:
        seen.add(name)
        uniqued.append(t)
    return uniqued

  def write(self):
    write_all(self.all_scores, self.filename)
