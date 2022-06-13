#! /usr/bin/env python
""" helloworld.py
This file contains models. 
""" 
from trytond.model import ModelSQL, ModelView, Workflow, fields
from trytond.transaction import Transaction
from trytond.pyson import Eval, Bool, If
from trytond.pool import Pool , PoolMeta
from trytond.exceptions import UserError, UserWarning
from trytond.report import Report

__all__ = ['QualityControlPreproduction','QualityControlPostproduction','PreProductionLabCritarea','DeviationTable']



class PostProductionReport(Report):
    __name__ = 'postproduction.report'

    @classmethod
    def get_context(cls , postproduction , data):
        pool = Pool()
        PostProduction = pool.get('quality.control.postproduction')
        context = super(PostProductionReport,cls).get_context(postproduction,data)
        postproduction = PostProduction(data["id"])
        context['postproduction'] = postproduction
        return context


class PreProductionReport(Report):
    __name__ = 'preproduction.report'

    @classmethod
    def get_context(cls , preproduction , data):
        pool = Pool()
        PreProduction = pool.get('quality.control.preproduction')
        context = super(PreProductionReport,cls).get_context(preproduction,data)
        preproduction = PreProduction(data["id"])
        context['preproduction'] = preproduction
        return context



# PRE PRODUCTION 

