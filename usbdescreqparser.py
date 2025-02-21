"""
USB Descriptor parser.

This script is based on 'USB Descriptor and Request Parser.html' Frank Zhao.

The Javascript code has been converted to Python using <https://app.codeconvert.ai>
and was then manually edited.
"""

# pylint: disable=invalid-name,too-many-lines

import re


usage_tbl = [
    [
        "Undefined",
    ],
    [  # generic desktop
        "Undefined",
        "Pointer",
        "Mouse",
        "Reserved",
        "Joystick",
        "Game Pad",
        "Keyboard",
        "Keypad",
        "Multi-axis Controller",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x0F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x1F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x2F
        "X",
        "Y",
        "Z",
        "Rx",
        "Ry",
        "Rz",
        "Slider",
        "Dial",
        "Wheel",
        "Hat switch",
        "Counted Buffer",
        "Byte Count",
        "Motion Wakeup",
        "Start",
        "Select",
        "Reserved",
        "Vx",
        "Vy",
        "Vz",
        "Vbrx",
        "Vbry",
        "Vbrz",
        "Vno",
        "Feature Notification",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x4F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x5F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x6F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x7F
        "Sys Control",
        "Sys Power Down",
        "Sys Sleep",
        "Sys Wake Up",
        "Sys Context Menu",
        "Sys Main Menu",
        "Sys App Menu",
        "Sys Menu Help",
        "Sys Menu Exit",
        "Sys Menu Select",
        "Sys Menu Right",
        "Sys Menu Left",
        "Sys Menu Up",
        "Sys Menu Down",
        "Sys Cold Restart",
        "Sys Warm Restart",
        "D-pad Up",
        "D-pad Down",
        "D-pad Right",
        "D-pad Left",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x9F
        "Sys Dock",
        "Sys Undock",
        "Sys Setup",
        "Sys Break",
        "Sys Debugger Break",
        "Application Break",
        "Application Debugger Break",
        "Sys Speaker Mute",
        "Sys Hibernate",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Sys Display Invert",
        "Sys Display Internal",
        "Sys Display External",
        "Sys Display Both",
        "Sys Display Dual",
        "Sys Display Toggle Int/Ext",
        "Sys Display Swap",
        "Sys Display LCD Autoscale",
    ],
    [  # simulation controls
        "Undefined",
        "Flight Sim Dev",
        "Automobile Sim Dev",
        "Tank Sim Dev",
        "Spaceship Sim Dev",
        "Submarine Sim Dev",
        "Sailing Sim Dev",
        "Motorcycle Sim Dev",
        "Sports Sim Dev",
        "Airplane Sim Dev",
        "Helicopter Sim Dev",
        "Magic Carpet Simulation",
        "Bicycle Sim Dev",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x0F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x1F
        "Flight Control Stick",
        "Flight Stick",
        "Cyclic Control",
        "Cyclic Trim",
        "Flight Yoke",
        "Track Control",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x2F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x3F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x4F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x5F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x6F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x7F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x8F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x9F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0xAF
        "Aileron",
        "Aileron Trim",
        "Anti-Torque Control",
        "Autopilot Enable",
        "Chaff Release",
        "Collective Control",
        "Dive Brake",
        "Electronic Countermeasures",
        "Elevator",
        "Elevator Trim",
        "Rudder",
        "Throttle",
        "Flight Communications",
        "Flare Release",
        "Landing Gear",
        "Toe Brake",
        "Trigger",
        "Weapons Arm",
        "Weapons Select",
        "Wing Flaps",
        "Accelerator",
        "Brake",
        "Clutch",
        "Shifter",
        "Steering",
        "Turret Direction",
        "Barrel Elevation",
        "Dive Plane",
        "Ballast",
        "Bicycle Crank",
        "Handle Bars",
        "Front Brake",
        "Rear Brake",
    ],
    [  # VR controls
        "Unidentified",
        "Belt",
        "Body Suit",
        "Flexor",
        "Glove",
        "Head Tracker",
        "Head Mounted Display",
        "Hand Tracker",
        "Oculometer",
        "Vest",
        "Animatronic Device",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Stereo Enable",
        "Display Enable",
    ],
    [  # Sport controls
        "Unidentified",
        "Baseball Bat",
        "Golf Club",
        "Rowing Machine",
        "Treadmill",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Oar",
        "Slope",
        "Rate",
        "Stick Speed",
        "Stick Face Angle",
        "Stick Heel/Toe",
        "Stick Follow Through",
        "Stick Tempo",
        "Stick Type",
        "Stick Height",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Putter",
        "1 Iron",
        "2 Iron",
        "3 Iron",
        "4 Iron",
        "5 Iron",
        "6 Iron",
        "7 Iron",
        "8 Iron",
        "9 Iron",
        "10 Iron",
        "11 Iron",
        "Sand Wedge",
        "Loft Wedge",
        "Power Wedge",
        "1 Wood",
        "3 Wood",
        "5 Wood",
        "7 Wood",
        "9 Wood",
    ],
    [  # game controls
        "Undefined",
        "3D Game Controller",
        "Pinball Device CA",
        "Gun Device CA",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Point of View",
        "Turn Right/Left",
        "Pitch Forward/Backward",
        "Roll Right/Left DV",
        "Move Right/Left",
        "Move Forward/Backward",
        "Move Up/Down",
        "Lean Right/Left",
        "Lean Forward/Backward",
        "Height of POV",
        "Flipper",
        "Secondary Flipper",
        "Bump",
        "New Game",
        "Shoot Ball",
        "Player",
        "Gun Bolt",
        "Gun Clip",
        "Gun Selector",
        "Gun Single Shot",
        "Gun Burst",
        "Gun Automatic",
        "Gun Safety",
        "Gamepad Fire/Jump",
        "Gamepad Trigger",  # possible mistake in documentation, 0x38 is skipped
        "Gamepad Trigger",
    ],
    [  # generic device controls
        "Unidentified",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Battery Strength",
        "Wireless Channel",
        "Wireless ID",
    ],
    [
        "Keyboard",
    ],
    [
        # LEDs
        "Undefined ",
        "Num Lock",
        "Caps Lock",
        "Scroll Lock",
        "Compose",
        "Kana",
        "Power",
        "Shift",
        "Do Not Disturb",
        "Mute",
        "Tone Enable",
        "High Cut Filter",
        "Low Cut Filter",
        "Equalizer Enable",
        "Sound Field On",
        "Surround On",
        "Repeat",
        "Stereo",
        "Sampling Rate Detect",
        "Spinning",
        "CAV",
        "CLV",
        "Recording Format Detect",
        "Off-Hook",
        "Ring",
        "Message Waiting",
        "Data Mode",
        "Battery Operation",
        "Battery OK",
        "Battery Low",
        "Speaker",
        "Head Set",
        "Hold",
        "Microphone",
        "Coverage",
        "Night Mode",
        "Send Calls",
        "Call Pickup",
        "Conference",
        "Stand-by",
        "Camera On",
        "Camera Off",
        "On-Line",
        "Off-Line",
        "Busy",
        "Ready",
        "Paper-Out",
        "Paper-Jam",
        "Remote",
        "Forward",
        "Reverse",
        "Stop",
        "Rewind",
        "Fast Forward",
        "Play",
        "Pause",
        "Record",
        "Error",
        "Usage Selected Indicator",
        "Usage In Use Indicator",
        "Usage Multi Mode Indicator",
        "Indicator On",
        "Indicator Flash",
        "Indicator Slow Blink",
        "Indicator Fast Blink",
        "Indicator Off",
        "Flash On Time",
        "Slow Blink On Time",
        "Slow Blink Off Time",
        "Fast Blink On Time",
        "Fast Blink Off Time",
        "Usage Indicator Color",
        "Indicator Red",
        "Indicator Green",
        "Indicator Amber",
        "Generic Indicator",
        "System Suspend",
        "External Power Connected",
    ],
    [  # buttons
        "Button 0x",
    ],
    [  # ordinal
        "Ordinal 0x",
    ],
    [  # telephony
        "Unassigned",
        "Phone",
        "Answering Machine",
        "Message Controls",
        "Handset",
        "Headset",
        "Telephony Key Pad",
        "Programmable Button",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Hook Switch",
        "Flash",
        "Feature",
        "Hold",
        "Redial",
        "Transfer",
        "Drop",
        "Park",
        "Forward Calls",
        "Alternate Function",
        "Line",
        "Speaker Phone",
        "Conference",
        "Ring Enable",
        "Ring Select",
        "Phone Mute",
        "Caller ID",
        "Send",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Speed Dial",
        "Store Number",
        "Recall Number",
        "Phone Directory",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Voice Mail",
        "Screen Calls",
        "Do Not Disturb",
        "Message",
        "Answer On/Off",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Inside Dial Tone",
        "Outside Dial Tone",
        "Inside Ring Tone",
        "Outside Ring Tone",
        "Priority Ring Tone",
        "Inside Ringback",
        "Priority Ringback",
        "Line Busy Tone",
        "Reorder Tone",
        "Call Waiting Tone",
        "Confirmation Tone 1",
        "Confirmation Tone 2",
        "Tones Off",
        "Outside Ringback",
        "Ringer",
        "Reserved",  # 0x9E is ringer, the doc has a mistake, this should be 0x9F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Phone Key 0",
        "Phone Key 1",
        "Phone Key 2",
        "Phone Key 3",
        "Phone Key 4",
        "Phone Key 5",
        "Phone Key 6",
        "Phone Key 7",
        "Phone Key 8",
        "Phone Key 9",
        "Phone Key Star",
        "Phone Key Pound",
        "Phone Key A",
        "Phone Key B",
        "Phone Key C",
        "Phone Key D",
    ],
    [  # Consumer
        "Unassigned",
        "Consumer Control",
        "Numeric Key Pad",
        "Programmable Buttons",
        "Microphone",
        "Headphone",
        "Graphic Equalizer",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "+10",
        "+100",
        "AM/PM",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # doc error, should end at 0x2F
        "Power",
        "Reset",
        "Sleep",
        "Sleep After",
        "Sleep Mode",
        "Illumination",
        "Buttons",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Menu",
        "Menu Pick",
        "Menu Up",
        "Menu Down",
        "Menu Left",
        "Menu Right",
        "Menu Escape",
        "Menu Value Increase",
        "Menu Value Decrease",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Data On Screen",
        "Closed Caption",
        "Closed Caption Select",
        "VCR/TV",
        "Broadcast Mode",
        "Snapshot",
        "Still",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Selection",
        "Assign Selection",
        "Mode Step",
        "Recall Last",
        "Enter Channel",
        "Order Movie",
        "Channel",
        "Media Selection",
        "Media Select Computer",
        "Media Select TV",
        "Media Select WWW",
        "Media Select DVD",
        "Media Select Telephone",
        "Media Select Program Guide",
        "Media Select Video Phone",
        "Media Select Games",
        "Media Select Messages",
        "Media Select CD",
        "Media Select VCR",
        "Media Select Tuner",
        "Quit",
        "Help",
        "Media Select Tape",
        "Media Select Cable",
        "Media Select Satellite",
        "Media Select Security",
        "Media Select Home",
        "Media Select Call",
        "Channel Increment",
        "Channel Decrement",
        "Media Select SAP",
        "Reserved",
        "VCR Plus",
        "Once",
        "Daily",
        "Weekly",
        "Monthly",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Play",
        "Pause",
        "Record",
        "Fast Forward",
        "Rewind",
        "Scan Next Track",
        "Scan Previous Track",
        "Stop",
        "Eject",
        "Random Play",
        "Select Disc",
        "Enter Disc",
        "Repeat",
        "Tracking",
        "Track Normal",
        "Slow Tracking",
        "Frame Forward",
        "Frame Back",
        "Mark",
        "Clear Mark",
        "Repeat From Mark",
        "Return To Mark",
        "Search Mark Forward",
        "Search Mark Backwards",
        "Counter Reset",
        "Show Counter",
        "Tracking Increment",
        "Tracking Decrement",
        "Stop/Eject",
        "Play/Pause",
        "Play/Skip",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Volume",
        "Balance",
        "Mute",
        "Bass",
        "Treble",
        "Bass Boost",
        "Surround Mode",
        "Loudness",
        "MPX",
        "Volume Increment",
        "Volume Decrement",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Speed Select",
        "Playback Speed",
        "Standard Play",
        "Long Play",
        "Extended Play",
        "Slow",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Fan Enable",
        "Fan Speed",
        "Light Enable",
        "Light Illumination Level",
        "Climate Control Enable",
        "Room Temperature",
        "Security Enable",
        "Fire Alarm",
        "Police Alarm",
        "Proximity",
        "Motion",
        "Duress Alarm",
        "Holdup Alarm",
        "Medical Alarm",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x11F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x12F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x13F
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x14F
        "Balance Right",
        "Balance Left",
        "Bass Increment",
        "Bass Decrement",
        "Treble Increment",
        "Treble Decrement",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Speaker System",
        "Channel Left",
        "Channel Right",
        "Channel Center",
        "Channel Front",
        "Channel Center Front",
        "Channel Side",
        "Channel Surround",
        "Channel Low Frequency Enhancement",
        "Channel Top",
        "Channel Unknown",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Sub-channel",
        "Sub-channel Increment",
        "Sub-channel Decrement",
        "Alternate Audio Increment",
        "Alternate Audio Decrement",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Application Launch Buttons",
        "AL Launch Button Configuration Tool",
        "AL Programmable Button Configuration",
        "AL Consumer Control Configuration",
        "AL Word Processor",
        "AL Text Editor",
        "AL Spreadsheet",
        "AL Graphics Editor",
        "AL Presentation App",
        "AL Database App",
        "AL Email Reader",
        "AL Newsreader",
        "AL Voicemail",
        "AL Contacts/Address Book",
        "AL Calendar/Schedule",
        "AL Task/Project Manager",
        "AL Log/Journal/Timecard",
        "AL Checkbook/Finance",
        "AL Calculator",
        "AL A/V Capture/Playback",
        "AL Local Machine Browser",
        "AL LAN/WAN Browser",
        "AL Internet Browser",
        "AL Remote Networking/ISP Connect",
        "AL Network Conference",
        "AL Network Chat",
        "AL Telephony/Dialer",
        "AL Logon",
        "AL Logoff",
        "AL Logon/Logoff",
        "AL Terminal Lock/Screensaver",
        "AL Control Panel",
        "AL Command Line Processor/Run Sel",
        "AL Process/Task Manager",
        "AL Select Task/Application",
        "AL Next Task/Application",
        "AL Previous Task/Application",
        "AL Preemptive Halt Task/Application",
        "AL Integrated Help Center",
        "AL Documents",
        "AL Thesaurus",
        "AL Dictionary",
        "AL Desktop",
        "AL Spell Check",
        "AL Grammar Check",
        "AL Wireless Status",
        "AL Keyboard Layout",
        "AL Virus Protection",
        "AL Encryption",
        "AL Screen Saver",
        "AL Alarms",
        "AL Clock",
        "AL File Browser",
        "AL Power Status",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x1CF
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x1DF
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x1EF
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",  # 0x1FF
        "Generic GUI Application Controls",
        "AC New",
        "AC Open",
        "AC Close",
        "AC Exit",
        "AC Maximize",
        "AC Minimize",
        "AC Save",
        "AC Print",
        "AC Properties",  # 0x209, but the next one is 0x21A
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "AC Undo",
        "AC Copy",
        "AC Cut",
        "AC Paste",
        "AC Select All",
        "AC Find",
        "AC Find and Replace",
        "AC Search",
        "AC Go To",
        "AC Home",
        "AC Back",
        "AC Forward",
        "AC Stop",
        "AC Refresh",
        "AC Previous Link",
        "AC Next Link",
        "AC Bookmarks",
        "AC History",
        "AC Subscriptions",
        "AC Zoom In",
        "AC Zoom Out",
        "AC Zoom",
        "AC Full Screen View",
        "AC Normal View",
        "AC View Toggle",
        "AC Scroll Up",
        "AC Scroll Down",
        "AC Scroll",
        "AC Pan Left",
        "AC Pan Right",
        "AC Pan",
        "AC New Window",
        "AC Tile Horizontally",
        "AC Tile Vertically",
        "AC Format",
        "AC Edit",
        "AC Bold",
        "AC Italics",
        "AC Underline",
        "AC Strikethrough",
        "AC Subscript",
        "AC Superscript",
        "AC All Caps",
        "AC Rotate",
        "AC Resize",
        "AC Flip horizontal",
        "AC Flip Vertical",
        "AC Mirror Horizontal",
        "AC Mirror Vertical",
        "AC Font Select",
        "AC Font Color",
        "AC Font Size",
        "AC Justify Left",
        "AC Justify Center H",
        "AC Justify Right",
        "AC Justify Block H",
        "AC Justify Top",
        "AC Justify Center V",
        "AC Justify Bottom",
        "AC Justify Block V",
        "AC indent Decrease",
        "AC indent Increase",
        "AC Numbered List",
        "AC Restart Numbering",
        "AC Bulleted List",
        "AC Promote",
        "AC Demote",
        "AC Yes",
        "AC No",
        "AC Cancel",
        "AC Catalog",
        "AC Buy/Checkout",
        "AC Add to Cart",
        "AC Expand",
        "AC Expand All",
        "AC Collapse",
        "AC Collapse All",
        "AC Print Preview",
        "AC Paste Special",
        "AC Insert Mode",
        "AC Delete",
        "AC Lock",
        "AC Unlock",
        "AC Protect",
        "AC Unprotect",
        "AC Attach Comment",
        "AC Delete Comment",
        "AC View Comment",
        "AC Select Word",
        "AC Select Sentence",
        "AC Select Paragraph",
        "AC Select Column",
        "AC Select Row",
        "AC Select Table",
        "AC Select Object",
        "AC Redo/Repeat",
        "AC Sort",
        "AC Sort Ascending",
        "AC Sort Descending",
        "AC Filter",
        "AC Set Clock",
        "AC View Clock",
        "AC Select Time Zone",
        "AC Edit Time Zones",
        "AC Set Alarm",
        "AC Clear Alarm",
        "AC Snooze Alarm",
        "AC Reset Alarm",
        "AC Synchronize",
        "AC Send/Receive",
        "AC Send To",
        "AC Reply",
        "AC Reply All",
        "AC Forward Msg",
        "AC Send",
        "AC Attach File",
        "AC Upload",
        "AC Download (Save Target As)",
        "AC Set Borders",
        "AC Insert Row",
        "AC Insert Column",
        "AC Insert File",
        "AC Insert Picture",
        "AC Insert Object",
        "AC Insert Symbol",
        "AC Save and Close",
        "AC Rename",
        "AC Merge",
        "AC Split",
        "AC Disribute Horizontally",
        "AC Distribute Vertically",
    ],
    [  # digitizers
        "Undefined",
        "Digitizer",
        "Pen",
        "Light Pen",
        "Touch Screen",
        "Touch Pad",
        "White Board",
        "Coordinate Measuring Machine",
        "3D Digitizer",
        "Stereo Plotter",
        "Articulated Arm",
        "Armature",
        "Multiple Point Digitizer",
        "Free Space Wand",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Stylus",
        "Puck",
        "Finger",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Tip Pressure",
        "Barrel Pressure",
        "In Range",
        "Touch",
        "Untouch",
        "Tap",
        "Quality",
        "Data Valid",
        "Transducer Index",
        "Tablet Keys",
        "Program Change Keys",
        "Battery Strength",
        "Invert",
        "X Tilt",
        "Y Tilt",
        "Azimuth",
        "Altitude",
        "Twist",
        "Tip Switch",
        "Secondary Tip Switch",
        "Barrel Switch",
        "Eraser",
        "Tablet Pick",
    ],
    [""],  # 0x0E
    [""],  # 0x0F
    [  # unicode
        "Unicode 0x",
    ],
    [""],  # 0x11
    [""],  # 0x12
    [""],  # 0x13
    [  # alphanumeric display
        "Undefined",
        "Alphanumeric Display",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Display Attributes Report",
        "ASCII Character Set",
        "Data Read Back",
        "Font Read Back",
        "Display Control Report",
        "Clear Display",
        "Display Enable",
        "Screen Saver Delay",
        "Screen Saver Enable",
        "Vertical Scroll",
        "Horizontal Scroll",
        "Character Report",
        "Display Data",
        "Display Status",
        "Stat Not Ready",
        "Stat Ready",
        "Err Not a loadable character",
        "Err Font data cannot be read",
        "Cursor Position Report",
        "Row",
        "Column",
        "Rows",
        "Columns",
        "Cursor Pixel Positioning",
        "Cursor Mode",
        "Cursor Enable",
        "Cursor Blink",
        "Font Report",
        "Font Data",
        "Character Width",
        "Character Height",
        "Character Spacing Horizontal",
        "Character Spacing Vertical",
        "Unicode Character Set",
        "Font 7-Segment",
        "7-Segment Direct Map",
        "Font 14-Segment",
        "14-Segment Direct Map",
        "Display Brightness",
        "Display Contrast",
        "Character Attribute",
        "Attribute Readback",
        "Attribute Data",
        "Char Attr Enhance",
        "Char Attr Underline",
        "Char Attr Blink",
    ],
    [""],  # 0x15
    [""],  # 0x16
    [""],  # 0x17
    [""],  # 0x18
    [""],  # 0x19
    [""],  # 0x1A
    [""],  # 0x1B
    [""],  # 0x1C
    [""],  # 0x1D
    [""],  # 0x1E
    [""],  # 0x1F
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],  # 0x2F
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],
    [""],  # 0x3F
    [  # medical instrument
        "Undefined",
        "Medical Ultrasound",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "VCR/Acquisition",
        "Freeze/Thaw",
        "Clip Store",
        "Update",
        "Next",
        "Save",
        "Print",
        "Microphone Enable",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Cine",
        "Transmit Power",
        "Volume",
        "Focus",
        "Depth",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Soft Step - Primary",
        "Soft Step - Secondary",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Depth Gain Compensation",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Zoom Select",
        "Zoom Adjust",
        "Spectral Doppler Mode Select",
        "Spectral Doppler Adjust",
        "Color Doppler Mode Select",
        "Color Doppler Adjust",
        "Motion Mode Select",
        "Motion Mode Adjust",
        "2-D Mode Select",
        "2-D Mode Adjust",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Reserved",
        "Soft Control Select",
        "Soft Control Adjust",
    ],
]


