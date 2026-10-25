left = "red"
right = "blue"
print("Before:", left, right)

# first method: with a temporary variable
temp = left
left = right
right = temp
print("After the first swap:", left, right)

# second method: Python's multiple assignment
left, right = right, left
print("After the second swap:", left, right)
