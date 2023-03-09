# ===== IMPORTY =====

import os
import time

from data_kavovaru import menu_vstup
from data_kavovaru import nabidka_vstup
from data_kavovaru import zasoby_vstup
from data_kavovaru import prodeje_vstup


# ===== FUNKCE ======

def zobrazeni_nabidky(kompletni_menu: dict, aktualni_zasoby: dict) -> str:
    """
    Popis: funkce pozdraví uživatele, zkontroluje aktuální stav zásob,
        dle nich zobrazí nabídku kávy a umožní výběr kávy či zadání 
        servisního slova.

    Return: servisní slovo (revize, stop) nebo číslo kávy dle číslování
        v menu a ve formátu string.
    """     
    from data_kavovaru import logo

    # KONTROLA ZÁSOB A ZOBRAZEN NABÍDKY
    os.system("cls")
    print(f"{logo}\nMENU:")

    for cislo, druh_kavy in enumerate((menu.keys()), 1):
        vypsat = True
        cena = menu[druh_kavy]["cena"]
        for ingredience in zasoby.keys():
            if zasoby[ingredience] < menu[druh_kavy]["složení"][ingredience]:
                vypsat = False
        if vypsat:
            print(f"| {cislo} | {druh_kavy:<15}|{cena:>5} Kč |")
            nouzovy_rezim = False

    # VOLBA KÁVY (ČI ZADÁN SERVISNÍHO SLOVA)
    if nouzovy_rezim:
        vybrana_kava = input("Je nám líto, ale kávovar je mimo provoz... Pro servisní "
                            "informace zadejte klíčové slovo: ")         
    else:
        vybrana_kava = input("\nZadejte číslo požadované kávy: ") 

    # VÝSTUP FUNKCE
    return vybrana_kava

def vypocet_ceny(index_kavy: int) -> int:
    """
    Popis: funkce získá vstup (index kávy v seznamu nabídky) a na základě
        něj vypočítá cenu požadované kávy.
        
    Return: int - cena požadované kávy.
    """
    cena = menu[nabidka[vybrana_kava]]["cena"]
    return cena

def platba(cena_vybrane_kavy) -> bool:
    """
    Popis: funkce zobrazí požadovanou čásku za vybranou kávu a umožní platbu kávy.

    Return: 
        True: pokud platba proběhne vpořádku.
        False: pokud platba neproběhne.
    """
    oddelovac = "-" * 45

    # VÝPOČET CENY
    print(f"\nVybrali jste {nabidka[vybrana_kava]}. Celková cena činí {cena} Kč.\n"
            "Automat příjímá mince v hodnotě: 1 Kč, 2 Kč, 5 Kč, 10 Kč, 20 Kč, 50 Kč.\n")
    
    # PLATBA
    moznosti_volby = ("1", "2", "5", "10", "20", "50", "exit")
    zaplaceno = 0
    while zaplaceno < cena:
        vhozena_mince = input("Zadejte hodnotu vhazované mince. \n"
                            "(Pro zrušení objednávky zadejte 'exit'): ")
        if vhozena_mince not in moznosti_volby:
            print("Neplatná volba, zkuste to znovu...")
            continue
        elif vhozena_mince == "exit":
            return False
            break
        else:
            zaplaceno += int(vhozena_mince)
            zbyva_zaplatit = cena - zaplaceno
            if zaplaceno == cena:
                print(f"Platba proběhla v pořádku, děkuji!\n{oddelovac}")
            elif zaplaceno > cena:
                vratit = zaplaceno - cena
                print(f"Platba proběběhla v pořku. Vracím {vratit} Kč.\n{oddelovac}")
            elif zaplaceno < cena:
                print(f"Celkem uhrazeno: {zaplaceno} Kč | Zbývá uhradit {zbyva_zaplatit} Kč."
                        f"\n{oddelovac}")
                        
    return True

def odecet_zasob(index_kavy: int, zasoby: dict) -> dict:
    """
    Popis: funkce při vstupu získá index požadované kávy a dict aktálního stavu zásob,
        ten pak aktualizuje na základě spotřeby zvolené kávy.

    Return: dict s aktualizovanými údaji o stavu zásob.
    """
    zasoby_aktualizace = zasoby

    for ingredience, hodnota in (menu[nabidka[vybrana_kava]]["složení"]).items():
        zasoby_aktualizace[ingredience] -= hodnota
    
    return zasoby_aktualizace

def priprava_kavy():
    """
    Popis: funkce imituje přípravu kávy. Zobrazí animaci a následně se
        rozloučí se zákazníkem.
    """
    from data_kavovaru import animace_vareni_kavy
    oddelovac = "=" *27

    # ANIMACE PŘÍPRAVY KÁVY
    for animace in animace_vareni_kavy:
        os.system("cls")
        print(f"{animace}\nPřipravuji kávu...")
        time.sleep(1)

    # ROZLOUČENÍ 
    os.system("cls")
    print(f"{animace_vareni_kavy[2]}\nProsím, odeberte svou kávu.\n"
        f"{oddelovac}\nDěkujeme za návštěvu a přejem krásný den!\n")
        
    time.sleep(3.5)

