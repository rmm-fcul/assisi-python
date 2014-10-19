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
    "<Casu Name>", "Peltier", "Off", "Temperature", "Temperature setpoint"
    "<Target Name>", "CommEth", "<Casu Name>", "String", "(Comunication message, addressed directly to target!)"


.. csv-table:: Messages subscribed to by CASUs
   :header: "Name", "Device", "Command", "Data Message Type"
   :widths: 20, 20, 20, 40

    "<Casu Name>", "DiagnosticLed", "On", "ColorStamped"
    "...", "...", "Off", "ColorStamped"
    "...", "Light", "On", "ColorStamped"
    "...", "...", "Off", "ColorStamped"
    "<Casu Name>", "Peltier", "temp", "Temperature"
    "<Casu Name>", "Peltier", "Off", "Temperature"
    "...", "VibeMotor", "On", "Vibration"
    "...", "VibeMotor", "Off", "Vibration"
    "<Casu Name>", "EM", "config", "EMDeviceConfig"
    "<Casu Name>", "EM", "temp", "Temperature"
    "<Casu Name>", "EM", "efield", "ElectricField"
    "<Casu Name>", "EM", "mfield", "MagneticField"
    "<Casu Name>", "EM", "Off", "Temperature"
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
