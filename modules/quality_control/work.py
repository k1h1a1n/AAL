from trytond.model import ModelSQL, ModelView,fields, sequence_ordered
from trytond.pool import Pool, PoolMeta
class WorkType( metaclass=PoolMeta):

     __name__ = 'production.work'
     treatment_freeparameter = fields.One2Many('treatment.freeparameter',
        'free_parameter', 'Free Parameters')


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