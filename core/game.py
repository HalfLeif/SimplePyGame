import pygame
import time

from core import level

def get_direction(pressed):
  dx = 0
  dy = 0
  if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
    dy += 1
  if pressed[pygame.K_UP] or pressed[pygame.K_w]:
    dy -= 1
  if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
    dx += 1
  if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
    dx -= 1
  return (dx, dy)


class Game:
  '''Runs one game instance.

     Sums player score.
  '''
  def __init__(self, screen, resources):
    self.screen = screen
    self.resources = resources
    self.score = 0
    self.highest_level = 0
    self.cheat = False


  def run(self):
    '''Runs one game, with many levels.'''
    alive = True
    num_level = 0
    while alive:
      num_level += 1
      alive = self.run_level(num_level)
    self.highest_level = num_level


  def play_music(self, num_level):
    '''Changes music track every N levels.'''
    change_each = 5
    if (num_level % 5 != 1):
      # continue with previous music without changing
      return
    track = (num_level // 5) % len(self.resources.music)
    pygame.mixer.music.load(self.resources.music[track])
    pygame.mixer.music.play()


  def run_level(self, num_level):
    '''Runs one level of the game.

       Returns whether the player cleared the level.
       Difficulty increases with `num_level`.
    '''
    instance = level.Level(num_level, self.screen, self.resources)
    self.play_music(num_level)

    running = True
    while running:
      # 50 fps = 1/50 sec = 20 ms
      # Sleep for 20 ms
      time.sleep(0.020)
      if instance.won or instance.lost:
        running = False

      pressed = pygame.key.get_pressed()
      instance.set_direction(get_direction(pressed))
      instance.tick()
      instance.draw()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_9:
            print('You cheated!')
            instance.won = True
            self.cheat = True
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False

    self.score += instance.compute_score()
    time.sleep(1)
    return instance.won
