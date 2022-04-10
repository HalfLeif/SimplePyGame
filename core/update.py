import math
import random


MAX_SPEED=9
ALPHA_MAX_SPEED=7
DELTA_MAX_SPEED=5
GIANT_MAX_SPEED=3

ALPHA_RADIUS=20
GIANT_RADIUS=80

ALPHA_ACC=0.7
GIANT_ACC=0.1

def add(pos, delta):
  x,y = pos
  dx,dy = delta
  return (x+dx, y+dy)


def negate(vec):
  x,y = vec
  return (-x, -y)


def sub(pos, delta):
  return add(pos, negate(delta))


def mul(pos, scalar):
  x,y = pos
  return (scalar * x, scalar * y)


def norm(vec):
  x,y = vec
  return math.sqrt(x**2 + y**2)


def normalize(vec):
  return mul(vec, 1/norm(vec))


# assert norm(normalize((3,4))) == 1
# assert norm(mul(normalize((3,4)), 2)) == 2


def bounds(pos, image_size, screen_size):
  '''Returns updated position after checking bounds.

     - pos: center of object
     - image_size: width and height of object
     - screen_size: width and height of screen
  '''
  x,y = pos
  w,h = image_size
  W,H = screen_size

  left = x - w/2
  right = x + w/2
  top = y - h/2
  bottom = y + h/2

  if left < 0:
    x = w/2
  if top < 0:
    y = h/2

  if x + w/2 > W:
    x = W - w/2
  if y + h/2 > H:
    y = H - h/2

  return (x,y)


def check_bounce(pos, velocity, image_size, screen_size):
  '''If object touches the wall, then bounces in opposite direction.
     Returns new velocity.
  '''
  x,y = pos
  w,h = image_size
  W,H = screen_size

  left = x - w/2
  right = x + w/2
  top = y - h/2
  bottom = y + h/2

  vx, vy = velocity
  if left < 0:
    vx = -vx
  if top < 0:
    vy = -vy

  if right > W:
    vx = -vx
  if bottom > H:
    vy = -vy

  return (vx,vy)


def check_max_speed(velocity, speed):
  '''If travelling faster than speed, reduces velocity to speed.
     Returns new velocity.
  '''
  if norm(velocity) > speed:
    return mul(normalize(velocity), speed)
  return velocity


def move_monsters(positions, velocities, fn):
  new_pos = []
  new_vs = []
  for pos, v in zip(positions, velocities):
    npos, nv = fn(pos, v)
    new_pos.append(npos)
    new_vs.append(nv)
  return new_pos, new_vs


def move_alpha(alpha, velocity, screen_size, monster_radius, max_speed, max_acc):
  '''Moves alpha virus, with bouncing.'''
  alpha = add(alpha, velocity)
  velocity = check_bounce(alpha, velocity, (monster_radius, monster_radius), screen_size)
  alpha = bounds(alpha, (monster_radius, monster_radius), screen_size)

  # Random acceleration
  dx = random.uniform(-1, 1)
  dy = random.uniform(-1, 1)
  acc = mul(normalize((dx, dy)), max_acc)
  velocity = add(velocity, acc)
  velocity = check_max_speed(velocity, max_speed)

  return alpha, velocity


def move_delta(pos, v, screen_size, target):
  '''Moves delta virus, with targetting.'''
  pos = add(pos, v)

  # Accelerate towards target
  direction = sub(target, pos)
  acc = normalize(direction)

  v = add(v, acc)
  v = check_max_speed(v, DELTA_MAX_SPEED)
  return pos, v


def move_alphas(positions, velocities, screen_size):
  return move_monsters(positions, velocities,
      lambda p,v: move_alpha(p, v, screen_size, ALPHA_RADIUS, ALPHA_MAX_SPEED, ALPHA_ACC))


def move_giants(positions, velocities, screen_size):
  return move_monsters(positions, velocities,
      lambda p,v: move_alpha(p, v, screen_size, GIANT_RADIUS, GIANT_MAX_SPEED, GIANT_ACC))


def move_deltas(positions, velocities, screen_size, target):
  return move_monsters(positions, velocities,
      lambda p,v: move_delta(p, v, screen_size, target))


def touches_circle(pos, image_size, circle, radius):
  '''Returns whether the object is overlapping this circle.'''
  distance = norm(sub(pos, circle))
  return distance < radius + 0.5*image_size[1]
