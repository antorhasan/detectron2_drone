from PIL import Image
import numpy as np
import rasterio
from rasterio.plot import reshape_as_image
import cv2
import fiona
import rasterio
import rasterio.mask
import shapefile
from Contour2Building2Heights2Json import pix_to_latlon_2

cnt = 0

# read tif to numpy array


def read_image():
    with rasterio.open('./data/dhanmondi/0.tif') as data:
        #data = rasterio.open('./data/dhanmondi/0.tif')
        data = data.read()
        data = reshape_as_image(data)
        data = np.asarray(data)
        """ data = np.asarray(data[:,:,0:3], dtype=np.uint8)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow('image', data)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(asd) """
        print(data.shape)

    return data


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
    A = A[:, :, 0:3]  # dsfds
    if check_blank_pixel(A):
        return

    im = Image.fromarray(A)
    name = './data/dhanmondi/crop/' + str(cnt) + ".jpg"
    im.save(name)
    cnt += 1


# scan each array of numpy array and find valid cells in each row
def scan_image(nparray):
    tallies = []
    height, width, numchannel = nparray.shape
    for row in nparray:
        start = False
        end = False
        startnum = -1
        endnum = -1
        for i in range(len(row)):
            a, b, c, d = row[i]  # r g b garbage
            if a or b or c:
                start = True
                startnum = i
                break
        for i in range(len(row)-1, -1, -1):
            a, b, c, d = row[i]  # r g b garbage
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


# convert numpy to grid sized images
def make_images(nparray, tallies):
    global cnt
    overlap = True
    start_offset = 4096
    row_ends = []
    constant = 3072
    count = 0
    tallylen = len(tallies)
    i = 0

    if overlap == True :
        window_step = constant//2
    else :
        window_step = constant

    while i < tallylen:
        if tallies[i][0] != -1 and tallies[i][1] != -1:
            startcol, stopcol = find_boundary(i, i+constant, tallies)

            startcol = startcol + start_offset
            stopcol = stopcol - start_offset

            print('starts are', startcol, stopcol)
            if (stopcol - startcol) < constant:
                i += 1
                continue
            
            for j in range(startcol, stopcol, window_step):
                temp_array = nparray[i:i+constant, j:j+constant, :]

                save_image(temp_array)
                count += 1
            i += ((window_step) - 1)
            row_ends.append(cnt-1)
        i += 1

    file = open('./data/dhanmondi/Endings.txt', 'w+')
    tempstr = ""
    for i, num in enumerate(row_ends):
        tempstr += str(num) + "\n"
    file.write(tempstr)
    file.close()


def print_to_file(tallies):
    file = open('./data/dhanmondi/0.txt', 'w+')

    for i in range(len(tallies)):
        line = str(tallies[i][0]) + " " + str(tallies[i][1]) + "\n"
        file.write(line)

    file.close()


def read_tally_from_file():
    file = open('./data/dhanmondi/0.txt', 'r')
    tallies = []
    lines = file.readlines()

    for i in range(len(lines)):
        temp = lines[i].split()
        a, b = int(temp[0]), int(temp[1])
        tallies.append([a, b])

    #create_shp(tallies)
    #print(tallies)
    file.close()
    return tallies



def create_shp(tallies):
    left_id = []
    right_id = []
    off_set = 3072
    #tallies = tallies[0:20000]
    print('introducing offset.....')
    for i in range(len(tallies)):
        if tallies[i][0] != -1 and tallies[i][1] != -1 :
            right_id.append([i,tallies[i][1] - off_set])
            left_id.append([i,tallies[i][0] + off_set])

    left_id.reverse()

    all_pix = right_id + left_id

    px_row = []
    px_col = []

    for i in range(len(all_pix)):
        px_row.append(all_pix[i][0])
        px_col.append(all_pix[i][1])

    tiff_path = './data/dhanmondi/0.tif'

    print('writing shapefile......')
    lats, lons = pix_to_latlon_2(tiff_path,False, px_row, px_col)

    w = shapefile.Writer('./data/dhanmondi/shp/polygon0')
    w.field('name', 'C')
    poly_list = []
    print('creating polygon.......')
    for i in range(len(lats)):
        poly_list.append([lons[i],lats[i]])
    #print(poly_list)
    w.poly([poly_list])
    w.record('polygon1')
    w.close


def msk_raster():

    with fiona.open("./data/dhanmondi/shp/temp.shp", "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    with rasterio.open("./data/dhanmondi/0.tif") as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

    with rasterio.open("./data/fin_0.tif", "w", **out_meta) as dest:
        dest.write(out_image)



if __name__ == "__main__":
    #msk_raster()
    nparray = read_image()
    print(nparray.shape)
    #tallies = scan_image(nparray)
    #tallies = read_tally_from_file()
    #print_to_file(tallies)
    #make_images(nparray, tallies)
    pass

