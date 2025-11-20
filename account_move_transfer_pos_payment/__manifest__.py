# Copyright 2015-2017 See manifest
# Copyright 2018 Raf Ven <raf.ven@dynapps.be>
# Copyright 2019 Akretion France (http://www.akretion.com/)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "POS Payment Transfer",
    "version": "13.0.1.0.0",
    "category": "Accounting & Point of Sale",
    "summary": "Create account moves to transfer amounts from POS payments.",
    "author": "Ingenioso co",
    "website": "https://github.com/ingenioso-co/account-financial-tools",
    "license": "AGPL-3",
    "depends": ["account", "point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "view/res_config_settings_view.xml",
        "wizard/move_transfer_pos_payment_wizard_view.xml",
    ],
    "installable": True,
}
