# import the necessary packages
import numpy as np
import argparse
import cv2
 
# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", help = "path to the image")
# args = vars(ap.parse_args())

# load the image
cam = cv2.VideoCapture(0)

ret, frame = cam.read()
cv2.imshow("test", frame)

capimg = cv2.imwrite("image", frame)
image = cv2.imread(capimg)

# define the list of boundaries
boundaries = [
	([40, 39, 59], [150, 149, 180])
]

# loop over the boundaries
for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
 
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(image, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)
 
	# show the images
	cv2.imshow("images", np.hstack([image, output]))
	cv2.waitKey(0)