def pHex(val):
    # returns hexadecimal string representation with 0x prefix
    x = f"{val:X}"

    if len(x) % 2 != 0:
        x = "0" + x

    return "0x" + x


def pHexC(val):
    # returns two-digit hexadecimal representation with a trailing space
    return "0x{:02X}, ".format(val)


def bBCD(x: int):
    upper = (x >> 8) & 0xFF
    lower = x & 0xFF
    return f"{upper:02d}{lower:02d}"


def pItemVal(s, v):
    if s <= 0:
        return ""

    else:
        b1 = 0x01 << ((8 * s) - 1)
        b2 = 0x01 << (8 * s)
        if v <= (b1 - 1):
            return f" ({v})"

        else:
            v = b2 - v
            v *= -1
            return f" ({v})"


def pUnit(s, v):
    if s <= 0:
        return ""

    else:
        str_ = ""
        for i in range(s * 2):
            nib = (v & (0xF << (i * 4))) >> (i * 4)
            if i == 0:
                if nib == 0x1:
                    str_ += "System: SI Linear, "

                elif nib == 0x2:
                    str_ += "System: SI Rotation, "

                elif nib == 0x3:
                    str_ += "System: English Linear, "

                elif nib == 0x4:
                    str_ += "System: English Rotation, "

            if i == 1:
                if nib == 0x1:
                    str_ += "Length: Centimeter, "

                elif nib == 0x2:
                    str_ += "Length: Radians, "

                elif nib == 0x3:
                    str_ += "Length: Inch, "

                elif nib == 0x4:
                    str_ += "Length: Degrees, "

            if i == 2:
                if nib == 0x1:
                    str_ += "Mass: Gram, "

                elif nib == 0x2:
                    str_ += "Mass: Gram, "

                elif nib == 0x3:
                    str_ += "Mass: Slug, "

                elif nib == 0x4:
                    str_ += "Mass: Slug, "

            if i == 3:
                if nib >= 0x1 and nib <= 0x4:
                    str_ += "Time: Seconds, "

            if i == 4:
                if nib == 0x1:
                    str_ += "Temperature: Kelvin, "

                elif nib == 0x2:
                    str_ += "Temperature: Kelvin, "

                elif nib == 0x3:
                    str_ += "Temperature: Fahrenheit, "

                elif nib == 0x4:
                    str_ += "Temperature: Fahrenheit, "

            if i == 5:
                if nib >= 0x1 and nib <= 0x4:
                    str_ += "Current: Ampere, "

            if i == 6:
                if nib >= 0x1 and nib <= 0x4:
                    str_ += "Luminous Intensity: Candela, "

        if str_ == "":
            return " (None)"

        else:
            str_ = str_[:-1]
            return " (" + str_ + ")"


