import csv
names = {
'J0146+6145'  : '4U 0142+61',
'B0531+21'    : 'Crab Pulsar:CM Tau:SN 1054',
'J0633+1746'  : 'Geminga:SN 437',
'B0656+14'    : 'Monogem Pulsar',
'B0833-45'    : 'Vela Pulsar:HU Vel',
'J1023+0038'  : 'AY Sex',
'B1257+12'    : 'Lich',
'J1412+7922'  : 'Calvera',
'B1509-58'    : 'Circinus Pulsar',
'J1740-5340B' : 'V1138 Ara',
'J1808-2024'  : 'SGR 1806-20',
'J1809-1943'  : 'V5634 Sgr', # http://vizier.u-strasbg.fr/viz-bin/VizieR-S?V*%20V5634%20Sgr
'J1856-3754'  : 'RX J1856.5-3754',
'B1913+16'    : 'Hulse-Taylor Pulsar',
'J1935+2154'  : 'SGR 1935+2154',
'B1957+20'    : 'Black Widow:QX Sge',
'J2051-0827'  : 'LY Aqr',
'B2224+65'    : 'Guitar Pulsar',
}
distances = {
'J1412+7922' : [2, 'Bogdanov et al., 2019ApJ...877...69B'],
'J1849-0001' : [7, 'Bogdanov et al., 2019ApJ...877...69B'],
'J1935+2154' : [6.6, 'Zhou et al., 2020ApJ...905...99Z'],
}
planethosts = ['B0943+10', 'B1257+12', 'B1620-26', 'J0312-0921', 'J1311-3430', 'J1701-3006H',
               'J1719-1438', 'J1807-2459A', 'J1928+1245', 'J2241-5236', 'J2322-2650']
coords = []
datafile = open('atnf_pulsars.csv', 'r')
stcfile = open('atnf_pulsars.stc', 'w')
sscfile = open('pulsar_jets.ssc', 'w')
script = open('mark_pulsars_period.cel', 'w')
stcfile.write("""# SPDX-FileCopyrightText: 2021-2025 SevenSpheres
# SPDX-License-Identifier: CC-BY-4.0
#
# Catalog of 3839 pulsars for Celestia from the ATNF database, v2.6.0.
# Source: https://www.atnf.csiro.au/research/pulsar/psrcat/
# Manchester, R. N., Hobbs, G. B., Teoh, A. & Hobbs, M., AJ, 129, 1993-2006 (2005)
#
# 11 pulsars with planets or substellar companions are included in extrasolar.stc,
# so they have been commented out in this file. Pulsars with the same coordinates as
# previously defined pulsars have also been commented out.\n\n""")
script.write("""{\n""")
rows = csv.DictReader(datafile)
for row in rows:
    if row['NAME'] == row['PSRJ']:
        namelist = 'PSR %s' % row['NAME']
    else:
        namelist = 'PSR %s:PSR %s' % (row['NAME'], row['PSRJ'])
    if row['NAME'] in names:
        namelist = '%s:%s' % (names[row['NAME']], namelist)
    ra = eval(row['RAJD'])
    dec = eval(row['DECJD'])
    if row['DIST'] == '*':
        if row['NAME'] in distances:
            dist = round(distances[row['NAME']][0]*3261.56, 2)
            dist = '%s # %s' % (dist, distances[row['NAME']][1])
        else:
            dist = '200000 # missing!'
    else:
        dist = round(eval(row['DIST'])*3261.56, 2)
    if row['P0'] == '*':
        period = ''
    else:
        period = eval(row['P0'])
    if row['NAME'] in planethosts or [ra, dec, dist] in coords:
        stcfile.write('# "%s"\n' % namelist)
        stcfile.write('# {\n')
        stcfile.write('#\tRA %s\n' % ra)
        stcfile.write('#\tDec %s\n' % dec)
        stcfile.write('#\tDistance %s\n' % dist)
        stcfile.write('#\tSpectralType "Q"\n')
        stcfile.write('#\tAbsMag 25\n')
        if period:
            stcfile.write('#\tRotationPeriod %s\n' % (period/3600))
        stcfile.write('# }\n\n')
    else:
        stcfile.write('"%s"\n' % namelist)
        stcfile.write('{\n')
        stcfile.write('\tRA %s\n' % ra)
        stcfile.write('\tDec %s\n' % dec)
        stcfile.write('\tDistance %s\n' % dist)
        stcfile.write('\tSpectralType "Q"\n')
        stcfile.write('\tAbsMag 25\n')
        if period:
            stcfile.write('\tRotationPeriod %s\n' % (period/3600))
        stcfile.write('}\n\n')
        coords.append([ra, dec, dist])
    sscfile.write('"" "PSR %s" {\n' % row['NAME'])
    sscfile.write('\tClass "diffuse"\n')
    sscfile.write('\tMesh "jets_sprites1.cmod"\n')
    sscfile.write('\tEmissive true\n')
    sscfile.write('\tRadius 1200\n')
    sscfile.write('\tFixedPosition [ 0 0 0 ]\n')
    sscfile.write('\tOrientation [ 45 1 0 0 ]\n')
    sscfile.write('\tUniformRotation {\n')
    if period:
        sscfile.write('\t\tPeriod %s\n' % (period/3600))
    else:
        sscfile.write('\t\tPeriod 0.0002777777777777778\n')
    sscfile.write('\t}\n')
    sscfile.write('}\n\n')
    if period == '':
        script.write('mark { object "PSR %s" size 5 color [ 1.0 0.0 0.0 ] symbol "plus" }\n' % row['NAME'])
    elif period >= 1:
        script.write('mark { object "PSR %s" size 5 color [ 0.997 0.333 0.333 ] symbol "plus" }\n' % row['NAME'])
    elif period >= 0.1:
        script.write('mark { object "PSR %s" size 5 color [ 0.65 0.65 0.35 ] symbol "plus" }\n' % row['NAME'])
    elif period >= 0.01:
        script.write('mark { object "PSR %s" size 5 color [ 0.00 0.75 0.65 ] symbol "plus" }\n' % row['NAME'])
    else: # < 0.01
        script.write('mark { object "PSR %s" size 5 color [ 0.333 0.333 0.917 ] symbol "plus" }\n' % row['NAME'])
datafile.close()
stcfile.close()
sscfile.close()
script.write('}\n')
script.close()