def servisni_rezim():
    """
    Popis: po zadání klíčového slova "revize" namísto vybrání nápoje
        kávovar zobrazí servisní informace (zásoby a případné upozornění
        podkud jsou == 0, tržba, návod) a případně umožní spustit 
        podfunkci pro doplnění zásob.
    """
    oddelovac = "+-----------+-----------+"
    global zasoby

    # VÝPIS ZÁSOB A UPOZORNĚNÍ
    os.system("cls")
    print(f"\nZÁSOBY:\n{oddelovac}")
    for zbozi, mnozstvi in zasoby.items():
        print(f"|{zbozi:<11}|{mnozstvi:^11}|")
    print(oddelovac)
    for zbozi, mnozstvi in zasoby.items():
        if mnozstvi == 0:
            print(f"UPOZORNĚNÍ:\nJe nutné doplnit {zbozi}!")

    # VÝPIS PRODANÉHO ZBOŽÍ A TŘŽBY
    print(f"\nPRODEJ:\n{oddelovac}")
    for zbozi, mnozstvi in prodeje.items():
        print(f"|{zbozi:<11}|{mnozstvi:^11}|")
    print(oddelovac)
    print(f"\nTRŽBA CELKEM: {trzba} Kč\n", "=" * 20, sep="")

    # SERVISNÍ VOLBY
    while True:
        volba_technika = input("\nNávod:\nDOPLNĚNÍ KÁVOVARU - zadejte 'stock'\n"
          "UKONČENÍ SERVISNÍHO REŽIMU - zadejte 'exit'\n"
          "VYPNUTÍ KÁVOVARU - zadejte  klíčové slovo 'stop'\nv hlavním menu"
          "kávovaru (místo volby kávy).\n\nZadejte svou volbu: ")
        if volba_technika.lower() == "exit":
            break
        elif volba_technika.lower() == "stock":
            zasoby = doplneni_kavovaru(zasoby)
        else:
            print("Neplatná volba, zkuste to znovu...")

def doplneni_kavovaru(zasoby: dict) -> dict:
    """
    Popis: funkce vezme slovník s aktuálním vstupem zásob, vyžádá si od uživatele
        informaci kolik jakých ingrediencí chce doplnit a aktualizuje stav zásob.

    Return: dict s aktualizovaným stavem zásob.
    """
    oddelovac = "=" *22
    zasoby_aktualizace = zasoby_vstup

    for ingredience in zasoby_aktualizace.keys():
        while True:
            pridano = input(f"{ingredience} - zadejte doplňované množství: ")
            if pridano.isnumeric():
                pridano = int(pridano)
                zasoby_aktualizace[ingredience] += pridano
                break
            else:
                print("Neplatná volba, zkuste to znovu...")

    print(f"Zásoby byly doplněny.\n{oddelovac}")
    return zasoby_aktualizace



# ===== KÓD KÁVOVARU ======

# PROMĚNNÉ
menu = menu_vstup
nabidka = nabidka_vstup
zasoby = zasoby_vstup
prodeje = prodeje_vstup
trzba = 0
moznosti_volby = ["revize", "exit", "stop"]

for cislo in range(1, len(menu) + 1):
    moznosti_volby.append(str(cislo))

# START KÁVOVARU PRO TECHNIKA
os.system("cls")
print("\nVítejte! Načítám aplikaci kávovaru...\n\nNávod:\n"
        "SERVISNÍ REŽIM - namísto volby kávy zadejte 'revize'\n"
        "UKONČENÍ APLIKACE - namísto volby kávy zadejte 'stop'")

while True:
    spusteni = input("\nPro spuštění kávovaru zadejte 'start',\n"
                         "pro vypnutí kávovaru zadejte 'stop': ")

# APLIKACE KÁVOVARU PRO UŽIVATELE
    if spusteni.lower() == "start":
        while True:
            vybrana_kava = zobrazeni_nabidky(menu, zasoby)
            vybrana_kava = vybrana_kava.lower()
            if vybrana_kava not in moznosti_volby:
                print("Neplatná volba, zkuste to znovu...")
                continue
            elif vybrana_kava == "stop":
                break
            elif vybrana_kava == "revize":
                servisni_rezim()
            else:
                vybrana_kava = int(vybrana_kava) -1
                cena = vypocet_ceny(vybrana_kava)
                platba_ok = platba(cena)
                time.sleep(1.5)
                if platba_ok:
                    priprava_kavy()
                    trzba += cena
                    prodeje[nabidka[vybrana_kava]] += 1
                    zasoby = odecet_zasob(vybrana_kava, zasoby)

    elif spusteni.lower() == "stop":
        print("\nVypínám kávovar... Přeji Vám příjemný den!")
        break
    else:
        print("Neplatná volba, zkuste to znovu...")