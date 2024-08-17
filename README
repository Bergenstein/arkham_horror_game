Report Detailing Advanced Features, Design Patterns and Custom Databases Used in Arkham Horror Game:

                           | Advanced Python Features |
                           | ======================== |
1. Metaclass(Action): This has been utilized on arkham_horror.py to automatically register methods into a dictionary that have "_action" prefix. The reason for using metaclass was to reduce boilderplate code and register actions centrally. I did this to simplify the option and to extend the game by registering other actions and preventing error if I were to later manually register actions. 

2. TypeVar and Generics: It is used throughout the game design extensively. My justification was to ensure type-safety of operations and flexibity for classes to handle various types as the game deals with different types of data such as Action, Item, Space, etc. 

3. Literal: Used in monster.py, fight_prep.py, mythos_token.py. In all these places it has been used to encapsulate different specific values that these components are allowed to have within the rules of the game. I used this feature both for type-safety and ease of understanding. 

4. Enums: Used in encounter_deck.py and skills.py to replace arbitrary values with meaningful names to simpify to the code-base and promote consistency. 

5. Custom Errors: I have utilized custom errors throughout the game to be handle game-related errors in a more meaningful and easier manner than built-in errors. 

6. Protocol classes: Used in fight_prep.py, monster.py and investigator.py. I have used protocols to allow structural subtyping to simplify extension of the classes within these modules. 

7. Dunder Methods: Used throughout the project. I have used the dunder methods to make the code more intuitive and easier to use, and make the custom classes more like native python objects.

8. Fluent API: Used in several places wihin the game. It is just so intuitive to customize instance creation through method chaining and returning self that is further passed to the next method, creating a builder pattern. It assisted me when I was creating more complex objects. 

9. if TYPE_CHECKING: I used it to avoid circular imports. 

10. TypedDict: I used this as a custom simple and lightweight database to maintain the integrity of investigator data via enforcing a strict schema.


--------------------------------------------------------------------------------------------------------------------------

                            |Object-Oriented Design Patterns|
                            |===============================|
1. Template Method Pattern: Has been used so that subclasses can define certain methods (override them) according to their specifications without the need to change the main skeleton in the template. It has been used in spell_effect.py, deck_interface.py, etc.

2. Strategy Pattern: Has been used in encounter_deck.py, fight_prep.py. If for example, if game behaviour is changed dynamically, as when investigator is faced with an encounter, there may be different encounters requiring different strategies for the encounters. It makes the game fluent and responsive. 

3. Command Pattern: Used in various locations within the game such as mythos_cup.py, fight_prep.py, and more. I have used command pattern to decouple the do from the how. In other words, decoupling the object that knows how to do something from an object that actually performs it and doesn't need to be bothered with implementation details. It was used again in spirit of Open Closed principle. 

4. Builder Pattern: As discussed already in previous section (8.Fluent API) to customize object creation via method chaining, implementing a fluent API. For example, with monster that has many attributes, the builder pattern allows to configure these attributes in a fluent manner. 

5. State Pattern: As monsters and other game entities can exist in different states, the behaviour of these entities changes accordingly. The state patterns allows for the changes to be reflected in states of these entities as it allows state transition. For example, as the monster exists in multiple states (not in all states at once I hope :-) ), state pattern allows state related actions for monsters in each state and transitions between those states. This pattern allows state-dependent behavior change, localizing behaviors to state objects, and allowing code extending and maintenance. 

6. Facade Pattern: investigator.py and game.py both exhibit elements of facade pattern. Facade has been used in game.py to encapsulate complexities of managing all various game components. It provides a clean and straightforward interface for clients to interact with various underlying components without having any knowledge of their complexities. Similar pattern, to some degree, has been used in investigator.py to hide complexity of other components within fight_prep.py and investigator_status.py, etc. 

7. Factory pattern: Used in arkham_horror.py and encounter_deck.py. The `ActionManager` within arkham_horror.py, for example, acts as the "factory". It utilizes the `Action` metaclass to obtain the required action objects. It allows for extension of the game, via for example introducing other actions, without having to modify the core logic. I have also tried to utilize factory pattern in encounter_deck.py for the same reason. 

8. Composition Pattern: Has been used extensively throughout the game. It has been used to allow object composition at runtime. This allows for dynamic behaviour of objects. This way, I have simplified some interfaces by utilizing some of the methods of the object instances,composed inside of the class, and avoided inheritance when not needed. 

9. Inheritance: Used throughout the game to define common behaviors and traits for classes that are related. For example, `Investigator` class can inherit common attributes and methods from the `BaseInvestigator` class to simplify its creation. Also, it has been used to maintance consistency for related objects across the game. Finally, I have utilized inheritance to allow extending game mechanics in the future in case version 3 or 4 or Arkham Horror introduces another investigator or character that shares common attributes with the base class but has some other cool features. This allows extension without altering the base class. 


--------------------------------------------------------------------------------------------------------------------------

                                |Custom Data Structure Used|
                                |==========================|

1. Custom Deque: Deque has been used throughout the game since it was just so intuitive to use a custom deque. The game had specific rules regarding different "Decks of Cards" such as ability to draw from front, draw from rear, add to front, add to rear, and shuffle, etc. So, I have implemented a custom deque to encapsulate these operations. The deque been composed internally inside of `EncounterDeck`, `EventDeck`, `MonsterDeck` to utilize its methods and allow for game extension (by for example creating more decks). 

2. Directed Graph: Has been used in the game setup inside of arkham_horror.py where `SpaceManager` used it to create spaces and connect them. As the locations within the board need connecting, a Directed Graph is a natural choice. The spaces represent nodes and their connection represent edges of the graph. It helps facilitate game flow. 


--------------------------------------------------------------------------------------------------------------------------
Concluding Remarks:

It was an awesome module, Stefano. The assignment made me a much better programmer. I learned a lot about design patterns used in OOP and some very advanced python features I had never heard of. I am sure to employ them extensively as I code for work. 

I attemped to build the entire game. However, I realized that it is a massive task. So, I implemented as much as I could, while adhering to best practices of OOP as much as possible. Fun fact, I even bought the game and played it to learn the rules. Quite addictive and fun actually :=) 

Thank you very much once again for such incredible module and great assignment. I really enjoyed it. 

