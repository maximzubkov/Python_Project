def insert_history_to_file(data,filepath):
	with open(filepath,'w') as file:
		keys_of_data = (list(data[0].keys()))
		keys_to_file = str(keys_of_data[0]) + ',' + str(keys_of_data[1]) + '\n'
		file.write(keys_to_file)
		for line in data:
			line_to_file = str(line['url'])+','+str(line['moment'])+'\n'
			file.write(line_to_file)