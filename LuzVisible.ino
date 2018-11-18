// BUZZER
int BUZ = 8;

// RGB LED
int R = 11;
int G = 9;
int B = 10;

void setup(){
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
  pinMode(BUZ, OUTPUT);
  for (int x=9; x<12; x++){pinMode(x, OUTPUT);}
}

void loop(){
  comunicate();
}

void comunicate(){
  String command = Serial.readStringUntil(char('\0'));
  if (command != 0){
    //"r:255 g:000 b:000"
    char copy[4];
    String s = command.substring(2, 6);
    s.toCharArray(copy, 4);
    int r = atoi(copy);
    s = command.substring(8, 13);
    s.toCharArray(copy, 4);
    int g = atoi(copy);
    s = command.substring(14, 17);
    s.toCharArray(copy, 4);
    int b = atoi(copy);
    
    analogWrite(R, r);
    analogWrite(G, g);
    analogWrite(B, b);
    
    int val = map(r+g+b, 0, 768, 0, 1023);
    tone(BUZ, val, 100);
  }
}
