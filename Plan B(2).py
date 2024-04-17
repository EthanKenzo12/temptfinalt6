import pandas as pd
import random
import string


class BookingReferenceGenerator:
    def __init__(self):
        self.generated_references = set()

    def generate_unique_reference(self):
        while True:
            reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if reference not in self.generated_references:
                self.generated_references.add(reference)
                return reference


class SeatBooking:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.seats = pd.read_csv(csv_file_path, index_col='Seat')
        self.reference_generator = BookingReferenceGenerator()
        self.booking_details = {}  # New attribute to store booking details

    def check_availability(self, seat_label):
        seat_label = seat_label.upper()
        return self.seats.at[seat_label, 'Status'] == 'Free'

    def book_seat(self, seat_label, customer_data):
        seat_label = seat_label.upper()
        if self.check_availability(seat_label):
            reference = self.reference_generator.generate_unique_reference()
            self.seats.at[seat_label, 'Status'] = 'Reserved'
            self.booking_details[seat_label] = {'reference': reference, 'customer_data': customer_data}
            self.seats.to_csv(self.csv_file_path)
            print(f"Booking complete. Reference: {reference}")
            return True
        else:
            return False

    def free_seat(self, seat_label):
        seat_label = seat_label.upper()
        if self.seats.at[seat_label, 'Status'] == 'Reserved':
            self.seats.at[seat_label, 'Status'] = 'Free'
            self.booking_details.pop(seat_label, None)  # Remove booking details
            self.seats.to_csv(self.csv_file_path)
            return True
        else:
            return False

    def show_booking_state(self):
        for seat_label, details in self.booking_details.items():
            status = self.seats.at[seat_label, 'Status']
            print(f"Seat {seat_label} is {status}. Booking reference: {details['reference']}")


def main_menu(csv_file_path):
    booking_system = SeatBooking(csv_file_path)

    while True:
        print("\nMenu:")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking state")
        print("5. Exit program")
        choice = input("Choose an option: ")

        if choice == '1':
            seat_label = input("Enter seat label (e.g., '1A'): ")
            if booking_system.check_availability(seat_label):
                print("The seat is available.")
            else:
                print("This seat is not available.")

        elif choice == '2':
            seat_label = input("Enter seat label (e.g., '1A'): ")
            name = input("Enter the customer's name: ")
            email = input("Enter the customer's email: ")
            customer_data = {'name': name, 'email': email}
            if booking_system.book_seat(seat_label, customer_data):
                print("The seat has been booked.")
            else:
                print("This seat has already been booked or does not exist.")

        elif choice == '3':
            seat_label = input("Enter seat label (e.g., '1A'): ")
            if booking_system.free_seat(seat_label):
                print("The seat has been freed.")
            else:
                print("Sorry this seat is not booked or does not exist.")

        elif choice == '4':
            booking_system.show_booking_state()

        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")


csv_file_path = '/Users/sylvin/Desktop/seatplan1.csv'

if __name__ == "__main__":
    csv_file_path = '/Users/sylvin/Desktop/seatplan1.csv'
    main_menu(csv_file_path)
