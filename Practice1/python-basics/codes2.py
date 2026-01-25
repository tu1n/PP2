ute = 0.85
utk = 499.53
a1 = float(input("Сумманы енгізіңіз: "))
a2 = input("Енгізілген валюта түрін таңдаңыз (USD, EUR, KZT): ").upper()

print("Валюта бағамының соңғы жаңартылуы: 2026 жылы 25 қаңтар")

if a2 == "USD":
    eur = a1 * ute
    kzt = a1 * utk
    print(f"Сіздің шотыңыз: {a1:.2f} USD")
    print(f"Еуромен: {eur:.2f} EUR")
    print(f"Теңгемен: {kzt:.2f} KZT")

elif a2 == "EUR":
    usd = a1 / ute
    kzt = usd * utk
    print(f"Сіздің шотыңыз: {a1:.2f} EUR")
    print(f"Доллармен: {usd:.2f} USD")
    print(f"Теңгемен: {kzt:.2f} KZT")

elif a2 == "KZT":
    usd = a1 / utk
    eur = usd * ute
    print(f"Сіздің шотыңыз: {a1:.2f} KZT")
    print(f"Доллармен: {usd:.2f} USD")
    print(f"Еуромен: {eur:.2f} EUR")

else:
    print("Қате: Валюта түрі танылмады! USD, EUR немесе KZT қолданыңыз")
