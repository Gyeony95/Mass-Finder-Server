from django.test import TestCase
from mass_finder_app.logic.amino_calc import calc_by_ion_type

# Create your tests here.

currentFormyType = "no"
currentIonType = "H"
initAmino = ""
inputAminos = {
    'G': 75.03,
    'A': 89.05,
    'S': 105.04,
    'T': 119.06,
    'C': 121.02,
    'V': 117.08,
    'L': 131.09,
    'I': 131.09,
    'M': 149.05,
    'P': 115.06,
    'F': 165.08,
    'Y': 181.07,
    'W': 204.09,
    'D': 133.04,
    'E': 147.05,
    'N': 132.05,
    'Q': 146.07,
    'H': 155.07,
    'K': 146.11,
    'R': 174.11,
}
totalWeight = 1000

calc_by_ion_type(totalWeight, initAmino, currentFormyType, currentIonType, inputAminos)

