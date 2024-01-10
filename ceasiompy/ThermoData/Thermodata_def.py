"""
CEASIOMpy: Conceptual Aircraft Design Software

Developed by CFS ENGINEERING, 1015 Lausanne, Switzerland

Calculate outlet conditions fot turbojet and turbofan engines

| Author: Francesco Marcucci
| Creation: 2023
"""

# =================================================================================================
#   IMPORTS
# =================================================================================================

from pathlib import Path

from ceasiompy.ThermoData.func.des_hbtf_func_test_2 import run_turbofan_analysis_test_2

from ceasiompy.ThermoData.func.des_turbojet_func import run_turbojet_analysis

from ceasiompy.utils.ceasiomlogger import get_logger

from ceasiompy.utils.moduleinterfaces import (
    check_cpacs_input_requirements,
    get_toolinput_file_path,
    get_tooloutput_file_path,
)
from ceasiompy.utils.commonxpath import (
    REF_XPATH,
    CLCALC_XPATH,
)
from cpacspy.cpacsfunctions import (
    get_value_or_default,
)
from cpacspy.cpacsfunctions import create_branch, get_value, get_value_or_default
from cpacspy.cpacspy import CPACS
from markdownpy.markdownpy import MarkdownDoc
from ceasiompy.utils.ceasiompyutils import get_results_directory


log = get_logger()

MODULE_DIR = Path(__file__).parent
MODULE_NAME = MODULE_DIR.name


# =================================================================================================
#   CLASSES
# =================================================================================================


# =================================================================================================
#   FUNCTIONS
# =================================================================================================


# =================================================================================================
#    MAIN
# =================================================================================================

# XPath definition

ref_area_xpath = REF_XPATH + "/area"

mass_type_xpath = CLCALC_XPATH + "/massType"

custom_mass_xpath = CLCALC_XPATH + "/customMass"

percent_fuel_mass_xpath = CLCALC_XPATH + "/percentFuelMass"

cruise_alt_xpath = CLCALC_XPATH + "/cruiseAltitude"

cruise_mach_xpath = CLCALC_XPATH + "/cruiseMach"

load_fact_xpath = CLCALC_XPATH + "/loadFactor"


def main(cpacs_path, cpacs_out_path):

    log.info("----- Start of " + MODULE_NAME + " -----")

    results_dir = get_results_directory("ThermoData")
    md = MarkdownDoc(Path(results_dir, "ThermoData.md"))

    cpacs = CPACS(cpacs_path)
    tixi = cpacs.tixi

    alt = get_value_or_default(tixi, cruise_alt_xpath, 1000)

    MN = get_value_or_default(tixi, cruise_mach_xpath, 0.3)

    Fn = 2000

    run_turbojet_analysis(alt, MN, Fn)

    run_turbofan_analysis_test_2(alt, MN, Fn)

    log.info("----- End of " + MODULE_NAME + " -----")


if __name__ == "__main__":

    cpacs_path = get_toolinput_file_path(MODULE_NAME)
    cpacs_out_path = get_tooloutput_file_path(MODULE_NAME)

    main(cpacs_path, cpacs_out_path)
