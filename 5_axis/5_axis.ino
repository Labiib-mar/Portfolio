 const int xInput = A7;
const int yInput = A6;
const int zInput = A5;
const int xRate = A2;
const int yRate = A1;

// initialize minimum and maximum Raw Ranges for each axis
int RawMin = 0;
int RawMax = 1023;

// Take multiple samples to reduce noise
const int sampleSize = 10;
void setup() {
  analogReference(EXTERNAL);
  Serial.begin(9600);
}

void loop() {
//Read raw values
  int xRaw = ReadAxis(xInput);
  int yRaw = ReadAxis(yInput);
  int zRaw = ReadAxis(zInput);
  int xRawRate = ReadAxis(xRate);
  int yRawRate = ReadAxis(yRate);

  float vscale = 3300/1023;
  float ref_value = 1350/vscale;
  int refx = 377;
  
  long xratescale = xRawRate - refx;
  long yratescale = yRawRate - ref_value;
  
  // Convert raw values to 'milli-Gs"
  long xScaled = map(xRaw, RawMin, RawMax, -3000, 3000);
  long yScaled = map(yRaw, RawMin, RawMax, -3000, 3000);
  long zScaled = map(zRaw, RawMin, RawMax, -3000, 3000);

  // re-scale to fractional Gs
  float xAccel = xScaled / 1000.0;
  float yAccel = yScaled / 1000.0;
  float zAccel = zScaled / 1000.0;
  //rescale deg/sec
  float xdeg = xratescale/0.67;
  float ydeg = yratescale/0.67;

//  Serial.print("X, Y, Z  :: ");
//  Serial.print(xRaw);
//  Serial.print(", ");
//  Serial.print(yRaw);
//  Serial.print(", ");
//  Serial.print(zRaw);
//  Serial.print(" :: ");
  Serial.println(xAccel,0);
//  Serial.println("G");
  Serial.println(yAccel,0);
//  Serial.println("G");
  Serial.println(zAccel,0);
//  Serial.println("G");
//  Serial.print("X deg, Y deg  ::  ");
//  Serial.print(xRawRate);
//  Serial.print(", ");
//  Serial.print(yRawRate);
//  Serial.print(" :: ");
  Serial.println(xdeg);
//  Serial.println("deg/sec");
  Serial.println(ydeg);
//  Serial.println("deg/sec");

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
