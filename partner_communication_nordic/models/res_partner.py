##############################################################################
#
#    Copyright (C) 2022 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __manifest__.py
#
##############################################################################
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_salutation_sv_SE(self):
        self.ensure_one()
        return ""

    def _get_salutation_nb_NO(self):
        self.ensure_one()
        return ""

    def _get_salutation_da_DK(self):
        self.ensure_one()
        return ""
