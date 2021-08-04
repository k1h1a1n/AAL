#! /usr/bin/env python
""" helloworld.py
This file contains models. 
""" 
from trytond.model import ModelSQL, ModelView, fields

__all__ = ['QualityControlPreproduction','QualityControlPostproduction','PreProductionLabCritarea']

class QualityControlPreproduction(ModelSQL, ModelView):
    "Quality Control Preproduction"
    __name__ = "quality.control.preproduction"
    shipment = fields.Many2One('stock.shipment.in', "Supplier Shipment",
    domain=[
            ('state', '=', 'done'),
            ]
    )
    critearea = fields.One2Many('preproduction.lab.test.critearea',
        'pre_production_lab_id', 'Analysis Report')
    colour = fields.Char("Colour")
    ph = fields.Char("ph")
    moisture = fields.Char("%Moisture")
    spgravity = fields.Char("Sp.Gravity")
    gcanalysis = fields.Char("GC Analysis")
    gcgraphno = fields.Char("GC Graph No.")
    
    

class QualityControlPostproduction(ModelSQL, ModelView):
    "Quality Control Postproduction"
    __name__ = "quality.control.postproduction"
    name = fields.Char("Name", required=True)
    test = fields.Char("test", required=True)

class PreProductionLabCritarea(ModelSQL,ModelView):
    "Lab Critearea"
    __name__ = "preproduction.lab.test.critearea"
    pre_production_lab_id = fields.Many2One('quality.control.preproduction' , 'Lab Test Id')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")
    gc1 = fields.Char("G.C.1")
    gc2 = fields.Char("G.C.2")
    gc3 = fields.Char("G.C.3")


    