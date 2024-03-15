# JSD-project
Cilj ovog projekta je razvijanje jezika specifičnog za domen koji omogućava opisivanje pravila, likova, sposobnosti i scenarija za <b>turn-based tekst rpg igru</b>. Ovaj jezik će biti usmeren na pojednostavljivanje procesa razvoja teksualnih igara.

### Instaliranje

   U terminal PyCharm-a vašeg projekta unosite sledeću komandu: `pip install JSD-project`

### Uputstvo za pokretanje projekta

- Importujte `main` iz `JSD_project`.
- U vaš kod dodajte `main.run_main()`.
- Pokrenite aplikaciju.

### Definisanje karakteristika igre:

 - #### Modelovanje likova: 

    Za igrača se može zadati njegov opis, zdravlje, osobine kao što su _vigor_ (koji povećava inicijalno zdravlje), _strenght_ (koji povećava jačinu igrača) i _endurance_ (koji povećava otpornost). Zatim je moguće zadati igračev početni XP, level, XP potreban za prelazak na naredni level. Takođe je moguće postaviti neke stvari u igračev ranac i na kraju postaviti igrača u početnu regiju.
    
    
    Primer igrača je prikazan u sledećem isečku:
 
        (adventurer) {
            portrayal "You are an intrepid adventurer."
            health 100
            vigor 10
            strength 10
            endurance 10
            currentExperience 0
            neededExperienceForLevelUp 20
            level 1
            inventory {
                twix
            }
            position entryway
        }

 - #### Modelovanje neprijatelja:

    Za neprijatelje je moguće zadati njihov opis, zdavlje, jačinu njihovog napada na igrača, određenu količinu XP poena koje će igrač dobiti nakon što ga pobedi i njegovu poziciju. Takođe je moguće definisati koja oružja ili stvari će neprijatelj ispustiti prilikom njegovog poraza.

    Primer neprijatelja je prikazan u sledećem isečku:

        ((young_dragon)) {
            portrayal "A young playful dragon looking for trouble."
            health 30
            damage 15
            xp 50
            position kitchen
            drops {
                twix,
                mars
            }
            dropsWeapon {
                katana
            }
        }

 - #### Modelovanje prostorija:

    Kod modelovanja prostorija kreator ima mogućnost da zada opis prostorijem, stvari koje se nalaze u prostoriji, povezanost prostorije sa drugim prostorijama, negativan efekat okoline kao i potrebne uslove za ulazak u samu prostoriju.

    Primer neprijatelja je prikazan u sledećem isečku:

        <hallway> {
            portrayal "a dimly lit hallway"
            contains key, flashlight, chest, katana
            ::
            N -> kitchen,
            S -> entryway
            ::
            environmental_dmg damage 33
            requirements key,flashlight
        }

 - #### Modelovanje stvari:

    Za stvari takođe postoji opis same stvari. Pored toga imamo i atribut _isStatic_ koji služi za označavanje da li igrač može da je pokupi i stavi u svoj ranac. Pored toga imamo i atribut _contains_ kojim kreator stavlja druge objekte unutar jednog. Ukoliko se objekat može koristiti potrebno je dodati i _аctivation_ atribut kojim se naglašava željena akcija.

    Primer stvari je prikazan u sledećem isečku:

        [chest] {
            portrayal "A wooden chest on the ground."
            contains twix, mars
            isStatic True
        }

        [twix] {
            portrayal "A twix bar. Caramel, shortbread and chocolate delightfully restoring health."
            activation heal 50
            isStatic False
        }

 - #### Modelovanje oružja:

    Oružje daje dodatnu snagu udarcima igrača. Iz tog razloga jedini atribut koji on ima jeste _damage_ kojim je označena dodatna slaga igračebog udarca.

    Primer oružja je prikazan u sledećem isečku:

        [[katana]] {
            damage 10
        }

 - Modelovanje podešavanja igre:

    Kreator može definisati da li je moguće nositi više oružja odjednom ili igrač mora da ispusti trenutno oružje kada pokupi novo. Takođe može definisati da li dobija dodatni potez ukoliko u toku borbe odluči da iskoristi neki _item_ ili ne. U igri je potrebno definisati početnu i finalnu prostoriju.

    Primer podešavanja igre je prikazan u sledećem isečku:

        *settings* {
            dropOldWeapon False
            additionalTurnAfterUse False
        }

        start_position entryway
        final_position backyard

 - #### Interpretacija borbe:

    Kada igrač uđe u prostoriju poroverava se da li u toj prostoiji postoji neprijatelj i ako postoji započinje borba. Borba se odvija po _turn base_ sistemu odnosno igrač i neprijatelj naizmenično odigravaju poteze. Prilikom svakog svog poteza igrač može odabrati da napadne neprijatelja, da iskoristi neki _item_ iz ranca ili da pobegne iz borbe, pri čemu se vraća u prethodnu prostoriju. Prilikom poraza igrač se oživljava u startnoj prostoriji sa praznim rancem, dok se sve njegove stvari koje je posedovao prilikom borbe smeštaju u prostoriju koja je prethodila prostoroji u kojoj se odvijala borba. Ako igrač pobedi neprijatelja on biva nagrađen sa XP poenima, _item_-ima i oružjima koje je neprijatelj ispustio.