# Copyright 2026 Ingenioso SAS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ReportTaxCertificate(models.AbstractModel):
    _name = "report.account_tax_certificate.report_tax_certificate"
    _description = "Reporte Certificado de Impuesto"

    def _get_report_values(self, docids, data=None):
        wizard = self.env["account.tax.certificate.wizard"].browse(docids)
        lines = wizard._get_certificate_lines()
        total_tax = sum(l["tax_amount"] for l in lines)
        return {
            "doc_ids": docids,
            "doc_model": "account.tax.certificate.wizard",
            "docs": wizard,
            "data_lines": lines,
            "total_tax": total_tax,
        }
