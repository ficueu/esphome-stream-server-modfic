import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation, core
from esphome.automation import Condition, maybe_simple_id
from esphome.components import binary_sensor
from esphome.const import (
    DEVICE_CLASS_CONNECTIVITY,
    ENTITY_CATEGORY_DIAGNOSTIC,
    CONF_ON_PRESS, 
    CONF_ON_RELEASE,
    CONF_TRIGGER_ID,
)
from . import ns, StreamServerComponent

CONF_CONNECTED = "connected"
CONF_STREAM_SERVER = "stream_server"

PressTrigger = ns.class_("PressTrigger", automation.Trigger.template())
ReleaseTrigger = ns.class_(
    "ReleaseTrigger", automation.Trigger.template()
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_STREAM_SERVER): cv.use_id(StreamServerComponent),
        cv.Required(CONF_CONNECTED): binary_sensor.binary_sensor_schema(
            device_class=DEVICE_CLASS_CONNECTIVITY,
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
        ),
        cv.Optional(CONF_ON_PRESS): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(PressTrigger),
            }
        ),
        cv.Optional(CONF_ON_RELEASE): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(ReleaseTrigger),
            }
        ),
    }
)



async def to_code(config):
    server = await cg.get_variable(config[CONF_STREAM_SERVER])

    sens = await binary_sensor.new_binary_sensor(config[CONF_CONNECTED])
    cg.add(server.set_connected_sensor(sens))
