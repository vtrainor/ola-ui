LAMP_ON_MODE = {
  0: "Off",
  1: "DMX",
  2: "On",
  3: "On After Calibration",
}

LAMP_STATE = {
  0: "Off",
  1: "On",
  2: "Strike",
  3: "Standby",
  4: "Not Present",
  127: "Error",
}

DISPLAY_INVERT = {
  0: "Off",
  1: "On",
  2: "Auto",
}

POWER_STATE = {
  0: "Full Off",
  1: "Shutdown",
  2: "Standby",
  255: "Normal",
}

RECORDED_SUPPORTED = 0x01
LOWEST_HIGHEST_SUPPORTED = 0x02

SENSOR_VALUE = {
	0: "Recorded Value Supported",
	1: "Lowest/Highest Detected Values Supported",
	2: "Reserved",
	3: "Reserved",
	4: "Reserved",
	5: "Reserved",
	6: "Reserved",
	7: "Reserved"
}

SLOT_ID_DEFINITIONS = {
  0x0001: 'Intesity',
  0x0002: 'Intensity Master',
  0x0101: 'Pan',
  0x0102: 'Tilt',
  0x0201: 'Color Wheel',
  0x0202: 'Subtractive Color Mixer - Cyan/Blue',
  0x0203: 'Subtractive Color Mixer - Yellow/Amber',
  0x0204: 'Subtractive Color Mixer - Magenta',
  0x0205: 'Additive Color Mixer - Red',
  0x0206: 'Additive Color Mixer - Green',
  0x0207: 'Additive Color Mixer - Blue',
  0x0208: 'Color Tempurature Correction',
  0x0209: 'Color Scroll',
  0x0210: 'Color Semaphore',
  0x0301: 'Static gobo wheel',
  0x0302: 'Rotating gobo wheel',
  0x0303: 'Prism wheel',
  0x0304: 'Effects wheel',
  0x0401: 'Beam size iris',
  0x0402: 'Edge/Lens focus',
  0x0403: 'Frost/Diffusion',
  0x0404: 'Strobe/Shutter',
  0x0405: 'Zoom lens',
  0x0406: 'Framing shutter',
  0x0407: 'Framing shutter rotation',
  0x0408: 'Douser',
  0x0409: 'Barn Door',
  0x0501: 'Lamp control functions',
  0x0502: 'Fixture control channel',
  0x0503: 'Overall speed setting applied to multiple or all parameters',
  0x0504: 'Macro control',
  0xffff: 'No definition',
}