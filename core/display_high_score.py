import pygame
from enum import Enum

from core import score


WHITE = (255, 255, 255)
BLUE = (0, 0, 128)


class Alignment(Enum):
  CENTER = 0
  RIGHT = 1

class TextArea:
  '''Draws a bounding box around several text rects.'''

  def __init__(self, screen, y):
    self.screen = screen
    self.screen_size = screen.get_size()
    self.rects = []
    self.y = y


  def add_text(self, text_string, fsize, align=Alignment.CENTER, offset=0):
    font = pygame.font.Font('freesansbold.ttf', fsize)
    text = font.render(text_string, True, WHITE, BLUE)

    self.y += 0.5*fsize
    textRect = text.get_rect()
    if align == Alignment.CENTER:
      textRect.center = (self.screen_size[0] // 2, self.y)
    elif align == Alignment.RIGHT:
      textRect.top = self.y
      textRect.right = offset
    else:
      raise ValueError(f'Alignment not implemented: {align}')

    self.y += 0.5*fsize + 5
    self.rects.append((text, textRect))
    return textRect


  def add_row(self, fields, fsize, offset=0):
    '''Aligns each column on RIGHT.'''
    y = self.y
    right = offset
    # Referencing other rects for distancing easily produces bad results, since
    # prevous rect size differs depending on its content. For now hardcode
    # difference. A proper solution would be to make a grid layout or so.
    for f in reversed(fields):
      self.y = y
      rect = self.add_text(str(f), fsize, align=Alignment.RIGHT, offset=right)
      right -= 140

    return rect


  def bounding_box(self):
    universe = self.rects[0][1]
    for (text, rec) in self.rects[1:]:
      universe = universe.union(rec)
    return universe.inflate(50, 50)


  def draw(self):
    box = self.bounding_box()
    pygame.draw.rect(self.screen, BLUE, box)
    pygame.draw.rect(self.screen, WHITE, box, width=2)
    for (text, textRect) in self.rects:
      self.screen.blit(text, textRect)
    pygame.display.update()


def high_score_screen(screen, score, resources):
  if score.last[1] >= 7:
    pygame.mixer.music.load(resources.happy_end_music)
  else:
    pygame.mixer.music.load(resources.sad_music)
  pygame.mixer.music.play()

  area = TextArea(screen, 200)

  title = area.add_text('HighScore', 64)
  area.add_text('', 16)

  offset = title.right + 30
  area.add_row(('Name', 'Level', 'Score'), 24, offset=offset)
  high_score = score.get_unique_scores()
  for row in high_score[:10]:
    area.add_row(row, 24, offset=offset)

  area.add_text('', 16)
  area.add_row(score.last, 32, offset=offset)
  area.draw()

  y = 100 + area.bounding_box().bottom
  bottom = TextArea(screen, y)
  bottom.add_text('Press ESC to quit. Press ENTER to try again.', 24)
  bottom.draw()
