# -*- coding: utf-8 -*-
from odoo.http import request, Controller, route
from dateutil.parser import parse


class EventController(Controller):
    @route('/event', type='http', auth='public', website=True)
    def event_list_view(self, **kwargs):
        """List view of events created from website"""
        events = request.env['manage.event'].sudo().search([('website_created', '=', True)])
        return request.render('school_management.event_list_template',  {'events': events})

    @route('/event/detail/<int:id>', type='http', auth='public', website=True)
    def event_details_template(self, id, **kwargs):
        """To show details of event in a particular row"""
        events = request.env['manage.event'].browse([id])
        return request.render('school_management.event_detail_template',{'event': events})

    @route('/event/register', type='http', auth='public', website=True)
    def event_registration_form(self,**kwargs):
        """Form for registering Events"""
        clubs = request.env['manage.club'].sudo().search([])
        return request.render('school_management.event_registration_template', { 'clubs': clubs, })

    @route('/event/submit', type='http', auth='public', methods=['POST'], website=True)
    def event_registration_submit(self, **post):
        """Submit action of event registration"""
        club_ids = request.httprequest.form.getlist('club_ids')
        # club_ids = request.httprequest.form.items('club_ids')
        # club_ids = request.httprequest.form.keys('club_ids')
        message = "Your Event registration has been received successfully"
        url = "/event"

        request.env['manage.event'].sudo().create({
            'name': post.get('event_name'),
            # 'image':post.get('event_img'),
            'start_date': parse(post.get('start_date'), parserinfo=None),
            'end_date': parse(post.get('end_date'), parserinfo=None),
            'club_ids':  [(6, 0, [int(c) for c in club_ids])],
            'website_created': True,
        })
        return request.render('school_management.thank_you_page',{'message': message, 'url': url})


    @route('/event/event_id', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def event_details(self, **kwargs):
        """jsonrpc for passing id along with url"""
        # print(kwargs['eventId'],'fun')
        events = request.env['manage.event'].sudo().search([('id', '=', kwargs['eventId'])])
        # print(events.id,'event_id')

        return {
            'event': events.id
        }

































