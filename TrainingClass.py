import cv2
import numpy as np

class training:
	def __init__(self):
		#Constructor function used to initialize the training class instance
		print("Robot Camera Calibration")
		self.configFile = "trainingData.csv"

		#initialize array containing the names of each cluster that will be considered
		self.clusterLabels = ['background', 'line', 'avoid', 'goal']
		# self.clusterLabels = ['line', 'avoid', 'goal']
		self.means = {}

		#Begin the video capture
		self.cap = cv2.VideoCapture(0)

		#Initialize the placement rectangle
		self.boxSize = 100
		self.setBoundingBox();

	def setBoundingBox(self):
		#Determine the north west and south east corner locations
		#for the bounding box of the training sample
		__, frame = self.cap.read()
		rows, cols, __ = frame.shape
		self.center = [rows/2, cols/2]
		self.nw_row = int( self.center[0] - (self.boxSize/2) )
		self.nw_col = int( self.center[1] + (self.boxSize/2) )
		self.se_row = int( self.center[0] + (self.boxSize/2) )
		self.se_col = int( self.center[1] - (self.boxSize/2) )


	def adjustBox(self, newSize):
		#Function used to change the size of the training box
		self.boxSize = newSize
		self.setBoundingBox()

	def meanOfROI(self, img):
		#Perform segmentation to separate the region of interest
		mask = np.zeros(img.shape[:2], dtype = "uint8")
		cv2.rectangle(mask,(self.nw_col, self.nw_row),(self.se_col, self.se_row),255,-1)
		mask = cv2.erode(mask, None, iterations = 2)

		#Calculate the mean color values of the region of interest
		#This is the mean value for the class label of the object
		mean = cv2.mean(img, mask = mask)[:3]
		return mean

	def recordingFrames(self):
		#Function to display successive frames of the video capture with the
		#region of interest bounding box
		while(1):
			#Save a still frame screenshot from the camera as the variable frame
			__, frame = self.cap.read()

			#display the bounding box of the region of interest
			cv2.rectangle(frame, (self.nw_col, self.nw_row), (self.se_col, self.se_row), (0, 255, 0), 1)
			cv2.imshow('train', frame)

			#Display until the letter t is pressed
			if cv2.waitKey(1) & 0xFF == ord('t'):
				break
		return frame

	def train(self):
		#Calculate the corresponding mean to each label from the training data
		for label in self.clusterLabels:
			#Instruct the user to move the camera to view the desired cluster training object
			print("Please move camera over " + label + " then press t to continue")

			#Obtain an image of the object in the class of interest
			frame = self.recordingFrames()

			if label=="background":
				#Calculate the mean RGB values for the entire image
				#This is a background image with not object of interest present
				clusterMean = cv2.mean(frame)[:3]
			else:
				#Calculate the mean RGB values within the region of interest
				clusterMean = self.meanOfROI(frame)

			mean = {label:clusterMean}
			self.means.update(mean)
			print(self.means[label])
		self.updateConfig()

	def updateConfig(self):
		#Save the training date (mean for each cluster label) to a file to prevent redundant
		#need for training at each run
		f = open(self.configFile, "wt")
		for label in self.clusterLabels:
			f.write(label + " : " + str(self.means[label]) + "\n")
		f.close()

	def classifyROI(self, img):
		distances = {}

		m = self.meanOfROI(img)
		mArray = np.asarray(m)

		for label in self.clusterLabels:
			labelMean = np.asarray(self.means[label], dtype = np.uint8)
			d = np.linalg.norm(labelMean - mArray)
			dist = {label:d}
			distances.update(dist)
		val = min(distances, key = distances.get)
		print(val)


	def classifyMean(self, m):
		distances = {}

		#m = self.meanOfROI(img)
		mArray = np.asarray(m)

		for label in self.clusterLabels:
			labelMean = np.asarray(self.means[label], dtype = np.uint8)
			d = np.linalg.norm(labelMean - mArray)
			dist = {label:d}
			distances.update(dist)
		val = min(distances, key = distances.get)
		#print(val)
		return(val)

	def testMeans(self):
		#Function used to test the calculated means by classifying the region of interest
		while(1):
			#Save a still frame screenshot from the camera as the variable frame
			__, frame = self.cap.read()

			#display the bounding box of the region of interest
			cv2.rectangle(frame, (self.nw_col, self.nw_row), (self.se_col, self.se_row), (0, 255, 0), 1)
			cv2.imshow('train', frame)

			self.classifyROI(frame)

			#Display until the letter t is pressed
			if cv2.waitKey(1) & 0xFF == ord('t'):
				break

	def parseConfig(self):
		#Read in the stored means for each object
		means = {}
		f = open(self.configFile, "rt")
		i=0
		for line in f.readlines():
			readMean = list()
			currentLabel = self.clusterLabels[i]
			line = line.strip(currentLabel)
			line = line.rstrip()
			line = line.strip(' ')
			line = line.strip(' :() ')
			line = line.split(",")
			j=0
			for word in line:
				readMean.insert(j,float(word))
				j=j+1
			temp = {currentLabel:tuple(readMean)}
			means.update(temp)
			i=i+1
		self.means = means
		f.close()

if __name__ == '__main__':
	t = training()
	#t.parseConfig()
	t.train()
	t.testMeans()
