#!/usr/bin/python
# Run this command as follows:
# ./*.py PREFIX
#run as  python gap.py bdt

import xml.etree.ElementTree as ET
import glob
import sys
import  math
import os


prefix = sys.argv[1]
savedir = prefix + ".save"

CBM = 100000
VBM = -100000




def main():

    datafile = savedir + "/data-file-schema.xml"

    try:
        f = open(datafile)
        f.close()
    except:
        print('File not found.')
        return

    tree = ET.parse(datafile)
    eigroot = tree.getroot()


    eig = eigroot.findall("output/band_structure/ks_energies/eigenvalues")
    occup = eigroot.findall("output/band_structure/ks_energies/occupations")
    Fermi = eigroot.findall("output/band_structure/fermi_energy")[0].text
    nks = eigroot.findall("output/band_structure/nks")[0].text
    nelec = eigroot.findall("output/band_structure/nelec")[0].text

    nelec = round(float(nelec), 5)

    print('The  number of electrons = ', nelec)
    if float(nelec) % 2 == 0 :
        vbi = float(nelec)/2
        print('Number of electrons is even')
    else:
        vbi = math.ceil(float(nelec)/2)
        print('Number of electrons is odd')

    print('The valence band index is ', vbi)

    vb_energies = []
    cb_energies = []
    vb1_energies = []
    cb1_energies = []
    vb2_energies = []
    cb2_energies = []

    for i in range(int(nks)):
        eig_vec = [s for s in eig[i].text.split()]
        occup_vec = [s for s in occup[i].text.split()]
        vb2_energies.append(float(eig_vec[int(vbi)-3]))
        vb1_energies.append(float(eig_vec[int(vbi)-2]))
        vb_energies.append(float(eig_vec[int(vbi)-1]))
        cb_energies.append(float(eig_vec[int(vbi)]))
        cb1_energies.append(float(eig_vec[int(vbi)+1]))
        cb2_energies.append(float(eig_vec[int(vbi)+2]))
        VBM = (max(vb_energies))
        CBM = (min(cb_energies))
        VBM1 =(max(vb1_energies))
        CBM1 = (min(cb1_energies))
        VBM2 = (max(vb2_energies))
        CBM2 = (min(cb2_energies))


    print("VBM-2\t",VBM2*27.211396132)
    print("VBM-1\t",VBM1*27.211396132)
    print("VBM\t",VBM*27.211396132)
    print("CBM\t",CBM*27.211396132)
    print("CBM+1\t",CBM1*27.211396132)
    print("CBM+2\t",CBM2*27.211396132)
    print("Bandgap\t",(CBM - VBM)*27.211396132)
    print("Fermi Energy:\t",(float(Fermi))*27.211396132)
    #print("Fermi Energy:\t",(float(vbi)))

if __name__ == '__main__':
    main()
