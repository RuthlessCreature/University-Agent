* Public CC0 palmerpenguins. Syntax example only; SPSS not installed or executed here.
* First import penguins.csv with species as string and body_mass_g as numeric.
* Treat the literal NA as system missing during the CSV import wizard.
SORT CASES BY species.
SPLIT FILE LAYERED BY species.
DESCRIPTIVES VARIABLES=body_mass_g /STATISTICS=MEAN STDDEV MIN MAX.
SPLIT FILE OFF.
