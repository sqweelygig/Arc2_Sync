# Arc2_Sync
A unified synchronisation engine to create a Object Orientated & Command Line approach to migration of various items between various endpoints.
The initial scope is intended to synchronise users & courses from Sims to AD & Google
prerequisites: Python 3.5
usage: python Arc2_Sync.py -sync <items> -from <sources> -to <destinations> -mode <enumerated, details to follow> <various endpoint specific settings>
Any amount of these arguments may be provided on the command line, or during run-time.