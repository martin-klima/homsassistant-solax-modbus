from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntityDescription,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)

from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_CURRENT_MILLIAMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_KILO_WATT_HOUR,
    FREQUENCY_HERTZ,
    PERCENTAGE,
    POWER_VOLT_AMPERE,
    POWER_WATT,
    TEMP_CELSIUS,
    TIME_HOURS,
)

DOMAIN = "solax_modbus"
DEFAULT_NAME = "SolaX"
DEFAULT_SCAN_INTERVAL = 2
DEFAULT_PORT = 502
CONF_READ_GEN2X1 = "read_gen2_x1"
CONF_READ_GEN3X1 = "read_gen3_x1"
CONF_READ_GEN3X3 = "read_gen3_x3"
CONF_READ_X1_EPS = "read_x1_eps"
CONF_READ_X3_EPS = "read_x3_eps"
CONF_SolaX_HUB = "solax_hub"
ATTR_MANUFACTURER = "SolaX Power"
DEFAULT_READ_GEN2X1 = False
DEFAULT_READ_GEN3X1 = False
DEFAULT_READ_GEN3X3 = False
DEFAULT_READ_X1_EPS = False
DEFAULT_READ_X3_EPS = False

NUMBER_TYPES = [
    ["Battery Minimum Capacity",
        "battery_minimum_capacity",
        0x20,
        "i",
        {
	        "min": 0,
            "max": 99,
            "step": 1,
            "unit": PERCENTAGE,
        },
        "battery_capacity_charge"
    ],
]
NUMBER_TYPES_G2 = [
	["Battery Charge",
	    "battery_charge",
	    0x24,
	    "f",
	    {
	        "min": 0,
            "max": 50,
            "step": 0.1,
            "unit": ELECTRIC_CURRENT_AMPERE,
        }
	],
    ["Battery Discharge",
        "battery_discharge",
        0x25,
        "f",
	    {
	        "min": 0,
            "max": 50,
            "step": 0.1,
            "unit": ELECTRIC_CURRENT_AMPERE,
        }
    ],
]
NUMBER_TYPES_G3 = [
	["Battery Charge",
	    "battery_charge",
	    0x24,
	    "f",
	    {
	        "min": 0,
            "max": 20,
            "step": 0.1,
            "unit": ELECTRIC_CURRENT_AMPERE,
        }
	],
    ["Battery Discharge",
        "battery_discharge",
        0x25,
        "f",
	    {
	        "min": 0,
            "max": 20,
            "step": 0.1,
            "unit": ELECTRIC_CURRENT_AMPERE,
        }
    ],
    ["ForceTime Period 1 Max Capacity",
        "forcetime_period_1_max_capacity",
        0xA4,
        "i",
	    {
	        "min": 5,
            "max": 100,
            "step": 1,
            "unit": PERCENTAGE,
        }
    ],
    ["ForceTime Period 2 Max Capacity",
        "forcetime_period_2_max_capacity",
        0xA5,
        "i",
	    {
	        "min": 5,
            "max": 100,
            "step": 1,
            "unit": PERCENTAGE,
        }
    ],
]
SELECT_TYPES = [
	["Run Mode Select",
	    "run_mode_select",
	    0x1F,
	    {
	        0: "Self Use Mode",
            1: "Force Time Use",
            2: "Back Up Mode",
            3: "Feedin Priority",
        }
	],
    ["Grid Charge Select",
        "grid_charge_select",
        0x40,
        {
            0: "Both Forbidden",
            1: "Period 1 Allowed",
            2: "Period 2 Allowed",
            3: "Both Allowed",
        }
    ],
    ["Battery Awaken",
        "battery_awaken",
        0x56,
        {
            0: "Disable",
            1: "Enable",
        }
    ],
]

@dataclass
class SolaXModbusSensorEntityDescription(SensorEntityDescription):
    """A class that describes SolaX Power Modbus sensor entities."""

