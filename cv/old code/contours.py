import numpy as np
import cv2
import imutils
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

#image = cv2.imread('mask4.png')

height = np.size(image, 0)
width = np.size(image, 1)

#convert images to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)
cv2.imshow("Gray", gray)
cv2.waitKey(0)


mask = gray.copy()
kernel = np.ones((5,5),np.uint8)
eroded = cv2.erode(mask, kernel, iterations=4)
cv2.imshow("eroded", eroded)
cv2.waitKey(0)

#Erosions and dilations
#erosions are apploed to reduce the size of foreground objects
mask = gray.copy()
kernel = np.ones((5,5),np.uint8)
dilated = cv2.dilate(eroded, kernel, iterations=3)
cv2.imshow("dilated", dilated)
cv2.waitKey(0)

#cv.Mat vesselImage = cv.imread(mask)


#edge detection
#applying edge detection 
edged = cv2.Canny(dilated, 30,150)
cv2.imshow("Edged", edged)
cv2.waitKey(0)

#Threshholding
#threshold the image by setting all pixel values less than 225
#to 225(white;foreground) and all pixel values >= 225 to 225
# (black; background), thereby segemnting the image
#thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
#cv2.imshow("Thresh", thresh)
#cv2.waitKey(0)
#return

#detecting and drawing countours
#find contours(outlines) of the foreground objects in the thresholded image
cnts, heirarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(immat,contours,-1,CV_RGB(255,0,0),2);
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:2]

print('cnts:')
print(cnts)
print('=========')
#cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
#grabbedcnts = imutils.grab_contours(cnts)
#output = image.copy()

#loop over the contours
'''for c in grabbedcnts:
		#draw wach contour on the output image with a 3px thick purple
		#outline, then display the output contours one at a time
		cv2.drawContours(output, [c], -1, (0,255,0),1)
		cv2.imshow("Contours", output)'''
#cnts = cnts[0]50
M = cv2.moments(cnts[0])
print (M)
#print(len(cnts))
#draw the total number of countours found in purple
#text = "{} objects found!!!!!!".format(len(cnts))
#cv2.putText(output, text, (10.25), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
	#(240,0,159),2)
#cv2.imshow("Contours", output)
#cv2.waitKey(0)

#this same code can be applied with Dilate/Dilated instead of Erode/Eroded

# loop over the contours

for c in cnts:
	#approcimate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	for x in range(len(approx)):
		cv2.circle(image, (approx[x][0][0], approx[x][0][1],), 7, (0, 0, 255), -1)
	#cv2.Circle(image, (approx[1][0][0], approx[1][0][1],), 7, (0, 0, 255), -1)

	print(approx)


	x,y,w,h = cv2.boundingRect(c)
	cv2.rectangle(image,(x,y), (x+w, y+h), (0,255,0), 2)
	cv2.imshow("bounding rectangle",image)
	cv2.waitKey(0)

	print(str(x/width) + " " + str(y/height) + " " + str((x+w)/width) + " " +  str((y+h)/height))

	# compute the center of the contour
	'''M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])'''

	if M["m00"] != 0:
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
	else:
		cX, cY = 0,0

		# draw the contour and center of the shape on the image
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
		#cv2.putText(image, "center", (cX - 20, cY - 20),
			#cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	print(cX/width, cY/height)



	# show the image
cv2.imshow("Image", image)
cv2.waitKey(0)
