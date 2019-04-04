import json

fields = ['currentHeight',
'currentWidth',
'scrollPositionY',
'scrollPositionX',
'keypress',
'shiftPress',
'ctrlPress',
'positionX',
'positionY']

def reader():
	with open("data_tmp.json", 'r') as f:
		json_str = (f.read()).split('\n\n')
		for string in json_str:
			try:
				json_data = json.loads('''{}'''.format(string))
				if (json_data):
					for info in json_data:
						if (info):
							event_type = info['type']
							current_page = info['current_page']
							minutes = info['minutes']
							seconds = info['seconds']
							data = info['data']
							if ('selectedText' in data.keys()):
								selectedText = data['selectedText']
							else:
								selectedText = None
							if ('currentHeight' in data.keys()):
								currentHeight = data['currentHeight']
							else:
								currentHeight = None
							if ('currentWidth' in data.keys()):
								currentWidth = data['currentWidth']
							else:
								currentWidth = None
							if ('scrollPositionY' in data.keys()):
								scrollPositionY = data['scrollPositionY']
							else:
								scrollPositionY = None
							if ('scrollPositionX' in data.keys()):
								scrollPositionX = data['scrollPositionX']
							else:
								scrollPositionX = None
							if ('keypress' in data.keys()):
								keypress = data['keypress']
							else:
								keypress = None
							if ('shiftPress' in data.keys()):
								shiftPress = data['shiftPress']
							else:
								shiftPress = None
							if ('ctrlPress' in data.keys()):
								ctrlPress = data['ctrlPress']
							else:
								ctrlPress = None
							if ('positionX' in data.keys()):
								positionX = data['positionX']
							else:
								positionX = None
							if ('positionY' in data.keys()):
								positionY = data['positionY']
							else:
								positionY = None
							print("    ", event_type, ' ', current_page, ' ', minutes, ' ', seconds, ' ', currentHeight, ' ', currentWidth, ' ', scrollPositionY, ' ', scrollPositionX, ' ', keypress, ' ', shiftPress, ' ', ctrlPress, ' ', positionX, ' ', positionY, ' ')
				# for data in json_data:
				# 	print("    ", data)
				# print("\n\n")
			except:
				print(1)
				

reader()
# json_data = json.loads('''{"type": 3, "current_page": "https://www.youtube.com/watch?v=tzTeWc9jPeI", "minutes": 56, "seconds": 30, "miliseconds": 43, "data": {"currentHeight": 900, "currentWidth": 1440}}''')
# print(json_data)