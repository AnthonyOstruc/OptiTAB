# holiday_planner.py - the Lisbon budget, now with variables

# Data
travellers = 2
nights = 6
days = 7
flight_price = 89.5      # return ticket, per person
room_price = 74          # per night, for the room
food_per_day = 25        # per person
museum_pass = 21.5       # per person
months = 6               # months left to save

# Calculations
flights = travellers * flight_price
hotel = nights * room_price
food = travellers * days * food_per_day
museums = travellers * museum_pass
total = flights + hotel + food + museums

# Display
print("=== HOLIDAY IN LISBON ===")
print("Travellers:", travellers)
print("Flights:", flights)
print("Hotel:", hotel)
print("Food:", food)
print("Museums:", museums)
print("Total:", total)
print("Per person:", round(total / travellers, 2))
print("To save each month:", round(total / months, 2))
