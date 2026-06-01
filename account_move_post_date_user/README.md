# Account Move Post Date User

This module tracks and displays the specific date, time, and user who posted a journal entry (Account Move) in Odoo.

## Features

- **Audit Trail**: Automatically records the user and timestamp when a journal entry is confirmed/posted.
- **Enhanced Visibility**: Adds two new fields to the Accounting and Miscellaneous tabs of the Journal Entry form:
  - **Last Posted on**: The exact date and time the entry was posted.
  - **Last Posted by**: The user who performed the posting action.
- **Traceability**: Useful for compliance and internal auditing to know exactly who validated a move.

## Installation

To install this module, you need to:

1. Clone the repository or download the module folder.
2. Add the path to your Odoo `addons_path`.
3. Update the app list in your Odoo instance.
4. Search for "Account Move Post Date User" and click install.

## Configuration

No additional configuration is required. Once installed, the fields will be automatically populated upon posting a journal entry.

## Usage

1. Go to **Accounting > Accounting > Journal Entries**.
2. Open a draft entry or create a new one.
3. Click **Post**.
4. Check the **Other Info** or **Accounting** tab to see the updated "Last Posted on" and "Last Posted by" fields.

## Technical Information

- **Inherits**: `account.move`
- **Dependencies**: `account`
- **Fields added**:
  - `last_post_date` (Datetime)
  - `last_post_uid` (Many2one to `res.users`)

## Credits

### Authors
* ForgeFlow S.L.
* Odoo Community Association (OCA)

### Contributors
* Jordi Masvidal <jordi.masvidal@forgeflow.com>
* Guillem Casassas <guillem.casassas@forgeflow.com>

### Maintainers
This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

For more information, please visit [https://odoo-community.org](https://odoo-community.org).
