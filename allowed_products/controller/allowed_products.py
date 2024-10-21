# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.http_routing.models.ir_http import slug
from werkzeug.exceptions import NotFound
from odoo.http import request
from odoo import http
from odoo.tools import lazy


class AllowedProducts(WebsiteSale):
   """Returns list of allowed products according to current user."""

   @http.route()
   def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
       """Show only the allowed products/categories in shop when the related user is logged in"""

       res = super().shop(self,category=None, search=search, min_price=min_price, max_price=max_price, ppg=ppg,**post)
       print('jhvhv')
       ppg = res.qcontext.get('ppg')
       ppr = res.qcontext.get('ppr')

       partner = request.env.user.partner_id

       website = request.env['website'].get_current_website()
       url = '/shop'

# when selecting a particular category from the website
       Category = request.env['product.public.category']
       if category:
           category = Category.search([('id', '=', int(category))], limit=1)
           if not category or not category.can_access_from_current_website():
               raise NotFound()
       else:
           category = Category
# When no allowed products or categories are specified inside the customer
       if not (partner.allowed_product_ids or partner.allowed_category_ids) :
       # when selecting a particular category from the website, the category will come along with the url
           if category:
               url = "/shop/category/%s" % slug(category)
               products = request.env['product.template'].sudo().search([('public_categ_ids', 'in', category.ids)])
               product_count = len(products)
               res.qcontext.update({
                   'products': products,
                   'category': category,
                   'bins': lazy(lambda: TableCompute().process(products, ppg, ppr)),
                   'ppg': ppg,
                   'ppr': ppr,
                   'pager': website.pager(url=url, total=product_count, page=page, step=ppg, scope=5, url_args=post)
               })

# When allowed products are specified inside the customer
       if partner.allowed_product_ids:
           products = partner.allowed_product_ids
           product_count = len(products)
           categs = products.public_categ_ids

       # when selecting a particular category from the website, the category will come along with the url
           if category:
               url = "/shop/category/%s" % slug(category)
               products = products.filtered(lambda c: c.public_categ_ids.id in category.ids)

           res.qcontext.update({
               'products': products,
               'category': category,
               'categories': categs,
               'bins': lazy(lambda: TableCompute().process(products, ppg, ppr)),
               'ppg': ppg,
               'ppr': ppr,
               'pager' : website.pager(url=url, total=product_count, page=page, step=ppg, scope=5, url_args=post)
           })

# When allowed categories are specified inside the customer
       if partner.allowed_category_ids:
           categs = request.env['product.public.category'].sudo().search(
               [('id', 'in', partner.allowed_category_ids.ids)])
           products = request.env['product.template'].sudo().search([('public_categ_ids', 'in', categs.ids)])
           product_count = len(products)

       # when selecting a particular category from the website, the category will come along with the url
           if category:
               url = "/shop/category/%s" % slug(category)
               products = request.env['product.template'].sudo().search([('public_categ_ids', 'in', category.ids)])

           res.qcontext.update({
               'products': products,
               'category': category,
               'categories': categs,
               # 'search_product': products,
               # 'search_count': len(products),
               'bins': lazy(lambda: TableCompute().process(products, ppg, ppr)),
               'ppg': ppg,
               'ppr': ppr,
               'pager': website.pager(url=url, total=product_count, page=page, step=ppg, scope=5, url_args=post)
           })

       return res
