
def write_content(content):
	if content:
		if type(content) == list or  type(content) == tuple:
			print(content, type(content)) '''поэлементно'''
		else:
			with open('data_tmp.json','a') as file:
			file.write(content)