from datetime import datetime, timedelta
import time
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow
from dateutil.relativedelta import relativedelta  
  
class sale_order(osv.osv):
    _inherit="sale.order"
      
    def find_products(self, cr, uid, ids, context=None):
        """Create the required procurements to supply sales order lines, also connecting
        the procurements to appropriate stock moves in order to bring the goods to the
        sales order's requested location.
 
        :return: True
        """
        tuple=[]
        list_prod=[]
        procurement_obj = self.pool.get('procurement.order').browse(cr,uid,context=context)
        sale_line_obj = self.pool.get('sale.order.line')
        prod_browse_obj=self.pool.get('product.template').browse(cr,uid,ids,context=context)
        stock_browse_obj=self.pool.get('stock.location.route').browse(cr,uid,context=context)
        for order in self.browse(cr, uid, ids, context=context):
            proc_ids = []
 
            for line in order.order_line:
                if line.state == 'cancel':
                    continue
                if line.procurement_ids:
                    procurement_obj.check(cr, uid, [x.id for x in line.procurement_ids if x.state not in ['cancel', 'done']])
                    line.refresh()
                    except_proc_ids = [x.id for x in line.procurement_ids if x.state in ('exception', 'cancel')]
                    procurement_obj.reset_to_confirmed(cr, uid, except_proc_ids, context=context)
                    proc_ids += except_proc_ids
                elif line.product_id and line.product_id.type != 'service':
                    
                    print "product_id=======================",line.product_id
                    print "order line route_id=======================",line.route_id.name
                    print "routes---------------",prod_browse_obj.route_ids.route_id
                    print "stock_browse_obj--------------------",stock_browse_obj.id
                    print "procurement_obj----****",procurement_obj.product_id.route_ids
#                     res=prod_obj.search(cr,uid,[('product_id','=',line.product_id)],context=context)
                    
                    if prod_browse_obj.route_ids.name=='Buy' and prod_browse_obj.route_ids.name=='Make To Order' and line.route_id.name==False:
                        list_prod.append(line.product_id)
                         
                    if prod_browse_obj.route_ids.name=='Buy' and line.route_id.name=='Make To Order':
                         list_prod.append(line.product_id)

                    if prod_browse_obj.route_ids.name=='Buy' and line.route_id.name=='Drop Shipping':
                         list_prod.append(line.product_id)
                         
                    if prod_browse_obj.route_ids.name=='Make To Order' and line.route_id.name=='Drop Shipping':
                         list_prod.append(line.product_id)
                         
        print list_prod,"--------------list of products"
