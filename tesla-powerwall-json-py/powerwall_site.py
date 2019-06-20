#!/usr/bin/env python
"""
Python class to interface with local Tesla Powerwall JSON API
https://github.com/piersdd/tesla-powerwall-json-py


Example:

import powerwall_site
gateway_host = '192.168.5.6'
password = 'ST17I0012345'
backup_reserve_percent = float("5.1")

tpw = powerwall_site.main('192.168.5.6', 'ST17I0012345')

"""

def main():
    gateway_host = 'powerwall.sb'
    password = 'ST17I0054321'
    backup_reserve_percent = float("5.1")

    ## Instantiate powerwall_site object
    tpw = powerwall_site(gateway_host, password)

    ## Query battery state of charge (SoC)
    stateofenergy = tpw.stateofenergy()

    ## Store battery SoC
    tpw.battery_soc = stateofenergy['percentage']

    ## Query meter aggregates
    meters_aggregates = tpw.meters_aggregates()

    ## Store meter aggregates
    #  Currently populated by site (grid), battery, load, and solar
    tpw.meters = meters(meters_aggregates)

    # ## Validate token
    # tpw.token = tpw.valid_token()

    # ## Set Battery to Charge (Backup)
    # real_mode = 'backup'
    # tpw.set_operation(real_mode, backup_reserve_percent)
    
    # ## Set Battery to Discharge (Self Consumption)
    # real_mode = 'self_consumption'
    # tpw.set_operation(real_mode, backup_reserve_percent)


    ## Some output
    print()
    print(tpw.meters.site.last_communication_time)
    print()
    print("battery_soc:           " + str(tpw.battery_soc))
    print()
    print("site.instant_power:    " + str(tpw.meters.site.instant_power))
    print("battery.instant_power: " + str(tpw.meters.battery.instant_power))
    print("load.instant_power:    " + str(tpw.meters.load.instant_power))
    print("solar.instant_power:   " + str(tpw.meters.solar.instant_power))
    print()
    print("site.energy_imported:  " + str(tpw.meters.site.energy_imported))
    print("site.energy_exported:  " + str(tpw.meters.site.energy_exported))
    print("solar.energy_exported: " + str(tpw.meters.solar.energy_exported))



import json
import requests
from requests.exceptions import HTTPError, Timeout

import urllib3
urllib3.disable_warnings() # For 'verify=False' SSL warning

