import math
import random
import pygame

from core import update


VICTORY_BG=(0xff, 0xd3, 0x00)
DEFEAT_BG=(106, 40, 126)

START_ALPHAS=7
GOAL_RADIUS=50


def get_background(num):
  '''Returns a background color for this level.

     Picks a color randomly within the specified color range.
  '''
  min = [30, 100, 160]
  max = [85, 240, 255]
  color = []
  for i in range(3):
    color.append(random.randrange(min[i], max[i]))
  return color


def generate_position(screen_size):
  '''Generate any random position.'''
  max_x, max_y = screen_size
  x = random.uniform(0, max_x)
  y = random.uniform(0, max_y)
  return (x,y)


def generate_position_with_distance(player, image_size, distance, screen_size):
  '''Generate position at least distance away from player.'''
  pos = generate_position(screen_size)
  while update.touches_circle(player, image_size, pos, distance):
    pos = generate_position(screen_size)
  return pos


def generate_alphas(player, number, image_size, screen_size):
  alphas = []
  alpha_velocities = []
  for i in range(number):
    alphas.append(generate_position_with_distance(player, image_size, 300, screen_size))
    alpha_velocities.append((0,0))
  return alphas, alpha_velocities


class Level:
  '''Tracks all objects for one level of the game.'''

  def __init__(self, num_level, screen, resources):
    self.num_level = num_level
    self.screen = screen
    self.resources = resources
    self.survived_iterations = 0

    self.screen_size = self.screen.get_size()
    self.image_size = self.resources.player_img.get_rect().size

    self.won = False
    self.lost = False

    self.player = (0,0)
    self.velocity = (0,0)

    self.goal = generate_position_with_distance(self.player, self.image_size, 450, self.screen_size)

    num_deltas = 0
    if num_level >= 3:
      num_deltas = (num_level // 2)

    num_giants = 0
    if num_level >= 5:
      num_giants = (num_level // 3)

    total_monster = START_ALPHAS + 3 * (self.num_level - 1)
    num_alphas = total_monster - 2*num_deltas - 3*num_giants

    self.alphas, self.alpha_velocities = generate_alphas(self.player, num_alphas, self.image_size, self.screen_size)
    self.deltas, self.delta_velocities = generate_alphas(self.player, num_deltas, self.image_size, self.screen_size)
    self.giants, self.giant_velocities = generate_alphas(self.player, num_giants, self.image_size, self.screen_size)

    self.background = get_background(self.num_level)


  def draw_img(self, img, center_pos):
    '''Draws image on screen.

       center_pos is the middle of the object.
       Calculates top left corner for drawing.
    '''
    w = img.get_width()
    h = img.get_height()
    (x,y) = center_pos
    self.screen.blit(img, (x - w/2, y - h/2))


  def draw(self, playing):
    '''Draws the current game state.'''
    if self.won:
      background = VICTORY_BG
    elif self.lost:
      background = DEFEAT_BG
    else:
      background = self.background

    self.screen.fill(background)

    self.draw_img(self.resources.goal_img, self.goal)
    self.draw_img(self.resources.player_img, self.player)

    for giant in self.giants:
      self.draw_img(self.resources.giant_img, giant)

    for alpha in self.alphas:
      self.draw_img(self.resources.alpha_img, alpha)

    for delta in self.deltas:
      self.draw_img(self.resources.delta_img, delta)

    if not playing:
      box = pygame.Rect(50, 50, 500, 250)
      pygame.draw.rect(self.screen, (0,0,0), box)

    pygame.display.flip()


  def lose(self):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(self.resources.explosion_sound)
    self.lost = True


  def tick(self, direction):
    '''Updates the model one iteration.

       Changes nothing if already won or lost.
    '''
    if self.won or self.lost:
      return

    self.velocity = update.mul(direction, update.MAX_SPEED)

    self.survived_iterations += 1
    self.player = update.add(self.player, self.velocity)
    self.player = update.bounds(self.player, self.image_size, self.screen_size)

    self.alphas, self.alpha_velocities = update.move_alphas(self.alphas, self.alpha_velocities, self.screen_size)
    self.giants, self.giant_velocities = update.move_giants(self.giants, self.giant_velocities, self.screen_size)
    self.deltas, self.delta_velocities = update.move_deltas(self.deltas, self.delta_velocities, self.screen_size, self.player)

    if update.touches_circle(self.player, self.image_size, self.goal, GOAL_RADIUS):
      pygame.mixer.Sound.play(self.resources.door_sound)
      self.won = True

    for alpha in (self.alphas + self.deltas):
      if not self.won and update.touches_circle(self.player, self.image_size, alpha, update.ALPHA_RADIUS):
        self.lose()
        break

    for giant in self.giants:
      if not self.won and update.touches_circle(self.player, self.image_size, giant, update.GIANT_RADIUS):
        self.lose()
        break


  def compute_score(self):
    '''If won, returns max score.

       Otherwise return asymptotically approaching max score based on survived_iterations.
    '''
    max_score = self.num_level * 1000
    if self.won: return max_score

    k = 1e-3
    progression = 1 - math.exp(-k*self.survived_iterations)
    return math.floor(max_score * progression)
