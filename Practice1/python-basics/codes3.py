import random
import string
a1 = string.ascii_letters + string.digits + "!@#$%^&*"
a2 = "".join(random.sample(a1, 8))
print(f"Сіздің құпия сөзіңіз: {a2}")
