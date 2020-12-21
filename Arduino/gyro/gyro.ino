const int xRate = A2;
const int yRate = A1;

// initialize minimum and maximum Raw Ranges for each axis
int RawMin = 0;
int RawMax = 1023;

const int sampleSize = 10;

void setup() {
  analogReference(EXTERNAL);
  Serial.begin(9600);
}

void loop() {
  //Read raw values
  int xRawRate = ReadAxis(xRate);
  int yRawRate = ReadAxis(yRate);

//int xRawRate = analogRead(xRate);
//int yRawRate = analogRead(yRate);
  
  float vscale = 3300/1023;
  float ref_value = 1350/vscale;
  float refx = 377;
  
  long xratescale = xRawRate - refx;
  long yratescale = yRawRate - ref_value;

  //rescale deg/sec
  float xdeg = xratescale/0.67;
  float ydeg = yratescale/0.67;
  Serial.print("X deg, Y deg  ::  ");
  Serial.print(xRawRate);
  Serial.print(", ");
  Serial.print(yRawRate);
  Serial.print(" :: ");
  Serial.print(xdeg);
  Serial.print("deg/sec, ");
  Serial.print(ydeg);
  Serial.println("deg/sec");

  delay(200);
}

// Take samples and return the average
int ReadAxis(int axisPin)
{
  long reading = 0;
  analogRead(axisPin);
  delay(1);
  for (int i = 0; i < sampleSize; i++)
  {
  reading += analogRead(axisPin);
  }
  return reading/sampleSize;
}
