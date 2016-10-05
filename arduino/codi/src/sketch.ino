#define potaTemp1 A0
#define potaTemp2 A1
#define potaTemp3 A2
#define potaTemp4 A3

#define potaPresio1 A8
#define potaPresio2 A10
#define potaPresio3 A11
#define potaPresio4 A12

#define potaCabalimetre1 22
#define potaCabalimetre2 23
#define potaCabalimetre3 24
#define potaCabalimetre4 25

#define potaElectrovalvula1 50
#define potaElectrovalvula2 51
#define potaElectrovalvula3 52
#define potaElectrovalvula4 53

boolean prevCont1, prevCont2, prevCont3, prevCont4;
boolean cont1, cont2, cont3, cont4;
boolean estatValvula1, estatValvula2, estatValvula3, estatValvula4;

void setup() 
{
  Serial.begin(9600);
  pinMode(potaCabalimetre1, INPUT_PULLUP);
  pinMode(potaCabalimetre2, INPUT_PULLUP);
  pinMode(potaCabalimetre3, INPUT_PULLUP);
  pinMode(potaCabalimetre4, INPUT_PULLUP);
  pinMode(potaElectrovalvula1, OUTPUT);
  pinMode(potaElectrovalvula2, OUTPUT);
  pinMode(potaElectrovalvula3, OUTPUT);
  pinMode(potaElectrovalvula4, OUTPUT);
  digitalWrite(potaElectrovalvula1, HIGH);
  digitalWrite(potaElectrovalvula2, HIGH);
  digitalWrite(potaElectrovalvula3, HIGH);
  digitalWrite(potaElectrovalvula4, HIGH);
  cont1 = false;
  cont2 = false;
  cont3 = false;
  cont4 = false;
  prevCont1 = false;
  prevCont2 = false;
  prevCont3 = false;
  prevCont4 = false;
  estatValvula1 = false;
  estatValvula2 = false;
  estatValvula3 = false;
  estatValvula4 = false;
}

void loop() 
{
  Serial.print("IT1-"); Serial.print(analogRead(potaTemp1));
  Serial.print(",T2-"); Serial.print(analogRead(potaTemp2));
  Serial.print(",T3-"); Serial.print(analogRead(potaTemp3));
  Serial.print(",T4-"); Serial.print(analogRead(potaTemp4));
  Serial.print(",P1-"); Serial.print(analogRead(potaPresio1));
  Serial.print(",P2-"); Serial.print(analogRead(potaPresio2));
  Serial.print(",P3-"); Serial.print(analogRead(potaPresio3));
  Serial.print(",P4-"); Serial.print(analogRead(potaPresio4));

  if(estatValvula1) Serial.print(",E1-1");
  else              Serial.print(",E1-0");

  if(estatValvula2) Serial.print(",E2-1");
  else              Serial.print(",E2-0");

  if(estatValvula3) Serial.print(",E3-1");
  else              Serial.print(",E3-0");

  if(estatValvula4) Serial.print(",E4-1");
  else              Serial.print(",E4-0");
  
  comprovaCabalimetres();
  Serial.print("F");
  comprovaElectrovalvules();
  delay(100);
}

void comprovaCabalimetres()
{
  //Cabalimentre 1
  if((digitalRead(potaCabalimetre1) == LOW) && (prevCont1 == LOW))
  {
	cont1 = !cont1; prevCont1 = HIGH;
  }
  else if((digitalRead(potaCabalimetre1) == HIGH) && (prevCont1 == HIGH))
	prevCont1 = LOW;

  //Cabalimentre 2
  if((digitalRead(potaCabalimetre2) == LOW) && (prevCont2 == LOW))
  {
	cont2 = !cont2; prevCont2 = HIGH;
  }
  else if((digitalRead(potaCabalimetre2) == HIGH) && (prevCont2 == HIGH))
	prevCont2 = LOW;
	
  //Cabalimentre 3
  if((digitalRead(potaCabalimetre3) == LOW) && (prevCont3 == LOW))
  {
	cont3 = !cont3; prevCont3 = HIGH;
  }
  else if((digitalRead(potaCabalimetre3) == HIGH) && (prevCont3 == HIGH))
	prevCont3 = LOW;

  //Cabalimentre 4
  if((digitalRead(potaCabalimetre4) == LOW) && (prevCont4 == LOW))
  {
	cont4 = !cont4; prevCont4 = HIGH;
  }
  else if((digitalRead(potaCabalimetre4) == HIGH) && (prevCont4 == HIGH))
	prevCont4 = LOW;

  //Cabalimentre 1
  if(cont1 == LOW) Serial.print(",C1-1");
  else Serial.print(",C1-0");

  //Cabalimentre 2
  if(cont2 == LOW) Serial.print(",C2-1");
  else Serial.print(",C2-0");
	
  //Cabalimentre 3
  if(cont3 == LOW) Serial.print(",C3-1");
  else Serial.print(",C3-0");

  //Cabalimentre 4
  if(cont4 == LOW) Serial.print(",C4-1");
  else Serial.print(",C4-0");
}

void comprovaElectrovalvules()
{
  char comanda,quina;
	if(Serial.available()==0) return;
	comanda=Serial.read(); quina=Serial.read();

	//si comanda no val ni O ni T, acaba
	if(comanda!='O' && comanda!='T') return;

	     if(comanda=='O' && quina=='1'){digitalWrite(potaElectrovalvula1,LOW );estatValvula1=1;}
	else if(comanda=='T' && quina=='1'){digitalWrite(potaElectrovalvula1,HIGH);estatValvula1=0;}
	else if(comanda=='O' && quina=='2'){digitalWrite(potaElectrovalvula2,LOW );estatValvula2=1;}
	else if(comanda=='T' && quina=='2'){digitalWrite(potaElectrovalvula2,HIGH);estatValvula2=0;}
	else if(comanda=='O' && quina=='3'){digitalWrite(potaElectrovalvula3,LOW );estatValvula3=1;}
	else if(comanda=='T' && quina=='3'){digitalWrite(potaElectrovalvula3,HIGH);estatValvula3=0;}
	else if(comanda=='O' && quina=='4'){digitalWrite(potaElectrovalvula4,LOW );estatValvula4=1;}
	else if(comanda=='T' && quina=='4'){digitalWrite(potaElectrovalvula4,HIGH);estatValvula4=0;}
}
