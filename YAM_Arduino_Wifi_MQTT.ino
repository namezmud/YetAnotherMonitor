#include <DallasTemperature.h>
#include <UnoWiFiDevEd.h>

#define REQUIRESALARMS false
#define CONNECTOR "mqtt"
#define TEMP_TOPIC "YarraRiverReptiles/data/temperature"
#define FLOW_TOPIC "YarraRiverReptiles/data/flow"

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 11
#define TEMPERATURE_PRECISION 10 // Mid resolution

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

int numberOfDevices; // Number of temperature devices found

DeviceAddress tempDeviceAddress; // We'll use this variable to store a found device address

// which pin to use for reading the sensor? can use any pin!
#define FLOWSENSORPIN 12

// count how many pulses!
volatile uint16_t pulses = 0;
// track the state of the pulse pin
volatile uint8_t lastflowpinstate;
// you can try to keep time of how long it is between pulses
volatile uint32_t lastflowratetimer = 0;
// and use that to calculate a flow rate
volatile float flowrate;

// Interrupt is called once a millisecond, looks for any pulses from the sensor!
SIGNAL(TIMER0_COMPA_vect) {
  uint8_t x = digitalRead(FLOWSENSORPIN);

  if (x == lastflowpinstate) {
    lastflowratetimer++;
    return; // nothing changed!
  }

  if (x == HIGH) {
    //low to high transition!
    pulses++;
  }
  lastflowpinstate = x;
  flowrate = 1000.0;
  flowrate /= lastflowratetimer;  // in hertz
  lastflowratetimer = 0;
}

void useInterrupt(boolean v) {
  if (v) {
    // Timer0 is already used for millis() - we'll just interrupt somewhere
    // in the middle and call the "Compare A" function above
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
  } else {
    // do not call the interrupt function COMPA anymore
    TIMSK0 &= ~_BV(OCIE0A);
  }
}

void setup(void)
{
  // start serial port
  Serial.begin(9600);
  // Serial.println("Yarra River Reptiles Temperature Monitor.  Based on Dallas Temperature IC Control Library Demo");

  Ciao.begin();

  // Start up the library
  sensors.begin();

  // Grab a count of devices on the wire
  numberOfDevices = sensors.getDeviceCount();

  // locate devices on the bus
  //  Serial.print("Locating devices...");

  Serial.print("Found ");
  Serial.print(numberOfDevices, DEC);
  Serial.println(" devices.");

  // report parasite power requirements
  //Serial.print("Parasite power is: ");
  //if (sensors.isParasitePowerMode()) Serial.println("ON");
  //else Serial.println("OFF");

  // Loop through each device, print out address
  for (int i = 0; i < numberOfDevices; i++)
  {
    // Search the wire for address
    if (sensors.getAddress(tempDeviceAddress, i))
    {
      Serial.print("Found device ");
      Serial.print(i, DEC);
      Serial.print(" with address: ");
      Serial.println(ToString(tempDeviceAddress));

      //      Serial.print("Setting resolution to ");
      Serial.println(TEMPERATURE_PRECISION, DEC);

      // set the resolution to TEMPERATURE_PRECISION bit (Each Dallas/Maxim device is capable of several different resolutions)
      sensors.setResolution(tempDeviceAddress, TEMPERATURE_PRECISION);

      Serial.print("Resolution is: ");
      Serial.print(sensors.getResolution(tempDeviceAddress), DEC);
      Serial.println();
    } else {
      Serial.print("Found ghost device at ");
      Serial.print(i, DEC);
      //      Serial.print(" but could not detect address. Check power and cabling");
    }
  }

  pinMode(FLOWSENSORPIN, INPUT);
  digitalWrite(FLOWSENSORPIN, HIGH);
  lastflowpinstate = digitalRead(FLOWSENSORPIN);
  useInterrupt(true);
  Serial.println("Flow Sensor Setup - DONE");

}


void loop(void)
{
  // call sensors.requestTemperatures() to issue a global temperature
  // request to all devices on the bus
  delay(10000);

  sensors.requestTemperatures(); // Send the command to get temperatures

  // Loop through each device, print out temperature data
  for (int i = 0; i < numberOfDevices; i++)
  {
    // Search the wire for address
    if (sensors.getAddress(tempDeviceAddress, i))
    {
      // Output the device ID
      Serial.print("Temperature for device: ");
      Serial.print(ToString(tempDeviceAddress));

      float tempC = sensors.getTempC(tempDeviceAddress);
      Serial.print(" Temp C: ");
      Serial.println(tempC);

      mqttSendTemp(tempDeviceAddress, tempC);


    }
    //else ghost device! Check your power requirements and cabling

  }
  mqttSendFlow(flowrate / 15.0, FLOWSENSORPIN);
}

void mqttSendTemp(DeviceAddress deviceAddress, float tempC) {

  String str = ToString(tempDeviceAddress) + "=" + String(tempC) + "C";
  Serial.println(str);

  Ciao.write(CONNECTOR, TEMP_TOPIC, str.c_str());

}

void mqttSendFlow(float FlowRateLperMin, int pin) {

  String str = "Flow Pin" + String(pin) + " =" + String(FlowRateLperMin) + "L/min";

  Serial.println(str.c_str());

  Ciao.write(CONNECTOR, FLOW_TOPIC, str.c_str());

}

String ToString(DeviceAddress deviceAddress)
{
  String s;
  char byte[3] = "  ";
  for (uint8_t i = 0; i < 8; i++)
  {
    sprintf(byte, "%02X", deviceAddress[i]);
    s += byte;
  }
  return s;
}

