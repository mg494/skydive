from paraview.simple import *
import re

casename = "skydive"
casepath = "/home/marc/OpenFOAM/marc-7/run/"
filename = casepath+casename+"/"+casename+".OpenFOAM"

reader = OpenFOAMReader(FileName=filename)
Show()
Render()

readerRep = GetRepresentation()

view = GetActiveView()
print(view)
layout = GetLayout()
location = layout.GetViewLocation(view)
layout.MaximizeCell(location)

ColorBy(readerRep, ("POINTS", "U"))
UpdateScalarBars()
Render()

file = open("./resultlog","r")
lines = file.readlines()
directories = []
for line in lines:
	match = re.search(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}",line)
	if match is not None: directories.append(match.group())
if len(directories)<1: sys.exit("error: no entries in resultlog")

WriteImage("./storage/"+directories[-1]+"/test_image.png")

#SaveScreenshot(casepath+"storage/test_image.jpeg")
