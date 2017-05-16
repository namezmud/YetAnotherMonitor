/** YetAnotherMonitor Particle Photon device
 * Provide temperature dta over mqtt in format accepted by YAM system
 * Tested on Particle Photon.
 */
#include <MQTT.h>

#include "DS18.h"

void callback(char* topic, byte* payload, unsigned int length);

/**
 * if want to use IP address,
 * byte server[] = { XXX,XXX,XXX,XXX };
 * MQTT client(server, 1883, callback);
 * want to use domain name,
 * MQTT client("www.sample.com", 1883, callback);
 **/
MQTT client("raspberrypi", 1883, callback);  // Raspberry Pi is MQTT broker and on local network so use local name
const char* topic = "YarraRiverReptiles/data/temperature";
int interval = 10000; // 10 secs
bool light = true;

// recieve message
// Not used at this stage.
void callback(char* topic, byte* payload, unsigned int length) {
    char p[length + 1];
    memcpy(p, payload, length);
    p[length] = NULL;

    RGB.color(0, 255, 0);  // Green
    delay(1000);
}

DS18 sensor(D3);

void setup() {
    RGB.control(true);
    RGB.color(0, 0, 255);  // Blue
    
    //Set power and ground for sensors either side to allow 3 pin header to be attached to breakout board
    pinMode(D2, OUTPUT);
    pinMode(D4, OUTPUT);
    pinMode(D7, OUTPUT);

    digitalWrite(D2, HIGH);
    digitalWrite(D4, LOW);
    digitalWrite(D7, HIGH);
    

    // connect to the server
    client.connect("sparkclient");

    // publish/subscribe
    if (client.isConnected()) {
        client.publish("YarraRiverReptiles/message","Photon starting up.");
    }
    RGB.color(0, 255, 0);  // Green
}

void loop() {
    // proces messages but nothing is subscribed to so does nothing at the moment.
  if (client.isConnected())
    client.loop();
        
  // Read the next available 1-Wire temperature sensor
  if (sensor.read()) {

    // Get the sensor ID
    uint8_t addr[8];
    sensor.addr(addr);
    
    RGB.color(0, 0, 255);  // Blue
  
    // Build the MQTT message "<id>=<tempC>"
    char msg[30] = "";
    sprintf(msg, "%02X%02X%02X%02X%02X%02X%02X%02X=%.2fC",
        addr[0], addr[1], addr[2], addr[3], addr[4], addr[5], addr[6], addr[7], sensor.celsius()
    );
    
    client.publish(topic,msg);
    Particle.publish("temperature", msg, PRIVATE);


  // If sensor.read() didn't return true you can try again later
  // This next block helps debug what's wrong.
  // It's not needed for the sensor to work properly
  } else {
    // Once all sensors have been read you'll get searchDone() == true
    // Next time read() is called the first sensor is read again
    if (sensor.searchDone()) {
      Serial.println("No more addresses.");
 //       Particle.publish("status", "None", PRIVATE);
      // Avoid excessive printing when no sensors are connected
      delay(1000);
    }
    
    light = !light;
    if(light) {
        digitalWrite(D7, LOW); 
    } else {
        digitalWrite(D7, HIGH); 
    }
  }

}

