# sdw2usdm

This step in the 360i process imports an existing LZZT study design sreadsheet into the Study Definitions Workbench
and then exports that study design as USDM 4.0 in JSON.

The [d4k Study Definitions Workbench](https://d4k-sdw.fly.dev/) (SDW) v0.30.0 software has been designed to work with 
the TransCelerate / CDISC Unified Study Definitions Model (USDM). It is currently under development. A user guide and
examples are available from the Help menu.

The `CDISC_Pilot_Study_USDM.xlsx` spreadsheet contains the LZZT, or CDISC Pilot, study design content.

The `usdm.json` is a USDM-based JSON file that contains the LZZT study design content as exported from the 
SDW application.