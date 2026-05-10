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

# Latest poznamky od smrcky

- modifiers jsou dopredu nedefinovane, ale nejsme si tim jisti
- entita muze mit nedefinovanou hodnotu -- v nejakem case entita nemusi existovat
- mnozina entit neni definovana, konecna nebo nekonecna -- konecna
- fire prejmenovat na happened
- prepsat formalne t_next
- u mnozin definovat, jestli jsou konecne a neprazdne
- updatnout expressions (mozna ode me)
- definice operatoru je confusing -- to, co mi vygeneroval claude a ani jsem to poradne nezkontroloval
- diskretizace spojiteho casu pomoci time elementu -- moznost realtime definice prev a next, pocita se s elementem










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

Dictionary bude jenom seznam typu entit
Sémantika tam nebude, protože entity mají definované operace atd.
Je možné že stačí opreace a typy tam vůbec nebudou

Přidat k typům sémantiku jak se vztahuje k cestě běhu programu
Channel - kdy se posle hodnota, jak dlouho to trvá, ...


Trace I k reálnému času, ne jenom logickému času, zatím stačí logický

Typ čas
- trace operace
- r(t) - v čase t
- r(t1,t2) - mezi časy 
- existuje čas v intervalu
- pro všechny časy v intervalu
- ...

Důležitý definovat funkční symboly které vrací čas -> dají se použít v trace

At symbol - dame mu predikát a on vrátí čas kdy platí, nebo například kdy platil poprvé naposled, nebo třeba množinu časů kdy platí predikát 

Podobně pracovat s množinami hodnot
- základ jsou teda čas, hodnoty, množiny 

Pro funkční predikáty jako addr, at, diff, atd. Definovat output domény co vrací

Přepsat 5. Sekci, na podporované akce datových typů pro každý zvlášť 

Každý použitý symbol musí být předtím definovaný 

Transformátor typ na typ, trasy a času na predikáty co plati= valuation, z predikátu času na množinu evaluaci, z množiny na jeden prvek, například count

# Razzy

Definovat trasu systému ve vztahu k času (pro začátek logický, chybí reálný - můžeme vzít z MTL) a základní operace a sémantiku a pro každý datový typ přidat spojovací body dané operace s okamžikem na dané trase

U predikátů zadefinovat "t"

Rozšířit čas místo konkrétního na třeba interval nebo něco jiného - potom budeme pracovat s hodnotami v tom například intervalovém čase, které budou v množině - ne jedna hodnota ale množina, nebo interval - anebo dokonce možné hodnoty (přidán aspekt možnosti)

expr "val" má být v konkrétním čase 

"at" změnit, aby z toho bylo jasné, že to je "prev" ale o víc kroků 

"addr" bude modifier typu, ne predikát

"signed" value - přemýšlet nad transformacemi hodnot

Základní datové typy - čas, hodnoty, množiny

Transformátor
z predikátů na časovou událost,
z trasy a času na predikáty, které tam platí (valuation), 
z množiny na jedno číslo,
z predikátů a různých časových okamžiků na množinu různých evaluací