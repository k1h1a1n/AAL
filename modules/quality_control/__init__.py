# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
# from qualitycontrol import QualityControl
from . import qualitycontrol
__all__ = ['register']


def register():
    Pool.register(
        qualitycontrol.PostProductionCustomerSpecification,
        qualitycontrol.PostProductionRejectedAnalysis,
        qualitycontrol.PostProductionAnalysis,
        qualitycontrol.PostProductionAnalysis1,
        qualitycontrol.PreProductionLabCritarea1,
        qualitycontrol.PreProductionCustomerSpecification,
        qualitycontrol.PreProductionRejectedAnalysis,
        qualitycontrol.PreProductionLabCritarea,
        qualitycontrol.QualityControlPreproduction,
        qualitycontrol.QualityControlPostproduction,
        module='quality_control', type_='model')
    Pool.register(
        module='quality_control', type_='wizard')
    Pool.register(
        module='quality_control', type_='report')
