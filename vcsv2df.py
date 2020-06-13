import pandas as pd
import csv, argparse, re
from functools import reduce

def vcsv2df(f_in):
#	if isinstance(fname, str):
#		f_in = open(f_in,'r')
	# 2. row: ; name,;
	# 3. row: ;X, Y,;
	# 5 .row: ;xname, Y,;
	# 6. row: ;xunit, yunit,;
	#---------------------------------------------------
	# creating a helper database
	# 2. and 5.row contains important data
	l_axes = []
	l_name = []
	with open(f_in,"r") as f_csv:
		for idx, line in enumerate(f_csv, 1):
			if idx in [2,5]: # only wave name, and xaxis name
				line = re.sub("^;","",line)	# remove first semicolon
				line = re.sub(",;",",", line)  # remove semicolon separators
				line = re.sub("\s*\n$",",", line)  # remove newline
				l_line = list(filter(len,line.split(',')))
				if idx==2:
					l_name = l_line.copy()
				elif idx==5:
					l_axes = l_line.copy()
				else:
					print(idx)
					raise ValueError("idx should be in the list of [2,5]")

	#---------------------------------------------------
	# check if all axis are the same
	n_x = len(set(l_axes[::2]))
	n_y = len(set(l_axes[1::2]))
	if n_x!=1:
		raise ValueError("Not all X axis name are the same. Either bad data, error in the code or a very unique dataset")
	if n_y!=1:
		raise ValueError("Not all Y axis name are the same. Either bad data, error in the code or a very unique dataset")
	x_axis = list(set(l_axes[::2]))[0]

	#---------------------------------------------------
	# build the final dataframe from small dataframes
	my_range = len(l_name)
	l_df = []
	for i in range(my_range):
		m = re.match('(?P<name>.*) \((?P<par>.*)\)',l_name[i])
		if m:
			sig_name = m.group('name')
			l_wp = m.group('par').split('|')  # wp = wave paramters
		else:
			sig_name = l_name[i]

		# print(m.group('name'))
		# print(l_wp)

		df = pd.read_csv(f_in, header=None, skiprows=6, usecols=[2*i,2*i+1], names=[x_axis,sig_name], dtype=float)
		if m:
			for j in l_wp:
				k = j.split("=")
				df[k[0]] = float(k[1])
		l_df.append(df)
		# print(df)
	
	if m: # we have the same signal for different paramter values
		return pd.concat(l_df, ignore_index=True)
	else: # we have different signals
		return reduce(lambda  left,right: pd.merge(left,right, how='outer'), l_df)   

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="""Read in a VCSV file (from Cadence ViVA waveform data) into a python dataframe""")
	parser.add_argument("f_in", help="input vcsv file", type=str, metavar='fname_in')
	args = parser.parse_args()

	df = vcsv2df(args.f_in)
	pd.set_option('display.max_rows', None)
	print(df)
	
