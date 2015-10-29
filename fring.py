### FRING ###

'''
a two element interferometer
observes a point source

assume a perfect point source occupying 1 pixel 
and broadcasting at one frequency

signal from point source ~ E cos wt

assume both antennas pointing at the source (it's at the phase centre)

assume the incoming radiation is at 45 degrees to the perpendicular

'''
import numpy as np
import scipy.constants as spc
from pylab import *


def antenna_voltage(E, w, t, tau):

	# this function returns the antenna voltage as a function of time
	
	# the antenna voltage is the voltage induced in the dipole due to incident
	# em radiation. It is focused on the dipole by a feed-horn. The dipole consists
	# of two things which look like wires. One is sensitive to STOKES R, the other
	# to STOKES L (which is perpendicular to STOKES R).
	
	# For simplicity, we assume here that one of either L or R is zero
	# (it doesn't matter which).
	
	# We also assume the feed-horn is perfect and focuses everything onto the dipole
		
	return(E*np.cos(w*(t-tau)))
	
	
def correlate(voltage_1,voltage_2):

	# Here is what happens in the correlator:
	# This function calculates the correlation: <v1*v2>, with a shift applied to v2
	# The shift is varied up to a given value
	# The shift which results in the highest integrated correlation is probably the correct one
	
	shift = 250	# maximum shift to try
	integ = np.zeros((shift))
	for i in range(0, shift):
		product = (voltage_1)*(np.roll(voltage_2,-i))
		integ[i] = np.sum(product)
	integ = np.multiply(integ, delta_t)	# integ is now set to the integral of v1*v2_shifted w.r.t. time
	shifts = np.arange(0,shift)
		
	return(integ,shifts)
	
	
'''	
execution starts here

'''

# First set some constants

E = 2.0 #The strength of the electric field. Intensity = E squared
w = 0.5 #w is the angular frequency of the em wave (w = 2*pi*f)

# To derive tau, decide how far apart antennas are #

anten_dist = 6E8 							#distance between antennas in meters
path_difference = anten_dist*np.cos(45) 	#additional distance travelled by light arriving at second antenna
tau = path_difference/spc.c					#time delay between light arriving at first antenna and light arriving at second antenna
print('Tau_exact = '+str(tau))

tmax = 100.0*w
delta_t = w/10.0
t = np.arange(0,tmax,delta_t)

# Now calculate the voltages that are recorded at each antenna

voltage_1 = antenna_voltage(E, w, t, 0.0)
voltage_2 = antenna_voltage(E, w, t, tau)

# Plot them. Note antenna 2 lags antenna one


plot(t, voltage_1,t,voltage_2)
show()

'''
From the plots above, you can see that the voltage induced at antenna 1 is out of phase 
with the voltage induced at antenna 2. This is as a result of the distance between them. 
The VLBI correlator can correct for this!

correlation = multiplying two things together and then integrating over time. If the
voltages were in phase, correlating them would yield a number which is related to the 
intensity of the source (but not equal to it).

If the voltages were out of phase, this number would be too small, and not be reflective
of the total intensity of the source.

'''

# Now attempt to correct for the geometric delay by correlating the two voltages
# The correlate function returns the correlation and its associated shift for a range of shifts
# The best correlation should occur when the second voltage has been overlapped exactly with the first

output,shifts = correlate(voltage_1,voltage_2)	# get the list of correlations and shifts
best = np.argmax(output)	# find the best shift
timeshift = (shifts[best])*delta_t	# Convert the shift to seconds by multiplying with dt
print('Correlator derived timeshift = '+str(timeshift))
print('Error in corrrelator shift = '+str(timeshift-tau))
print('This error should be small relative to tau. Further corrections will be applied by fring.')
plot(shifts,output)
show()










