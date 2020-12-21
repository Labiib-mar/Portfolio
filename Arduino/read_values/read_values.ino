int sens_ST_acc = A0;
int sens_Y_rate = A1;
int sens_X_rate = A2;
int sens_Y_ratex = A3;
int sens_X_ratex = A4;
int sens_z_acc = A5;
int sens_y_acc = A6;
int sens_x_acc = A7;
 
int ST_acc = 0;
int Y_Rate = 0;
int X_Rate = 0;
int y_Ratex = 0;
int x_Ratex = 0;
int z_acc = 0;
int y_acc = 0;
int x_acc = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
//    Serial.print("ST-acc:  ");
//    Serial.print(analogRead(sens_ST_acc));
//    Serial.print("/n");

    Serial.print("Y-Rate:  ");
    Serial.print(analogRead(sens_Y_rate));
    Serial.print("\n");

    Serial.print("X-Rate:  ");
    Serial.print(analogRead(sens_X_rate));
    Serial.print("\n");
    
//    Serial.print("Y-rate(inv):  ");
//    Serial.print(analogRead(sens_Y_ratex));
//    Serial.print("/n");
//    
//    Serial.print("X-rate(inv):  ");
//    Serial.print(analogRead(sens_X_ratex));
//    Serial.print("/n");

    Serial.print("Z-acc:  ");
    Serial.print(analogRead(sens_z_acc));
    Serial.print("\n");

    Serial.print("Y-acc:  ");
    Serial.print(analogRead(sens_y_acc));
    Serial.print("\n");
    
    Serial.print("X-acc:  ");
    Serial.print(analogRead(sens_x_acc));
    Serial.print("\n");
    
    
    
}
