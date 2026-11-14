# Design rationale

Why Blackjack Rover is made the way it is. Each choice below is traced to the decision that fixed it and to the material that supports it. Identifiers of the form D-nnn refer to the decision register of the project; every decision was taken by Alessandro Pistella on the date shown.

Licence: CC BY 4.0. Credit: Blackjack Rover by Alessandro Pistella, github.com/alepistella/blackjack.

## One sheet, no welds

**The choice.** Each sheet-metal part is one planar sheet, laser cut flat and then bent. No welds, no joints between panels.

**Why.** A welded enclosure needs a fixture, a welder and finishing, and its accuracy depends on all three. A part that is only cut and bent can be made by any shop with a laser and a press brake, from one file, and comes out the same every time. That is what makes the kit reproducible by someone else, which is the purpose of the project.

**What it imposes on the design.** Three written rules that the model is checked against:

- every hole and cut-out is drawn in the plane of its own face, so that it can be cut before bending;
- every panel hangs from exactly one bend line, and the flat blank never overlaps itself;
- an edge that ends near a bend of another panel keeps a clearance of at least 1.5 mm, so that no bend is asked to be sharp.

**Record.** Rear fins as flat fins instead of closed volumes, "no welding of sheets": D-041, 12 November 2026. Bend clearances: D-056. The cover is a 2 mm sheet with 9 bends and a flat blank of 285.2 x 241.1 mm, developed from the CAD model.

## Nothing drilled in the chassis

**The choice.** The kit bolts to the holes that already exist in the deck of the Waveshare UGV02, through an adapter plate.

**Why.** Asking a builder to drill and tap a new chassis raises the bar for fitting the kit and removes the way back to stock. Hole positions are taken from the official Waveshare CAD model, so the plate is designed and checked on the model.

**Record.** The model carries two ways of fixing the board: holes drilled and tapped in the deck, and a bolt-on adapter plate on the existing holes, with one cover that fits both. The plate is what lets the kit be fitted without drilling: D-019, 12 November 2026.

## One switch for the whole robot

**The choice.** The Arduino VENTUNO Q is fed from the switched rail of the rover battery module, through a fused line and a 90 degree barrel plug. The rover switch turns everything on and off.

**Why.** The board accepts the 3S battery voltage directly on its barrel jack, so no converter is needed. Taking the supply after the rover switch gives a single switch without any added electronics. The trade-off is stated in the study: the board current passes through the battery module, whose shunt sets the continuous current.

**Record.** [Power supply study BJ-STU-001](../studies/BJ-STU-001_power_supply_study.md): sections 4.6 (power inputs of the board), 4.9 (the rover switch), 5 (current budget), 6 (what the findings allow), 7 (bench test plan), 9 (ratings of the chosen parts). Decision D-079, 14 November 2026.

## Cooling by design

**The choice.** A 40 mm fan exchanges the air of the bay; two grilles on the roof sit above the heatsink of the board and above the fan; the number 21 is cut through both side walls.

**Why.** The board has its own heatsink and fan: what an enclosure must not do is trap the warm air around them. The bay fan is therefore there for air exchange, not to blow on the board. The side grilles of the first concepts were replaced by the cut-through 21, which keeps an air path in the side walls and gives the rover its face.

**Record.** Purpose of the bay fan: D-011. Exhaust on one side and intake on the other: D-022. Number 21 in place of the side grilles, two roof grilles: D-063. All 12 November 2026.

## Room to grow

**The choice.** The roof carries the mounting patterns of both a lidar and a pan-tilt turret on one shared centre; the cover and a rear plate carry the antennas. In the base configuration these stay unfitted.

**Why.** With a depth camera as the primary sensor a lidar is not required, so the base configuration is kept small. Sharing one mounting centre means that whichever of the two is fitted covers most of the holes of the other. Parts outside the base configuration are still modelled with their real geometry and listed in the bill of materials as "not mount", so that fitting one later is a matter of bolts and not of redesign.

**Record.** Lidar or turret, never both: D-014. One shared mounting centre: D-064. Turret or front camera: D-069. Optional parts kept in the model and in the bill of materials as "not mount": D-080. Rear antenna plate with ground plane for the GNSS antenna: D-081. Dates between 12 and 14 November 2026.
