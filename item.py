"""
Module that handles and defines basic structure for cards and items used in Arkham Horror.
"""


class Card:
    """
    simple class that represents a card from Arkham Horror. These are later used by game mechanics from more envolved modules.
    """

    name: str
    card_type: str
    description: str
    effect: str
    amount: int

    def __init__(
        self,
        name: str,
        card_type: str,
        description: str,
        effect: str,
        amount: int,
    ):
        """
        initializes a new Card instance.
        """
        self.name = name
        self.type = card_type
        self.description = description
        self.effect = effect
        self.amount = amount


class Item(Card):
    """
    :cls:`Item` inherits from :cls:`Card`.
    """

    def __init__(
        self, name: str, description: str, effect: str, amount: int
    ) -> None:
        """
        Initializes a new instance of :cls:`Item` class.
        """
        super().__init__(name, "Item", description, effect, amount)
