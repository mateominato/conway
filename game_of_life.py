import numpy as np
import argparse
from matplotlib import pyplot as plt
from matplotlib import animation as animation 

ON = 255
OFF = 0
vals = [ON, OFF]

def initializeBoard(size):
	board = np.random.choice(vals, size*size, p=[0.2, 0.8]).reshape(size, size)
	for i in range(size):
		for j in range(size):
			if (i == 0) or (j == 0) or (i == size-1) or (j == size-1): #maintain a border so I don't have to deal with any nonsense
				board[i, j] = OFF
	return board

def update(frameNum, img, grid, N):
	temp = grid.copy()
	for i in range(1, N-1): #keep buffer
		for j in range(1, N-1):
			count = int((grid[i, j-1] + grid[i, j+1] + grid[i+1, j-1] + grid[i+1, j+1] + grid[i+1, j] + grid[i-1, j+1] + grid[i-1, j-1] + grid[i-1, j])/255)
			if grid[i,j] == ON:
				if (count < 2) or (count > 3):
					temp[i, j] = OFF
			else:
				if count == 3:
					temp[i,j] = ON

	img.set_data(temp)
	grid[:] = temp[:]
	return img,


def main():
	parser = argparse.ArgumentParser(description="RIP John Conway")

	parser.add_argument("--size", dest='size', required=False)
	args = parser.parse_args()

	size = 100
	if args.size and int(args.size) > 10:
		size = int(args.size)

	interval = 100
	grid = np.array([])
	grid = initializeBoard(size)

	fig, ax = plt.subplots() #https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.subplots.html
	img = ax.matshow(grid) #https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.axes.Axes.matshow.html#matplotlib.axes.Axes.matshow, could also use imshow, not sure difference
	ani = animation.FuncAnimation(fig, update, fargs=(img, grid, size, ), frames=10, interval=interval, save_count=50)

	plt.show()

if __name__ == '__main__':
	main()