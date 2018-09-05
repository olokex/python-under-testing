from time import gmtime, strftime
import os
import sys

try:
	path = input("Zadej cestu: ")
	lst_dir = os.listdir(path)
	f_form = input("Zadej formát: ")
except:
	print("Něco se posralo")

cur_time = strftime("%Y%m%d", gmtime())
img_template = f"IMG_{cur_time}_"
i = 0

for filename in lst_dir:
	if i > 9999:
		print("Chyba moc souborů")
		sys.exit(1)
		break

	os.rename(path + "\\" +  filename, path + "\\" + img_template + "{:0>4}".format(i) + "." + f_form)
	i += 1
