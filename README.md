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

    Za igrača se može zadati njegov opis, te njegove osnovne osobine (zdravlje, mana, damage, defence, mana damage, mana defence). Pored osnovnih osobina kreator takođe može da zada i osobine kao što su _vigor_ (koji povećava inicijalno zdravlje), _strenght_ (koji povećava jačinu igrača) i _endurance_ (koji povećava otpornost) koje igrač može da povećava kroz sistem levelovanja. Zatim je moguće zadati igračev početni XP, level, XP potreban za prelazak na naredni level. Takođe je moguće postaviti neke stvari u igračev ranac i na kraju postaviti igrača u početnu regiju. Ako se ne zada neka od osobina podrazumevana vrednost te osobnine će biti dodeljena. Kreator može da definiše i kakve tipove oružja ili armora igrač može da koristi. 
    
    
 Primer igrača je prikazan u sledećem isečku:
 
 
        player adventurer {
            currentExperience 0
            neededExperienceForLevelUp 20
            levelScalingPercentage 50000
            level 1
            portrayal "You are an intrepid adventurer."
            position entryway
            inventory {
                mars
            }
            intelligence 5
            vigor 10
            strength 10
            endurance 10
        
            health 100
            mana 100
            damage 10
            defence 5
        
            canEquip {
                sword,wood
            }
        }

 - #### Modelovanje neprijatelja:

    Za neprijatelje je moguće zadati njihov opis i poziciju, te neke osnovne osobine (zdavlje i mana). Pored osnovnih osobina takođe je moguće definisati i njegove specijalne napade. Jedan specijalan napad se sastoji od sledećih osobina healthDamage, healthDamageVariance, manaDamage, manaDamageVariance i frequency. Pored specijalnih napada moguće je definisati i  healing akciju neprijatelja pri čemu se zadaju osobine verovatnoća, količina i varijansa za količinu hilovanja. Takođe je moguće definisati i određenu količinu XP poena koje će igrač dobiti nakon što ga pobedi kao i koja oružja, stvari ili armor će neprijatelj ispustiti prilikom njegovog poraza.

    Primer neprijatelja je prikazan u sledećem isečku:
    

        enemy young_dragon {
            portrayal "A young playful dragon looking for trouble."
            position kitchen
            drops {
                twix,
                mars,
                katana,
                shield
            }
            health 1000
            mana 10
            xp 50
            attacks {
                attack fire_attack {
                    manaDamage 30
                    manaDamageVariance 0.2
                    frequency 0.6
                }
                attack kick_attack {
                    healthDamage 40
                    healthDamageVariance 0.1
                    frequency 0.4
                }
            }
            healing {
                chance 0.5
                amount 10
                amountVariance 0.2
            }
        }

 - #### Modelovanje prostorija:

    Kod modelovanja prostorija kreator ima mogućnost da zada opis prostorijem, stvari koje se nalaze u prostoriji, povezanost prostorije sa drugim prostorijama, negativan efekat okoline kao i potrebne uslove za ulazak u samu prostoriju.

    Primer neprijatelja je prikazan u sledećem isečku:
    
        
        region hallway {
            portrayal "a dimly lit hallway"
            contains chest, katana
            ::
            N -> kitchen,
            S -> entryway
            ::
            environmental_dmg damage 33
            requirements key,flashlight
        }


 - #### Modelovanje stvari:

    Za stvari takođe postoji opis same stvari. Pored toga imamo i atribut _isStatic_ koji služi za označavanje da li igrač može da je pokupi i stavi u svoj ranac. Pored toga imamo i atribut _contains_ kojim kreator stavlja druge objekte unutar jednog. Ukoliko se objekat može koristiti potrebno je dodati i _аctivation_ atribut kojim se naglašava željena akcija (vraćanje health-a ili mane).

    Primer stvari je prikazan u sledećem isečku:
    

        item chest {
            portrayal "A wooden chest on the ground."
            contains twix, mars
            isStatic True
        }
        
        item twix {
            portrayal "A twix bar. Caramel, shortbread and chocolate delightfully restoring health."
            activation heal 50
            isStatic False
        }
        
        item mars {
            portrayal "A mars bar. Caramel and chocolate delightfully restoring health."
            activation restoreMana 700
            isStatic False
        }

 - #### Modelovanje oružja i armora:

    Oružje daje dodatnu snagu udarcima igrača. Atribut koje jedno oružje može da ima jesu:  healthDamage, healthCost, manaDamage, manaCost, minimalan potreban level za korišćenje oružja i tip samog oružja. Mimo dodatne snage može se definisati na oružje dok se koristi utiče na neku od osnovnih igračevih osobina kao sto su: current_max_health, current_max_mana, damage, defence, mana_damage i mana_defence. Oružje će modifikovati zadatu osobinu prema polinomijalnoj funkciji za koju se zadaju koeficijenti.
    Razlika između oružja i armora jeste ta što armor nema healthCost i manaCost i u tome što on smanjuje uticaj udaranja protivnika dok oružje povećava igračev udarac.

    Primer oružja je prikazan u sledećem isečku:
    

        weapon katana {
            portrayal "A very mighty sword"
            type sword
            healthDamage 10
            modifiers {
                modifier {
                    modifies current_max_health
                    coefficients 10,43
                }
                modifier {
                    modifies damage
                    coefficients 0.5,5,2
                }
                modifier {
                    modifies mana_defence
                    coefficients 25
                }
            }
        }
        
   Primer armora je prikazan u sledećem isečku:
   
       armor shield {
            portrayal "Ugly shield"
            type wood
            requiredLevel 1
            defense 30
            modifier {
                modifies defence
                coefficients 0.7,4,3
            }
        }

 - Modelovanje podešavanja igre:

    Kreator može definisati da li je moguće nositi više oružja,armora odjednom ili igrač mora da ispusti trenutno oružje kada pokupi novo. Takođe može definisati da li dobija dodatni potez ukoliko u toku borbe odluči da iskoristi neki _item_ ili ne. U igri je potrebno definisati početnu i finalnu prostoriju.

    Primer podešavanja igre je prikazan u sledećem isečku:


        settings {
            dropOtherWeapons True
            dropOtherArmors False
            additionalTurnAfterUse False
        }

        start_position entryway
        final_position backyard

 - #### Interpretacija borbe:

    Kada igrač uđe u prostoriju poroverava se da li u toj prostoiji postoji neprijatelj i ako postoji započinje borba. Borba se odvija po _turn base_ sistemu odnosno igrač i neprijatelj naizmenično odigravaju poteze. Prilikom svakog svog poteza igrač može odabrati da napadne neprijatelja, da iskoristi neki _item_ iz ranca ili da pobegne iz borbe, pri čemu se vraća u prethodnu prostoriju. Prilikom poraza igrač se oživljava u startnoj prostoriji sa praznim rancem, dok se sve njegove stvari koje je posedovao prilikom borbe smeštaju u prostoriju koja je prethodila prostoroji u kojoj se odvijala borba. Ako igrač pobedi neprijatelja on biva nagrađen sa XP poenima, _item_-ima i oružjima koje je neprijatelj ispustio.
  
 - #### Komande:
    Lista mogućih komandi koje igrač može da izvrši je sledeća: 
    - move \<dir> - kretanje u određenom pravcu
    - drop \<item> - ispuštanje stvari, oružja ili armora
    - open \<item> - otvaranje stvari
    - take \<item> - stavljanje stvari, oružja ili armora u igračev ranac
    - use \<item> - aktiviranje stvari
    - equip \<item> - opremanje oružjem ili armorom
    - unequip \<item> - skidanje oružja ili armora
    - info \<item> - detaljan opis stvari, oružja ili armora
    - inventory - uvid u igračev ranac
    - health - uvid u zdravstveno stanje
    - attack - napadanje portivnika
    - flee - povlačenje iz borbe
    - inc vigor - povećavanje vigora
    - inc endurance - povećavanje izdržljivosti
    - inc strength - povećavanje snage
    - inc intelligence - povećavanje inteligencije
    - stats - uvid u trenutno stanje igračevih osobina