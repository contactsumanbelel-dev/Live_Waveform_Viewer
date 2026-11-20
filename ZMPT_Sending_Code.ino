#define Pin 32

void setup() {
  
  Serial.begin(115200);

}

void loop() {
  
  int rawADC = analogRead(32);
  Serial.println(rawADC);
  
  delay(500);

}
