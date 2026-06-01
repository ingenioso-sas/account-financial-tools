==========================
Account Tax Certificate
==========================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-ingenioso--sas%2Faccount--financial--tools-lightgray.png?logo=github
    :target: https://github.com/ingenioso-sas/account-financial-tools/tree/13.0/account_tax_certificate
    :alt: ingenioso-sas/account-financial-tools

|badge1| |badge2| |badge3|

Este módulo permite generar y descargar en PDF un **certificado de impuesto**
(retención en la fuente, ICA, IVA u otro) para un tercero determinado,
filtrando por impuesto y rango de fechas.

El certificado agrupa los movimientos contables confirmados (*posted*) en los
que el tercero fue sujeto a retención bajo el impuesto seleccionado, calcula
la base gravable y el valor retenido por concepto, y genera un documento PDF
con el formato oficial colombiano.

**Tabla de contenido**

.. contents::
   :local:

Instalación
===========

No requiere configuración adicional. Instale el módulo desde el menú
*Aplicaciones* buscando ``account_tax_certificate``.

Depende únicamente del módulo ``account`` incluido en Odoo.

Uso
===

Acceso al certificado
~~~~~~~~~~~~~~~~~~~~~

Vaya a **Contabilidad → Informes → Certificado de Impuesto**.

Se abrirá un formulario con los siguientes campos:

* **Tercero**: el partner al que se le practicó la retención.
* **Impuesto**: el impuesto de retención (ej. *RteFte Compras Declarantes 2.5%*).
* **Fecha Desde / Fecha Hasta**: rango del período fiscal a certificar.
* **Compañía**: visible solo en entornos multi-compañía.

Generación del PDF
~~~~~~~~~~~~~~~~~~

Haga clic en el botón **"Generar Certificado"**. El sistema:

1. Busca en los apuntes contables (*account.move.line*) las líneas de
   impuesto donde ``tax_line_id`` coincide con el impuesto seleccionado,
   para el tercero y período indicados, solo en asientos confirmados.
2. Para cada línea de impuesto, busca la línea base del mismo asiento
   (``tax_ids`` que incluye el impuesto) para calcular el valor base.
3. Agrupa los resultados por concepto (nombre del impuesto).
4. Genera el PDF con el certificado.

Estructura del certificado PDF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El PDF generado contiene:

* Encabezado con nombre, NIT y dirección de la compañía emisora.
* Título: ``CERTIFICADO DE <nombre del impuesto>``.
* Texto introductorio con el período, impuesto, nombre y NIT del tercero.
* Tabla de conceptos:

  +-----------------------------------------+--------------+----------------+
  | CONCEPTO                                | VALOR BASE   | VALOR RETENIDO |
  +=========================================+==============+================+
  | RteFte Compras Declarantes 2.5%         | 479.680,43   | 11.992,01      |
  +-----------------------------------------+--------------+----------------+
  | **TOTAL RETENIDO**                      |              | **11.992,01**  |
  +-----------------------------------------+--------------+----------------+

* Fecha de expedición y nota legal (decreto 836 de 1991).

Ejemplo de certificado
~~~~~~~~~~~~~~~~~~~~~~

El certificado generado sigue el formato estándar de retención en Colombia:

.. code-block:: text

    GRUPO ASESORIA EN SISTEMATIZACION DE DATOS S.A.S
    Nit. 860510031-7
    CALLE 32 No. 13 - 07 — Bogotá

    CERTIFICADO DE RTEFTE COMPRAS DECLARANTES 2.5%

    Para efectos fiscales pertinentes, certificamos que durante el período
    comprendido entre el 01/01/2025 y el 31/12/2025 practicamos retención
    de RteFte Compras Declarantes 2.5% a:

    ULCUE TRUJILLO JULIO CESAR con NIT: 76330147-6
    por los siguientes conceptos y valores:

    CONCEPTO                            VALOR BASE    VALOR RETENIDO
    RteFte Compras Declarantes 2.5%     479.680,43        11.992,01
    TOTAL RETENIDO                                        11.992,01

    Este certificado se expide a los 31 días del mes de DICIEMBRE de 2025
    en Bogotá, D.C., ciudad donde fue consignada la retención efectuada.

    Esta certificación se expide sin firma autógrafa de acuerdo con lo
    establecido en el artículo 10 del decreto 836 del 26 de marzo de 1991.

Notas técnicas
~~~~~~~~~~~~~~

* Solo se consideran asientos en estado **Confirmado** (``state = 'posted'``).
* Los impuestos deben estar configurados con ``tax_line_id`` en las líneas
  de impuesto y ``tax_ids`` en las líneas base (comportamiento estándar de
  Odoo al registrar facturas con retenciones).
* El campo **NIT / VAT** del tercero y de la compañía se toma del campo
  ``vat`` del modelo ``res.partner`` y ``res.company`` respectivamente.
* El idioma de la fecha depende del idioma configurado en el sistema.
```bash
  # Generar el locale español
  sudo locale-gen es_CO.UTF-8
  sudo update-locale
  # Luego en el archivo de configuración de Odoo (odoo.conf) o en la
  # variables de entorno al arrancar el proceso:
  LC_TIME=es_CO.UTF-8 LANG=es_ES.UTF-8 LANGUAGE=es_ES:es LC_ALL=es_ES.UTF-8 python odoo-bin ...
``` 


Changelog
=========

13.0.1.0.0
~~~~~~~~~~

* [ADD] Módulo inicial ``account_tax_certificate``.

Bug Tracker
===========

Los errores se reportan en el repositorio del proyecto. En caso de problemas,
verifique si el issue ya fue reportado antes de crear uno nuevo.

Créditos
========

Autores
~~~~~~~

* Ingenioso SAS

Colaboradores
~~~~~~~~~~~~~

* `Ingenioso SAS <https://www.ingenioso.com.co>`

Mantenedores
~~~~~~~~~~~~

Este módulo es mantenido por Ingenioso SAS.
