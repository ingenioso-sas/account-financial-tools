====================
POS Payment Transfer
====================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1| |badge2|

The **POS Payment Transfer** module provides a streamlined interface to transfer amounts from Point of Sale (POS) payments to specific accounting accounts. It is designed to facilitate the reconciliation and transfer of funds collected via POS to distinct financial accounts (e.g., moving funds from a temporary POS clearing account to a main bank account or petty cash).

🤖 For AI and Developers (Technical Architecture)
=================================================

This section is dedicated to providing a quick technical context for AI assistants and developers working on this module:

* **Core Models**:
  * ``move.transfer.pos.payment.wizard`` (TransientModel): The main wizard handling the logic.
  * ``res.company`` / ``res.config.settings``: Extended to hold default accounts (``transfer_account_source_id`` and ``transfer_account_destination_id``).
* **Business Logic Flow**:
  1. The user selects multiple ``pos.payment`` records from a tree view and triggers the wizard via an Action.
  2. The wizard groups the selected payments using a composite key: ``(session_id, partner_id, payment_date.date())``.
  3. For each group with a total amount > 0, an ``account.move`` (Journal Entry) is created.
  4. The Journal Entry consists of:
     * **Debit Line**: Uses the wizard's Destination Account.
     * **Credit Line**: Uses the wizard's Source Account.
     * Both lines carry the partner and the session name as the reference.
  5. The created Journal Entries are automatically posted (``action_post()``).
* **Dependencies**: ``account``, ``point_of_sale``.

**Table of contents**

.. contents::
   :local:

Configuration
=============

To configure the default transfer accounts for your company:

1. Navigate to **Accounting > Configuration > Settings**.
2. Locate the **POS Payment Transfer** section.
3. Configure the **Source Account** (the default account to be credited).
4. Configure the **Destination Account** (the default account to be debited).
5. Save the configuration.

Usage
=====

To execute a payment transfer:

1. Navigate to your POS payments list (e.g., from a POS Session or via the POS orders menu).
2. Check the box next to the payments you wish to transfer.
3. Open the **Action** menu and select the wizard to transfer POS payments.
4. A wizard will appear, displaying the default Source and Destination accounts. You can override these for the current operation if necessary.
5. Click the button to create the transfer.
6. The system processes the payments, generates and posts the journal entries, and automatically redirects you to a view showing the newly created entries.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/ingenioso-co/account-financial-tools/issues>`_.
In case of trouble, please check there if your issue has already been reported.

Credits
=======

Authors
~~~~~~~

* Ingenioso co

Maintainers
~~~~~~~~~~~

This module is maintained by Ingenioso co.