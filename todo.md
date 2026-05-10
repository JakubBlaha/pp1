# Latest poznamky od smrcky

- modifiers jsou dopredu nedefinovane, ale nejsme si tim jisti
    - make entity modifier keys extensible per requirement
    - make entity modifier partial function definition extensible per requirement
- entita muze mit nedefinovanou hodnotu -- v nejakem case entita nemusi existovat
    - mela by se undefined hodnota propagovat?
    - mohli bychom pridat predikat isUndefined
- mnozina entit neni definovana, konecna nebo nekonecna -- konecna
- fire prejmenovat na happened
- prepsat formalne t_next
- u mnozin definovat, jestli jsou konecne a neprazdne
- updatnout expressions (mozna ode me)
- definice operatoru je confusing -- to, co mi vygeneroval claude a ani jsem to poradne nezkontroloval
- diskretizace spojiteho casu pomoci time elementu -- moznost realtime definice prev a next, pocita se s elementem
- projit cely dokument a verifikovat, ze vsechny pouzite symboly jsou pred pouzitim definovane
- fix predefined event kinds


# Compiled

- dictionary predicates
- vztah operaci k trase, effect predicaty, ktere pouzivaji cas
- datovy typ interval
- datovy typ mnozina
- vyresit signet, etc.
- funkcni prvek na pocet prvku v mnozine
- (vytvorit mnozinu entit, pro ktere plati nejaky predikat)?

- Channel - kdy se posle hodnota, jak dlouho to trvá, ...
- Trace I k reálnému času, ne jenom logickému času, zatím stačí logický
- dame predikat, vrati cas kdy predikat plati, pomoci toho by se dal definovat i event

Todo by me:
- big sigma is used in multiple places, we should use words more instead of symbols











# Ja

- dictionary neni self explanatory
- typ entity by mohl byt definovany pouze mnozinou operaci
- formalni vztah operaci k trase
- trace definovat k realnemu casu
- datovy typ cas
- funkcni symboly na cas dat napred
- sjednotit funkcni symbol na cas
- pridat matematicky interval
- datovy typ mnozina
- interval - cislo nebo zacatek a konec?

# Paja

Přidat k typům sémantiku jak se vztahuje k cestě běhu programu
Channel - kdy se posle hodnota, jak dlouho to trvá, ...

Trace I k reálnému času, ne jenom logickému času, zatím stačí logický

Transformátor typ na typ, trasy a času na predikáty co plati= valuation, z predikátu času na množinu evaluaci, z množiny na jeden prvek, například count

# Razzy

Transformátor
z predikátů na časovou událost,
z trasy a času na predikáty, které tam platí (valuation), 
z množiny na jedno číslo,
z predikátů a různých časových okamžiků na množinu různých evaluací