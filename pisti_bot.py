from random import random
from random import choice
from time import sleep

hazir_deste = []
deste = []
ortadakiler = []
el_oyuncu = []
el_pc = []
depo_oyuncu = []
depo_pc = []
cekilen_kart = 0
ortadaki = "boş"
atilacak_oyuncu = ""
atilacak_pc = ""
pisti_oyuncu = 0
pisti_pc = 0
puan_oyuncu = 0
puan_pc = 0

def kart_ver(liste):
	global cekilen_kart

	if cekilen_kart < 52:
		liste.append(deste[cekilen_kart])
		cekilen_kart += 1

def kart_at():
	global ortadaki
	global ortadakiler
	global el_pc
	global depo_pc
	global atilacak_pc
	atilacak_pc = ""

	for i in el_pc:
		if i[-1] == ortadaki[-1]:
			atilacak_pc = i

	if atilacak_pc == "":
		if ortadaki[-1] == "A" or ortadaki == "Karo 10" or ortadaki == "Sinek 2":
			for i in el_pc:
				if i[-1] == "J":
					atilacak_pc = i

			if atilacak_pc == "":
				atilacak_pc = choice(el_pc)
		else:
			atilacak_pc = choice(el_pc)

		if atilacak_pc[-1] == "J":
			digerleri = []
			for i in el_pc:
				if i[-1] != "J":
					digerleri.append(i)
			if digerleri != []:
				atilacak_pc = choice(digerleri)

	el_pc.remove(atilacak_pc)
	print("Cengiz ortaya {} attı.".format(atilacak_pc))
	sleep(0.5)

def kart_al_oyuncu():
	global atilacak_oyuncu
	global el_oyuncu
	al = input("Atılacak kart: ")
	while True:
		try:
			al = int(al) - 1

		except ValueError:
			al = int(input("Lütfen sayı giriniz: "))

		else: 
			break
	while True:
		if al >= 0 and al < (len(el_oyuncu)):
			break

		else:
			al = int(input("Lütfen geçerli aralıkta bir sayı giriniz: ")) - 1
	atilacak_oyuncu = el_oyuncu[al]
	el_oyuncu.remove(atilacak_oyuncu)
	print("\nOrtaya {} atıldı.".format(atilacak_oyuncu))
	sleep(0.5)

def karsilastir(atilan, depo, kim):
	global ortadaki
	global ortadakiler
	global pisti_pc
	global pisti_oyuncu
	pisti = 0
	ortadakiler.append(atilan)
#	print("ortadaki:{}\natilan:{}".format(ortadaki, atilan))
	if ortadaki[-1] == atilan[-1]:
		if len(ortadakiler) == 2:
			print("Pişti!")
			if ortadaki[-1] == "J":
				pisti += 20
				print(pisti)
			else:
				pisti += 10
				print(pisti)

			if kim == "pc":
				pisti_pc += pisti
			elif kim == "oyuncu":
				pisti_oyuncu += pisti

		depo += ortadakiler
		ortadaki = "boş"
		ortadakiler = []
	
	elif atilan[-1] == "J" and ortadaki != "boş":
		depo += ortadakiler
		ortadaki = "boş"
		ortadakiler = []

	else:
		ortadaki = atilan

	print("Ortadaki kart {}\n".format(ortadaki))
	sleep(1)

def yazdir():
	print("Elinizdekiler:")
	print("---------------")
	global el_oyuncu
	for i in range(len(el_oyuncu)):
		print(str(i + 1) + "-> " + el_oyuncu[i])
	print("\n")
	print("Ortadaki kart: " + ortadaki + "\n\n")

def puan_say(depo, pisti):
	puan = pisti
	for i in depo:
		if i[-1] == "A" or i[-1] == "J":
			puan += 1

		if i == "Karo 10":
			puan += 3

		if i == "Sinek 2":
			puan += 2
	return puan

for i in range(2, 11):
	hazir_deste.append("Kupa " + str(i))
	hazir_deste.append("Maça " + str(i))
	hazir_deste.append("Karo " + str(i))
	hazir_deste.append("Sinek " + str(i))


hazir_deste.append("Kupa A")
hazir_deste.append("Kupa K")
hazir_deste.append("Kupa Q")
hazir_deste.append("Kupa J")
hazir_deste.append("Maça A")
hazir_deste.append("Maça K")
hazir_deste.append("Maça Q")
hazir_deste.append("Maça J")
hazir_deste.append("Karo A")
hazir_deste.append("Karo K")
hazir_deste.append("Karo Q")
hazir_deste.append("Karo J")
hazir_deste.append("Sinek A")
hazir_deste.append("Sinek K")
hazir_deste.append("Sinek Q")
hazir_deste.append("Sinek J")

print("Kartlar karılıyor...")

for i in range(len(hazir_deste)):
	secilen  = choice(hazir_deste)
	deste.append(secilen)
	hazir_deste.remove(secilen)

print("Kartlar dağıtılıyor!\n")

for i in range(4):
	kart_ver(el_oyuncu)

for i in range(4):
	kart_ver(el_pc)

for i in range(4):
	kart_ver(ortadakiler)

ortadaki = ortadakiler[0]
sleep(2)

for tur in range(1, 25):
	yazdir()
	kart_al_oyuncu()
	karsilastir(atilacak_oyuncu, depo_oyuncu, "oyuncu")
	kart_at()
	karsilastir(atilacak_pc, depo_pc, "pc")
	if len(el_oyuncu) == 0:
		if cekilen_kart == 52:
			print("Maç bitti!")
			sleep(0.5)
			print("Puanlar sayılıyor...")
			sleep(2)

		else:
			print("Kartlar yeniden dağıtılıyor...\n\n")
			sleep(1.5)
			for i in range(4):
				kart_ver(el_oyuncu)

			for i in range(4):
				kart_ver(el_pc)

puan_pc = puan_say(depo_pc, pisti_pc)

puan_oyuncu = puan_say(depo_oyuncu, pisti_oyuncu)


if len(depo_pc) > len(depo_oyuncu):
	puan_pc += 3

elif len(depo_oyuncu) > len(depo_pc):
	puan_oyuncu += 3
print("Cengiz'in puanı: {}".format(puan_pc))
"""print("pc depo: {}".format(depo_pc))
for i in range(len(depo_pc)):
	for j in range(i+1, len(depo_pc)):
		if depo_pc[i] == depo_pc[j]:
			print("2 tane {} var".format(depo_pc[i]))"""
sleep(0.5)
print("Senin puanın: {}".format(puan_oyuncu))
"""print("oyuncu depo: {}".format(depo_oyuncu))
for i in range(len(depo_oyuncu)):
	for j in range(i+1, len(depo_oyuncu)):
		if depo_oyuncu[i] == depo_oyuncu[j]:
			print("2 tane {} var".format(depo_oyuncu[i]))"""
sleep(0.5)
if puan_pc == puan_oyuncu:
	print("Berabere!")
elif puan_pc >= puan_oyuncu:
	print("Kaybettin!")
else:
	print("Kazandın!")


input()
