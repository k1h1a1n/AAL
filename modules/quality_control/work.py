from trytond.model import ModelSQL, ModelView,fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import  Eval

class WorkType( metaclass=PoolMeta):

    __name__ = 'production.work'
    treatment_freeparameter = fields.One2Many('treatment.freeparameter',
        'free_parameter', 'Steps' ,
        states={
            'invisible': ~Eval('treatment_boolean', True),
            },
        depends=['treatment_boolean']
        )
    quantitytaken = fields.Char("Quantity taken for treatment" , 
        states={
            'invisible': ~Eval('treatment_boolean', True),
            },
        depends=['treatment_boolean']
        )
    initial_ph = fields.Char("Initial pH" ,
        states={
            'invisible': ~Eval('treatment_boolean', True),
            },
        depends=['treatment_boolean']
        )
    initial_moisture = fields.Char("Initial Moisture" ,
        states={
            'invisible': ~Eval('treatment_boolean', True),
            },
        depends=['treatment_boolean']
        )
    final_ph = fields.Char("Final pH" , 
        states={
            'invisible': ~Eval('treatment_boolean', True),
            },
        depends=['treatment_boolean']
        )
    final_moisture = fields.Char("Final Moisture" , 
        states={
            'invisible': ~Eval('treatment_boolean', True),
            },
        depends=['treatment_boolean']
        )
    treatment_boolean = fields.Boolean('Treatment')
    fd_boolean = fields.Boolean('Final Distillation')

    materialbalance = fields.One2Many('treatment.materialbalance',
        'material_balance', "Material Balance",
        states={
            'invisible': ~Eval('treatment_boolean', True),
            },
        depends=['treatment_boolean']
        )
    qty_sulphuric = fields.Char("Quantity of Sulfuric acid used for ph adjustment" ,
        states={
            'invisible': ~Eval('treatment_boolean', True),
            },
        depends=['treatment_boolean']
        )
    qty_bht = fields.Char("Quantity of B.H.T added as stabilizer",
        states={
            'invisible': ~Eval('treatment_boolean', True),
            },
        depends=['treatment_boolean']
        )
    distillation_input = fields.One2Many('finaldistillation.input',
        'input_details', "Input Details",
        states={
            'invisible': ~Eval('fd_boolean', True),
            },
        depends=['fd_boolean']
        )
    
    first = fields.Boolean("Ensure that instrument is cleaned properly",
        states={
            'invisible': ~Eval('fd_boolean', True),
            },
        depends=['fd_boolean']
        )
    second = fields.Boolean("Ensure cooling water circulation & appropriate level of water",
        states={
            'invisible': ~Eval('fd_boolean', True),
            },
        depends=['fd_boolean']
        )

    third = fields.Boolean("Ensure that house pipe is cleaned",
        states={
            'invisible': ~Eval('fd_boolean', True),
            },
        depends=['fd_boolean']
        )

    fourth = fields.Boolean("Ensure that drums for fraction , main & for residue are available",
        states={
            'invisible': ~Eval('fd_boolean', True),
            },
        depends=['fd_boolean']
        )

    fifth = fields.Boolean("Ensure that earthing connections are proper",
        states={
            'invisible': ~Eval('fd_boolean', True),
            },
        depends=['fd_boolean']
        )
    analysis = fields.One2Many('finaldistillation.analysis',
        'analysis_record', "Temperature & analysis Record",
        states={
            'invisible': ~Eval('fd_boolean', True),
            },
        depends=['fd_boolean']
        )

    @fields.depends('operation')
    def on_change_with_treatment_boolean(self, name=None):
        if (self.operation == None):
            return False
        else:
            if (self.operation.operation_type == 'treatment'):
                print('Success')
                return True
    @fields.depends('operation')
    def on_change_with_fd_boolean(self, name=None):
        if (self.operation == None):
            return False
        else:
            if (self.operation.operation_type == 'final_distilation'):
                print("final distillation")
                return True

class TreatmentFreeParameter(ModelSQL,ModelView):
    "Treatment Free Parameters"
    __name__ = "treatment.freeparameter"
    free_parameter = fields.Many2One('production.work' , 'Free Parameter Id')
    srno = fields.Char("Sr.No")
    rm_addition_details = fields.Char("RM addition details")
    lye_colected = fields.Char("Lye collected")
    m_c = fields.Char("%M/c")
    preoxide_value  = fields.Char("Preoxide value")
    sign = fields.Char("Sign")

class TreatmentMaterialBalance(ModelSQL,ModelView):
    "Treatment Material Balance"
    __name__ = "treatment.materialbalance"
    material_balance = fields.Many2One('production.work' , 'Material Balance Id')
    input_qty = fields.Char("Input qty")
    output_qty = fields.Char("Output qty")
    loss = fields.Char("Loss")
    lye_collected = fields.Char("Lye collected")
    
class FinalDistillationInput(ModelSQL,ModelView):
    "Final Distilaltion Input Details"
    __name__ = "finaldistillation.input"
    input_details = fields.Many2One('production.work' , 'Final Distillation Input Id')
    name = fields.Char("Name of material")
    unit = fields.Char("Unit")
    quantity = fields.Char("Qty taken for distillation")

class FinalDistillationAnalysis(ModelSQL,ModelView):
    "Temperature & analysis Record"
    __name__ = "finaldistillation.analysis"
    analysis_record = fields.Many2One('production.work' , 'Temperature & analysis Record Id')
    date = fields.Date("Date")
    time = fields.Char("Time")
    bottom = fields.Char("Bottom")
    mid_1 = fields.Char("Mid-1")
    mid_2 = fields.Char("Mid-2")
    top = fields.Char("Top")
    vacuum = fields.Char("Vacuum")
    feed_rate = fields.Char("Feed rate")
    reflux = fields.Char("Reflux")
    collection = fields.Char("Collection")
    sample = fields.Char("Sample")
    m_c = fields.Char("M/C")
    ph = fields.Char("Ph")
    density = fields.Char("Density")
    purity = fields.Char("Purity By GC")

