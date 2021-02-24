
<!--
!      ___   _   ___ ___ ___ ___ 
!     |   \ /_\ | _ \ _ \ __| _ \
!     | |) / _ \|  _/  _/ _||   /
!     |___/_/ \_\_| |_| |___|_|_\
! 
! 
-->

DAPPER is a set of templates for benchmarking the performance of
[data assimilation (DA)](https://sites.google.com/site/patricknraanespro/DA_tut.pdf)
methods.
The tests provide experimental support and guidance for new developments in DA.
Example diagnostics:

<!--
![EnKF - Lorenz'63](./data/figs/anims/Lor63_ens_anim_2.gif)
-->

![EnKF - Lorenz'63](./data/figs/anims/DAPPER_illust_v2.jpg)


The typical set-up is a **twin experiment**, where you
* specify a
  * dynamic model* 
  * observational model*
* use these to generate a synthetic
  * "truth"
  * and observations thereof*
* assess how different DA methods perform in estimating the truth,
    given the above starred (*) items.

**Pros:** DAPPER enables the numerical investigation of DA methods
through a variety of typical test cases and statistics.
It reproduces numerical benchmarks results reported in the literature,
and facilitates comparative studies,
thus promoting the reliability and relevance of the results.
DAPPER is open source, written in Python, and focuses on readability;
this promotes the reproduction and dissemination of the underlying science,
and makes it easy to adapt and extend.
In summary, it is well suited for teaching and fundamental DA research.

**Cons:** In a trade-off with the above advantages, DAPPER makes some sacrifices of efficiency and flexibility (generality).
I.e. it is not designed for the assimilation of real data in operational models (e.g. WRF).

**Getting started:** Read, run, and understand the scripts `example_{1,2,3}.py`.
There is no unified documentation,
but the code is reasonably well commented, including docstrings.
Alternatively, see the `tutorials` folder for an intro to DA.

  
Installation
------------------------------------------------
Prerequisite: `python3.5+` with
`scipy`, `matplotlib`, `pandas`.
This is all comes with [anaconda](https://www.anaconda.com/download)
by default.

Download, extract the DAPPER folder, and `cd` into it. To test it, run:

    python -i example_1.py

For the tutorials, you will also need
`jupyter` and the `markdown` package.

It is also recommended to install `tqdm` (e.g. `pip install tqdm`)
and `colorama`.



Methods
------------
References provided at bottom

Method name                                            | Literature RMSE results reproduced
------------------------------------------------------ | ---------------------------------------
EnKF <sup>1</sup>                                      | Sakov and Oke (2008)
EnKF-N                                                 | Bocquet (2012), (2015)
EnKS, EnRTS                                            | Raanes (2016a)
iEnKS (and -N)                                         | Sakov (2012), Bocquet (2012), (2014)
LETKF, local & serial EAKF                             | Bocquet (2011)
Sqrt. model noise methods                              | Raanes (2015)
Particle filter (bootstrap) <sup>2</sup>               | Bocquet (2010)
Optimal/implicit Particle filter  <sup>2</sup>         | "
NETF                                                   | Tödter (2015), Wiljes (2017)
Rank histogram filter (RHF)                            | Anderson (2010)
Extended KF                                            | Raanes (2016b)
Optimal interpolation                                  | "
Climatology                                            | "
3D-Var                                                 | 

<sup>1</sup>: Stochastic, DEnKF (i.e. half-update), ETKF (i.e. sym. sqrt.).  
Tuned with inflation and "random, orthogonal rotations".  
<sup>2</sup>: Resampling: multinomial (including systematic/universal and residual).  
The particle filter is tuned with "effective-N monitoring", "regularization/jittering" strength, and more.




Models
------------

Model       | Linear? | Phys.dim. | State len | # Lyap≥0 | Thanks to
----------- | ------- | --------- | --------- | -------- | ----------
Lin. Advect.| Yes     | 1d        | 1000 *    | 51       | Evensen/Raanes
Lorenz63    | No      | 0d        | 3         | 2        | Lorenz/Sakov
Lorenz84    | No      | 0d        | 3         | 2        | Lorenz/Raanes
Lorenz95    | No      | 1d        | 40 *      | 13       | Lorenz/Raanes
LorenzUV    | No      | 2x 1d     | 256 + 8 * | ≈60      | Lorenz/Raanes
Quasi-Geost | No      | 2d        | 129²≈17k  | ≈140     | Sakov

*: flexible; set as necessary


Additional features
------------------------------------------------
* Progressbar
* Tools to manage and display experimental settings and stats
* Visualizations, including
    * liveplotting (during assimilation)
    * intelligent defaults (axis limits, ...)
* Diagnostics and statistics with
    * Confidence interval on times series (e.g. rmse) averages with
        * automatic correction for autocorrelation 
        * significant digits printing
* Parallelisation:
    * (Independent) experiments can run in parallel; see `example_3.py`
    * Forecast parallelisation is possible since
        the (user-implemented) model has access to the full ensemble;
        see example in `mods/QG/core.py`.
    * Analysis parallelisation over local domains;
        see example in `da_methods.py:LETKF()`
    * Also, numpy does a lot of parallelization when it can.
        However, as it often has significant overhead,
        this has been turned off (see `tools/utils.py`)
        in favour of the above forms of parallelization.
* Gentle failure system to allow execution to continue if experiment fails.
* Classes that simplify treating:
    * Time sequences Chronology/Ticker with consistency checks
    * random variables (`RandVar`): Gaussian, Student-t, Laplace, Uniform, ...,
    as well as support for custom sampling functions.
    * covariance matrices (`CovMat`): provides input flexibility/overloading, lazy eval) that facilitates the use of non-diagnoal covariance matrices (whether sparse or full).


<!--
Also has:
* X-platform random number generator (for debugging accross platforms)
-->


What it can't do
------------------------------------------------
* Highly efficient DA on very big models (see discussion in introduction).
* Time-dependent error covariances and changes in lengths of state/obs
     (but models f and h may otherwise be time-dependent).
* Non-uniform time sequences not fully supported.


How to
------------------------------------------------
DAPPER is like a *set of templates* (not a framework);
do not hesitate make your own scripts and functions
(instead of squeezing everything into standardized configuration files).

#### Add a new method
Just add it to `da_methods.py`, using the others in there as templates.


#### Add a new model
* Make a new dir: `DAPPER/mods/`**your_mod**
* Add the empty file `__init__.py`
* See other examples, e.g. `DAPPER/mods/Lorenz63/sak12.py`
* Make sure that the model (and obs operator) supports
  2D-array (i.e. ensemble) and 1D-array (single realization) input.
  See `Lorenz63` and `Lorenz95` for typical implementation.



<!--
* To begin with, test whether the model works
    * on 1 realization
    * on several realizations (simultaneously)
* Thereafter, try assimilating using
    * a big ensemble
    * a safe (e.g. 1.2) inflation value
    * small initial perturbations
      (big/sharp noises might cause model blow up)
    * small(er) integrational time step
      (assimilation might create instabilities)
    * very large observation noise (free run)
    * or very small observation noise (perfectly observed system)
-->



Alternative projects
------------------------------------------------
Sorted by approximate project size.
DAPPER may be situated somewhere in the middle.

<!--
* DART         (NCAR)
* SANGOMA      (Liege/CNRS/Nersc/Reading/Delft)
* Verdandi     (INRIA)
* PDAF         (Nerger)
* ERT*         (Statoil)
* OpenDA       (TU Delft)
* MIKE         (DHI)
* PyOSSE       (Edinburgh)
* FilterPy     (R. Labbe)
* DASoftware   (Yue Li, Stanford)
* PyIT         (CIPR)
* OAK          (Liège)
* Siroco       (OMP)
* Datum*       (Raanes)
* EnKF-Matlab* (Sakov)
* IEnKS code*  (Bocquet)
* pyda         (Hickman)

*: Has been inspirational in the development of DAPPER. 
-->


Name               | Developers           | Purpose (vs. DAPPER)
------------------ | -------------------- | -----------------------------
[DART][1]          | NCAR                 | Operational and real-world DA
[ERT][2]*          | Statoil              | Operational (petroleum) history matching
[OpenDA][3]        | TU Delft             | Operational and real-world DA
[EMPIRE][4]        | Reading (Met)        | Operational and real-world DA
[SANGOMA][5]       | Conglomerate**       | Unified code repository researchers
[Verdandi][6]      | INRIA                | Real-world biophysical DA
[PDAF][7]          | Nerger               | Real-world and example DA
[PyOSSE][8]        | Edinburgh, Reading   | Real-world earth-observation DA
[MIKE][9]          | DHI                  | Real-world oceanographic DA. Commercial?
[OAK][10]          | Liège                | Real-world oceaonagraphic DA
[Siroco][11]       | OMP                  | Real-world oceaonagraphic DA
[FilterPy][12]     | R. Labbe             | Engineering, general intro to Kalman filter
[DASoftware][13]   | Yue Li, Stanford     | Matlab, large-scale
[Pomp][18]         | U of Michigan        | R, general state-estimation
[PyIT][14]         | CIPR                 | Real-world petroleum DA (?)
Datum*             | Raanes               | Matlab, personal publications
[EnKF-Matlab*][15] | Sakov                | Matlab, personal publications and intro
[EnKF-C][17]       | Sakov                | C, light-weight EnKF, off-line
IEnKS code*        | Bocquet              | Python, personal publications
[pyda][16]         | Hickman              | Python, personal publications


<!--
Real-world: supports very general models (e.g. time dependent state length, mapping to-from grids, etc.)
Operational: optimized for speed.
-->

*: Has been inspirational in the development of DAPPER. 

**: Liege/CNRS/NERSC/Reading/Delft

[1]: http://www.image.ucar.edu/DAReS/DART/
[2]: http://ert.nr.no/ert/index.php/Main_Page
[3]: http://www.openda.org/
[4]: http://www.met.reading.ac.uk/~darc/empire/index.php
[5]: http://www.data-assimilation.net/
[6]: http://verdandi.sourceforge.net/
[7]: http://pdaf.awi.de/trac/wiki
[8]: http://www.geos.ed.ac.uk/~lfeng/
[9]: http://www.dhigroup.com/
[10]: http://modb.oce.ulg.ac.be/mediawiki/index.php/Ocean_Assimilation_Kit
[11]: https://www5.obs-mip.fr/sirocco/assimilation-tools/sequoia-data-assimilation-platform/
[12]: https://github.com/rlabbe/filterpy
[13]: https://github.com/judithyueli/DASoftware
[14]: http://uni.no/en/uni-cipr/
[15]: http://enkf.nersc.no/
[16]: http://hickmank.github.io/pyda/
[17]: https://github.com/sakov/enkf-c
[18]: https://github.com/kingaa/pomp



<!--
Implementation choices
* Uses python3.5+
* NEW: Use `N-by-m` ndarrays. Pros:
    * python default
        * speed of (row-by-row) access, especially for models
        * same as default ordering of random numbers
    * facilitates typical broadcasting
    * less transposing for for ens-space formulae
    * beneficial operator precedence without `()`. E.g. `dy @ Rinv @ Y.T @ Pw` (where `dy` is a vector)
    * fewer indices: `[n,:]` yields same as `[n]`
    * no checking if numpy return `ndarrays` even when input is `matrix`
    * Regression literature uses `N-by-m` ("data matrix")
* OLD: Use `m-by-N` matrix class. Pros:
    * EnKF literature uses `m-by-N`
    * Matrix multiplication through `*` -- since python3.5 can just use `@`

Conventions:
* DA_Config, assimilate, stats
* fau_series
* E,w,A
* m-by-N
* m (not ndims coz thats like 2 for matrices), p, chrono
* n
* ii, jj
* xx,yy
* no obs at 0
-->


<!--
TODO
------------------------------------------------
* Darcy, LotkaVolterra, 2pendulum, Kuramoto-Sivashinsky , Nikolaevskiy Equation
* Lage demo fil/liveplotting for LorenzUV
* Reorg file structure: Turn into package?
* Simplify time management?
* Use pandas for stats time series?
* Defaults file (fail_gently, liveplotting, mkl.set_num_threads, etc)
* Replace set_ilabel by [eval("ax.set_%slabel('%s')"%(s,s)) for s in "xyz"]
* Welcome message (setting mkl.set_num_threads, setting style, importing from common "setpaths") etc
* Make citation format for DAPPER
* Upgrade example_4 with plot_1d_minz ?
* Implement spatialized inflation?
* Replace print_c and termcolors dict by 'with coloring:'
* Fix Windows bug (key listening: ncurses?)
* Fix issue with anaconda python framework install or whatever that fucks figure interaction
* Use inspect somehow instead of C.update_setting
* Use AlignedDict for DA_Config's repr?
* Get good/simple local PF with reproduction of Alban's results
* rename do_tab to tab
* Make function DA_Config() a member called 'method' of DAC. Rename DAC to DA_Config.
    => Yields (???) decorator syntax @DA_Config.method  (which would look nice) 
* Rename setup to HMM
* Change m to M and ndim? (what about model?)
* EITHER: Rm *args, **kwargs from da_methods? (less spelling errors)
*         Replace with opts argument (could be anything).
*     OR: implement warning if config argument was not used (warns against misspelling, etc)
* Fix dtObs bug
* Post version on nersc and link from enkf.nersc
* Post version on norce
-->


References
------------------------------------------------
- Sakov (2008)   : Sakov and Oke. "A deterministic formulation of the ensemble Kalman filter: an alternative to ensemble square root filters".  
- Anderson (2010): "A Non-Gaussian Ensemble Filter Update for Data Assimilation"
- Bocquet (2010) : Bocquet, Pires, and Wu. "Beyond Gaussian statistical modeling in geophysical data assimilation".  
- Bocquet (2011) : Bocquet. "Ensemble Kalman filtering without the intrinsic need for inflation,".  
- Sakov (2012)   : Sakov, Oliver, and Bertino. "An iterative EnKF for strongly nonlinear systems".  
- Bocquet (2012) : Bocquet and Sakov. "Combining inflation-free and iterative ensemble Kalman filters for strongly nonlinear systems".  
- Bocquet (2014) : Bocquet and Sakov. "An iterative ensemble Kalman smoother".  
- Bocquet (2015) : Bocquet, Raanes, and Hannart. "Expanding the validity of the ensemble Kalman filter without the intrinsic need for inflation".  
- Tödter (2015)  : Tödter and Ahrens. "A second-order exact ensemble square root filter for nonlinear data assimilation".  
- Raanes (2015)  : Raanes, Carrassi, and Bertino. "Extending the square root method to account for model noise in the ensemble Kalman filter".  
- Raanes (2016a) : Raanes. "On the ensemble Rauch-Tung-Striebel smoother and its equivalence to the ensemble Kalman smoother".  
- Raanes (2016b) : Raanes. "Improvements to Ensemble Methods for Data Assimilation in the Geosciences".  
- Wiljes (2017)  : Aceved, Wilje and Reich. "Second-order accurate ensemble transform particle filters".  

Further references are provided in the algorithm codes.

Contact
------------------------------------------------
patrick. n. raanes AT gmail

Licence
------------------------------------------------
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./licence.txt)

Contributors
------------------------------------------------
Patrick N. Raanes,
Colin Grudzien,
Maxime Tondeur,
Remy Dubois

Powered by
------------------------------------------------
<div>
<img src="./data/figs/logos/python.png"  alt="Python"  height="100">
<img src="./data/figs/logos/numpy.png"   alt="Numpy"   height="100">
<img src="./data/figs/logos/pandas.png"  alt="Pandas"  height="100">
<img src="./data/figs/logos/jupyter.png" alt="Jupyter" height="100">
</div>


<!--
"Outreach"
---------------
* http://stackoverflow.com/a/38191145/38281
* http://stackoverflow.com/a/37861878/38281
* http://stackoverflow.com/questions/43453707
-->




