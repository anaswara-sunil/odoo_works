# -*- coding: utf-8 -*-
from odoo import models, fields, _
import openpyxl
import base64
from io import BytesIO
from odoo.exceptions import  ValidationError


class ImportFileWizard(models.TransientModel):
   _name = "import.file.wizard"
   _description = "Import File Wizard"

   file = fields.Binary(string="File", required=True)

   def action_import_file(self):
       try:
           wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file)), read_only=True)
           ws = wb.active
           new = []
           lot =[]
           first_message = second_message = third_message =""
           counts = 0
           for row in ws.iter_rows(min_row=3):
               name = row[0].value
               prod = row[2].value
               print(f"Name: {name}, product: {prod} , internal ref: {row[1].value}")
               if not name and not prod and not row[1].value:
                   continue
               if (not name or not prod) and row[1].value :
                   counts += 1
               if name and prod:
                   product = self.env['product.product'].search([('name', '=', prod)])
                   if not product:
                       new_product = self.env['product.product'].create({'name': prod,'default_code': row[1].value})
                       new.append(new_product.name)
                       self.env['stock.lot'].create({'name': name, 'product_id': new_product.id})
                       lot.append(name)
                   else:
                       search = self.env['stock.lot'].search([('name', '=',name),('product_id','=', product.id )])
                       if not search:
                           self.env['stock.lot'].create({ 'name': name, 'product_id': product.id })
                           lot.append(name)
           if lot:
               first_message = " Successfully Imported Lot/Serial numbers \n"
           if counts>0:
               second_message = f"{counts} lines were skipped due to insufficient details \n"
           if new:
               third_message = ("New products have been created during the import process: " + ""
                                " {} " ","* len(new)).format(*new)
           messages = first_message+second_message+third_message
           return {
               'effect': {
                   'fadeout': 'slow',
                   'message': messages,
                   'type': 'rainbow_man',
               }
           }
       except:
            raise ValidationError(_('Please insert a valid file'))