SENSOR_TYPES: dict[str, list[SolaXModbusSensorEntityDescription]] = {  
    "allow_grid_charge": SolaXModbusSensorEntityDescription(
        name="Allow Grid Charge",
        key="allow_grid_charge",
    ),
    "battery_capacity_charge": SolaXModbusSensorEntityDescription(
    	name="Battery Capacity",
    	key="battery_capacity_charge",
    	native_unit_of_measurement=PERCENTAGE,
    	device_class=DEVICE_CLASS_BATTERY,
    ),
    "battery_charge_max_current": SolaXModbusSensorEntityDescription(
		name="Battery Charge Max Current",
		key="battery_charge_max_current",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
	),
	"battery_current_charge": SolaXModbusSensorEntityDescription(
		name="Battery Current Charge",
		key="battery_current_charge",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
    "battery_dicharge_cut_off_voltage": SolaXModbusSensorEntityDescription(
		name="Battery Discharge Cut Off Voltage",
		key="battery_discharge_cut_off_voltage",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
		entity_registry_enabled_default=False,
    ),
	"battery_discharge_max_current": SolaXModbusSensorEntityDescription(
		name="Battery Discharge Max Current",
		key="battery_discharge_max_current",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
	),
    "battery_input_energy_today": SolaXModbusSensorEntityDescription(
		name="Battery Input Energy Today",
		key="input_energy_charge_today",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    "battery_min_capacity": SolaXModbusSensorEntityDescription(
    	name="Battery Minimum Capacity",
    	key="battery_min_capacity",
    	native_unit_of_measurement=PERCENTAGE,
    ),
    "battery_output_energy_today": SolaXModbusSensorEntityDescription(
		name="Battery Output Energy Today",
		key="output_energy_charge_today",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    "battery_power_charge": SolaXModbusSensorEntityDescription(
    	name="Battery Power Charge",
    	key="battery_power_charge",
    	native_unit_of_measurement=POWER_WATT,
    	device_class=DEVICE_CLASS_POWER,
    	state_class=STATE_CLASS_MEASUREMENT,
    ),
    "battery_type": SolaXModbusSensorEntityDescription(
    	name="Battery Type",
    	key="battery_type",
    	entity_registry_enabled_default=False,
    ),
    "battery_temperature": SolaXModbusSensorEntityDescription(
    	name="Battery Temperature",
    	key="battery_temperature",
    	native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"battery_voltage_charge": SolaXModbusSensorEntityDescription(
		name="Battery Voltage Charge",
		key="battery_voltage_charge",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "battery_volt_fault_val": SolaXModbusSensorEntityDescription(
		name="Battery Volt Fault Val",
		key="battery_volt_fault_val",
		entity_registry_enabled_default=False,
	),
	"bms_charge_max_current": SolaXModbusSensorEntityDescription(
		name="BMS Charge Max Current",
		key="bms_charge_max_current",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
		entity_registry_enabled_default=False,
	),
    "bms_connect_state": SolaXModbusSensorEntityDescription(
    	name="BMS Connect State", 
    	key="bms_connect_state",
    ),
    "bms_discharge_max_current": SolaXModbusSensorEntityDescription(
		name="BMS Discharge Max Current",
		key="bms_discharge_max_current",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
		entity_registry_enabled_default=False,
	),
	"bus_volt": SolaXModbusSensorEntityDescription(
		name="Bus Volt",
		key="bus_volt",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        entity_registry_enabled_default=False,
    ),
    "charger_start_time_1": SolaXModbusSensorEntityDescription(
    	name="Start Time 1",
    	key="charger_start_time_1",
    ),
    "charger_end_time_1": SolaXModbusSensorEntityDescription(
    	name="End Time 1",
    	key="charger_end_time_1",
    ),
    "charger_start_time_2": SolaXModbusSensorEntityDescription(
    	name="Start Time 2",
    	key="charger_start_time_2",
    ),
    "charger_end_time_2": SolaXModbusSensorEntityDescription(
    	name="End Time 2",
    	key="charger_end_time_2",
    ),
    "charger_use_mode": SolaXModbusSensorEntityDescription(
    	name="Charger Use Mode",
    	key="charger_use_mode",
    ),
    "consumed_energy_total": SolaXModbusSensorEntityDescription(
		name="Consumed Energy Total",
		key="consumed_energy_total",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    "dc_fault_val": SolaXModbusSensorEntityDescription(
		name="DC Fault Val",
		key="dc_fault_val",
		entity_registry_enabled_default=False,
	),
    "energy_today": SolaXModbusSensorEntityDescription(
    	name="Today's Yield",
    	key="energy_today",
    	native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    "export_control_factory_limit": SolaXModbusSensorEntityDescription(
		name="Export Control Factory Limit",
		key="export_control_factory_limit",
		native_unit_of_measurement=POWER_WATT,
		entity_registry_enabled_default=False,
    ),
	"export_control_user_limit": SolaXModbusSensorEntityDescription(
		name="Export Control User Limit",
		key="export_control_user_limit",
		native_unit_of_measurement=POWER_WATT,
		entity_registry_enabled_default=False,
    ),
    "feedin_power": SolaXModbusSensorEntityDescription(
    	name="Measured Power",
    	key="feedin_power",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "firmwareversion_invertermaster": SolaXModbusSensorEntityDescription(
		name="Firmware Version Inverter Master",
		key="firmwareversion_invertermaster",
		entity_registry_enabled_default=False,
	),
	"firmwareversion_manager": SolaXModbusSensorEntityDescription(
		name="Firmware Version Manager",
		key="firmwareversion_manager",
		entity_registry_enabled_default=False,
	),
	"firmwareversion_modbustcp_major": SolaXModbusSensorEntityDescription(
		name="Firmware Version Modbus TCP Major",
		key="firmwareversion_modbustcp_major",
		entity_registry_enabled_default=False,
	),
	"firmwareversion_modbustcp_minor": SolaXModbusSensorEntityDescription(
		name="Firmware Version Modbus TCP Minor",
		key="firmwareversion_modbustcp_minor",
		entity_registry_enabled_default=False,
	),
    "grid_frequency": SolaXModbusSensorEntityDescription(
    	name="Inverter Frequency",
    	key="grid_frequency",
    	native_unit_of_measurement=FREQUENCY_HERTZ,
    ),
    "grid_import": SolaXModbusSensorEntityDescription(
    	name="Grid Import",
    	key="grid_import",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "grid_export": SolaXModbusSensorEntityDescription(
    	name="Grid Export",
    	key="grid_export",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "house_load": SolaXModbusSensorEntityDescription(
    	name="House Load",
    	key="house_load",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),    
    "inverter_voltage": SolaXModbusSensorEntityDescription(
    	name="Inverter Voltage",
    	key="inverter_voltage",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "inverter_current": SolaXModbusSensorEntityDescription(
    	name="Inverter Current",
    	key="inverter_current",
    	native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
    "inverter_load": SolaXModbusSensorEntityDescription(
    	name="Inverter Power",
    	key="inverter_load",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "inverter_temperature": SolaXModbusSensorEntityDescription(
    	name="Inverter Temperature",
    	key="inverter_temperature",
    	native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "language": SolaXModbusSensorEntityDescription(
		name="Language",
		key="language",
		entity_registry_enabled_default=False,
	),
	"lock_state": SolaXModbusSensorEntityDescription(
		name="Lock State",
		key="lock_state",
		entity_registry_enabled_default=False,
	),
	"myaddress": SolaXModbusSensorEntityDescription(
		name="My address",
		key="myaddress",
		entity_registry_enabled_default=False,
	),
	"modulename": SolaXModbusSensorEntityDescription(
		name="Module Name",
		key="modulename",
		entity_registry_enabled_default=False,
	),
	"normal_runtime": SolaXModbusSensorEntityDescription(
		name="Normal Runtime",
		key="normal_runtime",
		native_unit_of_measurement=TIME_HOURS,
		entity_registry_enabled_default=False,
	),
	"overload_fault_val": SolaXModbusSensorEntityDescription(
		name="Overload Fault Val",
		key="overload_fault_val",
		entity_registry_enabled_default=False,
	),
    "pv_current_1": SolaXModbusSensorEntityDescription(
    	name="PV Current 1",
    	key="pv_current_1",
    	native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
    "pv_current_2": SolaXModbusSensorEntityDescription(
    	name="PV Current 2",
    	key="pv_current_2",
    	native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
    "pv_power_1": SolaXModbusSensorEntityDescription(
    	name="PV Power 1",
    	key="pv_power_1",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "pv_power_2": SolaXModbusSensorEntityDescription(
    	name="PV Power 2",
    	key="pv_power_2",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "pv_voltage_1": SolaXModbusSensorEntityDescription(
    	name="PV Voltage 1",
    	key="pv_voltage_1",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "pv_voltage_2": SolaXModbusSensorEntityDescription(
    	name="PV Voltage 2",
    	key="pv_voltage_2",
    	native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "pv_total_power": SolaXModbusSensorEntityDescription(
    	name="PV Total Power",
    	key="pv_total_power",
    	native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "registration_code": SolaXModbusSensorEntityDescription(
		name="Registration Code",
		key="registration_code",
		entity_registry_enabled_default=False,
	),
	"rtc": SolaXModbusSensorEntityDescription(
		name="RTC",
		key="rtc",
		entity_registry_enabled_default=False,
	),
    "run_mode": SolaXModbusSensorEntityDescription(
    	name="Run Mode",
    	key="run_mode",
    ),
    "seriesnumber": SolaXModbusSensorEntityDescription(
		name="Series Number",
		key="seriesnumber",
		entity_registry_enabled_default=False,
	),
    "solar_energy_today": SolaXModbusSensorEntityDescription(
    	name="Today's Solar Energy",
    	key="solar_energy_today",
    	native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    "solar_energy_total": SolaXModbusSensorEntityDescription(
    	name="Total Solar Energy",
    	key="solar_energy_total",
    	native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
    "time_count_down": SolaXModbusSensorEntityDescription(
		name="Time Count Down",
		key="time_count_down",
		entity_registry_enabled_default=False,
	),
	"total_energy_to_grid": SolaXModbusSensorEntityDescription(
		name="Total Energy To Grid",
		key="total_energy_to_grid",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        entity_registry_enabled_default=False,
    ),
}

GEN3_X1_SENSOR_TYPES: dict[str, list[SolaXModbusSensorEntityDescription]] = {
	"backup_charge_end": SolaXModbusSensorEntityDescription(
		name="Backup Charge End",
		key="backup_charge_end",
	),
	"backup_charge_start": SolaXModbusSensorEntityDescription(
		name="Backup Charge Start",
		key="backup_charge_start",
	),
	"backup_gridcharge": SolaXModbusSensorEntityDescription(
		name="Backup Gridcharge",
		key="backup_gridcharge",
	),
	"cloud_control": SolaXModbusSensorEntityDescription(
		name="Cloud Control",
		key="cloud_control",
		entity_registry_enabled_default=False,
	),
	"ct_meter_setting": SolaXModbusSensorEntityDescription(
		name="CT Meter Setting",
		key="ct_meter_setting",
		entity_registry_enabled_default=False,
	),
	"disch_cut_off_capacity_grid_mode": SolaXModbusSensorEntityDescription(
		name="Discharge Cut Off Capacity Grid Mode",
		key="disch_cut_off_capacity_grid_mode",
		native_unit_of_measurement=PERCENTAGE,
		entity_registry_enabled_default=False,
	),
	"disch_cut_off_point_different": SolaXModbusSensorEntityDescription(
		name="Discharge Cut Off Point Different",
		key="disch_cut_off_point_different",
		entity_registry_enabled_default=False,
	),
	"disch_cut_off_voltage_grid_mode": SolaXModbusSensorEntityDescription(
		name="Discharge Cut Off Voltage Grid Mode",
		key="disch_cut_off_voltage_grid_mode",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
		entity_registry_enabled_default=False,
	),
	"export_energy_today": SolaXModbusSensorEntityDescription(
		name="Today's Export Energy",
		key="export_energy_today",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    "forcetime_period_1_max_capacity": SolaXModbusSensorEntityDescription(
    	name="Forcetime Period 1 Maximum Capacity",
    	key="forcetime_period_1_max_capacity",
    	native_unit_of_measurement=PERCENTAGE,
    ),
    "forcetime_period_2_max_capacity": SolaXModbusSensorEntityDescription(
    	name="Forcetime Period 2 Maximum Capacity",
    	key="forcetime_period_2_max_capacity",
    	native_unit_of_measurement=PERCENTAGE,
    ),
    "global_mppt_function": SolaXModbusSensorEntityDescription(
		name="Global MPPT Function",
		key="global_mppt_function",
		entity_registry_enabled_default=False,
	),
	"import_energy_today": SolaXModbusSensorEntityDescription(
		name="Today's Import Energy",
		key="import_energy_today",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    "machine_style": SolaXModbusSensorEntityDescription(
		name="Machine Style",
		key="machine_style",
		entity_registry_enabled_default=False,
	),
	"meter_1_id": SolaXModbusSensorEntityDescription(
		name="Meter 1 id",
		key="meter_1_id",
		entity_registry_enabled_default=False,
	),
	"meter_2_id": SolaXModbusSensorEntityDescription(
		name="Meter 2 id",
		key="meter_2_id",
		entity_registry_enabled_default=False,
	),
	"meter_function": SolaXModbusSensorEntityDescription(
		name="Meter Function",
		key="meter_function",
		entity_registry_enabled_default=False,
	),
	"power_control_timeout": SolaXModbusSensorEntityDescription(
		name="Power Control Timeout",
		key="power_control_timeout",
		entity_registry_enabled_default=False,
	),
    "was4777_power_manager": SolaXModbusSensorEntityDescription(
		name="wAS4777 Power Manager",
		key="was4777_power_manager",
		entity_registry_enabled_default=False,
	),
}
X1_EPS_SENSOR_TYPES: dict[str, list[SolaXModbusSensorEntityDescription]] = {
	"eps_auto_restart": SolaXModbusSensorEntityDescription(
		name="EPS Auto Restart",
		key="eps_auto_restart",
	),
	"eps_current": SolaXModbusSensorEntityDescription(
		name="EPS Current",
		key="eps_current",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
	"eps_frequency": SolaXModbusSensorEntityDescription(
		name="EPS Frequency",
		key="eps_frequency",
		native_unit_of_measurement=FREQUENCY_HERTZ,
	),
	"eps_min_esc_soc": SolaXModbusSensorEntityDescription(
		name="EPS Min Esc SOC",
		key="eps_min_esc_soc",
		native_unit_of_measurement=PERCENTAGE,
    ),
	"eps_min_esc_voltage": SolaXModbusSensorEntityDescription(
		name="EPS Min Esc Voltage",
		key="eps_min_esc_voltage",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
    ),
	"eps_mute": SolaXModbusSensorEntityDescription(
		name="EPS Mute",
		key="eps_mute",
	),
	"eps_power": SolaXModbusSensorEntityDescription(
		name="EPS Power",
		key="eps_power",
		native_unit_of_measurement=POWER_VOLT_AMPERE
	),
	"eps_set_frequency": SolaXModbusSensorEntityDescription(
		name="EPS Set Frequency",
		key="eps_set_frequency",
		native_unit_of_measurement=FREQUENCY_HERTZ,
    ),
	"eps_voltage": SolaXModbusSensorEntityDescription(
		name="EPS Voltage",
		key="eps_voltage",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
}
X3_EPS_SENSOR_TYPES: dict[str, list[SolaXModbusSensorEntityDescription]] = {
	"eps_auto_restart": SolaXModbusSensorEntityDescription(
		name="EPS Auto Restart",
		key="eps_auto_restart",
	),
	"eps_current_r": SolaXModbusSensorEntityDescription(
		name="EPS Current R",
		key="eps_current_r",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
	"eps_current_s": SolaXModbusSensorEntityDescription(
		name="EPS Current S",
		key="eps_current_s",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
	"eps_current_t": SolaXModbusSensorEntityDescription(
		name="EPS Current T",
		key="eps_current_t",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
    "eps_min_esc_soc": SolaXModbusSensorEntityDescription(
		name="EPS Min Esc SOC",
		key="eps_min_esc_soc",
		native_unit_of_measurement=PERCENTAGE,
    ),
	"eps_min_esc_voltage": SolaXModbusSensorEntityDescription(
		name="EPS Min Esc Voltage",
		key="eps_min_esc_voltage",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
    ),
	"eps_mode_runtime": SolaXModbusSensorEntityDescription(
		name="EPS Mode Runtime",
		key="eps_mode_runtime",
	),
	"eps_mute": SolaXModbusSensorEntityDescription(
		name="EPS Mute",
		key="eps_mute",
	),	
	"eps_power_r": SolaXModbusSensorEntityDescription(
		name="EPS Power R",
		key="eps_power_r",
		native_unit_of_measurement=POWER_VOLT_AMPERE,
    ),
	"eps_power_s": SolaXModbusSensorEntityDescription(
		name="EPS Power S",
		key="eps_power_s",
		native_unit_of_measurement=POWER_VOLT_AMPERE,
    ),
	"eps_power_t": SolaXModbusSensorEntityDescription(
		name="EPS Power T",
		key="eps_power_t",
		native_unit_of_measurement=POWER_VOLT_AMPERE,
    ),
	"eps_power_active_r": SolaXModbusSensorEntityDescription(
		name="EPS Power Active R",
		key="eps_power_active_r",
		native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"eps_power_active_s": SolaXModbusSensorEntityDescription(
		name="EPS Power Active S",
		key="eps_power_active_s",
		native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"eps_power_active_t": SolaXModbusSensorEntityDescription(
		name="EPS Power Active T",
		key="eps_power_active_t",
		native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "eps_set_frequency": SolaXModbusSensorEntityDescription(
		name="EPS Set Frequency",
		key="eps_set_frequency",
		native_unit_of_measurement=FREQUENCY_HERTZ,
    ),
	"eps_voltage_r": SolaXModbusSensorEntityDescription(
		name="EPS Voltage R",
		key="eps_voltage_r",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
	"eps_voltage_s": SolaXModbusSensorEntityDescription(
		name="EPS Voltage S",
		key="eps_voltage_s",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
	"eps_voltage_t": SolaXModbusSensorEntityDescription(
		name="EPS Voltage T",
		key="eps_voltage_t",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
}
GEN3_X3_SENSOR_TYPES: dict[str, list[SolaXModbusSensorEntityDescription]] = {
	"earth_detect_x3": SolaXModbusSensorEntityDescription(
		name="Earth Detect X3",
		key="earth_detect_x3",
	),
	"export_energy_today": SolaXModbusSensorEntityDescription(
		name="Today's Export Energy",
		key="export_energy_today",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    "feedin_energy_total": SolaXModbusSensorEntityDescription(
		name="Feedin Energy Total",
		key="feedin_energy_total",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
	"feedin_power_r": SolaXModbusSensorEntityDescription(
		name="Measured Power R",
		key="feedin_power_r",
		native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"feedin_power_s": SolaXModbusSensorEntityDescription(
		name="Measured Power S",
		key="feedin_power_s",
		native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"feedin_power_t": SolaXModbusSensorEntityDescription(
		name="Measured Power T",
		key="feedin_power_t",
		native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"grid_current_r": SolaXModbusSensorEntityDescription(
		name="Inverter Current R",
		key="grid_current_r",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
	"grid_current_s": SolaXModbusSensorEntityDescription(
		name="Inverter Current S",
		key="grid_current_s",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
	"grid_current_t": SolaXModbusSensorEntityDescription(
		name="Inverter Current T",
		key="grid_current_t",
		native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
    ),
	"grid_mode_runtime": SolaXModbusSensorEntityDescription(
		name="Grid Mode Runtime",
		key="grid_mode_runtime",
		native_unit_of_measurement=TIME_HOURS,
	),
	"grid_power_r": SolaXModbusSensorEntityDescription(
		name="Inverter Power R",
		key="grid_power_r",
		native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"grid_power_s": SolaXModbusSensorEntityDescription(
		name="Inverter Power S",
		key="grid_power_s",
		native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
	"grid_power_t": SolaXModbusSensorEntityDescription(
		name="Inverter Power T",
		key="grid_power_t",
		native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "grid_service_x3": SolaXModbusSensorEntityDescription(
		name="Grid Service X3",
		key="grid_service_x3",
	),
	"grid_voltage_r": SolaXModbusSensorEntityDescription(
		name="Inverter Voltage R",
		key="grid_voltage_r",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
	"grid_voltage_s": SolaXModbusSensorEntityDescription(
		name="Inverter Voltage S",
		key="grid_voltage_s",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
	"grid_voltage_t": SolaXModbusSensorEntityDescription(
		name="Inverter Voltage T",
		key="grid_voltage_t",
		native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
	"import_energy_today": SolaXModbusSensorEntityDescription(
		name="Today's Import Energy",
		key="import_energy_today",
		native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        icon="mdi:solar-power",
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    "phase_power_balance_x3": SolaXModbusSensorEntityDescription(
		name="Phase Power Balance X3",
		key="phase_power_balance_x3",
	),
}