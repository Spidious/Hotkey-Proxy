//#include "Keyboard.h"

const int buttonPin[] = {2, 3, 4, 5, 6, 7, 8, 9};
int pinCount = 8;
int buttonState[] = {0, 0, 0, 0, 0, 0, 0, 0};
int prevButtonState[] = {HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH};
int key_hold[] = {0, 0, 0, 0, 0, 0, 0, 0};
//int key_hold = 0;
int lastPin = -1;

long lastDebounceTime[] = {0, 0, 0, 0, 0, 0, 0, 0};
long debounceDelay = 50;
void setup() {
  Serial.begin(9600);
  for (int thisPin = pinCount - 1; thisPin >= 0; thisPin--) {
    pinMode(buttonPin[thisPin], INPUT);
    digitalWrite(buttonPin[thisPin], HIGH);
  }
//  Keyboard.begin();
}

// Output actions. Probably the only part that you need to change
int outputAction(int currentButton) {
    if (currentButton == 0) {
        Serial.print(0);
    }
    if (currentButton == 1) {
        Serial.print(1);
    }
    if (currentButton == 2) {
        Serial.print(2);
    }
    if (currentButton == 3) {
        Serial.print(3);
    }
    if (currentButton == 4) {
        Serial.print(4);
    }
    if (currentButton == 5) {
        Serial.print(5);
    }
    if (currentButton == 6) {
        Serial.print(6);
    }
    if (currentButton == 7) {
        Serial.print(7);
    }
}
void loop() {
  for (int thisPin = pinCount - 1; thisPin >= 0; thisPin--) {
    buttonState[thisPin] = digitalRead(buttonPin[thisPin]);

    if ((buttonState[thisPin] == LOW)) {
      if ((millis() - lastDebounceTime[thisPin]) > debounceDelay) {
        if(thisPin == lastPin){
          if((key_hold[thisPin] > 7 || key_hold[thisPin] == 0)){
            outputAction(thisPin);
            key_hold[thisPin]++;
          } else {
            key_hold[thisPin]++;
          }
        } else {
          outputAction(thisPin);
          lastPin = thisPin;
          key_hold[thisPin] = 1;
          
        }
        lastDebounceTime[thisPin] = millis();
      }
    } else {
      key_hold[thisPin] = 0;
    }
    prevButtonState[thisPin] = buttonState[thisPin];
  }
  
}
