import csv


def process_row(row):
	"""

	"""
	new_row = []
	for i in range(1,len(row)):
		new_row.append(value_dictionary[row[i]])

	return new_row


processed_data = []
value_dictionary = {"BEFRISTET" : 0, "UNBEFRISTET" : 1, "FRAU" : 0, "MANN": 1, "MITTLERE REIFE": 0, "VOLKS-,HAUPTSCHULE": 1, "FACHHOCHSCHULREIFE" : 2, "HOCHSCHULREIFE" : 3, "OHNE ABSCHLUSS" : 4, "ANDERER ABSCHLUSS": 5, "JA": 1, "NEIN":0, "NA": 0}

# read and process data
with open('dataset_selected.csv') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	# skip first row:
	next(readCSV, None)

	for row in readCSV:

		# only store those that don't have NA as label
		if(row[1] != "NA"):
			#print(row)
			new_row = process_row(row)
			print(new_row)
			processed_data.append(new_row)


#print(str(processed_data))

with open('dataset_processed.csv', 'w', newline = '') as csvfile:
	dataWriter = csv.writer(csvfile, delimiter=',')
	for i in range(len(processed_data)):
		dataWriter.writerow(processed_data[i])

