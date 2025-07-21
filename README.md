Koledar z dogodki


1. Uvod

Projekt predstavlja namizno aplikacijo za upravljanje osebnih dogodkov
preko koledarja. Uporabnik lahko znotraj intuitivnega grafičnega
vmesnika izbere datum, doda dogodek z imenom, opisom in časom, nato pa
ob določenem trenutku prejme obvestilo. Aplikacija je razvita v
programskem jeziku Python s pomočjo knjižnice Tkinter in modula za
sistemska obvestila Plyer.

Delovanje aplikacije

2 Glavno okno (main.py)

Glavni program prikazuje trenutno uro, dan in mesečni koledar. Uporabnik
lahko s puščicama navigira med meseci. Z miškino izbiro dneva se
omogočita gumba za ogled in dodajanje dogodkov. Dnevi se obarvajo, da je
trenutni dan označen, izbrani dan pa izstopa vizualno.

3 Dodajanje dogodka (add_event.py)

Uporabnik lahko dogodku dodeli ime, opis in čas (ure, minute). Po
potrditvi se dogodek shrani v datoteko \'events.json\'. Vsakemu dogodku
se samodejno dodeli edinstven identifikator (UUID). Ob uspešni oddaji se
v ozadju zažene program reminder.py, ki skrbi za opomnike.

4 Prikaz dogodkov (events_list.py)

Vsi dogodki iz datoteke \'events.json\' se izpišejo v posebnem oknu.
Uporabnik ima možnost dogodke izbrisati. Dogodki se prikažejo v
kronološkem zaporedju in vsebujejo ime, datum, uro in opis.

5 Opomniki (reminder.py)

Skripta reminder.py se izvaja v ozadju in vsako sekundo preverja, ali je
čas za kateri od dogodkov. Če se trenutni čas ujema z dogodkom, se
prikaže sistemsko obvestilo s pomočjo knjižnice Plyer. Vsak opomnik se
prikaže le enkrat (preverjanje na podlagi ID-ja dogodka).

6 Zaključek

Projekt Koledar je enostavna, a funkcionalna aplikacija za organizacijo
dogodkov. Združuje osnovne funkcionalnosti koledarja s shranjevanjem in
opominjanjem, kar je koristno za vsakodnevno uporabo. Možnost razširitve
vključuje sinhronizacijo z zunanjo bazo, dodajanje ponavljajočih
dogodkov ter izboljšan uporabniški vmesnik.
