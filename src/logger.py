import secrets
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from UPower import *
from Epever import EpeverChargeController
from flatdict import FlatDict

token = secrets.token
org = secrets.org
url = secrets.url
bucket="SolarPi"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


write_api = client.write_api(write_options=SYNCHRONOUS)

up = UPower()
if (up.connect() < 0):
	print ("Could not connect to the UPower device")
	exit -2

ep = EpeverChargeController()


ep_flat = FlatDict({
			"Solar voltage": ep.get_solar_voltage(),
			"Solar current": ep.get_solar_current(),
			"Solar power": ep.get_solar_current(),
			"Solar power L": ep.get_solar_power_l(),
			"Solar power H": ep.get_solar_power_h(),
			"Load voltage": ep.get_load_voltage(),
			"Load current": ep.get_load_current(),
			"Load power": ep.get_load_power(),
			"Load power L": ep.get_load_power_l(),
			"Load power H": ep.get_load_power_h(),
			"Battery current L": ep.get_battery_current_l(),
			"Battery current H": ep.get_battery_current_h(),
			"Battery voltage": ep.get_battery_voltage(),
			"Battery state of charge": ep.get_battery_state_of_charge(),
			"Battery temperature": ep.get_battery_temperature(),
			"Remote battery temperature": ep.get_remote_battery_temperature(),
			"Controller temperature": ep.get_controller_temperature(),
			"Battery status": ep.get_battery_status(),
			"Charging equipment status": ep.get_charging_equipment_status(),
			"Discharging equipment status": ep.get_discharging_equipment_status(),
			"Day time": ep.is_day(),
			"Night time": ep.is_night(),
			"Maximum battery voltage today": ep.get_maximum_battery_voltage_today(),
			"Minimum battery voltage today": ep.get_minimum_battery_voltage_today(),
			"Device over temperature": ep.is_device_over_temperature(),
			"Rated charging current": ep.get_rated_charging_current(),
			"Rated load current": ep.get_rated_load_current(),
			"Battery real rated voltage": ep.get_battery_real_rated_voltage(),
			"Battery type": ep.get_battery_type(),
			"Battery capacity": ep.get_battery_capacity(),
			"Temperature compensation coefficient": ep.get_temperature_compensation_coefficient(),
			"Over voltage disconnect voltage": ep.get_over_voltage_disconnect_voltage(),
			"Charging limit voltage": ep.get_charging_limit_voltage(),
			"Over voltage reconnect voltage": ep.get_over_voltage_reconnect_voltage(),
			"Equalize charging voltage": ep.get_equalize_charging_voltage(),
			"Boost charging voltage": ep.get_boost_charging_voltage(),
			"Float charging voltage": ep.get_float_charging_voltage(),
			"Boost reconnect charging voltage": ep.get_boost_reconnect_charging_voltage(),
			"Low voltage reconnect voltage": ep.get_low_voltage_reconnect_voltage(),
			"Under voltage recover voltage": ep.get_under_voltage_recover_voltage(),
			"Under voltage warning voltage": ep.get_under_voltage_warning_voltage(),
			"Low voltage disconnect voltage": ep.get_low_voltage_disconnect_voltage(),
			"Discharging limit voltage": ep.get_discharging_limit_voltage(),
			"Battery rated voltage": ep.get_battery_rated_voltage(),
			"Default load on/off in manual mode": ep.get_default_load_on_off_in_manual_mode(),
			"Equalize duration": ep.get_equalize_duration(),
			"Boost duration": ep.get_boost_duration(),
			"Battery discharge": ep.get_battery_discharge(),
			"Battery charge": ep.get_battery_charge(),
			"Charging mode": ep.get_charging_mode(),
		})
   
body_solar = [
    {
        "measurement": "UPower",
        "fields": {
            "PVvolt": up.readReg(PVvolt),
            "PVamps": up.readReg(PVamps),
            "PVwatt": up.readReg(PVwattL),
            "PVkwh": up.readReg(PVkwhL),
            "PVtemp": up.readReg(PVtemp),
            "BAvolt": up.readReg(BAvolt),
            "BAamps": up.readReg(BAamps),
            "BAwatt": up.readReg(BAwattL),
            "BAah": up.readReg(BAah),
            "BAtemp": up.readReg(BAtemp),
            "ACvoltIN": up.readReg(ACvoltIN),
            "ACvolt": up.readReg(ACvolt),
            "ACamps": up.readReg(ACamps),
            "ACwatt": up.readReg(ACwattL),
            "ACtemp": up.readReg(ACtemp),
            "IVwattL": up.readReg(IVwattL),
            "IVwattH": up.readReg(IVwattH),
            "IVherz": up.readReg(IVherz),
            "IVvoltIN": up.readReg(IVvoltIN),
            "IVvolt": up.readReg(IVvolt),
            "IVamps": up.readReg(IVamps),
            "IVstat": up.getIV(),
            "ACstat": up.getAC()
        }
    },
	{
		"measurement": "EPever",
		"fields": ep_flat,
	}
]

print (body_solar)

write_api.write(bucket, org, body_solar)