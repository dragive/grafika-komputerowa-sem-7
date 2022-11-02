from PIL import Image

"""
To
pixel
sort, we
first
need
to
load
all
the
pixels in an
image
file.
We'll
then
loop
through
each
row
of
the
image
data, record
the
color
value
of
each
pixel in the
row, then
sort
the
row
based
on
those
values.
"""


def sort_row(row):
    min = 255 * 3
    min_index = 0
    # find the darkest pixel in the row
    for i in range(len(row)):
    # each pixel has an RPG value, for instance (255, 255, 255)
    temp = row[i][0] + row[i][1] + row[i][2]
    if temp < min:
        min = temp
    min_index = i
    # sort the row up the brightest pixel
    sorted_row = row[:min_index]
    sorted_row.sort()


return sorted_row + row[min_index:]


def pixel_sort():
    print("loading
    the
    image...
    ")
    # load the image data
    img = Image.open("motorboat.jpg")
    # load the pixel data from the file.
    pixels = img.load()

    width, height = img.size
    print("sorting    the    image...    ")
    # loop through each row and sort the pixels in that row
    for y in range(height):
    # get a row
        row = []
    for x in range(width):
        row.append(pixels[x, y])
    # sort the row
    row = sort_row(row)
    # record the sorted data
    for x in range(width):
        pixels[x, y] = row[x]
    # to make a new image, we'll need to conver the data to a list
    sorted_pixels = []
    for y in range(height):
        for x in range(width):
            sorted_pixels.append(pixels[x, y])
            new_img = Image.new('RGB', (width, height))
            new_img.putdata(sorted_pixels)
    print("image    preview...    ")
    # preview the sorted image.
    new_img.show()
    print("saving    image...    ")
    # save the file with a new name.
    new_img.save("motorboat_sorted.jpg")
    pixel_sort()
