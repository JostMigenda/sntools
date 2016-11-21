#!/usr/bin/python

from optparse import OptionParser
import random
from math import pi, sin, cos, sqrt, gamma, exp
from scipy import integrate
import numpy as np

pid = {"pi0":111, "pi+":211, "k0l":130, "k0s":310, "k+":321,
       "e+":-11, "mu+":-13, "tau+":-15, 
       "nue":12, "nuebar":-12, 
       "numu":14, "numubar":-14, 
       "nutau":16, "nutaubar":-16,
       "p+":2212, "n0":2112}

#holds detector [radius, height] in cm
detectors = {"SuperK":[3368.15/2., 3620.],
             "Cylinder_60x74_20inchBandL_14perCent":[7400./2., 6000.],
	     "Cylinder_60x74_20inchBandL_40perCent":[7400./2., 6000.]} # TODO: change to ID size once that’s fully implemented in WCSim and BONSAI

for pname, no in list(pid.items()):
    if pname.endswith('+'):
        pid[pname.replace('+', '-')] = -1*pid[pname]





parser = OptionParser()
optdefault = 1
parser.add_option("-N", "--nfiles", dest="nfiles",
                  help="number of files of particles to produce. Default: %s" \
                      % (optdefault),
                  metavar="#", default=optdefault)
optdefault = 100
parser.add_option("-n", "--npart", dest="npart",
                  help="number of particles to simulate per file. Default: %s" \
                  % (optdefault),
                  metavar="#", default=optdefault)
optchoices = list(pid.keys())
optdefault = "e+"
parser.add_option("-t", "--type", dest="type",
                  help="Particle type to be generated. Choices: %s. Default: %s" \
                      % (optchoices, optdefault),
                  metavar="TYPE",
                  choices=optchoices, default=optdefault)
optdefault = 1000
parser.add_option("-e", "--energy", dest="energy",
                  help="Particle energy to be generated in MeV. Default: %s" \
                      % (optdefault),
                  metavar="ENERGY", default=optdefault)
optchoices = ["center", "random", "minusx", "plusx", "minusz", "plusz"]
optdefault = optchoices[1]
parser.add_option("-v", "--vertex", dest="vertname",
                  help="Type of vertex. Choices: %s. Default: %s" \
                      % (optchoices, optdefault),
                  choices=optchoices, default=optdefault)
optchoices = ["4pi", "towall", "tocap"]
optdefault = optchoices[0]
parser.add_option("-d", "--direction", dest="dirname",
                  help="Type of direction. Choices: %s. Default: %s" \
                      % (optchoices, optdefault),
                  choices=optchoices, default=optdefault)
optchoices = list(detectors.keys())
optdefault = "SuperK"
parser.add_option("-w", "--detector", dest="detector",
                  help="Detector water volume to use (for vertex positioning). Choices: %s. Default: %s" \
                      % (optchoices, optdefault),
                  choices=optchoices, default=optdefault)

(options, args) = parser.parse_args()

options.vertname = options.vertname.lower()
options.dirname = options.dirname.lower()


nfiles = int(options.nfiles)

def partPrint(p, f, recno):
    f.write("$ begin\n")
    f.write("$ nuance 0\n")
    rad    = detectors[options.detector][0] - 20.
    height = detectors[options.detector][1] - 20.
    while True:
        x = random.uniform(-rad, rad)
        y = random.uniform(-rad, rad)
        if x**2 + y**2 < rad**2: break
    z = random.uniform(-height/2, height/2)
    f.write("$ vertex %.5f %.5f %.5f %.5f\n" % (x, y, z, p["time"]))
    printTrack(nu, f, -1)   # "Neutrino" Track
    printTrack(prot, f, -1) # "Target" track
    f.write("$ info 0 0 %i\n" % recno)
    th = random.random()*2*pi
    u = 1.-2*random.random()
    x = sqrt(1.-u**2)*cos(th)
    y = sqrt(1.-u**2)*sin(th)
    z = u
    p["direction"] = (x, y, z)
    #th = random.random()*pi
    #phi = random.random()*2*pi
    #p["direction"] = (cos(phi)*cos(th), sin(phi)*cos(th), sin(th))
       
    printTrack(p, f)    # Outgoing Particle Track
    f.write("$ end\n")

