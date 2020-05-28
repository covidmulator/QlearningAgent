import time
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image

np.random.seed(1)
PhotoImage = ImageTk.PhotoImage
unit = 50
height = 15
width = 15

class Env(tk.Tk):
  def __init__(self):
    super(Env, self).__init__()
    self.action_space = ['w', 's', 'a', 'd'] # wsad 키보드 자판을 기준으로 상하좌우
    self.actions_length = len(self.action_space)
    self.height = height*unit
    self.width = width*unit
    self.title('codefair qlearning')
    self.geometry(f'{self.height}x{self.width}')
    self.shapes = self.load_images()
    self.canvas = self.build_canvas()


  def build_canvas(self):
    canvas = tk.Canvas(self, bg="white", height=self.height, width=self.width)

    for c in range(0, self.width, unit):
      x0, y0, x1, y1 = c, 0, c, self.height
      canvas.create_line(x0, y0, x1, y1)
    for r in range(0, self.height, unit):
      x0, y0, x1, y1 = 0, r, self.height, r
      canvas.create_line(x0, y0, x1, y1)

    # mark images to canvas
    self.agent = canvas.create_image(50, 50, image=self.shapes[0])
    self.virus = canvas.create_image(175, 175, image=self.shapes[1])
    self.destination = canvas.create_image(275, 275, image=self.shapes[2])

    canvas.pack()

    return canvas

  def load_images(self):
    agent = PhotoImage(Image.open("./img/agent.png").resize((50, 50)))
    virus = PhotoImage(Image.open("./img/virus.jpg").resize((50, 50)))
    destination = PhotoImage(Image.open("./img/destination.png").resize((50, 50)))

    return agent, virus, destination

  def coords_to_state(self, coords):
    x = int((coords[0] - 50) / 100)
    y = int((coords[1] - 50) / 100)
    return [x, y]
  
  def state_to_coords(self, state):
    x = int(state[0] * 100 + 50)
    y = int(state[1] * 100 + 50)
    return [x, y]

  def reset(self):
    self.update()
    time.sleep(.5)
    x, y = self.canvas.coords(self.agent)
    self.canvas.move(self.agent, unit/2 - x, unit/2 - y)
    self.render()
    return self.coords_to_state(self.canvas.coords(self.agent))

  def step(self, action):
    state = self.canvas.coords(self.agent)
    base_action = np.array([0, 0])
    self.render()

    # actions
    if action == 0: # w
      if state[1] > unit:
        base_action[1] -= unit
    elif action == 1: # s
      if state[1] < (height - 1) * unit:
        base_action[1] += unit
    elif action == 2: # a
      if state[0] > unit:
        base_action[0] -= unit
    elif action == 3: # d
      if state[0] < (width - 1) * unit:
        base_action[0] += unit
    
    self.canvas.move(self.agent, base_action[0], base_action[1])

    self.canvas.tag_raise(self.agent)
    next_state = self.canvas.coords(self.agent)

    # reward
    if next_state == self.canvas.coords(self.destination):
      reward = 100
      finish = True
    elif next_state == self.canvas.coords(self.virus):
      reward = -100
      finish = True
    else:
      reward = 0
      finish = False

    next_state = self.coords_to_state(next_state)
    return next_state, reward, finish

  def render(self):
    time.sleep(.03)
    self.update()