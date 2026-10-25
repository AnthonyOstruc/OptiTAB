n = 4728
thousands = n // 1000
hundreds = n // 100 % 10
tens = n // 10 % 10
units = n % 10
print("Sum of the digits:", thousands + hundreds + tens + units)
print("Backwards:", units * 1000 + tens * 100 + hundreds * 10 + thousands)
