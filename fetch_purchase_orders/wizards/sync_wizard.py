# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import ValidationError
import xmlrpc.client
import re


class SyncWizard(models.TransientModel):
    _name = "sync.wizard"
    _description = "Purchase Order Sync Wizard"

    # url_db1 = fields.Char('Database URL',required=True)
    # db1_name = fields.Char('Database Name',required=True)
    # user1_name = fields.Char('User Name',required=True)
    # password1 = fields.Char('Password',required=True)
    url_db1 = fields.Char('Database URL')
    db1_name = fields.Char('Database Name')
    user1_name = fields.Char('User Name')
    password1 = fields.Char('Password')

    url_db2 = fields.Char('Database URL')
    db2_name = fields.Char('Database Name')
    user2_name = fields.Char('User Name')
    password2 = fields.Char('Password')


    def action_purchase_order_sync(self):
        """Fetching details of two DBs from the wizard and importing"""
# Db1>>>>>>>>>>>>>>
        #url_db1 = self.url_db1
        #db_1 = self.db1_name
        #username_db_1 = self.user1_name
        #password_db_1 = self.password1
        url_db1 = 'http://localhost:8016/'
        db_1 = 'new_16'
        username_db_1 = 'demoodoo24@gmail.com'
        password_db_1 = '1234'

        common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
        models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
        try:
            version_db1 = common_1.version()
        except:
            raise ValidationError("Check Database URL in FROM details")

        version = version_db1['server_version']
        try:
            uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
        except:
            raise ValidationError("Check Your Database name")
        try:
# purchase orders from Db1
            db_1_leads = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order', 'search_read', [],
                                             {'domain': [('state', '=', 'purchase')]})
        except:
            raise ValidationError("Can't access user.Check Your Username or Password in FROM details")
# partners from Db1
        db_1_partners = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [],
                                            {'fields': ['id', 'name', 'email'], 'order': 'id ASC'}, )
# products from Db1
        db_1_products = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.template', 'search_read', [],
                                            {'fields': ['id', 'name', 'standard_price']})
# Db2>>>>>>>>>>>>>>>>>>
        #url_db2 = self.url_db2
        #db_2 = self.db2_name
        #username_db_2 = self.user2_name
        #password_db_2 = self.password2
        url_db2 = 'http://localhost:8017/'
        db_2 = 'oct'
        username_db_2 = 'admin'
        password_db_2 = '1234'

        common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
        models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
        try:
            version_db2 = common_2.version()
        except:
            raise ValidationError("Check Database URL in TO details")
        try:
            uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})
        except:
            raise ValidationError("Check Your Database name or url")
        try:
            db_2_leads = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'search_read', [],
                                         {'domain': [('state', '=', 'purchase')]})
        except:
            raise ValidationError("Can't access User.Check Your username or Password")
# creating partners in current db from old db
        for i in db_1_partners:
            db_2_partners = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search_read', [],
                                            {'domain': [('name', '=', i['name'])]})
            if not db_2_partners:
                new_partners = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create',
                                           [{
                                               'name': i['name'],
                                               'id': i['id'],
                                               'email': i['email']
                                           }]
                                           )
# creating products in current db from old db
        for i in db_1_products:
            db_2_products = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.template', 'search_read', [],
                                                {'domain': [('name', '=', i['name'])]})
            if not db_2_products:
                new_products = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.template', 'create',
                                           [{
                                               'name': i['name'],
                                               'id': i['id'],
                                               'standard_price': i['standard_price'],
                                           }]
                                           )
# Creating PO in current Db
        first_message = f"Nothing to import from odoo{version}"
        count = 0
        for i in db_1_leads:
            partner = self.env['res.partner'].search([('name', '=', i['partner_id'][1])])
            purchase_order = self.env['purchase.order'].sudo().search([('name','=',i['name'])]).id
            if not purchase_order:
                purchase_order = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'create',
                                         [{
                                             # 'id': i['id'],
                                             'name': i['name'],
                                             'partner_id': partner.id,
                                             'amount_total': i['amount_total'],
                                             # 'order_line': order_line[0],
                                             'state': i['state'],
                                             'date_approve': i['date_approve'],
                                             'date_planned': i['date_planned'],
                                             'currency_id': i['currency_id'][0]
                                         }]
                                         )
                order_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line', 'search_read', [],
                                         {'domain': [('order_id', '=', i['id'])]})
                for j in order_line:
                    prod_name= re.sub(r"\[.*?\]", "", j['product_id'][1])
                    product_name = prod_name.strip()
                    product_new = self.env['product.template'].search([('name','=',product_name)])
                    orders = self.env['purchase.order'].browse(purchase_order)
                    vals = {
                        'name': j['name'],
                        'product_id': product_new.id,
                        'order_id': int(orders.id),
                        'product_qty': j['product_qty'],
                        'price_unit': j['price_unit'],
                        'product_uom': j['product_uom'][0],
                        'display_type':j['display_type']
                    }
                    models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order.line', 'create',[vals])
                count += 1
                first_message = f"Successfully Imported {count} Purchase Orders from Odoo{version}"
# Rainbow man and re-directing to purchase order
        if first_message == f"Successfully Imported {count} Purchase Orders from Odoo{version}":
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': first_message,
                    'type': 'rainbow_man',
                },
                'name': _("Purchase Orders"),
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.order',
                'view_mode': 'tree,form',
                'view_type': 'tree',
                'target': 'main',
            }
        else:
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': first_message,
                    'type': 'rainbow_man',
                }
            }
