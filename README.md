# Charge Point Simulator v1.6
This repository generates Charge Point data with the following specs:

* 10 Charge Points
* Simulates 6 months worth of randomised Transactions
* OCPP v1.6 Events
  * BootNotification
  * Heartbeats (every 5 minutes)
  * StartTransaction
  * MeterValues (every 5 minutes)
  * StopTransaction

## Issues
- [ ] Why are we getting the same id_tag for all transactions?