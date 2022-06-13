from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.report import Report

class InwardReport(Report):
    __name__ = 'inward.report'

    @classmethod
    def get_context(cls, inward, data):
        pool = Pool()
        Inward = pool.get('stock.shipment.in')
        PreProdAnalysis = pool.get('quality.control.preproduction')
        context = super(InwardReport,cls).get_context(inward,data)
        print("Inward")
        print(str(inward))
        print(str(data))
        # employee_id = Transaction().context.get('employee')
        
        inward = Inward(data["id"])
        # preproduction = PreProdAnalysis(data["inward"])
        context['inward'] = inward

        preproduction = PreProdAnalysis.search([
                    ('shipment', '=', inward.id),
                    ])
        context['preproduction'] = preproduction
        # print("PreProduction",str(preproduction))
        # standard_analylsis = []
        # for i in preproduction:
        #     print("critearea" , str(i.critearea))
        #     for j in i.critearea:
        #         standard_analylsis.append(j)
        # context['standard_analylsis'] = standard_analylsis
        # print("azfal",str(standard_analylsis.parameters.parameter) , str(standard_analylsis.value))

        
        # context['bulk'] = True
        # inwards = ''
        # context['productname'] = production.product
        # for i in production.inwardno:
        #     print ("this is I" ,i.reference)
        #     inwards += i.reference + ", "
        # context['inwards'] = inwards
        return context

class customerShipmentReport(Report):
    __name__ = 'customerShipment.report'

    @classmethod
    def get_context(cls, customerShipment, data):
        pool = Pool()
        CustomerShipment = pool.get('stock.shipment.out')
        context = super(customerShipmentReport,cls).get_context(customerShipment,data)
        customerShipment = CustomerShipment(data["id"])
        print("customerShipment")
        print(str(customerShipment))
        print(str(data))
        context['customerShipmentReport'] = customerShipment
        context['quantity'] = customerShipment.inventory_moves
        print("inventory moves")
        print(str(customerShipment.inventory_moves[0].quantity))
        return context
