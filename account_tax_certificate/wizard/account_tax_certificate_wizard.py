# Copyright 2026 Ingenioso SAS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountTaxCertificateWizard(models.TransientModel):
    _name = "account.tax.certificate.wizard"
    _description = "Wizard para generar certificado de impuesto por tercero"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Tercero",
        required=True,
    )
    tax_id = fields.Many2one(
        comodel_name="account.tax",
        string="Impuesto",
        required=True,
        domain=[("type_tax_use", "in", ["purchase", "sale"])],
    )
    date_from = fields.Date(
        string="Fecha Desde",
        required=True,
    )
    date_to = fields.Date(
        string="Fecha Hasta",
        required=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compañía",
        required=True,
        default=lambda self: self.env.company,
    )

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise UserError(
                    _("La fecha de inicio no puede ser mayor a la fecha de fin.")
                )

    def _get_certificate_lines(self):
        """
        Busca en account.move.line las líneas de impuesto correspondientes al
        partner, impuesto y rango de fechas seleccionados.

        Retorna una lista de dicts con:
            - concept: nombre del impuesto (concepto)
            - base_amount: suma de las bases gravables
            - tax_amount: suma del impuesto retenido
        """
        self.ensure_one()
        MoveLine = self.env["account.move.line"]

        # Líneas que corresponden al impuesto seleccionado (tax_line_id)
        tax_lines = MoveLine.search(
            [
                ("partner_id", "=", self.partner_id.id),
                ("tax_line_id", "=", self.tax_id.id),
                ("date", ">=", self.date_from),
                ("date", "<=", self.date_to),
                ("move_id.state", "=", "posted"),
                ("company_id", "=", self.company_id.id),
            ]
        )

        if not tax_lines:
            raise UserError(
                _(
                    "No se encontraron movimientos para el tercero '%s', "
                    "impuesto '%s' y el rango de fechas seleccionado."
                )
                % (self.partner_id.name, self.tax_id.name)
            )

        # Agrupar por concepto (nombre del impuesto) y calcular base y retenido
        # La base gravable viene de las líneas base asociadas al mismo asiento
        concept_data = {}
        for tl in tax_lines:
            concept = self.tax_id.name
            tax_amount = abs(tl.balance)

            # Buscar las líneas base del mismo apunte contable que referencian
            # este impuesto
            base_lines = MoveLine.search(
                [
                    ("move_id", "=", tl.move_id.id),
                    ("tax_ids", "in", [self.tax_id.id]),
                    ("partner_id", "=", self.partner_id.id),
                ]
            )
            base_amount = sum(abs(bl.balance) for bl in base_lines)

            if concept not in concept_data:
                concept_data[concept] = {
                    "concept": concept,
                    "base_amount": 0.0,
                    "tax_amount": 0.0,
                }
            concept_data[concept]["base_amount"] += base_amount
            concept_data[concept]["tax_amount"] += tax_amount

        return list(concept_data.values())

    def action_print_certificate(self):
        """Lanza el reporte QWeb. El AbstractModel _get_report_values
        calculará las líneas y el total al momento de renderizar."""
        self.ensure_one()
        # Validación anticipada: si no hay movimientos lanza UserError
        self._get_certificate_lines()
        return self.env.ref(
            "account_tax_certificate.action_report_tax_certificate"
        ).report_action(self)
