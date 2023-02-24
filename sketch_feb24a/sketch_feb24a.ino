#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <SoftwareSerial.h>
#include <DFRobotDFPlayerMini.h>

MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;

static const uint8_t PIN_MP3_TX = 2; 
static const uint8_t PIN_MP3_RX = 3;
SoftwareSerial softwareSerial(PIN_MP3_RX, PIN_MP3_TX);

DFRobotDFPlayerMini myDFPlayer;
int count = 0;
int count1 = 0;
int threshold = -10000;
int minDiff = 0.1;
float prevAcceleration = 0;

enum State { 
  COUNTING, 
  CALIBRATING 
};

State state = COUNTING;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  accelgyro.initialize();
  softwareSerial.begin(9600);

  if (myDFPlayer.begin(softwareSerial)) {
    Serial.println("OK");
    myDFPlayer.volume(30);
    myDFPlayer.play(16);
  }
  softwareSerial.begin(9600);
}

bool lifted = false;
bool repetitionCounted = false;

void loop() {
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  delay(300);
  float acceleration = ay;
  float orientation = az;

  if (Serial.available() > 0){
    String value = Serial.readStringUntil('\n');
    if (value == "Tone-up\n") {
      count1 = 15;

      switch (state) {
        case COUNTING:
        //Serial.print("read: ");
        //Serial.println(ay);
        //Serial.print("orient.: ");
        //Serial.println(az);
        //Serial.print("Gyro: ");
        //Serial.println(gz);

          if (abs(acceleration - prevAcceleration) > minDiff){

            if (!repetitionCounted && acceleration < threshold){
              count++;
              Serial.print("Repetition: ");
              Serial.println(count);
              int t2t = count;
              myDFPlayer.play(t2t);
              lifted = true;
              repetitionCounted = true;
              delay(600);
            }

            if(lifted == true){ 
              if(gz < -12100) {
                Serial.println("too fast");
                myDFPlayer.play(17);
                delay(2000);
                lifted = false;
              }     
            }

            if (count > count1){
              count = 0;
            }
          
            if (orientation >= 10000 || orientation <= -10000){
              Serial.println("incorrect orientation");
              myDFPlayer.play(19);
              delay(2000);
            }
          }

          prevAcceleration = acceleration;
          repetitionCounted = false;
          lifted = false;
          
          if (Serial.available() > 0) {
            state = CALIBRATING;
          }
          
          break;

        case CALIBRATING:
          Serial.println("Enter new threshold val:");
          
          while (Serial.available() == 0) {
          }
          
          threshold = Serial.parseInt();
          
          Serial.print("New threshold val: ");
          Serial.println(threshold);

          state = COUNTING;
          break;
      }
      Serial.print("count:");
      Serial.println(count);
    } 
    
    else if (value == "Bulk-up\n"){
      count1 = 8;

      switch (state) {
        case COUNTING:
        //Serial.print("read: ");
        //Serial.println(ay);
        //Serial.print("orient.: ");
        //Serial.println(az);
        //Serial.print("Gyro: ");
        //Serial.println(gz);

          if (abs(acceleration - prevAcceleration) > minDiff){

            if (!repetitionCounted && acceleration < threshold){
              count++;
              Serial.print("Repetition: ");
              Serial.println(count);
              int t2t = count;
              myDFPlayer.play(t2t);
              lifted = true;
              repetitionCounted = true;
              delay(600);
            }

            if(lifted == true){ 
              if(gz < -12100) {
                Serial.println("too fast");
                myDFPlayer.play(17);
                delay(2000);
                lifted = false;
              }     
            }

            if (count > count1){
              count = 0;
            }
          
            if (orientation >= 10000 || orientation <= -10000){
              Serial.println("incorrect orientation");
              myDFPlayer.play(19);
              delay(2000);
            }
          }

          prevAcceleration = acceleration;
          repetitionCounted = false;
          lifted = false;
          
          if (Serial.available() > 0) {
            state = CALIBRATING;
          }
          
          break;

        case CALIBRATING:
          Serial.println("Enter new threshold val:");
          
          while (Serial.available() == 0) {
          }
          
          threshold = Serial.parseInt();
          
          Serial.print("New threshold val: ");
          Serial.println(threshold);

          state = COUNTING;
          break;
      }
      Serial.print("count:");
      Serial.println(count);      
    }
  }
}