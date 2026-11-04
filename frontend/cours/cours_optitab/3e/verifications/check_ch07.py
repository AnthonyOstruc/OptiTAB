# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 7 (Grandeurs composées et conversions)."""
from sympy import Rational as R, ceiling

# Cours
assert R('2.4') * 60 == 144 and 144 - 120 == 24          # 2,4 h = 2 h 24
assert 2 + R(15, 60) == R('2.25')
assert R(72000, 3600) == 20
assert 600 / 15 == 40
assert R('2.5') * 360 == 900

# Découverte
assert R('3.8') * 1000 == 3800                                           # D1
assert R('0.42') * 10000 == 4200 and R(6500, 10000) == R('0.65')         # D1
assert R('2.5') * 100 == 250                                             # D1
assert R('2.7') * 1000 == 2700 and R(450, 1000) == R('0.45')             # D2
assert R('3.5') * 1000 == 3500 and R(1600, 1000) == R('1.6') > R('1.5')  # D2
assert R('0.75') * 60 == 45 and 2 + R(42, 60) == R('2.7')                # D3
assert R('0.2') * 60 == 12 and 3 + R(20, 60) == R(10, 3)                 # D3
assert R(30, 60) == R('0.5')                                             # D3
assert 150 / R('2.5') == 60 and 60 * 4 == 240 and R(90, 60) == R('1.5')  # D4
assert 84 / 7 == 12 and 12 * 25 == 300 and R(30, 12) == R('2.5')         # D5
assert 12 * 60 == 720 and 12 + 12 == 24                                  # D5
assert R('3.2') * 1000 == 3200 and R(540, 1000) == R('0.54')             # D6
assert R('0.75') * 1000 == 750 and R(2500000, 10 ** 6) == R('2.5')       # D6
assert R('1.2') + R('0.8') == 2                                          # D6
assert 100 * 100 == 10000 and R('2.5') * 1000 == 2500                    # D7

# Entraînement
assert 90 / R('3.6') == 25 and 12 * R('3.6') == R('43.2')                # E1
assert R(1000, 3600) == 1 / R('3.6') and 108 / R('3.6') == 30            # E1
assert 30 * R('3.6') == 108 > 100                                        # E1
assert 54 / R('3.6') == 15 and 15 * R('0.8') == 12                       # E2
assert 25 * R('0.8') == 20 and R(90, 54) == R(20, 12) == R(5, 3)         # E2
assert R('2.5') * 360 == 900 and R(900, 1000) == R('0.9')                # E3
assert 1000 / R('2.5') == 400 and 1500 / R('2.5') == 600                 # E3
assert R(45, 60) == R('0.75') and R('1.2') * R('0.75') == R('0.9')       # E4
assert R('0.9') * R('0.24') == R('0.216')                                # E4
assert 3 * 30 == 90 and R('1.2') * 90 == 108 and 108 * R('0.24') == R('25.92')  # E4
assert R('0.35') * 1000 == 350 and 350 * 60 == 21000                     # E5
assert 21000 * 4 == 84000 and 63 / R('0.35') == 180 and 180 / 60 == 3    # E5
assert 80 * R('2.5') == 200 and R(90, 60) == R('1.5')                    # E6
assert R(210, 84) == R('2.5') and R(36, 60) == R('0.6') and 5 * R('0.6') == 3  # E6
assert 2 + R(48, 60) == R('2.8') and 42 / R('2.8') == 15                 # E6
assert 100 / 10 == 10 and 10 * R('3.6') == 36 < 45                       # E7
assert 200 / 10 == 20                                                    # E7

# Problèmes
assert R(12, 18) == R(2, 3) and R(12, 12) == 1                           # P1
assert R(2, 3) + 1 == R(5, 3) and 24 / R(5, 3) == R('14.4')              # P1
assert R(1, 30) + R(1, 45) == R(1, 18) and 1 / R(1, 18) == 18            # P2
assert 5 * R('2.6') - 2 == 11 and 11 * 2 == 22                           # P3
assert R(22, 8) == R('2.75') and ceiling(R('2.75') / R('2.5')) == 2      # P3
assert 2 * R('2.5') - R('2.75') == R('2.25')                             # P3
assert 2 * R('0.05') == R('0.1') and 24 * 3600 == 86400                  # P4
assert R('0.1') * 86400 / 1000 == R('8.64') and R('8.64') * 30 == R('259.2')  # P4
assert 12 * R('1.5') * R('0.06') == R('1.08')                            # P5
assert R('1.08') * R('1.6') == R('1.728') and ceiling(R('1.728') / R('1.5')) == 2  # P5
assert R('1.728') - R('1.5') == R('0.228')                               # P5
assert 8 * 4 * R('1.5') == 48 and 48 * 1000 == 48000                     # P6
assert 48000 / 20 == 2400 and 2400 / 60 == 40                            # P6
assert 48 * R('4.10') == R('196.80')                                     # P6
assert 11 * 60 + 17 - (9 * 60 + 47) == 90 and R(90, 60) == R('1.5')      # P7
assert 240 / R('1.5') == 160 and R(240, 120) == 2                        # P7
assert R('1.5') + 2 == R('3.5') and abs(480 / R('3.5') - R('137.1')) < R('0.1')  # P7
assert R(160 + 120, 2) == 140                                            # P7

print("check_ch07 : tous les contrôles passent.")
