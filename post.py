import matplotlib.pyplot as plt
import re
import numpy as np
import pandas as pd
from optparse import OptionParser
import os,sys, argparse
from glob import glob
from datetime import datetime

###--------------------store function--------------------------###

def getForces(source_path):
	# make regular expressions
	scalarStr = r"([0-9.eE\-+]+)"
	vectorStr = r"\(([0-9.eE\-+]+)\s([0-9.eE\-+]+)\s([0-9.eE\-+]+)\)"
	space =  r"\s+"
	threeVectorStr = r"\({}{}{}{}{}\)".format(vectorStr,space,vectorStr,space,vectorStr)
	forceRegex = r"{}{}{}{}{}".format(scalarStr,space,threeVectorStr,space,threeVectorStr)

	t = []
	fpx = []; fpy = []; fpz = []
	fpox = []; fpoy = []; fpoz = []
	fvx = []; fvy = []; fvz = []
	mpx = []; mpy = []; mpz = []
	mpox = []; mpoy = []; mpoz = []
	mvx = []; mvy = []; mvz = []

	pipefile = open(source_path+"/forces.dat",'r')
	#pipefile = open('./postProcessing/forcesIncompressible/0/forces.dat','r')
	lines = pipefile.readlines()

	for line in lines:
	        match = re.search(forceRegex,line)
	        if match:
	                t.append(float(match.group(1)))
	                fpx.append(float(match.group(2)))
	                fpy.append(float(match.group(3)))
	                fpz.append(float(match.group(4)))
	                fvx.append(float(match.group(5)))
	                fvy.append(float(match.group(6)))
	                fvz.append(float(match.group(7)))
	                fpox.append(float(match.group(8)))
	                fpoy.append(float(match.group(9)))
	                fpoz.append(float(match.group(10)))
	                mpx.append(float(match.group(11)))
	                mpy.append(float(match.group(12)))
	                mpz.append(float(match.group(13)))
	                mvx.append(float(match.group(14)))
	                mvy.append(float(match.group(15)))
	                mvz.append(float(match.group(16)))
	                mpox.append(float(match.group(17)))
	                mpoy.append(float(match.group(18)))
	                mpoz.append(float(match.group(19)))

	force_df = pd.DataFrame(data={"fpx":fpx,"fpy":fpy,"fpz":fpz,"fvx":fvx,"fvy":fvy,"fvz":fvz})
	force_df.index = t
	force_df.index.name = "Iter"

	return force_df

def getyPlus():
	source_path = os.getcwd()+"/postProcessing/yPlus/0"
	filelist = os.listdir(source_path)
	number_of_timesteps = len(filelist)
	# get patch names from abitrary file
	patchnames = []
	file = open(source_path+"/"+filelist[0])
	lines = file.readlines()[2:]
	for line in lines:
		patchnames.append(line.split()[1])
	file.close()

	# get patch values
	t = []; patch = []; min = []; max = []
	for filename in filelist:
		file = open(source_path+"/"+filename)
		lines = file.readlines()
		for line in lines[2:]:	# skip header lines
			t.append(int(line.split()[0]))
			patch.append(line.split()[1])
			min.append(float(line.split()[2]))
			max.append(float(line.split()[3]))
		file.close()

	# put errthang in a Dataframe
	all_files = pd.DataFrame(data={"patch":patch,"min":min,"max":max})
	all_files.index = t
	all_files.index.name = "Iter"

	# return frame sorted by patches
	all_files.sort_values("patch",inplace=True)
	return all_files, number_of_timesteps

##-----------------plot-function----------------------###
def plotForces(case,start=1):
	df = pd.read_csv("./storage/"+case+".csv")
	print(df.size)
	fig1, axs = plt.subplots(2,1)
	fig1.suptitle("Kraefte stationaer")
	if start != 1:
		df = df.truncate(before=start)
		print(df.size)
#	axs[0].plot(df.index,df["fpx"],label='fpx')
	axs[0].plot(df.index,df["fpy"],label='fpy')
	axs[0].set_ylabel('Pressure Forces')
	axs[0].legend(loc='best')

	axs[1].plot(df.index,df["fvx"],label='fvx')
	axs[1].plot(df.index,df["fvy"],label='fvy')
	axs[1].set_ylabel('Viscous Forces')
	axs[1].legend(loc='best')

	axs[-1].set_xlabel('Iterations')
	print(df.head())
	print(df.tail())
	plt.show()

def compare(cases,niter = 0):
	dfs = []
	fig = plt.figure()
	ax1 = fig.gca()
	count = 0

	for case in cases:
		fname = "./storage/"+case+".csv"
		dfs.append(pd.read_csv(fname))
		#if niter != 0:
		#	dfs[0:niter-1,:]
		print(type(dfs))
		ax1.plot(dfs[count].index,dfs[count]["fpy"])

		count += 1

	plt.show()


def initLog():
	logfile = open(os.getcwd()+"/resultlog","w")
	now = datetime.now()
	timestr = now.strftime("%Y-%m-%d_%H-%M")
	logfile.write(timestr+"\t"+"initialized resultlog"+"\n")
	logfile.close()
	return timestr

def addLog(description,new_result=True):
	logfile = open(os.getcwd()+"/resultlog","a+")
	now = datetime.now()
	timestr = now.strftime("%Y-%m-%d_%H-%M")
	if new_result:
		logfile.write("------\n")
		logfile.write(timestr+"\t"+description+"\n")
		logfile.close()
		return timestr
	logfile.write("\t\t\t"+description+"\n")
	logfile.close()

def plotFrameToAxis(axindex,comp):
	axs[axindex].plot(df.index,df["f"+comp],label='f'+comp)


