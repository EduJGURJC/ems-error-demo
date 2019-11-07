import requests
import time
import sys
import os
from threading import Timer
import json
import sys
import unittest
import xmlrunner

class AssertVariables():
  datavalues = {'test1':{'sensor':{'lasttriggertime':0, 'firstrun':True}, 'actuator':{'trigger': False}}}
variables = AssertVariables()

class TestSensorBehaviour(unittest.TestCase):
  def test_sensor_trigger_time(self):
    sensor_trigger_time = time.time()
    trigger_time = sensor_trigger_time - variables.datavalues['test1']['sensor']['lasttriggertime']
    time_behavior = trigger_time <= 6
    self.assertTrue(time_behavior, "Sensor trigger beyond expected interval")

class TestActuatorTrigger(unittest.TestCase):
  def test_actuator_trigger(self):
    if variables.datavalues['test1']['actuator']['trigger']:
      variables.datavalues['test1']['actuator']['trigger'] = False
    self.assertFalse(variables.datavalues['test1']['actuator']['trigger'], "Actuator was not triggered")

sensorBehaviourSuite = unittest.TestLoader().loadTestsFromTestCase(TestSensorBehaviour)
actuatorTriggerSuite = unittest.TestLoader().loadTestsFromTestCase(TestActuatorTrigger)

class MonitoringTest():
  def __init__(self):
    self.condition = True

    print("after sending requests")
    print("starting timer")
    # self.t.start()
    print("entering loop function")
    self.start_test()
    print("exiting loop function")

  def terminate(self):
    self.condition = False
    print("STOP_TEST")

  def start_test(self):
    url = "ws://" + self.ems + ":3232"
    ws = create_connection(url)
    print "entering loop"
    self.condition = True
    while(self.condition):
      result = ws.recv()
      result = json.loads(result)
      if "#terminate" in result["channels"]:
        print result
        print "test result found"
        self.condition = False
        break

      if "#test1sensor" in result["channels"]:
        print result
        if variables.datavalues['test1']['sensor']['firstrun']:
          variables.datavalues['test1']['sensor']['lasttriggertime'] = time.time()
          variables.datavalues['test1']['sensor']['firstrun'] = False
          continue
        xmlrunner.XMLTestRunner(verbosity=2, output='/tmp/test-reports').run(sensorBehaviourSuite)
        variables.datavalues['test1']['sensor']['lasttriggertime'] = time.time()
        xmlrunner.XMLTestRunner(verbosity=2, output='/tmp/test-reports').run(actuatorTriggerSuite)
        print "sensor has triggered"

      if "#test1actuator" in result["channels"]:
        print result
        variables.datavalues['test1']['actuator']['trigger'] = False
        print "actuator has triggered"

      if "#test1logic" in result["channels"]:
        print result
        print "logic has triggered"

      if "#test1sensortrigger" in result["channels"]:
        print result
        variables.datavalues['test1']['actuator']['trigger'] = True
        print "sensor has to trigger actuator"

import os
from websocket import create_connection
import json

if __name__ == "__main__":
    print("Starting the test")
    
    url = "ws://" + self.ems + ":3232"
    ws = create_connection(url)
   
    ems = os.environ["ET_EMS_LSBEATS_HOST"]
    tjobid = os.environ["TJOBID"]
    headers = {'content-type': 'text/plain'}
    stampers = ""
    monMachines = ""

    # get the stampers from file
    with open(os.environ['PWD'] + "/" + "stampers.txt") as f:
      stampers = f.read()

    # send stampers to EMS
    url = "http://" + self.ems + ":8888/stamper/tag0.1"
    response = requests.post(url, headers=headers, data=stampers)
    print(response.content)

    # get the monitoring machines from the file
    with open(os.environ['PWD'] + "/" + "monitoring_machines.txt") as f:
      monMachines = f.read()

    monMachines = monMachines.replace("TJOBID", tjobid)

    # send the monitoring machines to EMS
    url = "http://" + self.ems + ":8888/MonitoringMachine/signals0.1"
    response = requests.post(url, headers=self.headers, data=self.monMachines)
    print(response.content)
 
    
    
    result = ws.recv()
    result = json.loads(result)


    print("Ending the test")
