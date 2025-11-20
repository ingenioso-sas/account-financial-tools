# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    pos_payment_method_id = fields.Many2one(
        comodel_name="pos.payment.method",
        string="Default POS Payment Method for Transfer",
        help="Default payment method to be used for transfers.",
    )
    transfer_account_source_id = fields.Many2one(
        comodel_name="account.account",
        string="Source Account for Transfer",
        help="Default source account for transfers.",
    )
    transfer_account_destination_id = fields.Many2one(
        comodel_name="account.account",
        string="Destination Account for Transfer",
        help="Default destination account for transfers.",
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_payment_method_id = fields.Many2one(
        related="company_id.pos_payment_method_id",
        readonly=False,
    )
    transfer_account_source_id = fields.Many2one(
        related="company_id.transfer_account_source_id",
        readonly=False,
    )
    transfer_account_destination_id = fields.Many2one(
        related="company_id.transfer_account_destination_id",
        readonly=False,
    )

