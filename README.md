# Getting started
## Windows:
* Dowload the newest version of python on: https://www.python.org/downloads/
* Install pygame by entering following command in to the cmd:  
`pip install pygame`
* Download this repository as a zip and extract the zip in a chosen folder.
* Locate your cmd to that folder en enter:  
`python qwirkle.py`

## macOS:
* Download the latest version of python on: https://www.python.org/downloads/
* To install pygame, open the terminal and run the following command:  
`python3 -m pip install -U pygame --user`
* Either download this repository as a zip and extract or clone it with  
`git clone https://github.com/stijn-geerits/Qwirkle.git`
* With your terminal in the correct directory, run the command  
`python qwirkle.py`  
or  
`./qwirkle.py`  
(You may need to `chmod +x qwirkle.py`)


## Linux:
* Install a python 3.X package (if it isn't already):
  + On Debian based systems:  
  `sudo apt-get install python3`
  + On Fedora based systems:  
  `sudo dnf install python3`
* Install pygame:  
`python3 pip install pygame`
* Either download this repository as a zip or clone it:  
  + Install git (if it isn't already)
    - On Debian based systems:  
    `sudo apt-get install git`
    - On Fedora based systems:  
    `sudo dnf install git`
  + Clone the repository:  
  `git clone https://github.com/stijn-geerits/Qwirkle`
* Run the game by double clicking or running in a terminal:  
`python3 qwirkle.py`  
or  
`./qwirkle.py`  
(If this does not work, run: `chmod +x qwirkle.py`)

# Requirements

* Er zullen 108 blokken zijn.
* Er zullen zes kleuren zijn: rood, oranje, geel, groen, blauw en paars.
* Er zullen zes vormen zijn: cirkel, x, diamant, vierkant, ster en klaver.
* Elk blokje zal een kleur en een vorm hebben.
* Er zullen 3 blokjes zijn voor elke mogelijke combinatie van kleur en vorm.
* Er zullen tussen de twee en de acht spelers zijn.
* Bij het begin van het spel, zal elke speler zes blokjes krijgen.
* De speler die de langste aaneengesloten lijn kan leggen, zal het spel beginnen door deze lijn te leggen.
* Bij elke beurt zal de speler uit twee opties kiezen: aanleggen of ruilen.
  + Aanleggen
    - Alle blokjes zullen met elkaar verbonden zijn.
    - Alle aangelegde blokjes zullen een lijn vormen.
    - Elke aaneengesloten lijn zal bestaan uit blokjes met dezelfde kleur of vorm.
    - Een aaneengesloten lijn zal nooit langer zijn dan zes blokjes.
    - Een aaneengesloten lijn zal nooit identieke blokjes bevatten.
    - De speler zal evenveel blokjes uit de zak nemen als hij/zij heeft aangelegd.
    - Als de zak leeg is, zal de speler geen nieuwe blokjes nemen.
  + Ruilen
    - De speler zal evenveel blokjes in de zak steken als hij/zij er uit haalt.
    - De genomen blokjes zullen willekeurig zijn.
    - Als de zak leeg is en de speler kan niet aanleggen, zal de speler zijn/haar beurt overslaan.
* Als alle spelers hun beurt achtereenvolgens overslaan, zal het spel eindigen.
* Als de zak leeg is, zal het spel eindigen wanneer een speler geen blokjes meer heeft.
* Als de speler heeft aangelegd, zal deze punten ontvangen.
  + De speler zal een punt ontvangen voor elk aanliggend blokje per lijn waaraan hij/zij aanlegt.
  + De speler zal zes bonuspunten ontvangen wanneer hij/zij een aaneengesloten lijn van zes blokjes legt/aanvult.
  + De speler zal zes bonuspunt ontvangen wanneer deze als eerst al zijn blokjes heeft opgebruikt.
* De speler met de hoogste eindscore zal winnen.
