# tesla-powerwall-json-py
Python module to access local Tesla Powerwall JSON API
https://github.com/piersdd/tesla-powerwall-json-py

**NOTE**: Tesla offer no official API to their Powerwall & Gateway; therefore, this library may well stop working at any time without warning.

Written by Piers Dawson-Damer

# Description
Python interface to the local Tesla Powerwall Gateway API.
- Meter information: Battery, Grid, Load & Solar
- Battery state of charge
- Toggle the operation state from Charge to Discharge.
- Set reserve for backup/blackout event.

Principlly developed to interface with the excellent **Home Assistant** project https://developers.home-assistant.io/en and a time series database such as InfluxDB.

# Credits
Many thanks to:
Vince Loschiavo for documenting the API (https://github.com/vloschiavo/powerwall2)

Božo Stojković for his JSON-Python object code (https://stackoverflow.com/users/4936137/božo-stojković)





# License
[Apache-2.0](LICENSE). By providing a contribution, you agree the contribution is licensed under Apache-2.0.
This code is provided as-is with no warranty. Use at your own risk.