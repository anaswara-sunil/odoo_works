# -*- coding: utf-8 -*-
from gevent.util import print_run_info

from odoo import http
from odoo.http import request


class DynamicSnippets(http.Controller):
   """This class is for the getting values for dynamic event snippets"""

   @http.route('/latest_events', type='json', auth='public')
   def latest_events(self):
       """Function for getting the current website,and latest events.
           Return
                 events - latest events
                 current_website-the current website for checking events
       """

       events = request.env['manage.event'].search_read([],['name','event_poster','start_date','end_date'], order="start_date desc", limit=4)
       print(events,'events')
       return events

