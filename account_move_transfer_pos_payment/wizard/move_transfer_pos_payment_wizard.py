# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from collections import defaultdict

class MoveTransferPosPaymentWizard(models.TransientModel):
    _name = "move.transfer.pos.payment.wizard"
    _description = "POS Payment Transfer Wizard"

    transfer_account_source_id = fields.Many2one(
        comodel_name="account.account",
        string="Source Account",
        required=True,
    )
    transfer_account_destination_id = fields.Many2one(
        comodel_name="account.account",
        string="Destination Account",
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        company = self.env.company
        res.update({
            "transfer_account_source_id": company.transfer_account_source_id.id,
            "transfer_account_destination_id": company.transfer_account_destination_id.id,
        })
        return res

    def create_transfer(self):
        payment_ids = self.env.context.get("active_ids")
        payments = self.env["pos.payment"].browse(payment_ids)

        if not payments:
            raise UserError(_("No payments selected."))

        # Group payments by session, partner and date
        grouped_payments = defaultdict(lambda: self.env["pos.payment"])
        for payment in payments:
            key = (payment.session_id, payment.partner_id, payment.payment_date.date())
            grouped_payments[key] += payment

        move_vals_list = []
        for (session, partner, date), payments_group in grouped_payments.items():
            if not session:
                raise UserError(_("Payments must be associated with a POS session."))

            total_amount = sum(payments_group.mapped("amount"))
            if total_amount == 0:
                continue

            move_vals = self._prepare_move_vals(session, partner, date, total_amount)
            move_vals_list.append(move_vals)

        if not move_vals_list:
            raise UserError(_("No transfer to be made."))

        moves = self.env["account.move"].create(move_vals_list)
        moves.action_post()

        return {
            "name": _("Generated Journal Entries"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "domain": [("id", "in", moves.ids)],
        }

    def _prepare_move_vals(self, session, partner, date, amount):
        debit_line = (0, 0, {
            "name": session.name,
            "account_id": self.transfer_account_destination_id.id,
            "partner_id": partner.id,
            "debit": amount,
            "credit": 0,
        })
        credit_line = (0, 0, {
            "name": session.name,
            "account_id": self.transfer_account_source_id.id,
            "partner_id": partner.id,
            "debit": 0,
            "credit": amount,
        })
        return {
            "ref": session.name,
            "date": date,
            "journal_id": session.config_id.journal_id.id,
            "line_ids": [debit_line, credit_line],
        }