class powerwall_site(object):
    """Tesla Powerwall Sitemaster

    Attributes:
        token: for access to Powerwall gateway.
        running: Boolean
		uptime: in seconds
		connected_to_tesla: Boolean
		gateway_host: fqdn or IP address of gateway
		password: derivative of serial number
        battery_soc: percentage charge in battery
        backup_reserve_percent: backup event reserve limit for discharge

    """

    def __init__(self, gateway_host, password):
        """Return a new Powerwall_site object."""
        self.token = 'ku8J3iPLKtTBOvOburYsXj-0GSCZhM6MrBgjCONZEPsZnkDT1d1D82F_hfbTdHqcjb_kzUC2FtyO5MggRtGU5A=='
        # self.running = False
        # self.uptime = 0
        # self.connected_to_tesla = False
        self.gateway_host = gateway_host
        self.password = password
        self.battery_soc = 0
        self.backup_reserve_percent = 13.14159265358979

        self.base_path = 'https://' + self.gateway_host

    ### Returns current valid token or new valid token
    def valid_token(self):
        auth_header = {'Authorization': 'Bearer ' + self.token}
        payload = json.dumps({ 'username' : 'installer', 'password' : self.password, "force_sm_off": True })

        # ## Debug
        # print("## Returns current valid token")
        # print("auth_header: " + str(auth_header))
        # print("payload: " + str(payload))

        endpoint = '/api/login/Basic'
        url = self.base_path + endpoint 

        status_endpoint = '/api/status'
        status_url = self.base_path + status_endpoint 

        ## Assess token validity [with /api/status]
        result = requests.get(status_url, headers=auth_header, verify=False, timeout=2)

        # Use the built-in JSON function to return parsed data
        dataobj = result.json()

        ## Token expired, Retrieve new token [with /api/login/Basic]
        if result.status_code == 401:
            result = requests.post(url, data=payload, verify=False, timeout=5)
            new_dataobj = result.json()

            ## Unable to retrieve new token (Unauthorised). Error with password perhaps
            if result.status_code == 401:
                print("401 /api/login/Basic - Login Error (perhaps)???")
                # Use the built-in JSON function to return parsed data
                print(json.dumps(new_dataobj,indent=4))
            
            elif result.status_code == 200:
                new_token = new_dataobj['token']

                ## Restart Powerwall sitemaster.
                auth_header = {'Authorization': 'Bearer ' + new_token}
                self.sitemaster_run(auth_header)

                return new_token
        else:
            return self.token # existing invalid token




    ## This starts the Powerwall(s) & Gateway (after getting an authentication token)
    def sitemaster_run(self, auth_header):
        endpoint = '/api/sitemaster/run'
        url = self.base_path + endpoint 

        try:
            result = requests.get(url, headers=auth_header, verify=False, timeout=5)

            # print('Response HTTP Status Code: {status_code}'.format(
            #     status_code=result.status_code))
            # print('Response HTTP Response Body: {content}'.format(
            #     content=result.content))
        except requests.exceptions.RequestException:
            print('HTTP Request failed')



    ## Reads aggregate meter information.
    def meters_aggregates(self):
        endpoint = '/api/meters/aggregates'
        url = self.base_path + endpoint 
        result = requests.get(url, verify=False, timeout=5)

        # ## Debug - Use the built-in JSON function to return parsed data
        # dataobj = result.json()
        # print("## meters_aggregates JSON")
        # print(print(json.dumps(dataobj,indent=4)))

        return result.json()




    ## Reads charge state in percent of the Powerwall.
    def stateofenergy(self):

        # When Sitemaster is not running, caught:
        # Error: 502 Server Error: Bad Gateway for url: https://powerwall.local/api/system_status/soe

        endpoint = '/api/system_status/soe'
        url = self.base_path + endpoint 

        try:
            result = requests.get(url, verify=False, timeout=5)

            # raise_for_status will throw an exception if an HTTP error
            # code was returned as part of the response
            result.raise_for_status()

            return result.json()

        except HTTPError as err:
            print("Error: {0}".format(err))
        except Timeout as err:
            print("Request timed out: {0}".format(err))




    ## Set Powerwall Operation to Charge (Backup) or Discharge (self_consumption)
    #  Pause PERHAPS WITH (self_consumption) w/ Current SoC as backup_reserve_percent
    def set_operation(self, real_mode, backup_reserve_percent):
        auth_header = {'Authorization': 'Bearer ' + self.token}
        payload = json.dumps({"real_mode": real_mode, "backup_reserve_percent": backup_reserve_percent})

        # # Debug
        # print("## Set Powerwall Operation")
        # print("auth_header: " + str(auth_header))
        # print("payload: " + str(payload))

        set_endpoint = '/api/operation'
        set_url = self.base_path + set_endpoint

        enable_operation_endpoint = '/api/config/completed'
        enable_operation_url = self.base_path + enable_operation_endpoint 

        try:
            result = requests.post(set_url, data=payload, headers=auth_header, verify=False, timeout=5)

            print('Response HTTP Status Code: {status_code}'.format(
                status_code=result.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=result.content))

            # Enable Powerwall operation (after set operation)
            try:
                result = requests.get(enable_operation_url, headers=auth_header, verify=False, timeout=5)

                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=result.status_code))
                print('Response HTTP Response Body: {content}'.format(
                    content=result.content))

            except HTTPError as err:
                print("Error: {0}".format(err))
            except Timeout as err:
                print("Request timed out: {0}".format(err))#

        except HTTPError as err:
            print("Error: {0}".format(err))
        except Timeout as err:
            print("Request timed out: {0}".format(err))#




## Meter class to store meter_aggregates JSON
# code -- Božo Stojković (https://stackoverflow.com/users/4936137/božo-stojković)
class meters(object):
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)
        self.convert_json(d)

    def convert_json(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = meters(value)
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

if __name__ == "__main__":
    main()