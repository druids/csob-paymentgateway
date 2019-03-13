from decimal import Decimal
from typing import Optional, Union


class Item:
    """
    Item in a cart to be shown in Gateway.

    Notes:
        If the amount=0, the cart content display on the payment gateway will indicate the text FREE

    Warnings:
        At least 1 item (e.g. “Your purchase”) and at most 2 items must be in the cart
        (e.g. “Your purchase” and “Shipping & Handling”). The limitation is given by the graphical design.

    """
    name: str
    quantity: int = 1
    amount: Union[Decimal, int]
    description: Optional[str] = None

    def __init__(self, name: str, amount: Union[Decimal, int], quantity: int = 1,
                 description: Optional[str] = None) -> None:
        """

        Args:
            name: Item’s name, maximum length 20 characters
            amount: Total price for the quantity of the items in hundredths of the currency.
                    The item currency of all the requests will be automatically used as the price.
            quantity: Quantity, must be >=1, integer only
            description: Cart item’s description, maximum length 40 characters
        """
        self.name = name
        self.amount = amount
        self.quantity = quantity
        if description is not None:
            self.description = description

    @property
    def dict(self):
        out_dict = {
            'name': self.name,
            'amount': self.amount,
            'quantity': self.quantity
        }

        if self.description is not None:
            out_dict['description'] = self.description

        return out_dict
