import random
import string

class BookingSystem:
    def __init__(self):
        self.booking_references = set()
        self.customer_data = {}
        self.seat_status = {}

    def generate_unique_reference(self):
        while True:
            reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if reference not in self.booking_references:
                self.booking_references.add(reference)
                return reference

    def book_seat(self, seat_label, customer_info):
        if seat_label not in self.seat_status or self.seat_status[seat_label] == 'F':
            reference = self.generate_unique_reference()
            self.seat_status[seat_label] = reference
            self.customer_data[reference] = customer_info
            return reference
        return None

    def free_seat(self, seat_label):
        if seat_label in self.seat_status and self.seat_status[seat_label] != 'F':
            reference = self.seat_status[seat_label]
            self.seat_status[seat_label] = 'F'
            del self.customer_data[reference]
            return True
        return False

# Example Usage
booking_system = BookingSystem()

# A customer books a seat
seat_booked = booking_system.book_seat('1A', {'name': 'John Doe', 'email': 'johndoe@example.com'})
print(f"Seat booked with reference: {seat_booked}")

# Freeing a seat
if booking_system.free_seat('1A'):
    print("Seat has been freed and customer data removed.")
