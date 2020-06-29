import matplotlib.pyplot as plt
import re
import numpy as np
import pandas as pd


###--------------------store function--------------------------###

def storeForces(case,dim=2):
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

	pipefile = open('./postProcessing/forcesIncompressible/0/forces.dat','r')
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

	force_df.to_csv("./storage/"+case+".csv")


##-----------------plot-function----------------------###
def plotForces(case,start=1):
	df = pd.read_csv("./storage/"+case+".csv")
	print(df.size)
	fig1, axs = plt.subplots(2,1)
	fig1.suptitle("Kräfte stationär")
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
#	print(dfs)
#	print(type(dfs))


case = "ballute6_linearU"
#cases = ["linUpw", "upw"]

storeForces(case)
plotForces(case,start=1500)
#compare(cases, niter = 300)
