#!/usr/bin/env python
"""
Python class to store local Tesla Powerwall JSON data in InfluxDB

Example:

import powerwall_site
from influxdb import InfluxDBClient

gateway_host = '192.168.5.6'
password = 'ST17I0012345'
backup_reserve_percent = float("5.1")

influxdb_host = 'hass.groupthink.asia'
influxdb_port=8086
influxdb_username='powerwall_site_py'
influxdb_password='cfFRGV2VgZpZKU36bz4hTpku'
influxdb_database='powerwall_site'


tpw_database = influxdb_site
hass_database = homeassistant

client = InfluxDBClient(influxdb_host, influxdb_port=8086, influxdb_username, influxdb_password, influxdb_database)

>>> client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

>>> client.create_database('example')

>>> client.write_points(json_body)

tpw = powerwall_site.main('192.168.5.6', 'ST17I0012345')

"""
import logging
import powerwall_site
from influxdb import InfluxDBClient


def main():
    gateway_host = 'powerwall.sb'
    # password = 'ST17I0054321'
    backup_reserve_percent = float("5.1")

    influxdb_host = 'influxdb.sb'
    influxdb_port=8086
    influxdb_username='powerwall_site_py'
    influxdb_password='cfFRGV2VgZpZKU36bz4hTpku'
    influxdb_database='powerwall_site_py'

    logging.basicConfig(filename='powerwall_site.log', level=logging.DEBUG)

    client = InfluxDBClient(influxdb_host, influxdb_port, influxdb_username, influxdb_password, influxdb_database)

    # ## Instantiate powerwall_site object
    # # tpw = powerwall_site(gateway_host, password)
    # tpw = powerwall_site(gateway_host)

    # ## Query battery state of charge (SoC)
    # stateofenergy = tpw.stateofenergy()

    # ## Query meter aggregates
    # meters_aggregates = tpw.meters_aggregates()

    # json_body = [ {'site': {'last_communication_time': '2019-06-22T08:31:33.087026875+10:00', 'instant_power': 16844.9599609375, 'instant_reactive_power': -62.21001052856445, 'instant_apparent_power': 16845.0748342356, 'frequency': 50, 'energy_exported': 2084986.307868993, 'energy_imported': 51111927.05953567, 'instant_average_voltage': 236.42333475748697, 'instant_total_current': 0, 'i_a_current': 0, 'i_b_current': 0, 'i_c_current': 0, 'timeout': 1500000000}, 'battery': {'last_communication_time': '2019-06-22T08:31:33.090072863+10:00', 'instant_power': -10, 'instant_reactive_power': 930, 'instant_apparent_power': 930.0537618869137, 'frequency': 50.078, 'energy_exported': 13504950, 'energy_imported': 15099330, 'instant_average_voltage': 233.0666666666667, 'instant_total_current': -0.6000000000000001, 'i_a_current': 0, 'i_b_current': 0, 'i_c_current': 0, 'timeout': 1500000000}, 'load': {'last_communication_time': '2019-06-22T08:31:33.087026875+10:00', 'instant_power': 17496.119606675657, 'instant_reactive_power': 846.716844619149, 'instant_apparent_power': 17516.59586523769, 'frequency': 50, 'energy_exported': 0, 'energy_imported': 65805288.22500001, 'instant_average_voltage': 236.42333475748697, 'instant_total_current': 74.0033534533401, 'i_a_current': 0, 'i_b_current': 0, 'i_c_current': 0, 'timeout': 1500000000}, 'solar': {'last_communication_time': '2019-06-22T08:31:33.088119204+10:00', 'instant_power': 62.80999994277954, 'instant_reactive_power': -5.179999470710754, 'instant_apparent_power': 63.02323767729273, 'frequency': 50, 'energy_exported': 18386800.73730396, 'energy_imported': 14073.263970627544, 'instant_average_voltage': 285.4966634114583, 'instant_total_current': 0, 'i_a_current': 0, 'i_b_current': 0, 'i_c_current': 0, 'timeout': 1500000000}} ]
    json_body = [
        {
            "measurement":"power_meters",
            "tags": { "meter": 'site' },
            'time': '2019-06-22T08:31:33.087026875+10:00',
            'fields': {
                'instant_power': 16844.9599609375,
                'instant_reactive_power': -62.21001052856445,
                'instant_apparent_power': 16845.0748342356,
                'frequency': 50,
                'energy_exported': 2084986.307868993,
                'energy_imported': 51111927.05953567,
                'instant_average_voltage': 236.42333475748697,
                'instant_total_current': 0,
                'i_a_current': 0,
                'i_b_current': 0,
                'i_c_current': 0,
                'timeout': 1500000000
            }
        },
        {
            "measurement":"power_meters",
            "tags": { "meter": 'battery' },
            'time': '2019-06-22T08:31:33.090072863+10:00',
            'fields': {
                'instant_power': -10,
                'instant_reactive_power': 930,
                'instant_apparent_power': 930.0537618869137,
                'frequency': 50.078,
                'energy_exported': 13504950,
                'energy_imported': 15099330,
                'instant_average_voltage': 233.0666666666667,
                'instant_total_current': -0.6000000000000001,
                'i_a_current': 0,
                'i_b_current': 0,
                'i_c_current': 0,
                'timeout': 1500000000
            }
        },
        {
            "measurement":"power_meters",
            "tags": { "meter": 'load' },
            'time': '2019-06-22T08:31:33.087026875+10:00',
            'fields': {
                'instant_power': 17496.119606675657,
                'instant_reactive_power': 846.716844619149,
                'instant_apparent_power': 17516.59586523769,
                'frequency': 50,
                'energy_exported': 0,
                'energy_imported': 65805288.22500001,
                'instant_average_voltage': 236.42333475748697,
                'instant_total_current': 74.0033534533401,
                'i_a_current': 0,
                'i_b_current': 0,
                'i_c_current': 0,
                'timeout': 1500000000
            }
        },
        {
            "measurement":"power_meters",
            "tags": { "meter": 'solar' },
            'time': '2019-06-22T08:31:33.088119204+10:00',
            'fields': {                
                'instant_power': 62.80999994277954,
                'instant_reactive_power': -5.179999470710754,
                'instant_apparent_power': 63.02323767729273,
                'frequency': 50,
                'energy_exported': 18386800.73730396,
                'energy_imported': 14073.263970627544,
                'instant_average_voltage': 285.4966634114583,
                'instant_total_current': 0,
                'i_a_current': 0,
                'i_b_current': 0,
                'i_c_current': 0,
                'timeout': 1500000000
            }
        }
    ]
    
    # [
    #     {
    #         "measurement": "cpu_load_short",
    #         "tags": {
    #             "host": "server01",
    #             "region": "us-west"
    #         },
    #         "time": "2009-11-10T23:00:00Z",
    #         "fields": {
    #             "value": 0.64
    #         }
    #     }
    # ]

    # json_body = [
    #     {"measurement":"UserLogins",
    #     "tags": {
    #         "Area": "North America",
    #         "Location": "New York City",
    #         "ClientIP": "192.168.0.256"
    #     },
    #     "fields":
    #     {
    #     "SessionDuration":1.2
    #     }       
    #     },
    #     {"measurement":"UserLogins",
    #       "tags": {
    #         "Area": "South America",
    #         "Location": "Lima",
    #         "ClientIP": "192.168.1.256"
    #     },
    #     "fields":
    #     {
    #     "SessionDuration":2.0
    #     }       
    #     }        
    #     ]

    client.write_points(json_body)

    result = client.query('select * from power_meters;')

    print("Result: {0}".format(result)) 


if __name__ == "__main__":
    main()