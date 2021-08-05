#! /usr/bin/env python
""" helloworld.py
This file contains models. 
""" 
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['QualityControlPreproduction','QualityControlPostproduction','PreProductionLabCritarea']


# PRE PRODUCTION 

class QualityControlPreproduction(ModelSQL, ModelView):
    "Quality Control Preproduction"
    __name__ = "quality.control.preproduction"
    shipment = fields.Many2One('stock.shipment.in', "Supplier Shipment",
    domain=[
            ('state', '=', 'done'),
            ]
    )
    # party = fields.Many2One('party.party',"Party")
    # material = fields.Char('Material')
    # inwarddate = fields.Date('Inward Date')
    critearea = fields.One2Many('preproduction.lab.test.critearea',
        'pre_production_lab_id', 'Analysis Report')
    critearea1 = fields.One2Many('preproduction.lab.test.critearea1',
        'pre_production_lab1_id', 'Analysis Report')
    rejected = fields.One2Many('preproduction.rejected.analysis',
        'pre_production_rejected_id', 'GC Analysis')
    customer = fields.One2Many('preproduction.customer.analysis', 
        'pre_production_customer_id' , 'Customer Specification')
    colour = fields.Char("Colour")
    ph = fields.Char("ph")
    moisture = fields.Char("%Moisture")
    spgravity = fields.Char("Sp.Gravity")
    gcanalysis = fields.Char("%Acidty")
    gcgraphno = fields.Char("Preoxide Value ppm")
    remark = fields.Text("Remarks by R&D")
    image = fields.Binary("Graph Upload")
    graph = fields.Binary("Graph Upload")
    

class PreProductionLabCritarea(ModelSQL,ModelView):
    "Lab Critearea"
    __name__ = "preproduction.lab.test.critearea"
    pre_production_lab_id = fields.Many2One('quality.control.preproduction' , 'Lab Test Id')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")


class PreProductionLabCritarea1(ModelSQL,ModelView):
    "Lab Critearea1"
    __name__ = "preproduction.lab.test.critearea1"
    pre_production_lab1_id = fields.Many2One('quality.control.preproduction' , 'Lab Test Id1')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")

class PreProductionRejectedAnalysis(ModelSQL,ModelView):
    "Rejected Analysis"
    __name__ = "preproduction.rejected.analysis"
    pre_production_rejected_id = fields.Many2One('quality.control.preproduction' , 'Rejected Id')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")

class PreProductionCustomerSpecification(ModelSQL,ModelView):
    "Customer Specification"
    __name__ = "preproduction.customer.analysis"
    pre_production_customer_id = fields.Many2One('quality.control.preproduction' , 'Customer Id')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")

# POST PRODUCTION

class QualityControlPostproduction(ModelSQL, ModelView):
    "Quality Control Postproduction"
    __name__ = "quality.control.postproduction"
    production = fields.Many2One('production', "Production Batch")
    analysis = fields.One2Many('postproduction.analysis.report',
    'post_production_analysis_id', 'Analysis Report')
    analysis1 = fields.One2Many('postproduction.analysis1.report',
    'post_production_analysis1_id', 'Analysis Report')
    postgraph = fields.Binary("Graph Upload")
    rejected = fields.One2Many('postproduction.rejected.analysis',
        'post_production_rejected_id', 'GC Analysis')
    customer = fields.One2Many('postproduction.customer.analysis', 
        'post_production_customer_id' , 'Customer Specification')
    colour = fields.Char("Colour")
    ph = fields.Char("ph")
    moisture = fields.Char("%Moisture")
    spgravity = fields.Char("Sp.Gravity")
    gcanalysis = fields.Char("%Acidty")
    gcgraphno = fields.Char("postoxide Value ppm")
    remark = fields.Text("Remarks by R&D")
    postimage = fields.Binary("Graph Upload")

class PostProductionAnalysis(ModelSQL, ModelView):
    "Post Production analysis"
    __name__ = "postproduction.analysis.report"
    post_production_analysis_id = fields.Many2One('quality.control.postproduction' , 'Analysis Report')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")

class PostProductionAnalysis1(ModelSQL, ModelView):
    "Post Production analysis 1"
    __name__ = "postproduction.analysis1.report"
    post_production_analysis1_id = fields.Many2One('quality.control.postproduction' , 'Analysis Report')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")

class PostProductionRejectedAnalysis(ModelSQL,ModelView):
    "Rejected Analysis"
    __name__ = "postproduction.rejected.analysis"
    post_production_rejected_id = fields.Many2One('quality.control.postproduction' , 'Rejected Id')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")

class PostProductionCustomerSpecification(ModelSQL,ModelView):
    "Customer Specification"
    __name__ = "postproduction.customer.analysis"
    post_production_customer_id = fields.Many2One('quality.control.postproduction' , 'Customer Id')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")