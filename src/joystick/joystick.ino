// X and Y are analog and Z is digital!
const int joyX = A0;
const int joyY = A1;
const int joyZ = 2;

// reset values
int readX = 0;
int readY = 0;
int readZ = 0;

void setup() {
    Serial.begin(230400); // lower this if it doesn't work
    pinMode(joyZ, INPUT_PULLUP); // register Z btn
}

void loop() {
    // read analog and btn
    readX = analogRead(joyX);
    readY = analogRead(joyY);
    readZ = !digitalRead(joyZ);

    // send results
    Serial.print(readX);
    Serial.print(",");
    Serial.print(readY);
    Serial.print(",");
    Serial.println(readZ);
}
