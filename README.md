![image](https://github.com/patternizer/tropomi-so2/blob/master/tropomi-so2-rio.png)

# tropomi-so2

Python code to read GeoTIFF SO2 from TROPOMI onboard the Sentinel-5P satellite for purposes of volcanic eruption monitoring 

## Contents

* `plot-tropomi.py` - python code to read TROPIMI GeoTIFFs and plot the extracted data with Cartopy
* `tropomi-so2-rasterio.png` - data graphic over Fagradalsfjall in Iceland
* `tropomi-so2-rio.png` - data graphic of L2 swathe over Iceland

The first step is to clone the latest tropomi-so2 code and step into the check out directory: 

    $ git clone https://github.com/patternizer/tropomi-so2.git
    $ cd tropomi-so2

### Using Standard Python

The code should run with the [standard CPython](https://www.python.org/downloads/) installation and was tested in a conda virtual environment running a 64-bit version of Python 3.8+.

tropomi-so2 scripts can be run from sources directly, once the required data dependencies are satisfied.

Run with:

    $ python tropomi-so2.py

## License

The code is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Michael Taylor](michael.a.taylor@uea.ac.uk)

