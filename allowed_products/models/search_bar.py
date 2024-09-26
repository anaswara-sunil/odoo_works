# -*- coding: utf-8 -*-
from odoo import models,fields, api
from odoo.http import request

class SearchBar(models.AbstractModel):
    _inherit = "website.searchable.mixin"

    @api.model
    def _search_fetch(self, search_detail, search, limit, order):
        """search bar inside website"""

        super()._search_fetch(search_detail, search, limit, order)

        fields = search_detail['search_fields']
        base_domain = search_detail['base_domain']
        domain = self._search_build_domain(base_domain, search, fields, search_detail.get('search_extra'))
        model = self.sudo() if search_detail.get('requires_sudo') else self
        # print(model,'product.template() model')
        count = model.search_count(domain)
        allowed_product_ids =  request.env.user.partner_id.allowed_product_ids

        allowed_category_ids =  request.env.user.partner_id.allowed_category_ids
        if allowed_product_ids:
            results = allowed_product_ids
        elif allowed_category_ids:
            results = allowed_category_ids.product_tmpl_ids
        else:
            results = model.search(
                domain,
                limit=limit,
                order=search_detail.get('order', order)
            )
        return results, count


