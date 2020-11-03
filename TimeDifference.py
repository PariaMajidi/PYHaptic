#!/usr/bin/env python
import csv, os

thresholdPhone = 5.126
thresholdWatch = 8.5

durationBetween2Vibrations = 0.05

def detectVibrations(rows, threshold, column):
	isVibrating = False
	lastTimeAboveThreshold = 0
	vibrations = []

	for row in rows:

		time = float(row[0])
		voltage = abs(float(row[column]))

		if voltage > threshold:
			if not isVibrating:
				vibrations.append(time)
				isVibrating = True


			lastTimeAboveThreshold = time
		elif time - lastTimeAboveThreshold > durationBetween2Vibrations:
			isVibrating = False

	return vibrations

phoneVibrations = []
watchVibrations = []


def convertReaderIntoArray (reader):
	rows = []
	for row in reader:
		rows.append(row)
	return rows


dirname = 'Experiment5_with_filters'

for filename in os.listdir('./' + dirname):
	with open('./' + dirname + '/' + filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		next(reader, None)
		next(reader, None)
		next(reader, None)

		rows = convertReaderIntoArray(reader)

		phoneVibrationsForPlot = detectVibrations(rows, thresholdPhone, 1)
		watchVibrationsForPlot =  detectVibrations(rows, thresholdWatch, 2)
		phoneVibrations = phoneVibrations + phoneVibrationsForPlot
		watchVibrations = watchVibrations + watchVibrationsForPlot

		print(filename)
		print(phoneVibrationsForPlot)
		print(watchVibrationsForPlot)


with open('vibrations.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter='\t')

	vibrationsCount = max(len(phoneVibrations), len(watchVibrations))
	writer.writerow(['vibration phone (s)', 'vibration watch (s)', 'difference (s)', 'error indicator'])
	for index in range(0, vibrationsCount - 1):

		phoneVibrationTime = 0
		if index >= len(phoneVibrations):
			phoneVibrationTime = 'X'
		else:
			phoneVibrationTime = phoneVibrations[index]

		watchVibrationTime = 0
		if index >= len(watchVibrations):
			watchVibrationTime = 'X'
		else:
			watchVibrationTime = watchVibrations[index]

		diff = 'X'
		if watchVibrations != 'X' and phoneVibrationTime != 'X':
			diff = watchVibrationTime - phoneVibrationTime 


		errorIndicator = ''
		if diff != 'X' and diff < 0:
			errorIndicator = 'FATAL ERROR: missing one phone vibration'
		elif index + 1 < len(phoneVibrations) :
			nextPhoneVibration = phoneVibrations[index + 1]
			differenceWithNextPhoneVibration = watchVibrationTime - nextPhoneVibration
			if differenceWithNextPhoneVibration > 0:
				errorIndicator = 'FATAL ERROR: missing one watch vibration'

		writer.writerow([phoneVibrationTime, watchVibrationTime, diff, errorIndicator])
