# Arc2_Sync
A unified synchronisation engine to create a Object Orientated and Command Line approach to migration of various items between various endpoints.

The initial scope is intended to synchronise users and courses from Sims to AD and Google

## prerequisites:
* Python 3.5

## install:
1. Upgrade pip (python -m pip install --upgrade pip)
2. Get Google API (pip install --upgrade google-api-python-client)
3. Add custom field to SIMS

## usage:
* python Arc2_Sync.py -sync (items) -from (sources) -to (destinations) -mode (enumerated, details to follow) (various endpoint specific settings)
  * Any amount of these arguments may be provided on the command line, or during run-time.