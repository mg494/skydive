# Aerodynamics of a ballute
This repository is part of the analysis of the aero(thermo)dynamics of a reentering space vehicle. During supersonic reentry the capsule will deploy a ballute (towed behind the capsule) to slow down and orient itself heatshield first. After reentering the athmosphere the ballute will be cut off and the main parachutes will be launched to slow the capsule down for water landing. 
A ballute is an inflateable device to slow down a falling object or vehicle by generating drag. 
Ultimatly the cfd analysis should show how the shock waves during supersonic reentry are forming around the capsule towing the ballute, but due to the instability of the cfd method I start with a incompressible analysis of the terminal velocity during a skydive (hence the name of this repo).

## CFD Model
The model will be a 2D Model due to my available compute power. 

## current to dos
* evaluate the influence of the inflation layer
* get to around 980N of drag force at terminal velocity of 107 kph
