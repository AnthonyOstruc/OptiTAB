# -*- coding: utf-8 -*-
"""Contrôles numériques du chapitre 6 (Proportionnalité, ratios, pourcentages)."""
from sympy import Rational as R

# Cours
assert R('7.20') / 3 == R('2.40') and 5 * R('2.40') == 12
assert R(2, 5) * 35 == 14 and R(3, 5) * 35 == 21
assert 80 * R('0.85') == 68
assert R('1.2') * R('0.8') == R('0.96')
assert R(184 - 160, 160) == R(15, 100)
assert R(6, 30) == R(1, 5) == R(20, 100)

# Découverte
assert R('10.80') / 4 == R('2.70') and 7 * R('2.70') == R('18.90')       # D1
assert 10 * R('2.70') == 27 and R('16.20') / R('2.70') == 6              # D1
assert R(7, 2) == R('17.5') / 5 == R(28, 8) == R('3.5')                  # D2
assert 11 * R('3.5') == R('38.5') and R(13, 4) == R('3.25')              # D2
assert 250 * R('0.3') == 75 and 50 * R('0.12') == 6                      # D3
assert 60 * R('1.5') == 90 and 480 * R('0.05') == 24                     # D3
assert 200 * R('1.1') == 220                                             # D3
assert 64 * R('0.75') == 48 and 64 - 48 == 16                            # D4
assert 184 - 160 == 24 and R(24, 160) == R('0.15')                       # D4
assert 3 + 5 == 8 and 56 // 8 == 7 and 3 * 7 == 21 and 5 * 7 == 35       # D5
assert 21 + 35 == 56 and R(21, 35) == R(3, 5)                            # D5
assert 72 // 9 == 8 and 4 * 8 == 32 and 5 * 8 == 40                      # D5
assert R(6, 100) == R('0.06') and 250 * R('0.06') == 15                  # D6
assert 9 / R('0.06') == 150 and 80 * R('0.06') == R('4.8')               # D6
assert R(9, 720000) == R(1, 80000)                                       # D7
assert 80000 == 800 * 100 and 15 * R('0.8') == 12 and 20 / R('0.8') == 25  # D7

# Entraînement
assert 81 / R('1.08') == 75 and 75 * R('1.08') == 81                     # E1
assert 81 * R('0.92') == R('74.52') != 75                                # E1
assert 84 / R('0.7') == 120                                              # E1
assert 250 * R('0.9') == 225 and 225 * R('0.8') == 180                   # E2
assert R('0.9') * R('0.8') == R('0.72') and 250 * R('0.72') == 180       # E2
assert 1 - R('0.72') == R('0.28')                                        # E2
assert 1 + 6 + 3 == 10 and R('4.5') / 10 == R('0.45')                    # E3
assert 6 * R('0.45') == R('2.70') and 3 * R('0.45') == R('1.35')         # E3
assert R('0.45') + R('2.70') + R('1.35') == R('4.5')                     # E3
assert 5 + 2 * 3 == 11 and 5 + 2 * 6 == 17 and 2 * 11 != 17              # E4
assert R(11, 3) != R(17, 6)                                              # E4
assert R('3.2') * 5 == 16 and R(24, 5) == R('4.8')                       # E5
assert R(5, 1500000) == R(1, 300000)                                     # E5
assert R(12, 50) == R('0.24')                                            # E5
assert R('1.2') * R('1.1') == R('1.32') and 150 * R('1.32') == 198       # E6
assert R('1.5') * R('0.5') == R('0.75')                                  # E6
assert 1 / R('0.8') == R('1.25')                                         # E7
assert 100 * R('0.8') == 80 and 80 * R('1.25') == 100                    # E7
assert 1 / R('0.5') == 2                                                 # E7

# Problèmes
assert 120 - 30 == 90 and 120 * R('0.8') == 96 and 96 - 10 == 86         # P1
assert 90 - 86 == 4                                                      # P1
assert 100 - 30 == 70 == 100 * R('0.8') - 10                             # P1 Q5
assert 2 + 8 == 10 and R(2, 10) == R('0.2')                              # P2
assert 2 / R('0.16') == R('12.5') and R('12.5') - 10 == R('2.5')         # P2
assert R(2, R('12.5')) == R('0.16')                                      # P2
assert 720 * R('0.45') == 324 and 324 * R(2, 9) == 72                    # P3
assert R(72, 720) == R('0.10') and R('0.45') * R(2, 9) == R('0.1')       # P3
assert 800 * R('0.12') == 96 and 800 * R('0.15') == 120                  # P4
assert 15 - 12 == 3 and R(3, 12) == R('0.25') and 120 - 96 == 24         # P4
assert R(24, 96) == R('0.25')                                            # P4
assert 240 * R('1.2') == 288 and 288 * R('0.7') == R('201.60')           # P5
assert R('1.2') * R('0.7') == R('0.84') and 240 * R('0.84') == R('201.6')  # P5
assert R('0.84') - 1 == -R('0.16')                                       # P5
assert R('4.80') / R('1.5') == R('3.20') and R('7.13') / R('2.3') == R('3.10')  # P6
assert 4 * R('3.20') == R('12.80') and 4 * R('3.10') == R('12.40')       # P6
assert R('12.80') - R('12.40') == R('0.40')                              # P6
assert abs(16 / R('3.10') - R('5.16')) < R('0.01')                       # P6
assert R(2 - R('2.5'), R('2.5')) == -R('0.2')                            # P7
assert R(R('2.4') - 2, 2) == R('0.2')                                    # P7
assert R('0.8') * R('1.2') == R('0.96') and R('0.96') - 1 == -R('0.04')  # P7
assert (R('2.4') - R('2.5')) / R('2.5') == -R('0.04')                    # P7

print("check_ch06 : tous les contrôles passent.")
