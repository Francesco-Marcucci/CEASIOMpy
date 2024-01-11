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

from ceasiompy.ThermoData.func.des_hbtf_func_test_2 import (
    run_turbofan_analysis_test_2,
    write_hbtf_file,
)

from ceasiompy.ThermoData.func.des_turbojet_func import (
    run_turbojet_analysis,
    write_turbojet_file,
)

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

    cpacs = CPACS(cpacs_path)
    tixi = cpacs.tixi

    alt = get_value_or_default(tixi, cruise_alt_xpath, 1000)

    MN = get_value_or_default(tixi, cruise_mach_xpath, 0.3)

    Fn = 2000
    a=1
    if a==1:
    (
        T_tot_out,
        V_stat_out,
        MN_out,
        P_tot_out,
        massflow_stat_out,
        T_stat_out,
        P_stat_out,
    ) = run_turbojet_analysis(alt, MN, Fn)
    else:
    (
        T_tot_out_byp,
        V_stat_out_byp,
        MN_out_byp,
        P_tot_out_byp,
        massflow_stat_out_byp,
        T_stat_out_byp,
        T_tot_out_core,
        V_stat_out_core,
        MN_out_core,
        P_tot_out_core,
        massflow_stat_out_core,
        T_stat_out_core,
    ) = run_turbofan_analysis_test_2(alt, MN, Fn)

    f = write_hbtf_file(
        file=f,
        T_tot_out_byp=T_tot_out_byp,
        V_stat_out_byp=V_stat_out_byp,
        MN_out_byp=MN_out_byp,
        P_tot_out_byp=P_tot_out_byp,
        massflow_stat_out_byp=massflow_stat_out_byp,
        T_stat_out_byp=T_stat_out_byp,
        T_tot_out_core=T_tot_out_core,
        V_stat_out_core=V_stat_out_core,
        MN_out_core=MN_out_core,
        P_tot_out_core=P_tot_out_core,
        massflow_stat_out_core=massflow_stat_out_core,
        T_stat_out_core=T_stat_out_core,
    )

    g = write_turbojet_file(
        file=g,
        T_tot_out=T_tot_out,
        V_stat_out=V_stat_out,
        MN_out=MN_out,
        P_tot_out=P_tot_out,
        massflow_stat_out=massflow_stat_out,
        T_stat_out=T_stat_out,
        P_stat_out=P_stat_out,
    )

    log.info("----- End of " + MODULE_NAME + " -----")


if __name__ == "__main__":

    cpacs_path = get_toolinput_file_path(MODULE_NAME)
    cpacs_out_path = get_tooloutput_file_path(MODULE_NAME)

    main(cpacs_path, cpacs_out_path)
