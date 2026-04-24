# Renewable Energy Design Portfolio

A collection of engineering calculation tools and reference designs for
domestic renewable energy systems in the Irish market, developed to
demonstrate technical competence for design engineering roles.

**Author**: Nikhil Krishnan Karthikeyan Nair
**Background**: BEng Mechanical Engineering, MSc Business Analytics
**Location**: Cork, Ireland

## Contents

| Tool | Description | Standards |
|------|-------------|-----------|
| [Heat Loss Calculator](./heat-loss-calculator/) | Room-by-room domestic heat loss for heat pump sizing | I.S. EN 12831, TGD Part L, SEAI |
| [Solar PV Sizing](./solar-pv-sizing/) | PV system sizing with SEAI grant estimation | SEAI Solar Electricity Scheme |
| [Radiator Sizing](./radiator-sizing/) | Low-temperature emitter correction | EN 442 |
| [Sample Designs](./sample-designs/) | Reference drawings and schematics | — |

## Regulatory framework

All tools are aligned with the current Irish regulatory environment:

- **Technical Guidance Document Part L (2022)** – conservation of fuel and energy
- **SEAI Domestic Technical Standards and Specifications** – grant compliance
- **I.S. EN 12831** – energy performance of buildings, heating design load
- **EN 442** – radiators and convectors

## Running the tools

Each folder is self-contained:

    cd heat-loss-calculator
    py -m venv venv
    venv\Scripts\activate
    pip install pandas openpyxl
    py heat_loss.py

## About

Developed in preparation for roles in the Irish renewable energy sector.
Feedback and suggestions welcome.