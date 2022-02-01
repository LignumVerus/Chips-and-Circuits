# Chips and Circuits
Chips kunnen worden gebruik voor het vervullen van verschillende functies in apparaten zoals computers en bijvoorbeeld telefoons. Chips zijn meestal logisch ontworpen en getransformeerd naar een lijst (netlist) met koppelbare poorten (gates). In de praktijk is het leggen van de bedrading (vanaf nu 'routes' genoemd) tussen de chips een moeilijke en kostbare taak. De manier waarop de routes tussen de chips worden gelegd is van groot belang. Kortere routes leiden tot minder kosten en snellere circuits, terwijl langere routes leiden tot hogere kosten en langzamere circuits. Kruisingen van routes leiden tot een grote verhoging van de kosten. 

In dit project zijn de chips zelf al geplaatst en houden wij ons alleen bezig met de routes tussen de chips op een zo kort mogelijk manier te leggen met zo weinig mogelijk kruisende routes, om dus zo weinig mogelijk kosten te genereren. Hieronder is een formule te zien hoe de kosten in het circuit worden berekend, waarbij *n* stukje lijn tussen 2 coördinaten voorstelt en *k* het aantal kruisingen tussen routes voorsteld. Het is dus de bedoeling om alle chips met elkaar te verbinden met zo weinig mogelijk kosten:  

```C = n + 300 * k```  

<plaatje>

## Aan de Slag
### Vereisten
Deze codebase is volledig geschreven in [Python3.7.3](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip d.m.v. de volgende instructie:  

```pip install -r requirements.txt```

### Structuur
* **code:** 
  * .py bestanden 
* **data:**
  * **chip_0:**
    * netlist .csv bestanden en print .csv bestanden 
  * **chip_1:**
    * netlist .csv bestanden en print .csv bestanden 
  * **chip_2:**
    * netlist .csv bestanden en print .csv bestanden
* **output:**
  * **chip_0:**
    * output .csv bestand netlist 1-3
  * **chip_1:**
    * output .csv bestand netlist 4-6
  * **chip_2:**
    * output .csv bestand 7-9
  * **optimize:** 
    * output .csv bestand 
  * **plots:**
    * plot .png files
  * README.md
  * requirements.txt
  * run.py (lost de gewenste netlist op)
  * try_all.py (lost alle netlists op)  

 De netlist .csv bestanden bevatten de info welke chips met elkaar verbonden moeten worden. De print .csv bestanden bevatten de x,y coordinaten van de chips in de netslisten. De output .csv bestanden bevatten de coordinaten van de routes die zijn gelegd. En de plot .png bestanden bevatten de plots die bij deze routes horen.


### Testen
Om het programma te gebruiken, is daar de volgende instructie voor nodig:  

```python run.py {chip} {netlist}```


## Algoritme
### Random
Eerste versie. Kiezen elke keer random een van de mogelijkheden om naar toe te gaan. De mogelijkheden zijn inprinicipe naar het noorden, oosten, zuiden, westen, boven en beneden. Waneer er op een van de mogelijkheden een andere chip ligt of als dat de plek is waar de route net vandaan kwam, wordt deze mogelijkheid uit de lijst gehaald. In deze versie is het dus nog mogelijk voor routes omzichzelf en andere routes te kruizen.

### Depth first and breath first search
Om aan het random algortime iets meer restricties toe te voegen, hebben we eerste een depth first search algortime gebruikt. Hierbij werden de restricties dat routes zichzelf en andere routes niet mogen kruizen toegevoegd. De netlist werd echter snel te groot om een depth first search te kunnen toepassen. Daarom hebben we deze omgeschreven naar een breath first search. Deze zal natuurlijk altijd de korste route vinden, nooit een willekeurige route. Met een maximale diepte voor de breath search konden de eerste paar routes wel opgelost worden, maar daarna werden de routes toch te lang en ingewikkeld. Ook werden er routes ingesloten door eerder gelegde routes, waardoor het uberhaupt niet meer mogelijk was voor deze routes om de eind chip te bereiken. Om dit een klein beetje op te lossen hebben we de volgorde waarin de routes gelegd worden aangepast. De routes werden neergelegd op volgorde van de manhattan distance tussen de begin- en eindchip. De route tussen de begin- en eindchip met de korste manhattan distance wordt als eerste gelegd. Ook met deze toevoeging, gebeurd het dat routes die later gelegd worden ingesloten worden door eerder gelegde routes. Ook kan dit algoritme erg lang duren.

### A*

#### Extra cost


#### Iterative

#### Recursief

#### Optimize

### Hill climber


## Autheurs
* Rachel de Haan
* Viola Koers
* Finn Peranovic

## Dankwoord
* StackOverflow
* minor programmeren van de UvA
