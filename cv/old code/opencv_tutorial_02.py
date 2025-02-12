
#counting objects

#import the necesarry packages
import argparse
import imutils
import cv2

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args=vars(ap.parse_args)

#converting image to grayscale
#load the input image (whose path was supplied via command line)
#argument) and display the image to our screen
image = cv2.imread(args["image"])
cv2.imshow("image", image)
cv2.waitKey(0)

#convert images to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
cv2.waitKey(0)

#edge detection
#applying edge detection 
edged = cv2.Canny(gray, 30,150)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

#Threshholding
#threshold the image by setting all pixel values less than 225
#to 225(white;foreground) and all pixel values >= 225 to 225
# (black; background), thereby segemnting the image
thresh = cv2.threshold(gray, 225, 335, cv2,THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

#detecting and drawing countours
#find contours(outlines) of the foreground objects in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

#loop over the contours
for c in cnts:
		#draw wach contour on the output image with a 3px thick purple
		#outline, then display the output contours one at a time
		cv2.drawContours(output, [c], -1, (240,0,159),3)
		cv2,imshow("Contours", output)
		cv2.waitKey(0)

#draw the total number of countours found in purple
text = "{} objects found!!!!!!".format(len(cnts))
cv2.putText(output, text, (10.25), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
	(240,0,159),2)
cv2.imshow("Contours", output)
cv2.waitKey(0)

#Erosions and dilations
#erosions are apploed to reduce the size of foreground objects
mask = thresh.copy()
mast = cv2.erode(mask, None, iterations=5)
cv2.imshow("Eroded", mask)
cv2.waitKey(0)
#this same code can be applied with Dilate/Dilated instead of Erode/Eroded

#a typical operation applied is to take the mask and apply
#a bitwise AND to the unput image, keepingo only the masked regions
mask = thresh.copy()
output - cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Output", output)
cv2.waitKey(0)
