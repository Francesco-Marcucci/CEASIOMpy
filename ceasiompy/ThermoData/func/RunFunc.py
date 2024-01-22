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
    ENGINE_TYPE_XPATH,
)
from ceasiompy.utils.commonnames import (
    ENGINE_BOUNDARY_CONDITIONS,
    CONFIG_CFD_NAME,
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

# XPath definition

ref_area_xpath = REF_XPATH + "/area"
cruise_alt_xpath = CLCALC_XPATH + "/cruiseAltitude"
cruise_mach_xpath = CLCALC_XPATH + "/cruiseMach"


def ThermoData_run(cpacs_path, cpacs_out_path, wkdir):

    if not wkdir.exists():
        raise OSError(f"The working directory : {wkdir} does not exit!")

    cpacs = CPACS(cpacs_path)
    tixi = cpacs.tixi

    alt = get_value_or_default(tixi, cruise_alt_xpath, 1000)
    MN = get_value_or_default(tixi, cruise_mach_xpath, 0.3)
    Fn = 2000

    EngineBC = Path(wkdir, ENGINE_BOUNDARY_CONDITIONS)

    f = open(EngineBC, "w")

    engine_type = get_value_or_default(tixi, ENGINE_TYPE_XPATH, 0)

    if engine_type == 0:
        (
            T_tot_out,
            V_stat_out,
            MN_out,
            P_tot_out,
            massflow_stat_out,
            T_stat_out,
            P_stat_out,
        ) = run_turbojet_analysis(alt, MN, Fn)

        f = write_turbojet_file(
            file=f,
            T_tot_out=T_tot_out,
            V_stat_out=V_stat_out,
            MN_out=MN_out,
            P_tot_out=P_tot_out,
            massflow_stat_out=massflow_stat_out,
            T_stat_out=T_stat_out,
            P_stat_out=P_stat_out,
        )

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


def add_ThermoData(cfg, cpacs, case_dir_path, file, mesh_markers, alt, mach):
    """Add ThermoData parameter to the config file."""
    cfg["INLET_TYPE"] = "TOTAL_CONDITIONS"
