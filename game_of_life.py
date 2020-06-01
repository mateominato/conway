import numpy as np
import argparse
from collections import deque

from matplotlib import pyplot as plt
from matplotlib import animation as animation 
from matplotlib.widgets import Button

ON = 255
OFF = 0
vals = [ON, OFF]

class GameOfLife:
	def __init__(self, size, interval, data, display_len, glider, gosper, pulsar):
		self.buff = deque(np.zeros(display_len))
		self.display_len = display_len
		self.data = data
		self.size = size
		self.interval = interval

		#setup plot
		self.grid = np.array([])
		self.grid = np.zeros(size*size).reshape(size, size)

		if pulsar:
			#self._initializeBoard(True)
			self._add_pulsar(30, 30)
		elif gosper:
			#self._initializeBoard(True)
			self._add_gosper_glider_gun(1, 1)
		elif glider:
			#self._initializeBoard(True)
			self._add_glider(1, 1)
		else:
			self._initializeBoard()

		self.fig, self.ax = plt.subplots() #https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.subplots.html
		self.img = self.ax.matshow(self.grid) #https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.axes.Axes.matshow.html#matplotlib.axes.Axes.matshow, could also use imshow, not sure difference
		self.lines = self.ax.plot([], [])

		#setup animation
		self.cur_frame = 0
		self.anim = animation.FuncAnimation(self.fig, self._update, fargs=(self.img, self.grid, self.size, ), frames=10, interval=interval, save_count=50)

		# setup the animation control
		self.anim_running = True

	def _add_to_buff(self, buf, val):
		if len(buf) < self.display_len:
			buf.appendLeft(val)
		else:
			buf.popleft()
			buf.append(val)

	def _update(self, frameNum, img, grid, N):
		frame = self.cur_frame
		self._add_to_buff(self.buff, self.data[frame:frame+1])
		self.lines[0].set_data(range(self.display_len), self.buff)

		temp = self.grid.copy()
		for i in range(1, N-1): #keep buffer
			for j in range(1, N-1):
				count = int((self.grid[i, j-1] + self.grid[i, j+1] + self.grid[i+1, j-1] + self.grid[i+1, j+1] + self.grid[i+1, j] + self.grid[i-1, j+1] + self.grid[i-1, j-1] + self.grid[i-1, j])/255)
				if self.grid[i,j] == ON:
					if (count < 2) or (count > 3):
						temp[i, j] = OFF
				else:
					if count == 3:
						temp[i,j] = ON

		img.set_data(temp)
		grid[:] = temp[:]

		self.cur_frame += 1

		return img,

	def _initializeBoard(self):
		self.grid = np.random.choice(vals, self.size*self.size, p=[0.2, 0.8]).reshape(self.size, self.size)
		for i in range(self.size):
			for j in range(self.size):
				if (i == 0) or (j == 0) or (i == self.size-1) or (j == self.size-1): #maintain a border so I don't have to deal with any nonsense
					self.grid[i, j] = OFF

	def _reset(self, event):
		self._set_val(0)


	def _set_val(self, frame=0):
		frame = int(frame)
		self.cur_frame = frame
		new_start = frame - self.display_len
		if new_start >= 0:
			self.buff = deque(self.data[new_start:frame])
		else:
			self.buff = deque(np.concatenate((np.zeros(np.abs(new_start)), self.data[:frame])))

		self.anim.event_source.stop()
		self._initializeBoard()
		self.anim = animation.FuncAnimation(self.fig, self._update, fargs=(self.img, self.grid, self.size, ), frames=10, interval=self.interval, save_count=50)
		self.anim_running = True

	def animate(self):
		self.ax.set_axis_off()

		axstart = plt.axes([0.58, 0.02, 0.1, 0.075])
		bstart = Button(axstart, 'Start')
		bstart.on_clicked(self._start)

		axstop = plt.axes([0.70, 0.02, 0.1, 0.075])
		bstop = Button(axstop, 'Stop')
		bstop.on_clicked(self._stop)

		axreset = plt.axes([0.46, 0.02, 0.1, 0.075])
		breset = Button(axreset, 'Reset')
		breset.on_clicked(self._reset)

		plt.show()

	def _start(self, event):
		self.anim.event_source.start()
		self.anim_running = True

	def _stop(self, event):
		self.anim.event_source.stop()
		self.anim_running = False

	def _add_glider(self, i, j):
		glider = np.array([[0, 0, 255], [255, 0, 255], [0, 255, 255]])
		self.grid[i:i+3, j:j+3] = glider

	def _add_gosper_glider_gun(self, i, j): #credit to https://www.geeksforgeeks.org/conways-game-life-python-implementation/ for shape implementation
	    gun = np.zeros(11*38).reshape(11, 38)
	  
	    gun[5][1] = gun[5][2] = ON
	    gun[6][1] = gun[6][2] = ON
	  
	    gun[3][13] = gun[3][14] = ON
	    gun[4][12] = gun[4][16] = ON
	    gun[5][11] = gun[5][17] = ON
	    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = ON
	    gun[7][11] = gun[7][17] = ON
	    gun[8][12] = gun[8][16] = ON
	    gun[9][13] = gun[9][14] = ON
	  
	    gun[1][25] = ON
	    gun[2][23] = gun[2][25] = ON
	    gun[3][21] = gun[3][22] = ON
	    gun[4][21] = gun[4][22] = ON
	    gun[5][21] = gun[5][22] = ON
	    gun[6][23] = gun[6][25] = ON
	    gun[7][25] = ON
	  
	    gun[3][35] = gun[3][36] = ON
	    gun[4][35] = gun[4][36] = ON
	  
	    self.grid[i:i+11, j:j+38] = gun

	def _add_pulsar(self, i, j):
		pulsar = np.zeros(15*15).reshape(15, 15)

		pulsar[3][1] = pulsar[4][1] = pulsar[5][1] = ON
		pulsar[9][1] = pulsar[10][1] = pulsar[11][1] = ON
		pulsar[1][3] = pulsar[1][4] = pulsar[1][5] = ON
		pulsar[1][9] = pulsar[1][10] = pulsar[1][11] = ON

		pulsar[3][13] = pulsar[4][13] = pulsar[5][13] = ON
		pulsar[9][13] = pulsar[10][13] = pulsar[11][13] = ON
		pulsar[13][3] = pulsar[13][4] = pulsar[13][5] = ON
		pulsar[13][9] = pulsar[13][10] = pulsar[13][11] = ON

		pulsar[3][6] = pulsar[4][6] = pulsar[5][6] = ON
		pulsar[3][8] = pulsar[4][8] = pulsar[5][8] = ON

		pulsar[9][6] = pulsar[10][6] = pulsar[11][6] = ON
		pulsar[9][8] = pulsar[10][8] = pulsar[11][8] = ON

		pulsar[6][3] = pulsar[6][4] = pulsar[6][5] = ON
		pulsar[6][9] = pulsar[6][10] = pulsar[6][11] = ON

		pulsar[8][3] = pulsar[8][4] = pulsar[8][5] = ON
		pulsar[8][9] = pulsar[8][10] = pulsar[8][11] = ON

		self.grid[i:i+15, j:j+15] = pulsar

parser = argparse.ArgumentParser(description="RIP John Conway")
parser.add_argument("--size", dest='size', required=False)
parser.add_argument("--glider", action='store_true', dest='glider', required=False)
parser.add_argument("--gosper", action='store_true', dest='gosper', required=False)
parser.add_argument("--pulsar", action='store_true', dest='pulsar', required=False)
args = parser.parse_args()

size = 100
if args.size and int(args.size) > 100:
	size = int(args.size)

interval = 100

lin_sig = np.linspace(0, 1, 1000)
sim = GameOfLife(size, interval, lin_sig, 100, args.glider, args.gosper, args.pulsar)
sim.animate()


