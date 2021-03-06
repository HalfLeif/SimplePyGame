import pygame
import time

from core import level


FPS=40
SEC_PER_FRAME=1/FPS


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
    change_each = 6
    if (num_level % change_each != 1):
      # continue with previous music without changing
      return
    track = (num_level // change_each) % len(self.resources.music)
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
    santa = True
    t = time.time()
    while running:
      time_spent = time.time() - t
      if time_spent < SEC_PER_FRAME:
        # Only sleep until the next tick.
        # This keeps FPS relatively stable, although sleep time is not exact.
        time.sleep(SEC_PER_FRAME - time_spent)
      t = time.time()

      if instance.won or instance.lost:
        running = False

      pressed = pygame.key.get_pressed()
      if santa:
        instance.tick(get_direction(pressed))
      instance.draw(santa)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_9:
            print('You cheated!')
            instance.won = True
            self.cheat = True
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            if santa:
              print('Currenlty play, start pause')
              santa = False
            else:
              print('Currenlty pause, start play')
              santa = True

          if event.key == pygame.K_ESCAPE:
            running = False

    self.score += instance.compute_score()
    time.sleep(1)
    return instance.won
