from paraview.simple import *
import re

casename = "skydive"
casepath = "/home/marc/OpenFOAM/marc-7/run/"
filename = casepath+casename+"/"+casename+".OpenFOAM"

reader = OpenFOAMReader(FileName=filename)
reader.SkipZeroTime = 0
reader.Refresh()

print(reader.SkipZeroTime)
timesteps = [0]+reader.TimestepValues[:]
print(timesteps)
Show()
Render()


# where to write figures
file = open("./resultlog","r")
lines = file.readlines()
directories = []
for line in lines:
	match = re.search(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}",line)
	if match is not None: directories.append(match.group())
if len(directories)<1: sys.exit("error: no entries in resultlog")


# write initial field
view = GetActiveView()
layout = GetLayout()
location = layout.GetViewLocation(view)
layout.MaximizeCell(location)

readerRep = GetRepresentation()
ColorBy(readerRep, ("POINTS", "U"))
UpdateScalarBars()
Render()

for camera_position in range(2):
	if camera_position is 1:
		# control the camera
		view.CameraPosition = [0,3,14]
		view.CameraFocalPoint = [0,3,0]


	for time in timesteps:

		view = GetActiveView()
		layout = GetLayout()
		location = layout.GetViewLocation(view)
		layout.MaximizeCell(location)

		readerRep = GetRepresentation()
		ColorBy(readerRep, ("POINTS", "U"))
		UpdateScalarBars()

		view.ViewTime = time
		print(view.ViewTime)

		Render()

		WriteImage("./storage/"+directories[-1]+"/velocity_{}_t{}.png".format(camera_position,int(time)))

#SaveScreenshot(casepath+"storage/test_image.jpeg")
