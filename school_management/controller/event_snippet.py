# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class DynamicSnippets(http.Controller):
   """This class is for the getting values for dynamic event snippets"""

   @http.route('/latest_events/event_id', type='json', auth='public', methods=['POST'], website=True, csrf=False)
   def event_details(self, **kwargs):
       """jsonrpc for passing id along with url"""
       print(kwargs['eventId'],'fun')
       events = request.env['manage.event'].sudo().search([('id', '=', kwargs['eventId'])])
       print(events.id,'event_id')

       return {
           'event': events.id
       }

   @http.route('/latest_events', type='json', auth='public')
   def latest_events(self):
       """Function for getting the current website,and latest events.
           Return
                 events - latest events
                 current_website-the current website for checking events
       """

       events = request.env['manage.event'].search_read([],['name','event_poster','start_date','end_date'], order="start_date desc")
       # print(events,'events')

       return events

