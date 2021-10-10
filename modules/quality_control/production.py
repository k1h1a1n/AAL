from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.report import Report

__all__ = ['QualityControlProduction','QualityShipmentIn','ProdShipment','TemperatureAnalysisRecord'        ]


class ProductionReport(Report):
    __name__ = 'production.report'

    @classmethod
    def get_context(cls, production, data):
        pool = Pool()
        Production = pool.get('production')
        context = super(ProductionReport,cls).get_context(production,data)
        # employee_id = Transaction().context.get('employee')
        production = Production(data["id"])
        context['production'] = production
        inwards = ''
        # context['productname'] = production.product
        for i in production.inwardno:
            # print ("this is I" ,i.reference)
            inwards += i.reference + ", "
        context['inwards'] = inwards
        context['treatment_boolean'] = False
        for i in production.works:
            if i.operation.operation_type == "treatment":
                context['treatment_boolean'] = True
                context['treatment_equipment_no'] = i.equipment_no
                # context['from'] = i.cycles.from_
                # context['to'] = i.cycles.to
                # print ("this is I" ,i.cycles.to)
                context['initialPH'] = i.initial_ph
                context['finalPH'] = i.final_ph
                context['initialmoisture'] = i.initial_moisture
                context['finalmoisture'] = i.final_moisture
                context['phadjustment'] = i.qty_sulphuric
                context['stabilizer'] = i.qty_bht
                context['T_ip_qty'] = i.treatment_input_qty
                context['T_ip_qty_per'] = i.treatment_input_qty_percent
                context['T_io_qty'] = i.treatment_output_qty
                context['T_io_qty_per'] = i.treatment_output_qty_percent
                context['T_loss'] = i.treatment_loss
                context['T_loss_per'] = i.treatment_loss_percent
                context['T_lye'] = i.treatment_lye_collected
                context['T_lye_per'] = i.treatment_lye_collected_percent
        return context
        
class QualityControlProduction(ModelSQL, ModelView):
    "Quality Control Production"
    __name__ = 'production'
    party = fields.Many2One('party.party','Party')
    reactorno = fields.Char('Reactor No')
    reactorcapacity =  fields.Integer('Reactor Capacity')
    # details = fields.Text("Deviation Details")
    remarks = fields.Text("Remarks")
    # inputqty = fields.Char("Input qty")
    # water = fields.Char("Water")
    # f1 = fields.Char("F-1")
    # f2 = fields.Char("F-2")
    # main = fields.Char("Main")
    # aftermain = fields.Char("After Main")
    # residue = fields.Char("Residue")
    # loss = fields.Char("Loss")
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

