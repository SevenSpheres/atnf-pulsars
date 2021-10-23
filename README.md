# ATNF pulsar catalog for Celestia
This is a Python script to generate a catalog of pulsars for [Celestia](https://github.com/CelestiaProject/Celestia),
using the [ATNF pulsar database](https://www.atnf.csiro.au/research/pulsar/psrcat/). It's based on earlier work by
[Cham](https://celestia.space/forum/viewtopic.php?f=6&t=11372) and [Selden](https://www.classe.cornell.edu/~seb/celestia/catalogs.html#3.5.14).

The data file necessary to generate the catalog is included in this repository as *atnf_pulsars.csv*, but if you want to
download it yourself (for example, if the database is updated), here are instructions to do so:
- Go to the ATNF pulsar database and select "Name", "JName", "RaJD", "DecJD", "P0", "Dist".
- Set the "Output style" to "Long csv with errors", then click on "TABLE".
- Copy the output, remove the second line (`;;;;;(deg);;(deg);;(s);;;(kpc);`), and save as *atnf_pulsars.csv*.
  - This can be done in a text editor by replacing semicolons with commas, or in Excel through "Data" -> "Text to Columns",
    and then saving the file with the appropriate extension.