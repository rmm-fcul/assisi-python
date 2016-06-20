.. Description of the ASSISI communication protocol
   TODO: Move this to the msg package.

Assisi communication protocol
=============================

.. csv-table:: Messages published by CASUs
   :header: "Name", "Device", "Command", "Data Message Type", "Note"
   :widths: 20, 20, 20, 40, 40
   
    "<Casu Name>", "Temp", "Temperatures", "TemperatureArray",  "bla"
    "<Casu Name>", "IR", "Ranges", "RangeArray", "(Change naming)"
    "<Casu Name>", "Acc", "Measurements", "VibrationArray", "(Data not valid!)"
    "<Casu Name>", "Peltier", "On", "Temperature", "Temperature setpoint"
    "<Casu Name>", "Peltier", "Off", "Temperature", "Temperaturesetpoint"
    "<Casu Name>", "Airflow", "On", "Airflow", "Airflow intensity setpoint"
    "<Casu Name>", "Airflow", "Off", "Airflow", "Airflow intensity setpoint"
    "<Casu Name>", "DiagnosticLed", "On", "ColorStamped", "Color setpoint"
    "<Casu Name>", "DiagnosticLed", "Off", "ColorStamped", "Color setpoint"
    "<Casu Name>", "Speaker", "On", "VibrationSetpoint", "Vibration setpoint"
    "<Casu Name>", "Speaker", "Off", "VibrationSetpoint", "Vibration setpoint"
    "<Target Name>", "CommEth", "<Casu Name>", "String", "(Comunication message, addressed directly to target!)"


.. csv-table:: Messages subscribed to by CASUs
   :header: "Name", "Device", "Command", "Data Message Type"
   :widths: 20, 20, 20, 40

    "<Casu Name>", "IR", "Standby", "0"
    "<Casu Name>", "IR", "Activate", "0"
    "<Casu Name>", "DiagnosticLed", "On", "ColorStamped"
    "...", "...", "Off", "ColorStamped"
    "<Casu Name>", "Peltier", "On", "Temperature"
    "<Casu Name>", "Peltier", "Off", "Temperature"
    "...", "Speaker", "On", "VibrationSetpoint"
    "...", "Speaker", "Off", "VibrationSetpoint"
    "...", "Airflow", "On", "Airflow"
    "...", "Airflow", "Off", "Airflow"
    "<Casu Name>", "CommEth", "<Source Casu>", "String"

.. csv-table:: Messages published by the Simulator
   :header: "Name", "Device", "Command", "Data Message Type"
   :widths: 20, 20, 20, 40   
   
    "Sim", "Spawn", "<Object Name>", "Spawn"
    "...", "Teleport", "<Object Name>", "PoseStamped"

.. csv-table:: Messages published by simulated Bees
   :header: "Name", "Device", "Command", "Data Message Type"
   :widths: 20, 20, 20, 40

    "<Bee Name>", "Base", "Enc", "DiffDrive"
    "...", "...", "VelRef", "DiffDrive"
    "...", "...", "GroundTruth","PoseStamped"
    "...", "Object", "Ranges", "ObjectArray"
    "...", "Light","Readings", "ColorStamped"
    "...", "Color", "ColorVal", "ColorSamped"

.. csv-table:: Messages subscribed to by simulated Bees
   :header: "Name", "Device", "Command", "Data Message Type"
   :widths: 20, 20, 20, 40

    "<Bee Name>", "Base", "Vel", "DiffDrive"
