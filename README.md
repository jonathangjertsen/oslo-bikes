# Oslo Bysykkel

Verktøy for å hente ut og behandle [åpne data fra Oslo Bysykkel](https://oslobysykkel.no/apne-data).

Følgende verktøy finnes:

* `stream_availability_data_to_csv.py`: et script som lagrer sanntidsdata til disk i CSV-format.
    * Sanntidsdata hentes hvert 9. sekund.
    * Filnavn og client-identifier blir etterspurt ved oppstart.
    * Det kreves at `requests` er installert (kjør `pip install -r requirements.txt`)
* `save_station_data_to_csv.py`: et script som lagrer stasjons-informasjon til disk i CSV-format.
    * Data hentes kun ut én gang.
    * Det tas ikke høyde for at stasjoner kan endres.
    * Filnavn og client-identifier blir etterspurt ved oppstart.
    * Det kreves at `requests` er installert (kjør `pip install -r requirements.txt`)
* `bike_analysis.py`: funksjoner for å konvertere fra CSV-filer generert med ovennevnte scripts til
pandas DataFrames og for å behandle disse.
    * Det kreves at `pandas`, `geopandas` og `numpy` er installert, typisk via en Anaconda-distribusjon
* `bikes.ipynb` er en Jupyter Notebook jeg bruker til å kikke på dataene.
    * Det kreves at `matplotlib` er installert i tillegg til alt fra bike_analysis
    * Det kreves også at shapefiles for Oslo har blitt lastet ned fra
[BBBike](https://download.bbbike.org/osm/bbbike/Oslo/) til en mappe som heter "oslo-shapefile"

Demo av plotting fra `bikes.ipynb`:

![Animasjon av bysyklenes tilgjengelighet](https://raw.githubusercontent.com/jonathangjertsen/oslo-bikes/master/demo.gif)