if __name__ == "__main__":
	# throw exception if no arguments are provided
	if len(sys.argv) < 2:
		sys.exit("error: arguments needed")

	# init method is initialising folder (date_no) and logs description in file
	if sys.argv[1] == "init":
		folderName = initLog()

	# add method is adding a new result to the resultlog
	# with option -a an additional string can be appended to the latest resultlog
	elif sys.argv[1] == "add":
		if len(sys.argv) < 3 or (sys.argv[2] == "-a" and len(sys.argv) < 4):
			sys.exit("error: description needed")

		if "-a" in sys.argv[1:]:
			addLog(sys.argv[-1],new_result=False)
		else:
			newFolder = addLog(sys.argv[-1])
			os.makedirs(os.getcwd()+"/storage/"+newFolder)

	# store method stores the results from /postProcessing in dataframe for plotting
	# the name of the entity to store is provided as an argument
	# the method reads the latest folder from the resultlog and stores the dataframe there
	elif sys.argv[1] == "store":
		if len(sys.argv) < 3:
			sys.exit("error: entity name needed")

		# determine where to store
		file = open("./resultlog","r")
		lines = file.readlines()
		directories = []
		for line in lines:
			match = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}', line)
			if match is not None: directories.append(match.group())
		if len(directories) < 1: sys.exit("no entries in resultlog")

		# get the values
		# storing the dataframes
		if sys.argv[2] == "forces":

			# init an empty Dataframe to append to
			frames_to_store = pd.DataFrame()

			# get the list of time folders
			postProcessing_directory = "./postProcessing/forcesIncompressible/"
			time_directories = os.listdir(postProcessing_directory)
			for time_directory in time_directories:
				path = postProcessing_directory+time_directory
				frames_to_store=frames_to_store.append(other=getForces(path))

			# store the frames
			frames_to_store.to_csv("./storage/"+directories[-1]+"/forces.csv")

		# get the yPlus values
		# store the dataframes
		elif sys.argv[2] == "yPlus":

			"""
			# init an empty Dataframe to append to
			frames_to_store = pd.DataFrame()
			no_of_timesteps = 0
			# get the list of time folders
			postProcessing_directory = "./postProcessing/yPlus/"
			time_directories = os.listdir(postProcessing_directory)
			for time_directory in time_directories:
				path = postProcessing_directory+time_directory
				frames_to_store=frames_to_store.append(other=getyPlus(path)[0])
				no_of_timesteps += getyPlus(path)[1]
			print(no_of_timesteps)
			"""

			# split the frame by patches
			#no_of_patches = len(frames_to_store.patch.unique())
			data_by_patches = np.split(getyPlus()[0],[getyPlus()[1]],axis=0)

			# store all frames separately
			for frame in data_by_patches:
				name = frame.patch[0]
				frame.drop("patch",axis=1,inplace=True)
				frame.sort_index(ascending=True,inplace=True)
				frame.to_csv("./storage/"+directories[-1]+"/yPlus_"+name+".csv")

	# plot method should plot the stored data from the latest directory
	elif sys.argv[1] == "plot":
		if len(sys.argv) < 3:
			sys.exit("error: entity name needed")

		# handle options
		start = 1
		components = "xy"
		drag_bool = False
		for index,option in enumerate(sys.argv):
			if  "-s" in option:
				start = int(sys.argv[index+1])
			if "-c" in option:
				components = sys.argv[index+1]
			if "--drag" in option:
				drag_bool = True

		# where to read from
		directory = sys.argv[3]

		# handle entities to plot
		if sys.argv[2] == "forces":
			df = pd.read_csv(directory+"forces.csv")

			# calculate coefficant of drag
			if drag_bool: df.fpy=df.fpy

			# initalize for plots
			fig1, axs = plt.subplots(2,1)
			fig1.suptitle("Kraefte stationaer")

			# truncate to zoom in at the end
			if start is not 1:
				df = df.truncate(before=start)
			# plot the pressure and viscous force components
			for component in components:
				plotFrameToAxis(0,"p"+component)
				plotFrameToAxis(1,"v"+component)

			# graphics
			axs[0].set_ylabel('Pressure Forces')
			axs[0].legend(loc='best')
			axs[1].set_ylabel('Viscous Forces')
			axs[1].legend(loc='best')
			axs[-1].set_xlabel('Iterations')

			# command line output
			print(df.head())
			print(df.tail())

			# export figure
			plt.savefig(directory+"forces_"+component+"t_"+str(start)+".png")
			plt.show()

		elif sys.argv[2] == "yPlus":

			# handle options
			start = 1
			patchnames = ""
			for index,option in enumerate(sys.argv):
				if  "-s" in option:
					start = int(sys.argv[index+1])
				if "-p" in option:
					patchnames = sys.argv[index+1].split()

			fig = plt.figure()
			ax1 = fig.gca()
			fig.suptitle("yPlus values")

			frames = glob(directory+"yPlus_*.csv")
			for patch in frames:
				for patchname in patchnames:
					if patch.find(patchname) is not -1:
						df = pd.read_csv(patch)
						df.index = df.index.values *100
						if start is not 1:
							df = df.truncate(before=start)

						ax1.plot(df.index,df.iloc[:,1].values,label="{} min".format(patchname))
						ax1.plot(df.index,df.iloc[:,2].values,label="{} max".format(patchname))

			ax1.legend(loc="best")
			plt.savefig(directory+"yPlus_{}_t{}.png".format(patchnames[:],start))
			plt.show()

	# compare method
	elif sys.argv[1] == "compare":
		compare()

	else:
		print("unknown command")

