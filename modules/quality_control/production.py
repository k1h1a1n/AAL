from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta

__all__ = ['QualityControlProduction','QualityShipmentIn','ProdShipment','TemperatureAnalysisRecord'        ]

class QualityControlProduction(ModelSQL, ModelView):
    "Quality Control Production"
    __name__ = 'production'
    party = fields.Many2One('party.party','Party')
    reactorno = fields.Char('Reactor No')
    reactorcapacity =  fields.Integer('Reactor Capacity')
    # details = fields.Text("Deviation Details")
    remarks = fields.Text("Remarks")
    inputqty = fields.Char("Input qty")
    water = fields.Char("Water")
    f1 = fields.Char("F-1")
    f2 = fields.Char("F-2")
    main = fields.Char("Main")
    aftermain = fields.Char("After Main")
    residue = fields.Char("Residue")
    loss = fields.Char("Loss")
    inwardno = fields.Many2Many('prod.shipment.relation',
        'prodid','shipid', 'Inward',domain=[
            ('state', '=', 'done'),
            ])

   

class QualityShipmentIn(ModelSQL,ModelView):
    "Quality Shipment In"
    __name__ = "stock.shipment.in"
    inwardid = fields.Many2One('production','Inward ID')
    prodstate = fields.Boolean("In Production")

class ProdShipment(ModelSQL):
    
    "Prod Shipment Relation"
    __name__ = "prod.shipment.relation"
    
    shipid = fields.Many2One('stock.shipment.in','Shipment ID')
    prodid = fields.Many2One('production','Production ID')

class TemperatureAnalysisRecord(ModelSQL,ModelView):
    "Temperature and Analysis Record"
    __name__ = "temp.analysis.record"
    temp_table = fields.Many2One('production' , 'Temperature Record')
    date = fields.Date("Date")
    time = fields.Char("Time")
    bottom = fields.Char("Bottom")
    mid1 = fields.Char("Mid-1")
    mid2 = fields.Char("Mid-2")
    top = fields.Char("Top")
    vaccum = fields.Char("Vaccum")
    feedrate = fields.Char("Feed Rate")
    reflux = fields.Char("Reflux")
    collection = fields.Char("Collection")
    sample = fields.Char("Sample")
    mc = fields.Char("M/C")
    ph = fields.Char("ph")
    density = fields.Char("Density")
    purity = fields.Char("Purity By GC")
    purity1 = fields.Char(" ")
    purity2 = fields.Char(" ")
    purity3 = fields.Char(" ")
    purity4 = fields.Char(" ")
    purity5 = fields.Char(" ")
    sign = fields.Char("Sign")

