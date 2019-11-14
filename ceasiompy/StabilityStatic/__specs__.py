#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ceasiompy.utils.moduleinterfaces import CPACSInOut, CEASIOM_XPATH
STABILITY_STATIC_XPATH =  '/cpacs/toolspecific/CEASIOMpy/stability/static'


# ===== RCE integration =====

RCE = {
    "name": "StabilityStatic",
    "description": "Determine if a vehicle is statically stable or not  ",
    "exec": "pwd\npython stabilitystatic.py",
    "author": "Loïc Verdier",
    "email": "loic.verdier@epfl.ch",
}


# ===== CPACS inputs and outputs =====

cpacs_inout = CPACSInOut()


# ===== Input =====

cpacs_inout.add_input(
    var_name='',
    var_type=list,
    default_value=None,
    unit=None,
    descr="Name of the aero map to evaluate",
    cpacs_path=STATICSTAB_XPATH + '/aeroMapUid',
    gui=True,
    gui_name='__AEROMAP_SELECTION',
    gui_group='Inputs',
)


# ===== Output =====

cpacs_inout.add_output(
    var_name='longitudinaly_stable',
    default_value=None,
    unit='1',
    descr='Is the aircraft longitudinaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/results/longitudinalStaticStable',
)

cpacs_inout.add_output(
    var_name='dirrectionaly_stable',
    default_value=None,
    unit='1',
    descr='Is the aircraft dirrectionaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/results/directionnalStaticStable',
)


cpacs_inout.add_output(
    var_name='trim_alt_longi_list',
    default_value=None,
    unit='m',
    descr='corresponding trim altitude at which the airraft have been noticed to be longitudinaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/trimconditions/longitudinal/altitude',
)

cpacs_inout.add_output(
    var_name='trim_mach_longi_list',
    default_value=None,
    unit='-',
    descr='corresponding trim mach at which the airraft have been noticed to be longitudinaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/trimconditions/longitudinal/machNumber',
)

cpacs_inout.add_output(
    var_name='trim_aoa_longi_list',
    default_value=None,
    unit='degree',
    descr='corresponding trim AOA at which the airraft have been noticed to be longitudinaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/trimconditions/longitudinal/angleOfAttack',
)

cpacs_inout.add_output(
    var_name='trim_aos_longi_list',
    default_value=None,
    unit='degree',
    descr='corresponding trim AOS at which the airraft have been noticed to be longitudinaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/trimconditions/longitudinal/angleOfSideslip',
)

cpacs_inout.add_output(
    var_name='trim_alt_direc_list',
    default_value=None,
    unit='m',
    descr='corresponding trim altitude at which the airraft have been noticed to be directionaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/trimconditions/directional/altitude',
)

cpacs_inout.add_output(
    var_name='trim_mach_direc_list',
    default_value=None,
    unit='-',
    descr='corresponding trim mach at which the airraft have been noticed to be directionaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/trimconditions/directional/machNumber',
)

cpacs_inout.add_output(
    var_name='trim_aoa_direc_list',
    default_value=None,
    unit='degree',
    descr='corresponding trim AOA at which the airraft have been noticed to be directionaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/trimconditions/directional/angleOfAttack',
)

cpacs_inout.add_output(
    var_name='trim_aos_direc_list',
    default_value=None,
    unit='degree',
    descr='corresponding trim AOA at which the airraft have been noticed to be directionaly stable',
    cpacs_path=STABILITY_STATIC_XPATH+'/trimconditions/directional/angleOfSideslip',
)