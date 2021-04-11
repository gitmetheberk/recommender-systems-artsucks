import re
while True:
	x = input()
	x = x.replace('_', ' ')
	x = re.sub(r'[0-9]*\.jpg', '',x)
	print(x)