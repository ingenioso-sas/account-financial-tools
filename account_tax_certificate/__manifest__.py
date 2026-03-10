# Copyright 2026 Ingenioso SAS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Tax Certificate",
    "version": "13.0.1.0.0",
    "category": "Accounting",
    "license": "AGPL-3",
    "summary": "Genera certificados de retención/impuesto por tercero, impuesto y rango de fechas. 12345678",
    "author": "Ingenioso SAS",
    "website": "https://github.com/OCA/account-financial-tools",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/wizard_view.xml",
        "report/report.xml",
        "report/report_tax_certificate.xml",
    ],
    "installable": True,
}