class QualityControlPreproduction(Workflow, ModelSQL, ModelView):
    "Quality Control Preproduction"
    __name__ = "quality.control.preproduction"
    shipment = fields.Many2One('stock.shipment.in', "Inward",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    moves = fields.Many2One('stock.move', "Moves",states={'readonly': Eval('state').in_(['approved', 'rejected'])},
            domain=[
                ('shipment', '=', ('stock.shipment.in', Eval('shipment', -1))),
                ('from_location.code','=','IN'),
                ('to_location.code','=','STO'),
                 ]
            )
    date = fields.Date("Date",states={'readonly': Eval('state').in_(['approved', 'rejected'])})

    # inward_no = fields.Char('Inward')

    drum = fields.Char("Drum",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    input_qty = fields.Integer("Quantity",required=True,states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    # party = fields.Many2One('party.party',"Party")
    # material = fields.Char('Material')
    # inwarddate = fields.Date('Inward Date')

    critearea = fields.One2Many('preproduction.lab.test.critearea',
        'pre_production_lab_id', 'Analysis Report',states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    critearea1 = fields.One2Many('preproduction.lab.test.critearea1',
        'pre_production_lab1_id', 'Analysis Report',states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    rejected = fields.One2Many('preproduction.rejected.analysis',
        'pre_production_rejected_id', 'GC Analysis',states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    colour = fields.Char("Colour",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    ph = fields.Char("ph",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    moisture = fields.Char("%Moisture",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    spgravity = fields.Char("Sp.Gravity",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    gcanalysis = fields.Char("%Acidty",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    gcgraphno = fields.Char("Preoxide Value ppm",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    remark = fields.Text("Remarks by R&D",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    # image = fields.Binary("Graph Upload",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    # graph = fields.Binary("Graph Upload")
    my_deviation_table = fields.One2Many('preproduction.deviation','deviation_table','Deviation Table',states={'readonly': Eval('state').in_(['approved', 'rejected'])})

    ph1 = fields.Char("ph",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    moisture1 = fields.Char("%Moisture",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    peroxide = fields.Char("Peroxide Value(ppm)",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    purity1 = fields.Char("Purity by GC",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    state = fields.Selection([
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ], 'State', readonly=True)

    
    
    # def get_moves(self, name):
    #     if self.shipment == None:
    #         return [1,2]
    #     else:
    #         pool = Pool()
    #         ShipmentIn = pool.get('stock.shipment.in')
    #         shipments = ShipmentIn.search([
    #             ('id', '=', self.shipment.id),
    #             ])
    #         return [1,2]


    @fields.depends('shipment','moves')
    def on_change_with_input_qty(self, name=None):

        try:
            pool = Pool()
            PRE_QC = pool.get('quality.control.preproduction')
            # ShipmentIn = pool.get('stock.shipment.in')
            # shipments = ShipmentIn.search([
            #         ('id', '=', shipment[0].shipment.id),
            #         ])
            pre_qc = PRE_QC.search([
                    ('shipment', '=', self.shipment),
                    ])
            if len(pre_qc) == 0:
                return self.moves.quantity
            else:
                index = len(pre_qc) - 1
                sum = 0
                for i in range(0,len(pre_qc)):
                    sum = sum + pre_qc[i].input_qty
                    

                v1 = int(self.moves.quantity)
                v2 = int(sum)
                qty = v1 - v2
                return int(qty)
        
        
        except:
            pass

        

        
        
        
        

    
    @classmethod
    def __setup__(cls):
        super(QualityControlPreproduction, cls).__setup__()
        cls._transitions |= set((
                ('draft', 'approved'),
                ('approved', 'draft'),
                ('draft', 'rejected'),
                ('rejected', 'draft'),
                    ))
        cls._buttons.update({
                'draft': {
                    'invisible': ~Eval('state').in_(['approved', 'rejected',
                            ]),
                    'depends': ['state'],
                    }, 
                'approve': {
                    'invisible': ~Eval('state').in_(['draft'
                            ]),
                    'depends': ['state'],
                    }, 
                'reject': {
                    'invisible': ~Eval('state').in_(['draft'
                            ]),
                    'depends': ['state'],
                    }
            }) 

    @staticmethod
    def default_state():
        return 'draft'
    

    @classmethod
    @ModelView.button
    @Workflow.transition('approved')
    def approve(self,shipment):
        sum = 0
        pool = Pool()
        PRE_QC = pool.get('quality.control.preproduction')
        ShipmentIn = pool.get('stock.shipment.in')
        shipments = ShipmentIn.search([
                ('id', '=', shipment[0].shipment.id),
                ])
        pre_qc = PRE_QC.search([
                ('shipment', '=', shipment[0].shipment),
                ])

       

        if len(pre_qc) <= 1:
            if shipment[0].input_qty > shipment[0].moves.quantity:
                raise UserError("Failed","Input Quantity Must not be greater than Move Quantity") 
        else:
            
            for i in pre_qc:
                print(str(sum)+" "+str(i.input_qty) )
                sum = sum + i.input_qty
                print(sum)
            
            if sum > shipment[0].moves.quantity:
                raise UserError("Failed","Sum of All pre production analysis must not be greater than Input Moves quantity ")

        
        # List = []
       
        # for i in pre_qc:
        #     print(i.state)
        #     List.append(i.state)
        # first_element = List[0]

        # if len(List) == 0:

        #     ShipmentIn.write(shipments, {'preproduction_state': 'pending'})
        
        # else:
        #     for word in range(len(List)-1):

        #         if first_element != List[word]:
        #             result = False
        #             print("All elements are not equal")
        #             ShipmentIn.write(shipments, {'preproduction_state': 'pending'})
        #             break
        #         else:
        #             result = True
        #         if result:
        #             print("All elements are equal")
        #             ShipmentIn.write(shipments, {'preproduction_state': 'approved'})


        
            
        
                    # print(shipments)

    @classmethod
    @ModelView.button
    @Workflow.transition('rejected')
    def reject(cls,shipment):


        pool = Pool()
        ShipmentIn = pool.get('stock.shipment.in')
        shipments = ShipmentIn.search([
                ('id', '=', shipment[0].shipment.id),
                ])
        ShipmentIn.write(shipments, {'preproduction_state': 'rejected'})

    @classmethod
    @ModelView.button
    @Workflow.transition('draft')
    def draft(cls,shipment):
        pool = Pool()
        ShipmentIn = pool.get('stock.shipment.in')
        shipments = ShipmentIn.search([
                ('id', '=', shipment[0].shipment.id),
                ])
        ShipmentIn.write(shipments, {'preproduction_state': 'pending'})
        


class PreProductionLabCritarea(ModelSQL,ModelView):
    "Lab Critearea"
    __name__ = "preproduction.lab.test.critearea"
    pre_production_lab_id = fields.Many2One('quality.control.preproduction' , 'Lab Test Id')
    parameters = fields.Many2One('standard.analysis' , 'Parameter')
    value = fields.Char("Value")


class PreProductionLabCritarea1(ModelSQL,ModelView):
    "Lab Critearea1"
    __name__ = "preproduction.lab.test.critearea1"
    pre_production_lab1_id = fields.Many2One('quality.control.preproduction' , 'Lab Test Id1')
    parameters = fields.Many2One('gc.analysis' , 'Parameter')
    value = fields.Char("Value")

class PreProductionRejectedAnalysis(ModelSQL,ModelView):
    "Rejected Analysis"
    __name__ = "preproduction.rejected.analysis"
    pre_production_rejected_id = fields.Many2One('quality.control.preproduction' , 'Rejected Id')
    parameters = fields.Many2One('gc.analysis' , 'Parameter')
    value = fields.Char("Value")

# class PreProductionCustomerSpecification(ModelSQL,ModelView):
#     "Customer Specification"
#     __name__ = "preproduction.customer.analysis"
#     pre_production_customer_id = fields.Many2One('quality.control.preproduction' , 'Customer Id')
#     parameter = fields.Char("Parameter")
#     value = fields.Char("Value")

# POST PRODUCTION

class QualityControlPostproduction(Workflow,ModelSQL, ModelView):
    "Quality Control Postproduction"
    __name__ = "quality.control.postproduction"
    production = fields.Many2One('production', "Production Batch",required=True,states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    effective_date = fields.Date("Date",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    analysis_reports = fields.One2Many('preproduction.lab.test.critearea',
        'pre_production_lab_id', 'Analysis Report',states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    analysis1 = fields.One2Many('postproduction.analysis1.report',
    'post_production_analysis1_id', 'Analysis Report',states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    # postgraph = fields.Binary("Graph Upload")
    rejecteds = fields.One2Many('preproduction.rejected.analysis',
        'pre_production_rejected_id', 'GC Analysis',states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    customer = fields.One2Many('postproduction.customer.analysis', 
        'post_production_customer_id' , 'Customer Specification',states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    colour = fields.Char("Colour",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    ph = fields.Char("ph",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    moisture = fields.Char("%Moisture",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    spgravity = fields.Char("Sp.Gravity",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    gcanalysis = fields.Char("%Acidty",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    gcgraphno = fields.Char("postoxide Value ppm",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    remark = fields.Text("Remarks by R&D",states={'readonly': Eval('state').in_(['approved', 'rejected'])})
    # postimage = fields.Binary("Graph Upload")
    state = fields.Selection([
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ], 'State', readonly=True)
    
    dispatch_state = fields.Selection([
            ('pending', 'Pending'),
            ('inprogress', 'In Progress'),
            ('done', 'Done'),
            ], 'Dispatch', readonly=True)
    
    @classmethod
    def __setup__(cls):
        super(QualityControlPostproduction, cls).__setup__()
        cls._transitions |= set((
                ('draft', 'approved'),
                ('approved', 'draft'),
                ('draft', 'rejected'),
                ('rejected', 'draft'),
                    ))


        cls._buttons.update({
                'draft': {
                    'invisible': ~Eval('state').in_(['approved', 'rejected',
                            ]),
                    'depends': ['state'],
                    }, 
                'approve': {
                    'invisible': ~Eval('state').in_(['draft'
                            ]),
                    'depends': ['state'],
                    }, 
                'reject': {
                    'invisible': ~Eval('state').in_(['draft'
                            ]),
                    'depends': ['state'],
                    }
            }) 

    @staticmethod
    def default_state():
        return 'draft'
    
    @staticmethod
    def default_dispatch_state():
        return 'pending'
    
    @classmethod
    @ModelView.button
    @Workflow.transition('approved')
    def approve(self,postproduction):
        pool = Pool()
        production_id = postproduction[0].production.id
        Production = pool.get('production')
        productions = Production.search([
                ('id', '=', production_id),
                ])
        Production.write(productions, {'postproduction_state': 'approved'})


    
    @classmethod
    @ModelView.button
    @Workflow.transition('rejected')
    def reject(self,postproduction):
        pool = Pool()
        production_id = postproduction[0].production.id
        Production = pool.get('production')
        productions = Production.search([
                ('id', '=', production_id),
                ])
        Production.write(productions, {'postproduction_state': 'rejected'})
    
    @classmethod
    @ModelView.button
    @Workflow.transition('draft')
    def draft(self,postproduction):
        pool = Pool()
        production_id = postproduction[0].production.id
        Production = pool.get('production')
        productions = Production.search([
                ('id', '=', production_id),
                ])
        Production.write(productions, {'postproduction_state': 'pending'})

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

class DeviationTable(ModelSQL,ModelView):
    "Deviation"
    __name__ = "preproduction.deviation"
    deviation_table = fields.Many2One('quality.control.preproduction','Deviation')
    parameter = fields.Char("Parameter")
    value = fields.Char("Value")

class StandardAnalysis(ModelSQL,ModelView):
     "Standard Analysis"
     __name__ = "standard.analysis"
     _rec_name = 'parameter'
     parameter = fields.Char("Parameter")


class GcAnalysis(ModelSQL,ModelView):
     "GC Analysis"
     __name__ = "gc.analysis"
     _rec_name = 'parameter'
     parameter = fields.Char("Parameter")