def printTrack(p, f, code=0):
    f.write("$ track %(type)i %(energy).5f " % p)
    f.write("%.5f %.5f %.5f %i\n" % (p["direction"]+(code,)))

for fileno in range(nfiles):
            typestr = options.type.replace("+", "plus").replace("-", "minus")
            
            filename="%s_%s_%s_%s_%03i.kin" % (typestr, options.vertname, options.dirname, options.detector, fileno)
        
            outfile = open(filename, 'w')

totnevt = 0           
nP = 4.96e+34 #number of hydrogen nuclei in whole inner volume; needs to be updated for design changes
dSquared = (1.5637e+33)**2 # length/hbar*c - distance in MeV^-1 = 10 kpc/((6.582*10**-22 sMeV)*(9.717*10**-12 kpc s^-1))
mN = 939.57 #MeV
mP = 938.28 #MeV
mE = 0.511 #MeV
mPi = 139.6 #MeV
delta = mN-mP
mAvg=(mP+mN)/2
gF=1.16637e-11 #Fermi coupling constant in MeV^-2
eThr=((mN+mE)**2 - mP**2)/(2*mP)

#for 1ms time intervals:
with open('simData.txt') as simData:
    for line in simData:
    
        #import time, mean energy, mean squared energy and no of events in interval
        t, eNu, eNuSquared, L = line.split(",")
        t=float(t)
        eNu = float(eNu)
        eNuSquared = float(eNuSquared)
        L=float(L)
        eE = eNu - 1.3
        sMinusU = (2*mP*(eNu+eE))-mE**2
        t_eNu_eE = mN**2 - mP**2 - 2*mP*(eNu-eE)
        x = t_eNu_eE/(4*mAvg**2)
        y = 1-(t_eNu_eE/710000)
        z = 1-(t_eNu_eE/1000000)
        f1 = (1-(4.706*x))/((1-x)*y**2)
        f2 = 3.706/((1-x)*(y**2))
        g1 = -1.27/z**2
        g2 = (2 * g1 * mAvg**2)/(mPi**2 - t_eNu_eE)
        
        A = (mAvg**2 * (f1**2 - g1**2) * (t_eNu_eE-mE**2)) - (mAvg**2 * delta**2 * (f1**2+g1**2)) - (2 * mE**2 * mAvg * delta * g1 * (f1+f2))
        B = t_eNu_eE*g1*(f1+f2)
        C = (f1**2 + g1**2)/4
        
        absMsquared = A-(sMinusU*B)+((sMinusU**2)*C)
        dSigmadE = ((gF**2 * 0.9746**2)/(8 * pi * mP**2 * eNu**2))*absMsquared*2*mP
        alpha = (eNuSquared-(2*eNu**2))/(eNu**2-eNuSquared)
        dFluxdE = ((1/(4*pi*dSquared))*((L*624.15)/eNu))*(eNu**alpha/(gamma(alpha+1)))*(((alpha+1)/eNu)**(alpha+1))*(exp(((alpha+1)*eNu)/A))
        
        def f(eE, eNu):
            return dSigmadE*dFluxdE
        def bounds_eNu():
            return [eThr,50]
        def bounds_eE(eNu):
            return [0,(eNu-1.3)]
        simnevt= nP * integrate.nquad(f, [bounds_eE, bounds_eNu])[0]
        
        nevt_poisson= np.random.poisson(simnevt, 1000)
        nevt=np.random.choice(nevt_poisson) # select nevt from poisson distribution
        a = (eNuSquared-2*eNu**2)/(eNu**2-eNuSquared)
        nevt= np.random.poisson(1, simnevt) #number of events in 1ms interval
        totnevt += len(nevt)
    
        for i in range(len(nevt)):

            #Define the particle
            particle = {"vertex":(),
                        "time":t,
                        "type":pid[options.type],
                        "energy":np.random.gamma(a+1, eNu/(a+1)),
                        "direction":()}
    

            nu =   {"type":pid["numu"], "energy":1000.0, #removed energy+
                   "direction":(1, 0, 0)}
            prot = {"type":pid["p+"], "energy":935.9840,
                  "direction":(0, 0, 1)}
              
            partPrint(particle, outfile, i)

print(("Writing %i particles to " % totnevt) + filename)

outfile.write("$ stop")
outfile.close()