def pInterfaceSubClass(c, v):
    if c == 0x01:
        if v == 0x01:
            return " (Audio Control)"

        elif v == 0x02:
            return " (Audio Streaming)"

    return ""


def get_bytes(s: str) -> str:
    inTxt = s
    inTxt = re.sub(r"^radix:(.*)$", "", inTxt, flags=re.MULTILINE | re.IGNORECASE)
    inTxt = re.sub(
        r"(\/\*(.*?)\*\/)|(\/\/(.*?)$)|[g-w]|[yz]",
        "",
        inTxt,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    # Split by all non-alphanumeric characters except for + or -
    inSplit = re.split(r"(?![+-])\W", inTxt)
    if len(inSplit) == 1 and len(inSplit[0]) > 2:
        # split every 2 chars
        inSplit = re.findall(r".{1,2}", inSplit[0])
    inVals = []
    for inSplitElem in inSplit:
        inSplitElem = inSplitElem.strip()
        if len(s) > 0:  # ignore blank entries
            try:
                x = int(inSplitElem, 16)
                if x >= 0 and x <= 0xFF:
                    inVals.append(x)
            except ValueError:
                pass
    return inVals


class Parser:
    def __init__(self):
        self.indent = 0
        self.possible_errors = 0

    def pindentComment(self, x, bs):
        y = " //   "
        preSpace = max(2 - bs, 0)

        for _ in range(preSpace):
            y = "      " + y

        for _ in range(self.indent):
            y += "  "

        y += x
        return y.rstrip() + "\n"

    def pDescriptorType(self, x):
        tbl = [
            "Undefined",
            "Device",
            "Configuration",
            "String",
            "Interface",
            "Endpoint",
            "Device Qualifier",
            "Other Speed",
            "Interface Power",
            "OTG",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "Unknown",
            "HID",  # 0x21
            "HID Report",
            "Unknown",
            "Dependant on Type",
            "Dependant on Type",
            "Unknown",
            "Unknown",
            "Unknown",
            "Hub",  # 0x29
        ]

        if x < 0 or x >= len(tbl):
            self.possible_errors += 1
            return " (Unknown)"

        else:
            if tbl[x] == "Unknown" or tbl[x] == "Undefined":
                self.possible_errors += 1

            return " (" + tbl[x] + ")"

    def pDeviceClass(self, c):
        tbl = (
            [
                "Use class information in the Interface Descriptors",
                "Audio",
                "Communications and CDC Control",
                "HID",
                "",
                "Physical",
                "Image",
                "Printer",
                "Mass Storage",
                "Hub",
                "CDC-Data",
                "Smart Card",
                "Content Security",
                "Video",
                "Personal Healthcare",
                "Audio/Video Devices",  # 0x10
            ]
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0x1F
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0x2F
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0x3F
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0x4F
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0x5F
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0x6F
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0x7F
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0x8F
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0x9F
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0xAF
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0xBF
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0xCF
            + ["", "", "", "", "", "", "", "", "", "", "", ""]  # 0xDB
            + [
                "Diagnostic Device",  # 0xDC
                "",
                "",
                "",  # 0xDF
            ]
            + [
                "Wireless Controller",  # 0xE0
            ]
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0xEE
            + [
                "Miscellaneous",  # 0xEF
            ]
            + ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]  # 0xFD
            + [
                "Application Specific",
                "Vendor Specific",
            ]
        )

        assert len(tbl) == 255

        str_ = ""
        if c < len(tbl):
            str_ = tbl[c]

        if str_ != "":
            str_ = "(" + str_ + ")"

        if str_ == "":
            self.possible_errors += 1

        return str_

    def pDeviceSubClass(self, c, sc):
        if c == 0x10:  # AV device
            if sc == 0x01:
                return "(AV Control Interface)"

            if sc == 0x02:
                return "(AV Data Video)"

            if sc == 0x03:
                return "(AV Data Audio)"

        if c == 0xFE:
            if sc == 0x01:
                return "(Device Firmware Upgrade)"

            if sc == 0x02:
                return "(IRDA Bridge Device)"

            if sc == 0x03:
                return "(USB Test and Measurement Device)"

        return ""

    def pDeviceProtocol(self, c, _sc, p):
        if c == 0x09:
            if p == 0x00:
                return "(Full Speed Hub)"

            if p == 0x01:
                return "(High Speed Hub with single TT)"

            if p == 0x02:
                return "(High Speed Hub with multiple TT)"

            else:
                self.possible_errors += 1

        return ""

    def pInterfaceClass(self, v):
        if v == 0x01:
            return " (Audio)"

        return ""

    def pInputOutputFeature(self, s, v, t):
        if s <= 0:
            return ""

        else:
            str_ = ""
            if (v & 0x01) == 0:
                str_ += "Data,"

            else:
                str_ += "Const,"

            if (v & 0x02) == 0:
                str_ += "Array"

            else:
                str_ += "Var"

            if (v & 0x04) == 0:
                str_ += ",Abs"

            else:
                str_ += ",Rel"

            if (v & 0x08) == 0:
                str_ += ",No Wrap"

            else:
                str_ += ",Wrap"

            if (v & 0x10) == 0:
                str_ += ",Linear"

            else:
                str_ += ",Nonlinear"

            if (v & 0x20) == 0:
                str_ += ",Preferred State"

            else:
                str_ += ",No Preferred State"

            if (v & 0x40) == 0:
                str_ += ",No Null Position"

            else:
                str_ += ",Null State"

            if t != 0x08:
                if (v & 0x80) == 0:
                    str_ += ",Non-volatile"

                else:
                    str_ += ",Volatile"

            if s > 1:
                if (v & 0x100) == 0:
                    str_ += ",Bit Field"

                else:
                    str_ += ",Buffered Bytes"

            if str_ == "":
                str_ = pHex(v)
                self.possible_errors += 1

            return " (" + str_ + ")"

    def pUnitExp(self, s, v):
        if s <= 0 or v > 0x0F:
            self.possible_errors += 1
            return ""

        else:
            tbl = [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "-8",
                "-7",
                "-6",
                "-5",
                "-4",
                "-3",
                "-2",
                "-1",
            ]
            return " (" + tbl[v] + ")"

    def pusagePage(self, s, v):
        if s <= 0:
            self.possible_errors += 1
            return ""

        else:
            tbl = [
                "Undefined",
                "Generic Desktop Ctrls",
                "Sim Ctrls",
                "VR Ctrls",
                "Sport Ctrls",
                "Game Ctrls",
                "Generic Dev Ctrls",
                "Kbrd/Keypad",
                "LEDs",
                "Button",
                "Ordinal",
                "Telephony",
                "Consumer",
                "Digitizer",
                "Reserved 0x0E",
                "PID Page",
                "Unicode",
                "Reserved 0x11",
                "Reserved 0x12",
                "Reserved 0x13",
                "Alphanumeric Display",
            ]
            if v == 0 or v == 14 or v == 17 or v == 18 or v == 19:
                self.possible_errors += 1

            if v < len(tbl):
                return " (" + tbl[v] + ")"

            elif v == 0x40:
                return " (Medical Instruments)"

            elif v >= 0x80 and v <= 0x83:
                return " (Monitor Pages)"

            elif v >= 0x84 and v <= 0x87:
                return " (Power Pages)"

            elif v == 0x8C:
                return " (Bar Code Scanner Page)"

            elif v == 0x8D:
                return " (Scale Page)"

            elif v == 0x8E:
                return " (MagStripe Reading Devices)"

            elif v == 0x8F:
                return " (Rsv'ed Point-of-Sale Pages)"

            elif v == 0x90:
                return " (Camera Control Page)"

            elif v == 0x91:
                return " (Arcade Page)"

            elif v >= 0x92 and v <= 0xFEFF:
                self.possible_errors += 1
                return " (Reserved " + pHex(v) + ")"

            elif v >= 0xFF00 and v <= 0xFFFFF:
                return " (Vendor Defined " + pHex(v) + ")"

            else:
                return " (" + pHex(v) + ")"

    def pUsage(self, s, v, u):
        if s <= 0:
            return ""

        else:
            str_ = ""
            if u == 0x07 or u == 0x09 or u == 0x0A or u == 0x10:
                str_ = pHex(v)

            else:
                if u >= len(usage_tbl):
                    str_ = None
                elif v >= len(usage_tbl[u]):
                    str_ = None
                else:
                    str_ = usage_tbl[u][v]

                if str_ == "Reserved":
                    self.possible_errors += 1
                    str_ = pHex(v)

                elif str_ == "Unknown" or str_ == "Undefined":
                    self.possible_errors += 1

                if (
                    str_ == 0
                    or str_ == 0
                    or str_ == ""
                    or str_ is None
                    or str_.strip() == ""
                ):
                    self.possible_errors += 1
                    str_ = pHex(v)

            return " (" + str_ + ")"

    def pcollection(self, s, v):
        if s <= 0:
            return ""

        else:
            tbl = [
                "Physical",
                "Application",
                "Logical",
                "Report",
                "Named Array",
                "Usage Switch",
                "Usage Modifier",
            ]
            if v < 0:
                self.possible_errors += 1

            if v < len(tbl):
                return " (" + tbl[v] + ")"

            elif v >= 0x07 and v <= 0x7F:
                self.possible_errors += 1
                return " (Reserved " + pHex(v) + ")"

            elif v >= 0x80 and v <= 0xFF:
                self.possible_errors += 1
                return " (Vendor Defined " + pHex(v) + ")"

            return " (" + pHex(v) + ")"

    def parse_hidrepdesc(self, inTxt):
        self.possible_errors = 0
        inVals = get_bytes(inTxt)
        outTxt = ""
        self.indent = 0
        usagePage = {}
        collection = {}
        stack_ptr = 0

        i = 0
        while i < len(inVals):
            b0 = inVals[i]
            i += 1
            bSize = b0 & 0x03
            bSize = 4 if bSize == 3 else bSize  # size is 4 when bSize is 3
            bType = (b0 >> 2) & 0x03
            bTag = (b0 >> 4) & 0x0F

            if bType == 0x03 and bTag == 0x0F and bSize == 2 and i + 2 < len(inVals):
                bDataSize = inVals[i]
                i += 1
                bLongItemTag = inVals[i]
                i += 1
                outTxt += (
                    pHexC(b0)
                    + pHexC(bDataSize)
                    + pHexC(bLongItemTag)
                    + self.pindentComment("Long Item (" + pHex(bLongItemTag) + ")", 2)
                )
                for j in range(bDataSize):
                    if i >= len(inVals):
                        break
                    outTxt += pHexC(inVals[i])
                    i += 1
                    self.possible_errors += (
                        1  # there are no devices that use long item data right now
                    )

                self.indent += 1
                outTxt += self.pindentComment(
                    "Long Item Data (" + bDataSize.toString(10) + " bytes)", 2
                )
                self.indent -= 1

                self.possible_errors += (
                    1  # there are no devices that use long item data right now
                )

            else:
                bSizeActual = 0
                itemVal = 0
                outTxt += pHexC(b0)
                for j in range(bSize):
                    if i + j < len(inVals):
                        outTxt += pHexC(inVals[i + j])
                        itemVal += inVals[i + j] << (8 * j)
                        bSizeActual += 1

                if bType == 0x00:
                    if bTag == 0x08:
                        outTxt += self.pindentComment(
                            "Input" + self.pInputOutputFeature(bSize, itemVal, bTag),
                            bSizeActual,
                        )

                    elif bTag == 0x09:
                        outTxt += self.pindentComment(
                            "Output" + self.pInputOutputFeature(bSize, itemVal, bTag),
                            bSizeActual,
                        )

                    elif bTag == 0x0B:
                        outTxt += self.pindentComment(
                            "Feature" + self.pInputOutputFeature(bSize, itemVal, bTag),
                            bSizeActual,
                        )

                    elif bTag == 0x0A:
                        collection[stack_ptr] = itemVal
                        outTxt += self.pindentComment(
                            "Collection" + self.pcollection(bSize, itemVal), bSizeActual
                        )
                        self.indent += 1

                    elif bTag == 0x0C:
                        self.indent -= 1
                        outTxt += self.pindentComment("End Collection", bSizeActual)

                    else:
                        outTxt += self.pindentComment(
                            "Unknown (bTag: "
                            + pHex(bTag)
                            + ", bType: "
                            + pHex(bType)
                            + ")",
                            bSizeActual,
                        )
                        self.possible_errors += 1

                elif bType == 0x01:
                    if bTag == 0x00:
                        usagePage[stack_ptr] = itemVal
                        outTxt += self.pindentComment(
                            "Usage Page" + self.pusagePage(bSize, itemVal), bSizeActual
                        )

                    elif bTag == 0x01:
                        outTxt += self.pindentComment(
                            "Logical Minimum" + pItemVal(bSize, itemVal),
                            bSizeActual,
                        )

                    elif bTag == 0x02:
                        outTxt += self.pindentComment(
                            "Logical Maximum" + pItemVal(bSize, itemVal),
                            bSizeActual,
                        )

                    elif bTag == 0x03:
                        outTxt += self.pindentComment(
                            "Physical Minimum" + pItemVal(bSize, itemVal),
                            bSizeActual,
                        )

                    elif bTag == 0x04:
                        outTxt += self.pindentComment(
                            "Physical Maximum" + pItemVal(bSize, itemVal),
                            bSizeActual,
                        )

                    elif bTag == 0x05:
                        outTxt += self.pindentComment(
                            "Unit Exponent" + self.pUnitExp(bSize, itemVal), bSizeActual
                        )

                    elif bTag == 0x06:
                        outTxt += self.pindentComment(
                            "Unit" + pUnit(bSize, itemVal), bSizeActual
                        )

                    elif bTag == 0x07:
                        outTxt += self.pindentComment(
                            "Report Size" + pItemVal(bSize, itemVal), bSizeActual
                        )

                    elif bTag == 0x08:
                        outTxt += self.pindentComment(
                            "Report ID" + pItemVal(bSize, itemVal), bSizeActual
                        )

                    elif bTag == 0x09:
                        outTxt += self.pindentComment(
                            "Report Count" + pItemVal(bSize, itemVal), bSizeActual
                        )

                    elif bTag == 0x0A:
                        outTxt += self.pindentComment("Push", bSizeActual)
                        self.indent += 1
                        stack_ptr += 1
                        usagePage[stack_ptr] = usagePage[stack_ptr - 1]
                        collection[stack_ptr] = collection[stack_ptr - 1]

                    elif bTag == 0x0B:
                        self.indent -= 1
                        stack_ptr -= 1
                        outTxt += self.pindentComment("Pop", bSizeActual)

                    else:
                        outTxt += self.pindentComment(
                            "Unknown (bTag: "
                            + pHex(bTag)
                            + ", bType: "
                            + pHex(bType)
                            + ")",
                            bSizeActual,
                        )
                        self.possible_errors += 1

                elif bType == 0x02:
                    if bTag == 0x00:
                        outTxt += self.pindentComment(
                            "Usage" + self.pUsage(bSize, itemVal, usagePage[stack_ptr]),
                            bSizeActual,
                        )

                    elif bTag == 0x01:
                        outTxt += self.pindentComment(
                            "Usage Minimum"
                            + self.pUsage(bSize, itemVal, usagePage[stack_ptr]),
                            bSizeActual,
                        )

                    elif bTag == 0x02:
                        outTxt += self.pindentComment(
                            "Usage Maximum"
                            + self.pUsage(bSize, itemVal, usagePage[stack_ptr]),
                            bSizeActual,
                        )

                    elif bTag == 0x03:
                        outTxt += self.pindentComment(
                            "Designator Index" + pItemVal(bSize, itemVal),
                            bSizeActual,
                        )

                    elif bTag == 0x04:
                        outTxt += self.pindentComment(
                            "Designator Minimum" + pItemVal(bSize, itemVal),
                            bSizeActual,
                        )

                    elif bTag == 0x05:
                        outTxt += self.pindentComment(
                            "Designator Maximum" + pItemVal(bSize, itemVal),
                            bSizeActual,
                        )

                    elif bTag == 0x07:
                        outTxt += self.pindentComment(
                            "String Index" + pItemVal(bSize, itemVal), bSizeActual
                        )

                    elif bTag == 0x08:
                        outTxt += self.pindentComment(
                            "String Minimum" + pItemVal(bSize, itemVal),
                            bSizeActual,
                        )

                    elif bTag == 0x09:
                        outTxt += self.pindentComment(
                            "String Maximum" + pItemVal(bSize, itemVal),
                            bSizeActual,
                        )

                    elif bTag == 0x0A:
                        outTxt += self.pindentComment(
                            "Delimiter" + pItemVal(bSize, itemVal), bSizeActual
                        )

                    else:
                        outTxt += self.pindentComment(
                            "Unknown (bTag: "
                            + pHex(bTag)
                            + ", bType: "
                            + pHex(bType)
                            + ")",
                            bSizeActual,
                        )
                        self.possible_errors += 1

                else:
                    outTxt += self.pindentComment(
                        "Unknown (bTag: "
                        + pHex(bTag)
                        + ", bType: "
                        + pHex(bType)
                        + ")",
                        bSizeActual,
                    )
                    self.possible_errors += 1

                i += bSize

        outTxt += f"\n// {len(inVals)} bytes\n"
        return outTxt

    # XXXX

    def parse_stddesc(self, inTxt: str) -> str:
        self.possible_errors = 0
        inVals = get_bytes(inTxt)

        outTxt = ""
        bLength = 0
        bDescriptorType = 0
        j = -2

        bInterfaceClass = -1
        bInterfaceSubClass = -1

        i = 0
        while i < len(inVals):
            if j <= 0:
                bLength = inVals[i]
                i += 1
                j = bLength - 1
                outTxt += pHexC(bLength) + self.pindentComment("bLength", 1)
                if bLength > len(inVals):
                    self.possible_errors += 2

            elif j == bLength - 1:
                bDescriptorType = inVals[i]
                i += 1
                j -= 1
                if bDescriptorType != 0x04 and bInterfaceClass == 0x01:
                    outTxt += pHexC(bDescriptorType) + self.pindentComment(
                        "bDescriptorType (See Next Line)", 1
                    )

                else:
                    outTxt += pHexC(bDescriptorType) + self.pindentComment(
                        "bDescriptorType" + self.pDescriptorType(bDescriptorType), 1
                    )

            else:
                if bDescriptorType == 0x21:
                    # HID
                    bcdHID = 0
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bcdL = inVals[i] & 0x0F
                        bcdH = (inVals[i] & 0xF0) >> 4
                        bcdHID = (bcdL + (bcdH * 10)) / 100
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bcdL = inVals[i] & 0x0F
                        bcdH = (inVals[i] & 0xF0) >> 4
                        bcdHID += bcdL + (bcdH * 10)
                        i += 1
                        j -= 1
                        outTxt += self.pindentComment(f"bcdHID {bcdHID:2.2f}", 2)

                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        outTxt += self.pindentComment("bCountryCode", 1)
                        i += 1
                        j -= 1

                    bNumDescriptors = 0
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bNumDescriptors = inVals[i]
                        outTxt += self.pindentComment("bNumDescriptors", 1)
                        i += 1
                        j -= 1

                    for k in range(bNumDescriptors):
                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            str_ = " (HID)"
                            if inVals[i] != 0x22:
                                self.possible_errors += (
                                    1  # for HID, this field must also be HID
                                )
                                str_ = " (Unknown " + pHex(inVals[i]) + ")"

                            outTxt += self.pindentComment(
                                f"bDescriptorType[{k}]" + str_, 1
                            )
                            i += 1
                            j -= 1

                        wDescriptorLength = 0
                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            wDescriptorLength += inVals[i]
                            i += 1
                            j -= 1

                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            wDescriptorLength += inVals[i] << 8
                            outTxt += self.pindentComment(
                                f"wDescriptorLength[{k}] {wDescriptorLength}",
                                2,
                            )
                            i += 1
                            j -= 1

                elif bDescriptorType == 0x29:
                    # Hub
                    bNbrPorts = 0
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bNbrPorts = inVals[i]
                        outTxt += self.pindentComment("bNbrPorts", 1)
                        i += 1
                        j -= 1

                    wHubCharacteristics = 0
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        wHubCharacteristics += inVals[i]
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        wHubCharacteristics += inVals[i] << 8
                        outTxt += self.pindentComment("wHubCharacteristics", 2)
                        i += 1
                        j -= 1

                    bPwrOn2PwrGood = 0
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bPwrOn2PwrGood = inVals[i]
                        outTxt += self.pindentComment(
                            "bPwrOn2PwrGood " + (bPwrOn2PwrGood * 2) + "ms", 1
                        )
                        i += 1
                        j -= 1

                    bHubContrCurrent = 0
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bHubContrCurrent = inVals[i]
                        outTxt += self.pindentComment(
                            "bHubContrCurrent " + (bHubContrCurrent * 1) + " mA", 1
                        )
                        i += 1
                        j -= 1

                    hasP = False
                    for k in range(1, bNbrPorts + 1, 8):
                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            i += 1
                            j -= 1
                            hasP = True

                    if bNbrPorts > 0 and hasP:
                        outTxt += self.pindentComment(
                            "DeviceRemovable", (bNbrPorts // 8) + 1
                        )

                    hasP = False
                    for k in range(1, bNbrPorts + 1, 8):
                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            i += 1
                            j -= 1
                            hasP = True

                    if bNbrPorts > 0 and hasP:
                        outTxt += self.pindentComment(
                            "PortPwrCtrlMask", (bNbrPorts // 8) + 1
                        )

                elif bDescriptorType == 0x01 or bDescriptorType == 0x06:
                    # device or device qualifier

                    bcdUSB = 0
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bcdL = inVals[i] & 0x0F
                        bcdH = (inVals[i] & 0xF0) >> 4
                        bcdUSB = (bcdL + (bcdH * 10)) / 100
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bcdL = inVals[i] & 0x0F
                        bcdH = (inVals[i] & 0xF0) >> 4
                        bcdUSB += bcdL + (bcdH * 10)
                        i += 1
                        j -= 1
                        outTxt += self.pindentComment(f"bcdUSB {bcdUSB:2.2f}", 2)

                    bDeviceClass = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bDeviceClass = inVals[i]
                        outTxt += self.pindentComment(
                            "bDeviceClass " + self.pDeviceClass(bDeviceClass), 1
                        )
                        i += 1
                        j -= 1

                    bDeviceSubClass = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bDeviceSubClass = inVals[i]
                        outTxt += self.pindentComment(
                            "bDeviceSubClass "
                            + self.pDeviceSubClass(bDeviceClass, bDeviceSubClass),
                            1,
                        )
                        i += 1
                        j -= 1

                    bDeviceProtocol = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bDeviceProtocol = inVals[i]
                        outTxt += self.pindentComment(
                            "bDeviceProtocol "
                            + self.pDeviceProtocol(
                                bDeviceClass, bDeviceSubClass, bDeviceProtocol
                            ),
                            1,
                        )
                        i += 1
                        j -= 1

                    bMaxPacketSize0 = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bMaxPacketSize0 = inVals[i]
                        outTxt += self.pindentComment(
                            f"bMaxPacketSize0 {bMaxPacketSize0}", 1
                        )
                        i += 1
                        j -= 1

                    if bDescriptorType == 0x01:
                        idVendor = 0
                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            idVendor = inVals[i]
                            i += 1
                            j -= 1

                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            idVendor += inVals[i] << 8
                            i += 1
                            j -= 1
                            outTxt += self.pindentComment(
                                "idVendor " + pHex(idVendor), 2
                            )

                        idProduct = 0
                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            idProduct = inVals[i]
                            i += 1
                            j -= 1

                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            idProduct += inVals[i] << 8
                            i += 1
                            j -= 1
                            outTxt += self.pindentComment(
                                "idProduct " + pHex(idProduct), 2
                            )

                        bcdDevice = 0
                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            bcdL = inVals[i] & 0x0F
                            bcdH = (inVals[i] & 0xF0) >> 4
                            bcdDevice = (bcdL + (bcdH * 10)) / 100
                            i += 1
                            j -= 1

                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            bcdDevice += inVals[i]
                            bcdL = inVals[i] & 0x0F
                            bcdH = (inVals[i] & 0xF0) >> 4
                            bcdDevice += bcdL + (bcdH * 10)
                            i += 1
                            j -= 1
                            outTxt += self.pindentComment(
                                f"bcdDevice {bcdDevice:2.2f}", 2
                            )

                        if i < len(inVals) and j > 0:
                            iManufacturer = inVals[i]
                            outTxt += pHexC(iManufacturer)
                            outTxt += self.pindentComment(
                                "iManufacturer (String Index)", 1
                            )
                            i += 1
                            j -= 1

                        if i < len(inVals) and j > 0:
                            iProduct = inVals[i]
                            outTxt += pHexC(iProduct)
                            outTxt += self.pindentComment("iProduct (String Index)", 1)
                            i += 1
                            j -= 1

                        if i < len(inVals) and j > 0:
                            iSerialNumber = inVals[i]
                            outTxt += pHexC(iSerialNumber)
                            outTxt += self.pindentComment(
                                "iSerialNumber (String Index)", 1
                            )
                            i += 1
                            j -= 1

                    bNumConfigurations = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bNumConfigurations = inVals[i]
                        outTxt += self.pindentComment(
                            f"bNumConfigurations {bNumConfigurations}", 1
                        )
                        i += 1
                        j -= 1

                    if bDescriptorType == 0x06:
                        if i < len(inVals) and j > 0:
                            outTxt += pHexC(inVals[i])
                            outTxt += self.pindentComment("bReserved", 1)
                            i += 1
                            j -= 1

                elif (
                    bDescriptorType == 0x02 or bDescriptorType == 0x07
                ):  # config or other speed config
                    wTotalLength = 0
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        wTotalLength += inVals[i]
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        wTotalLength += inVals[i] << 8
                        outTxt += self.pindentComment(f"wTotalLength {wTotalLength}", 2)
                        i += 1
                        j -= 1

                    bNumInterfaces = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bNumInterfaces = inVals[i]
                        outTxt += self.pindentComment(
                            f"bNumInterfaces {bNumInterfaces}", 1
                        )
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        bConfigurationValue = inVals[i]
                        outTxt += pHexC(bConfigurationValue)
                        outTxt += self.pindentComment("bConfigurationValue", 1)
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        iConfiguration = inVals[i]
                        outTxt += pHexC(iConfiguration)
                        outTxt += self.pindentComment(
                            "iConfiguration (String Index)", 1
                        )
                        i += 1
                        j -= 1

                    bmAttributes = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bmAttributes = inVals[i]
                        str_ = ""
                        if (bmAttributes & (1 << 5)) != 0:
                            str_ += " Remote Wakeup,"

                        if (bmAttributes & (1 << 6)) != 0:
                            str_ += " Self Powered,"

                        if str_ != "":
                            str_ = str_[:-1]

                        outTxt += self.pindentComment("bmAttributes" + str_, 1)
                        i += 1
                        j -= 1

                    bMaxPower = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bMaxPower = inVals[i]
                        outTxt += self.pindentComment(f"bMaxPower {bMaxPower * 2}mA", 1)
                        i += 1
                        j -= 1

                elif bDescriptorType == 0x04:  # interface
                    bInterfaceNumber = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bInterfaceNumber = inVals[i]
                        outTxt += self.pindentComment(
                            f"bInterfaceNumber {bInterfaceNumber}", 1
                        )
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        bAlternateSetting = inVals[i]
                        outTxt += pHexC(bAlternateSetting)
                        outTxt += self.pindentComment("bAlternateSetting", 1)
                        i += 1
                        j -= 1

                    bNumEndpoints = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bNumEndpoints = inVals[i]
                        outTxt += self.pindentComment(
                            f"bNumEndpoints {bNumEndpoints}", 1
                        )
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bInterfaceClass = inVals[i]
                        outTxt += self.pindentComment(
                            "bInterfaceClass" + self.pInterfaceClass(bInterfaceClass), 1
                        )
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bInterfaceSubClass = inVals[i]
                        outTxt += self.pindentComment(
                            "bInterfaceSubClass"
                            + pInterfaceSubClass(bInterfaceClass, bInterfaceSubClass),
                            1,
                        )
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        bInterfaceProtocol = inVals[i]
                        outTxt += pHexC(bInterfaceProtocol)
                        outTxt += self.pindentComment("bInterfaceProtocol", 1)
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        iInterface = inVals[i]
                        outTxt += pHexC(iInterface)
                        outTxt += self.pindentComment("iInterface (String Index)", 1)
                        i += 1
                        j -= 1

                elif bDescriptorType == 0x05:  # endpoint
                    bEndpointAddress = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bEndpointAddress = inVals[i]
                        str_ = ""
                        if bEndpointAddress != 0:
                            if (bEndpointAddress & 0x80) != 0:
                                str_ = " (IN/D2H)"

                            else:
                                str_ = " (OUT/H2D)"

                        else:
                            str_ = " (Control)"

                        outTxt += self.pindentComment("bEndpointAddress" + str_, 1)
                        i += 1
                        j -= 1

                    bmAttributes = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bmAttributes = inVals[i]
                        str_ = ""
                        if (bmAttributes & 0x03) == 0x00:
                            str_ = " (Control)"

                        elif (bmAttributes & 0x03) == 0x01:
                            str_ = " (Isochronous, "

                            if ((bmAttributes >> 2) & 0x03) == 0x00:
                                str_ += "No Sync, "

                            elif ((bmAttributes >> 2) & 0x03) == 0x01:
                                str_ += "Async, "

                            elif ((bmAttributes >> 2) & 0x03) == 0x02:
                                str_ += "Adaptive, "

                            elif ((bmAttributes >> 2) & 0x03) == 0x03:
                                str_ += "Sync, "

                            if ((bmAttributes >> 4) & 0x03) == 0x00:
                                str_ += "Data EP)"

                            elif ((bmAttributes >> 4) & 0x03) == 0x01:
                                str_ += "Feedback EP)"

                            elif ((bmAttributes >> 4) & 0x03) == 0x02:
                                str_ += "Implicit Feedback EP)"

                            elif ((bmAttributes >> 4) & 0x03) == 0x03:
                                str_ += "Reserved)"

                        elif (bmAttributes & 0x03) == 0x02:
                            str_ = " (Bulk)"

                        elif (bmAttributes & 0x03) == 0x03:
                            str_ = " (Interrupt)"

                        outTxt += self.pindentComment("bmAttributes" + str_, 1)
                        i += 1
                        j -= 1

                    wMaxPacketSize = 0
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        wMaxPacketSize += inVals[i]
                        i += 1
                        j -= 1

                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        wMaxPacketSize += inVals[i] << 8
                        wMaxPacketSize_ = wMaxPacketSize & 0x07FF
                        additional = (wMaxPacketSize & 0xE000) >> 11
                        str_ = ""
                        if additional > 0:
                            str_ = f" + {additional}"

                        outTxt += self.pindentComment(
                            f"wMaxPacketSize {wMaxPacketSize_}" + str_, 2
                        )
                        i += 1
                        j -= 1

                    bInterval = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bInterval = inVals[i]
                        outTxt += self.pindentComment(
                            f"bInterval {bInterval} (unit depends on device speed)", 1
                        )
                        i += 1
                        j -= 1

                    if bInterfaceClass == 0x01 and bInterfaceSubClass == 0x02:
                        if i < len(inVals) and j > 0:
                            bRefresh = inVals[i]
                            outTxt += pHexC(bRefresh)
                            outTxt += self.pindentComment("bRefresh", 1)
                            i += 1
                            j -= 1

                        if i < len(inVals) and j > 0:
                            bSyncAddress = inVals[i]
                            outTxt += pHexC(bSyncAddress)
                            outTxt += self.pindentComment("bSyncAddress", 1)
                            i += 1
                            j -= 1

                elif (
                    bDescriptorType == 0x25
                    and bInterfaceClass == 0x01
                    and bInterfaceSubClass == 0x02
                ):
                    # CS_ENDPOINT for Audio Streaming
                    bDescriptorSubtype = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bDescriptorSubtype = inVals[i]
                        if bDescriptorSubtype == 0x01:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype (CS_ENDPOINT -> EP_GENERAL)", 1
                            )
                            i += 1
                            j -= 1
                            bmAttributes = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bmAttributes = inVals[i]
                                atrstr = ""
                                if (bmAttributes & 0x01) != 0:
                                    atrstr += "Sampling Freq Control, "

                                if (bmAttributes & 0x02) != 0:
                                    atrstr += "Pitch Control, "

                                if (bmAttributes & 0x04) != 0:
                                    atrstr += "Packet Padding"

                                if atrstr.length <= 0:
                                    atrstr = "None"

                                atrstr = re.sub(r"^[,\s]+|[,\s]+$", "", atrstr)
                                atrstr = re.sub(r"\s*,\s*", ",", atrstr)
                                atrstr = atrstr.trim()
                                if atrstr.length > 0:
                                    atrstr = " (" + atrstr + ")"

                                outTxt += self.pindentComment(
                                    "bmAttributes" + atrstr, 1
                                )
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                bLockDelayUnits = inVals[i]
                                outTxt += pHexC(bLockDelayUnits)
                                outTxt += self.pindentComment("bLockDelayUnits", 1)
                                i += 1
                                j -= 1

                            wLockDelay = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wLockDelay = inVals[i]
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wLockDelay += inVals[i] << 8
                                outTxt += self.pindentComment(
                                    f"wLockDelay {wLockDelay}", 2
                                )
                                i += 1
                                j -= 1

                        else:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype Unknown", 1
                            )
                            i += 1
                            j -= 1

                elif (
                    bDescriptorType == 0x24
                    and bInterfaceClass == 0x01
                    and bInterfaceSubClass == 0x01
                ):
                    # CS_INTERFACE, Audio, Audio Control

                    bDescriptorSubtype = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bDescriptorSubtype = inVals[i]
                        if bDescriptorSubtype == 0x01:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype (CS_INTERFACE -> HEADER)", 1
                            )
                            i += 1
                            j -= 1
                            bcdADC = 0
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bcdL = inVals[i] & 0x0F
                                bcdH = (inVals[i] & 0xF0) >> 4
                                bcdADC = (bcdL + (bcdH * 10)) / 100
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bcdL = inVals[i] & 0x0F
                                bcdH = (inVals[i] & 0xF0) >> 4
                                bcdADC += bcdL + (bcdH * 10)
                                i += 1
                                j -= 1
                                outTxt += self.pindentComment(
                                    f"bcdADC {bcdADC:2.2f}", 2
                                )

                            wTotalLength = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wTotalLength = inVals[i]
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wTotalLength += inVals[i] << 8
                                outTxt += self.pindentComment(
                                    f"wTotalLength {wTotalLength}", 2
                                )
                                i += 1
                                j -= 1

                            bincollection = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bincollection = inVals[i]
                                outTxt += self.pindentComment(
                                    "bincollection " + pHex(bincollection), 1
                                )
                                i += 1
                                j -= 1

                            while j > 0:
                                baInterfaceNr = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    baInterfaceNr = inVals[i]
                                    outTxt += self.pindentComment(
                                        f"baInterfaceNr {baInterfaceNr}", 1
                                    )
                                    i += 1
                                    j -= 1

                        elif bDescriptorSubtype == 0x02:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype (CS_INTERFACE -> INPUT_TERMINAL)", 1
                            )
                            i += 1
                            j -= 1
                            if i < len(inVals) and j > 0:
                                bTerminalID = inVals[i]
                                outTxt += pHexC(bTerminalID)
                                outTxt += self.pindentComment("bTerminalID", 1)
                                i += 1
                                j -= 1

                            wTerminalType = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wTerminalType = inVals[i]
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wTerminalType += inVals[i] << 8
                                outTxt += self.pindentComment(
                                    "wTerminalType" + self.pTerminalType(wTerminalType),
                                    2,
                                )
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                bAssocTerminal = inVals[i]
                                outTxt += pHexC(bAssocTerminal)
                                outTxt += self.pindentComment("bAssocTerminal", 1)
                                i += 1
                                j -= 1

                            bNrChannels = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bNrChannels = inVals[i]
                                outTxt += self.pindentComment(
                                    f"bNrChannels {bNrChannels}", 1
                                )
                                i += 1
                                j -= 1

                            wChannelConfig = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wChannelConfig = inVals[i]
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wChannelConfig += inVals[i] << 8
                                outTxt += self.pindentComment(
                                    "wChannelConfig"
                                    + self.pChannelConfig(wChannelConfig),
                                    2,
                                )
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                iChannelNames = inVals[i]
                                outTxt += pHexC(iChannelNames)
                                outTxt += self.pindentComment("iChannelNames", 1)
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                iTerminal = inVals[i]
                                outTxt += pHexC(iTerminal)
                                outTxt += self.pindentComment("iTerminal", 1)
                                i += 1
                                j -= 1

                        elif bDescriptorSubtype == 0x03:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype (CS_INTERFACE -> OUTPUT_TERMINAL)",
                                1,
                            )
                            i += 1
                            j -= 1
                            if i < len(inVals) and j > 0:
                                bTerminalID = inVals[i]
                                outTxt += pHexC(bTerminalID)
                                outTxt += self.pindentComment("bTerminalID", 1)
                                i += 1
                                j -= 1

                            wTerminalType = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wTerminalType = inVals[i]
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wTerminalType += inVals[i] << 8
                                outTxt += self.pindentComment(
                                    "wTerminalType" + self.pTerminalType(wTerminalType),
                                    2,
                                )
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                bAssocTerminal = inVals[i]
                                outTxt += pHexC(bAssocTerminal)
                                outTxt += self.pindentComment("bAssocTerminal", 1)
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                bSourceID = inVals[i]
                                outTxt += pHexC(bSourceID)
                                outTxt += self.pindentComment("bSourceID", 1)
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                iTerminal = inVals[i]
                                outTxt += pHexC(iTerminal)
                                outTxt += self.pindentComment("iTerminal", 1)
                                i += 1
                                j -= 1

                        elif bDescriptorSubtype == 0x04:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype (CS_INTERFACE -> MIXER_UNIT)", 1
                            )
                            i += 1
                            j -= 1
                            if i < len(inVals) and j > 0:
                                bUnitID = inVals[i]
                                outTxt += pHexC(bUnitID)
                                outTxt += self.pindentComment("bUnitID", 1)
                                i += 1
                                j -= 1

                            bNrInPins = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bNrInPins = inVals[i]
                                outTxt += self.pindentComment(
                                    f"bNrInPins {bNrInPins}", 1
                                )
                                i += 1
                                j -= 1

                            for pinIdx in range(bNrInPins):
                                baSourceID = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    baSourceID = inVals[i]
                                    outTxt += self.pindentComment(
                                        f"baSourceID[{pinIdx}] = {baSourceID:x}", 1
                                    )
                                    i += 1
                                    j -= 1

                            bNrChannels = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bNrChannels = inVals[i]
                                outTxt += self.pindentComment(
                                    f"bNrChannels {bNrChannels}", 1
                                )
                                i += 1
                                j -= 1

                            wChannelConfig = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wChannelConfig = inVals[i]
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wChannelConfig += inVals[i] << 8
                                outTxt += self.pindentComment(
                                    "wChannelConfig"
                                    + self.pChannelConfig(wChannelConfig),
                                    2,
                                )
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                iChannelNames = inVals[i]
                                outTxt += pHexC(iChannelNames)
                                outTxt += self.pindentComment("iChannelNames", 1)
                                i += 1
                                j -= 1

                            while j > 1:
                                if i < len(inVals) and j > 0:
                                    bmControls = inVals[i]
                                    outTxt += pHexC(bmControls)
                                    outTxt += self.pindentComment("bmControls", 1)
                                    i += 1
                                    j -= 1

                            if i < len(inVals) and j > 0:
                                iMixer = inVals[i]
                                outTxt += pHexC(iMixer)
                                outTxt += self.pindentComment("iMixer", 1)
                                i += 1
                                j -= 1

                        elif bDescriptorSubtype == 0x06:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype (CS_INTERFACE -> FEATURE_UNIT)", 1
                            )
                            i += 1
                            j -= 1
                            bUnitID = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bUnitID = inVals[i]
                                outTxt += self.pindentComment("bUnitID", 1)
                                i += 1
                                j -= 1

                            bSourceID = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bSourceID = inVals[i]
                                outTxt += self.pindentComment("bSourceID", 1)
                                i += 1
                                j -= 1

                            bControlSize = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bControlSize = inVals[i]
                                outTxt += self.pindentComment(
                                    f"bControlSize {bControlSize}", 1
                                )
                                i += 1
                                j -= 1

                            arrSz = bLength - 1 - 6
                            arrSz /= 2
                            for bmaControlsIdx in range(arrSz):
                                bmaControls = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    bmaControls = inVals[i]
                                    i += 1
                                    j -= 1

                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    bmaControls += inVals[i] << 8
                                    bmaAudCtrls = ""
                                    if (bmaControls & 0x01) != 0:
                                        bmaAudCtrls += "Mute, "

                                    if (bmaControls & 0x02) != 0:
                                        bmaAudCtrls += "Volume, "

                                    if (bmaControls & 0x04) != 0:
                                        bmaAudCtrls += "Bass, "

                                    if (bmaControls & 0x08) != 0:
                                        bmaAudCtrls += "Mid, "

                                    if (bmaControls & 0x10) != 0:
                                        bmaAudCtrls += "Trebel, "

                                    if (bmaControls & 0x20) != 0:
                                        bmaAudCtrls += "Graphic, "

                                    if (bmaControls & 0x40) != 0:
                                        bmaAudCtrls += "Automatic, "

                                    if (bmaControls & 0x80) != 0:
                                        bmaAudCtrls += "Delay, "

                                    bmaAudCtrls = re.sub(
                                        r"^[,\s]+|[,\s]+$", "", bmaAudCtrls
                                    )
                                    bmaAudCtrls = re.sub(r"s*,\s*", ",", bmaAudCtrls)
                                    bmaAudCtrls = bmaAudCtrls.trim()
                                    if bmaAudCtrls.length > 0:
                                        bmaAudCtrls = " (" + bmaAudCtrls + ")"

                                    else:
                                        bmaAudCtrls = " (None)"

                                    outTxt += self.pindentComment(
                                        f"bmaControls[{bmaControlsIdx}]" + bmaAudCtrls,
                                        2,
                                    )
                                    i += 1
                                    j -= 1

                            if i < len(inVals) and j > 0:
                                iFeature = inVals[i]
                                outTxt += pHexC(iFeature)
                                outTxt += self.pindentComment("iFeature", 1)
                                i += 1
                                j -= 1

                        else:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype Unknown", 1
                            )
                            i += 1
                            j -= 1

                elif (
                    bDescriptorType == 0x24
                    and bInterfaceClass == 0x01
                    and bInterfaceSubClass == 0x02
                ):
                    # CS_INTERFACE, Audio, Audio Streaming
                    bDescriptorSubtype = -1
                    if i < len(inVals) and j > 0:
                        outTxt += pHexC(inVals[i])
                        bDescriptorSubtype = inVals[i]
                        if bDescriptorSubtype == 0x01:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype (CS_INTERFACE -> AS_GENERAL)", 1
                            )
                            i += 1
                            j -= 1
                            if i < len(inVals) and j > 0:
                                bTerminalLink = inVals[i]
                                outTxt += pHexC(bTerminalLink)
                                outTxt += self.pindentComment("bTerminalLink", 1)
                                i += 1
                                j -= 1

                            bDelay = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bDelay = inVals[i]
                                outTxt += self.pindentComment(f"bDelay {bDelay}", 1)
                                i += 1
                                j -= 1

                            wFormatTag = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wFormatTag = inVals[i]
                                i += 1
                                j -= 1

                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                wFormatTag += inVals[i] << 8
                                outTxt += self.pindentComment(
                                    "wFormatTag" + self.pWaveFormat(wFormatTag), 2
                                )
                                i += 1
                                j -= 1

                        elif bDescriptorSubtype == 0x02:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype (CS_INTERFACE -> FORMAT_TYPE)", 1
                            )
                            i += 1
                            j -= 1
                            bFormatType = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bFormatType = inVals[i]
                                outTxt += self.pindentComment(
                                    f"bFormatType {bFormatType}", 1
                                )
                                i += 1
                                j -= 1

                            if bFormatType == 1 or bFormatType == 3:
                                bNrChannels = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    bNrChannels = inVals[i]
                                    if bNrChannels == 1:
                                        outTxt += self.pindentComment(
                                            "bNrChannels (Mono)", 1
                                        )

                                    elif bNrChannels == 2:
                                        outTxt += self.pindentComment(
                                            "bNrChannels (Stereo)", 1
                                        )

                                    else:
                                        outTxt += self.pindentComment(
                                            f"bNrChannels {bNrChannels}", 1
                                        )

                                    i += 1
                                    j -= 1

                                bSubFrameSize = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    bSubFrameSize = inVals[i]
                                    outTxt += self.pindentComment(
                                        f"bSubFrameSize {bSubFrameSize}", 1
                                    )
                                    i += 1
                                    j -= 1

                                bBitResolution = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    bBitResolution = inVals[i]
                                    outTxt += self.pindentComment(
                                        f"bBitResolution {bBitResolution}",
                                        1,
                                    )
                                    i += 1
                                    j -= 1

                            elif bFormatType == 2:
                                wMaxBitRate = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    wMaxBitRate = inVals[i]
                                    i += 1
                                    j -= 1

                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    wMaxBitRate += inVals[i] << 8
                                    outTxt += self.pindentComment(
                                        f"wMaxBitRate {wMaxBitRate} kbits/s",
                                        2,
                                    )
                                    i += 1
                                    j -= 1

                                wSamplesPerFrame = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    wSamplesPerFrame = inVals[i]
                                    i += 1
                                    j -= 1

                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    wSamplesPerFrame += inVals[i] << 8
                                    outTxt += self.pindentComment(
                                        f"wSamplesPerFrame {wMaxBitRate}",
                                        2,
                                    )
                                    i += 1
                                    j -= 1

                            else:
                                self.possible_errors += 1

                            bSamFreqType = -1
                            if i < len(inVals) and j > 0:
                                outTxt += pHexC(inVals[i])
                                bSamFreqType = inVals[i]
                                i += 1
                                j -= 1

                            if bSamFreqType == 0:
                                outTxt += self.pindentComment(
                                    "bSamFreqType (Continuous)", 1
                                )
                                tLowerSamFreq = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    tLowerSamFreq = inVals[i]
                                    i += 1
                                    j -= 1

                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    tLowerSamFreq += inVals[i] << 8
                                    i += 1
                                    j -= 1

                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    tLowerSamFreq += inVals[i] << 16
                                    outTxt += self.pindentComment(
                                        f"tLowerSamFreq {tLowerSamFreq} Hz",
                                        2,
                                    )
                                    i += 1
                                    j -= 1

                                tUpperSamFreq = -1
                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    tUpperSamFreq = inVals[i]
                                    i += 1
                                    j -= 1

                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    tUpperSamFreq += inVals[i] << 8
                                    i += 1
                                    j -= 1

                                if i < len(inVals) and j > 0:
                                    outTxt += pHexC(inVals[i])
                                    tUpperSamFreq += inVals[i] << 16
                                    outTxt += self.pindentComment(
                                        f"tUpperSamFreq {tUpperSamFreq} Hz",
                                        2,
                                    )
                                    i += 1
                                    j -= 1

                            else:
                                outTxt += self.pindentComment(
                                    f"bSamFreqType {bSamFreqType}", 1
                                )
                                for freqCnter in range(bSamFreqType):
                                    if j <= 0:
                                        break

                                    tSamFreq = -1
                                    if i < len(inVals) and j > 0:
                                        outTxt += pHexC(inVals[i])
                                        tSamFreq = inVals[i]
                                        i += 1
                                        j -= 1

                                    if i < len(inVals) and j > 0:
                                        outTxt += pHexC(inVals[i])
                                        tSamFreq += inVals[i] << 8
                                        i += 1
                                        j -= 1

                                    if i < len(inVals) and j > 0:
                                        outTxt += pHexC(inVals[i])
                                        tSamFreq += inVals[i] << 16
                                        outTxt += self.pindentComment(
                                            f"tSamFreq[{freqCnter + 1}] {tSamFreq} Hz",
                                            2,
                                        )
                                        i += 1
                                        j -= 1

                        else:
                            outTxt += self.pindentComment(
                                "bDescriptorSubtype Unknown", 1
                            )
                            i += 1
                            j -= 1

                else:
                    self.possible_errors += 1
                    # all other types are not supported

                # print the rest
                while (i < len(inVals)) and (j > 0):
                    outTxt += pHexC(inVals[i])
                    self.possible_errors += 1
                    i += 1
                    j -= 1

                outTxt += "\n"

        outTxt += f"// {len(inVals)} bytes\n"
        return outTxt

    def best_guess(self, inTxt):
        # pylint: disable=broad-exception-caught
        try:
            self.parse_hidrepdesc(inTxt)
        except Exception:
            self.possible_errors += 1
        hid_errs = self.possible_errors

        try:
            self.parse_stddesc(inTxt)
        except Exception:
            self.possible_errors += 1
        stddesc_errs = self.possible_errors

        try:
            self.parse_stdrequest(inTxt)
        except Exception:
            self.possible_errors += 1
        stdreq_errs = self.possible_errors

        if hid_errs < stddesc_errs and hid_errs < stdreq_errs:
            outTxt = self.parse_hidrepdesc(inTxt)
            outTxt += "\n// best guess: USB HID Report Descriptor"

        elif stddesc_errs < hid_errs and stddesc_errs < stdreq_errs:
            outTxt = self.parse_stddesc(inTxt)
            outTxt += "\n// best guess: USB Standard Descriptor"

        elif stdreq_errs < hid_errs and stdreq_errs < stddesc_errs:
            outTxt = self.parse_stdrequest(inTxt)
            outTxt += "\n// best guess: USB Standard Request"

        elif hid_errs <= stddesc_errs and hid_errs <= stdreq_errs:
            outTxt = self.parse_hidrepdesc(inTxt)
            outTxt += "\n// best guess: USB HID Report Descriptor"

        elif stddesc_errs <= hid_errs and stddesc_errs <= stdreq_errs:
            self.parse_stddesc(inTxt)
            outTxt += "\n// best guess: USB Standard Descriptor"

        elif stdreq_errs <= hid_errs and stdreq_errs <= stddesc_errs:
            self.parse_stdrequest(inTxt)
            outTxt += "\n// best guess: USB Standard Request"

        else:
            outTxt = "// unable to determine data packet type"

        return outTxt

    def parse_stdrequest(self, inTxt):
        self.possible_errors = 0
        inVals = get_bytes(inTxt)

        outTxt = ""

        bmRequestType = -1
        bRequest = -1
        wValue = -1
        wIndex = -1
        wLength = -1

        if len(inVals) != 8:
            # all standard requests are supposed to be 8 bytes long
            self.possible_errors = 8

        # pylint: disable=consider-using-enumerate
        for i in range(len(inVals)):
            if i == 0:
                bmRequestType = inVals[i]

                outTxt += pHexC(bmRequestType)
                str_ = "bmRequestType: "

                if (bmRequestType & 0x80) != 0:
                    str_ += "Dir: D2H, "

                else:
                    str_ += "Dir: H2D, "

                if ((bmRequestType >> 5) & 0x03) == 0x00:
                    str_ += "Type: Standard, "

                elif ((bmRequestType >> 5) & 0x03) == 0x01:
                    str_ += "Type: Class, "

                elif ((bmRequestType >> 5) & 0x03) == 0x02:
                    str_ += "Type: Vendor, "

                elif ((bmRequestType >> 5) & 0x03) == 0x03:
                    str_ += "Type: Reserved, "
                    self.possible_errors += 1

                if (bmRequestType & 0x1F) == 0x00:
                    str_ += "Recipient: Device"

                elif (bmRequestType & 0x1F) == 0x01:
                    str_ += "Recipient: Interface"

                elif (bmRequestType & 0x1F) == 0x02:
                    str_ += "Recipient: Endpoint"

                elif (bmRequestType & 0x1F) == 0x03:
                    str_ += "Recipient: Other"

                else:
                    str_ += "Recipient: Reserved"
                    self.possible_errors += 1

                outTxt += self.pindentComment(str_, 1)

            elif i == 1:
                bRequest = inVals[i]
                outTxt += pHexC(bRequest)
                str_ = "bRequest"
                if ((bmRequestType >> 5) & 0x03) == 0x00:
                    tbl = [
                        "Get Status",
                        "Clear Feature",
                        "Reserved",
                        "Set Feature",
                        "Reserved",
                        "Set Address",
                        "Get Descriptor",
                        "Set Descriptor",
                        "Get Config",
                        "Set Config",
                        "Get Interface",
                        "Set Interface",
                        "Sync Frame",
                    ]
                    if bRequest < len(tbl):
                        str_ += " (" + tbl[bRequest] + ")"
                        if tbl[bRequest] == "Reserved":
                            self.possible_errors += 1

                outTxt += self.pindentComment(str_, 1)

            elif i == 2:
                wValue = inVals[i]
                outTxt += pHexC(wValue)
                if ((bmRequestType >> 5) & 0x03) == 0x00 and (
                    bRequest == 0x06 or bRequest == 0x07
                ):
                    outTxt += self.pindentComment(
                        f"wValue[0:7]  Desc Index: {wValue}", 1
                    )

            elif i == 3:
                wValue += inVals[i] << 8
                outTxt += pHexC(inVals[i])
                if ((bmRequestType >> 5) & 0x03) == 0x00:
                    if bRequest == 0x06 or bRequest == 0x07:
                        outTxt += self.pindentComment(
                            "wValue[8:15] Desc Type:" + self.pDescriptorType(inVals[i]),
                            1,
                        )

                    elif bRequest == 0x01 or bRequest == 0x03:
                        outTxt += self.pindentComment(
                            f"wValue Feature Selector: {wValue}", 2
                        )

                    elif bRequest == 0x05:
                        outTxt += self.pindentComment(
                            f"wValue Device Addr: {wValue}", 2
                        )

                    elif bRequest == 0x09:
                        outTxt += self.pindentComment(f"wValue Config Num: {wValue}", 2)

                    elif bRequest == 0x0B:
                        outTxt += self.pindentComment(
                            f"wValue Alt Setting: {wValue}", 2
                        )

                    else:
                        outTxt += self.pindentComment("wValue = " + pHex(wValue), 2)

                else:
                    outTxt += self.pindentComment("wValue[0:15] = " + pHex(wValue), 2)

            elif i == 4:
                wIndex = inVals[i]
                outTxt += pHexC(wIndex)

            elif i == 5:
                wIndex += inVals[i] << 8
                outTxt += pHexC(inVals[i])
                if ((bmRequestType >> 5) & 0x03) == 0x00:
                    if (
                        (bmRequestType == 0x01 and bRequest == 0x01)
                        or (bmRequestType == 0x81 and bRequest == 0x0A)
                        or (bmRequestType == 0x81 and bRequest == 0x00)
                        or (bmRequestType == 0x01 and bRequest == 0x03)
                        or (bmRequestType == 0x01 and bRequest == 0x0B)
                    ):
                        outTxt += self.pindentComment(f"wIndex Interface: {wIndex}", 2)

                    elif (
                        (bmRequestType == 0x02 and bRequest == 0x01)
                        or (bmRequestType == 0x82 and bRequest == 0x00)
                        or (bmRequestType == 0x02 and bRequest == 0x03)
                        or (bmRequestType == 0x82 and bRequest == 0x0C)
                    ):
                        str_ = ""
                        if wIndex & 0x80 != 0:
                            str_ += " (IN/D2H)"

                        else:
                            str_ += " (OUT/H2D)"

                        outTxt += self.pindentComment(
                            "wIndex Endpoint: " + pHex(wIndex) + str_, 2
                        )

                    elif bRequest == 0x06 or bRequest == 0x07:
                        outTxt += self.pindentComment(
                            "wIndex Language ID: " + pHex(wIndex), 2
                        )

                    else:
                        outTxt += self.pindentComment("wIndex = " + pHex(wIndex), 2)

                else:
                    outTxt += self.pindentComment("wIndex = " + pHex(wIndex), 2)

            elif i == 6:
                wLength = inVals[i]
                outTxt += pHexC(wLength)

            elif i == 7:
                wLength += inVals[i] << 8
                outTxt += pHexC(inVals[i])
                outTxt += self.pindentComment(f"wLength = {wLength}", 2)

            else:
                outTxt += pHexC(inVals[i]) + "\n"
                self.possible_errors += 1

        outTxt += f"\n# {len(inVals)} bytes\n"
        return outTxt
