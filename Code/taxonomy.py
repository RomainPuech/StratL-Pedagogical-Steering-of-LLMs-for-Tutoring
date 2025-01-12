from enum import Enum

class Intent(Enum):
    # Problematizing category
    P_LIMITS = 1
    P_GENERALIZATION = 2
    P_HYPOTHESIS = 3
    P_ARTICULATION = 4
    P_REFLECTION = 5
    P_CONNECTION = 6

    # Structuring category
    S_SELFCORRECTION = 11
    S_CORRECTION = 12
    S_STRATEGY = 13
    S_STATE = 14
    S_SIMPLIFY = 15
    S_OFFLOAD = 16
    S_HINT = 17

    # Affective category
    A_CHALLENGE = 21
    A_CONFIDENCE = 22
    A_CONTROL = 23
    A_CURIOSITY = 24

    #Generic category
    G_GREETINGS = 31
    G_OTHER = 32


    