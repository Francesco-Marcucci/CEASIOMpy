"""
CEASIOMpy: Conceptual Aircraft Design Software

Developed by CFS ENGINEERING, 1015 Lausanne, Switzerland

Small description of the script

Python version: >=3.8

| Author: Name
| Creation: YEAR-MONTH-DAY

TODO:

    * Things to improve ...
    * Things to add ...

"""


# ==============================================================================
#   IMPORTS
# ==============================================================================

from ceasiompy.utils.ceasiomlogger import get_logger

log = get_logger()


# ==============================================================================
#   CLASSES
# ==============================================================================


# ==============================================================================
#   FUNCTIONS
# ==============================================================================


def simple_turbofan(Mach, Alt, Fn):

    """Function to calculate ...
    Function to calculate output variables of interest from a simple turbojet

    Source:
        * Reference paper or book, with author and date

    Args:
        Mach (float):  Argument 1 [adim]
        Alt (float): Argument 2 [feet]
        Fn (float): Argument 3 [lbf]

    Returns:
        P_out_nozzle: Return 1 [psi]
        T_out_nozzle: Return 2 [degr]
        V_out_nozzle: Return 3 []
    """

    return (T_out_nozzle, Mach_out_nozzle)


# ==============================================================================
#    MAIN
# ==============================================================================

if __name__ == "__main__":

    print("Nothing to execute!")
