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
* `csv_to_pandas.py`: funksjoner for å konvertere fra CSV-filer generert med ovennevnte scripts til
pandas DataFrames
    * Det kreves at `pandas` er installert, typisk via en Anaconda-distribusjon
* `bikes.ipynb` er en Jupyter Notebook jeg bruker til å kikke på dataene.

Demo av plotting (kode kommer etter hvert):

![Animasjon av bysyklenes tilgjengelighet](https://raw.githubusercontent.com/jonathangjertsen/oslo-bikes/master/demo.gif)
