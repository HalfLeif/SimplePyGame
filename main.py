import pygame
import sys
import time
from enum import Enum

from core import game
from core import score
from core import display_high_score as hs


class Resources:
  def __init__(self):
     self.player_img = pygame.image.load("resources/player.png")
     self.alpha_img = pygame.image.load("resources/virus2.png")
     self.delta_img = pygame.image.load("resources/delta.png")
     self.giant_img = pygame.image.load("resources/giant.png")
     self.goal_img = pygame.image.load("resources/star.png")

     self.door_sound = pygame.mixer.Sound("resources/door.wav")
     self.explosion_sound = pygame.mixer.Sound("resources/explosion.wav")
     self.music = [
       "resources/ode_to_dub_step.wav",
       # Doesn't work because unsupported format...
       # "resources/edtijo__happy-8bit-pixel-adenture.wav",
       "resources/edwardszakal__game-music.mp3",
     ]
     self.sad_music = 'resources/toivo161__melancholic-piano-ballad.wav'
     self.happy_end_music = 'resources/michorvath__rivalry-8-bit-music-loop.wav'


class ExitCode(Enum):
  QUIT = 1
  RETRY = 2


def wait(t) -> ExitCode:
  '''Return on ESC with timeout `t`.'''
  while t > 0:
    # 50 fps = 1/50 sec = 20 ms
    # Sleep for 20 ms
    time.sleep(0.020)
    t -= 0.020
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return ExitCode.QUIT
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          return ExitCode.QUIT
        if event.key in (pygame.K_r, pygame.K_RETURN):
          return ExitCode.RETRY
  return ExitCode.QUIT


def main(player_name):
  pygame.init()
  pygame.display.set_caption("Leif's mini")
  screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  resources = Resources()

  code = ExitCode.RETRY
  while (code != ExitCode.QUIT):
    g = game.Game(screen, resources)
    g.run()
    print(f'\n{player_name} made it unto level {g.highest_level}, with score {g.score}.')

    if g.cheat:
      # no high score update
      break
    s = score.HighScore()
    s.add_score(player_name, g.highest_level, g.score)
    s.write()

    hs.high_score_screen(screen, s, resources)
    code = wait(60)

if __name__ == '__main__':
  if (len(sys.argv) <= 1):
    print('Must provide player name as argument.')
  else:
    main(sys.argv[1])
