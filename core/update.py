import math
import random


ALPHA_MAX_SPEED=7
ALPHA_RADIUS=20
DELTA_MAX_SPEED=5


def add(pos, delta):
  x,y = pos
  dx,dy = delta
  return (x+dx, y+dy)


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


def negate(vec):
  x,y = vec
  return (-x, -y)


def bounds(pos, image_size, screen_size):
  x,y = pos
  w,h = image_size
  W,H = screen_size
  if x < 0:
    x = 0
  if y < 0:
    y = 0
  if W < x + w:
    x = W - w
  if H < y + h:
    y = H - h
  return (x,y)


def check_bounce(pos, velocity, image_size, screen_size):
  x,y = pos
  w,h = image_size
  W,H = screen_size
  vx, vy = velocity
  if x < 0:
    vx = -vx
  if y < 0:
    vy = -vy
  if W < x + w:
    vx = -vx
  if H < y + h:
    vy = -vy
  return (vx,vy)


def check_max_speed(velocity, speed):
  if norm(velocity) > speed:
    return mul(normalize(velocity), speed)
  return velocity


def move_alpha(alpha, velocity, screen_size):
  alpha = add(alpha, velocity)
  velocity = check_bounce(alpha, velocity, (ALPHA_RADIUS, ALPHA_RADIUS), screen_size)
  alpha = bounds(alpha, (ALPHA_RADIUS, ALPHA_RADIUS), screen_size)

  # Random acceleration
  dx = random.uniform(-1, 1)
  dy = random.uniform(-1, 1)
  velocity = add(velocity, (dx, dy))
  velocity = check_max_speed(velocity, ALPHA_MAX_SPEED)

  return alpha, velocity


def move_alphas(alphas, alpha_velocities, screen_size):
  new_alphas = []
  new_vs = []
  for alpha, velocity in zip(alphas, alpha_velocities):
    new_pos, new_velocity = move_alpha(alpha, velocity, screen_size)
    new_alphas.append(new_pos)
    new_vs.append(new_velocity)
  return new_alphas, new_vs


def move_delta(pos, v, screen_size, target):
  pos = add(pos, v)

  # Accelerate towards target
  direction = sub(target, pos)
  acc = normalize(direction)

  v = add(v, acc)
  v = check_max_speed(v, DELTA_MAX_SPEED)
  return pos, v


def move_deltas(positions, velocities, screen_size, target):
  new_pos = []
  new_vs = []
  for pos, v in zip(positions, velocities):
    npos, nv = move_delta(pos, v, screen_size, target)
    new_pos.append(npos)
    new_vs.append(nv)
  return new_pos, new_vs


def touches_circle(pos, image_size, circle, radius):
  distance = norm(sub(pos, circle))
  return distance < radius + 0.5*image_size[1]
