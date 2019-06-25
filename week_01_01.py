import sys
digit_string = sys.argv[1]
digitals = 0
for dig in digit_string:
    digitals += int(dig)
print(digitals)
