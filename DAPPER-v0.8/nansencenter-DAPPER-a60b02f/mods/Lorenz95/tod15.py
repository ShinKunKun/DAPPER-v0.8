# Concerns figure 4 of Todter and Ahrens (2015):
# "A Second-Order Exact Ensemble Square Root Filter for Nonlinear Data Assimilation"

from common import *

from mods.Lorenz95 import core
from tools.localization import partial_direct_obs_nd_loc_setup as loc_setup

t = Chronology(0.05,dkObs=2,T=4**5,BurnIn=20)

m = 80
f = {
    'm'    : m,
    'model': core.step,
    'noise': 0
    }

X0 = GaussRV(m=m, C=0.001)

jj = arange(0,m,2)
h = partial_direct_obs_setup(m,jj)
h['localizer'] = loc_setup( (m,), (1,), jj, periodic=True )
# h['noise'] = LaplaceRV(C=1,m=len(jj))
h['noise'] = LaplaceParallelRV(C=1,m=len(jj))

other = {'name': os.path.relpath(__file__,'mods/')}
setup = TwinSetup(f,h,t,X0,**other)

####################
# Suggested tuning
####################

#                                                           rmse_a
# cfgs += LETKF(N=20,rot=True,infl=1.04       ,loc_rad=5) # 0.44
# cfgs += LETKF(N=40,rot=True,infl=1.04       ,loc_rad=5) # 0.44
# cfgs += LETKF(N=80,rot=True,infl=1.04       ,loc_rad=5) # 0.43
# These scores are quite variable:
# cfgs += LNETF(N=40,rot=True,infl=1.10,Rs=2.5,loc_rad=5) # 0.57
# cfgs += LNETF(N=80,rot=True,infl=1.10,Rs=1.6,loc_rad=5) # 0.45

# In addition to standard post-analysis inflation,
# we also find the necessity of tuning the inflation (Rs) for R,
# which is not mentioned in the reference.

# In summary, compared to the reference paper:
# - Our rmse scores for the local ETKF are better
# - Our rmse scores for the local NETF
#   - with N=80 seems to be equal
#   - with N=40 is worse
# 
# These results (contradict and) pretty much void the merit of the NETF,
# especially considering how the Laplace obs-error favours the NETF.
# A possible explanation is that they use T=100 (unit-less),
# which is way too short, and so they might have gotten "lucky".
# Another explanation is that our implementation is buggy,
# but this seems unlikely, especially since we reproduce the NETF
# results from Wiljes'2017.
