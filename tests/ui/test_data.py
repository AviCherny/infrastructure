from ui.pages.purchase_page import PassengerDetails


def make_passenger(prefix: str = "") -> PassengerDetails:
    name = f"{prefix}_John Doe" if prefix else "John Doe"
    return PassengerDetails(
        name=name,
        address="123 Main St",
        city="Springfield",
        state="IL",
        zip_code="62701",
        card_type="visa",
        credit_card_number="4111111111111111",
        credit_card_month="12",
        credit_card_year="2027",
        name_on_card=name,
    )
