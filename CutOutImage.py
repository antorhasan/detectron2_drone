from PIL import Image 
import numpy as np 


cnt = 0

#read tif to numpy array
def read_image():
	im = Image.open('odm_orthophoto_cut.tif')
	nparray = np.array(im) 
	#print(nparray[6600][5000]) #height, width, channels
	return nparray


def check_blank_pixel(A):
	emptycount = 0
	for row in A:
		for col in row:
			a, b, c = col 
			if (not a) and (not b) and (not c):
				emptycount += 1

	if emptycount > 3000:
		return True 
	else:
		return False 


def save_image(A):
	global cnt 
	A = A[:,:,0:3]
	if check_blank_pixel(A):
		return 

	im = Image.fromarray(A)
	name = 'New Segment Images 5/cut' + str(cnt) + ".jpg"
	im.save(name)
	cnt += 1


#scan each array of numpy array and find valid cells in each row
def scan_image(nparray):
	tallies = []
	height, width, numchannel = nparray.shape 
	for row in nparray:
		start = False 
		end = False 
		startnum = -1
		endnum = -1
		for i in range(len(row)):
			a, b, c, d = row[i] #r g b garbage
			if a or b or c:
				start = True 
				startnum = i 
				break
		for i in range(len(row)-1, -1, -1):
			a, b, c, d = row[i] #r g b garbage
			if a or b or c:
				end = True 
				endnum = i
				break
		
		tallies.append([startnum, endnum])

	return tallies 


def find_boundary(start, stop, tallies):
	tallystart = [i[0] for i in tallies[start:stop]]
	tallyend = [i[1] for i in tallies[start:stop]]
	
	left = max(tallystart)
	right = min(tallyend)

	return left, right 



#convert numpy to grid sized images
def make_images(nparray, tallies):
	global cnt 
	row_ends = []
	constant = 512
	count = 0
	tallylen = len(tallies)
	i = 0
	while i < tallylen:
		if tallies[i][0]!=-1 and tallies[i][1]!=-1:
			startcol, stopcol = find_boundary(i, i+constant, tallies)
			print('starts are', startcol, stopcol)
			if (stopcol - startcol) < constant:
				i += 1
				continue
			for j in range(startcol, stopcol, constant//2):
				temp_array = nparray[i:i+constant, j:j+constant, :]
				print('saving image')
				save_image(temp_array)
				count += 1
			i += ((constant//2) - 1)
			row_ends.append(cnt-1)
		i += 1
		
	file = open('Endings.txt', 'w+')
	tempstr = ""
	for i, num in enumerate(row_ends):
		tempstr += str(num) + "\n"
	file.write(tempstr)
	file.close()

def print_to_file(tallies):
	file = open('tallies3.txt', 'w+')

	for i in range(len(tallies)):
		line = str(tallies[i][0]) + " " + str(tallies[i][1]) + "\n"
		file.write(line)

	file.close()



def read_tally_from_file():
	file = open('tallies3.txt', 'r')
	tallies = []
	lines = file.readlines()
	
	for i in range(len(lines)):
		temp = lines[i].split()
		a, b = int(temp[0]), int(temp[1])
		tallies.append([a, b])
	
	file.close()
	return tallies






nparray = read_image()
#tallies = scan_image(nparray)
tallies = read_tally_from_file()
#print_to_file(tallies)
make_images(nparray, tallies)



