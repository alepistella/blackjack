# Power scenario figure

Source: public study BJ-STU-001 revision C, section 5; Arduino ABX00181 reference-workload powers of 13.5, 14.7 and 33 W. Equation: board current = constant power / input voltage. Battery reference voltages: 12.6, 11.1 and 9.0 V.

`build_power_scenarios.py` produces the PNG and SVG figure plus the nine-row CSV table. Figure authoring used Python 3.12 and Matplotlib 3.11.2. Matplotlib is not needed to build or serve the blog. Install it only in a separate authoring environment, then run this script with that interpreter. Colours are read from the site's existing tactical-dark tokens.

The curves extrapolate constant-power reference loads; they are not recorded rover demand and do not establish that the board operates throughout the plotted voltage range. The motors are excluded. The 2 A comparison is the retail module's published output, pending identification of the installed module. Below the connector table's 12 V minimum, actual board behaviour requires verification. The source study provides the supporting references and bench-test plan.
