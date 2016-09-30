
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

}

void loop() 
{
  Serial.print("I");
  Serial.print("T1-");
  Serial.print(analogRead(potaTemp1));
  Serial.print(",T2-");
  Serial.print(analogRead(potaTemp2));
  Serial.print(",T3-");
  Serial.print(analogRead(potaTemp3));
  Serial.print(",T4-");
  Serial.print(analogRead(potaTemp4));
  //---
  Serial.print(",P1-");
  Serial.print(analogRead(potaPresio1));
  Serial.print(",P2-");
  Serial.print(analogRead(potaPresio2));
  Serial.print(",P3-");
  Serial.print(analogRead(potaPresio3));
  Serial.print(",P4-");
  Serial.print(analogRead(potaPresio4));
  //---
  comprovaCabalimetres();
  Serial.print("F");
  comprovaElectrovalvules();
  delay(100);
}
// ========================================================

void comprovaCabalimetres()
{
  // Codi Cabalimentre 1:
  if (digitalRead(potaCabalimetre1) == LOW)
    Serial.print(",C1-1");
  else
    Serial.print(",C1-0");

  // Codi Cabalimentre 2:
  if (digitalRead(potaCabalimetre2) == LOW) 
    Serial.print(",C2-1");
  else 
    Serial.print(",C2-0");
    
  // Codi Cabalimentre 3:
  if (digitalRead(potaCabalimetre3) == LOW) 
    Serial.print(",C3-1");
  else 
    Serial.print(",C3-0");

  // Codi Cabalimentre 4:
  if (digitalRead(potaCabalimetre4) == LOW) 
    Serial.print(",C4-1");
  else 
    Serial.print(",C4-0");
}

// --------------------------------------------------------

void comprovaElectrovalvules()
{
  char comanda;
  char quina;
  if (Serial.available() > 0)
  {
    comanda = Serial.read();
    quina = Serial.read();

    if ((comanda == 'O') || (comanda == 'T'))
    {
      if ((quina >= '0') && (quina <= '9'))
      {
        if (quina == '1')
        {
          if (comanda == 'O')
            digitalWrite(potaElectrovalvula1, HIGH);
          else
            digitalWrite(potaElectrovalvula1, LOW);
        }
        else if (quina == '2')
        {
          if (comanda == 'O')
            digitalWrite(potaElectrovalvula2, HIGH);
          else
            digitalWrite(potaElectrovalvula2, LOW);
        }
        if (quina == '3')
        {
          if (comanda == 'O')
            digitalWrite(potaElectrovalvula3, HIGH);
          else
            digitalWrite(potaElectrovalvula3, LOW);
        }
        if (quina == '4')
        {
          if (comanda == 'O')
            digitalWrite(potaElectrovalvula4, HIGH);
          else
            digitalWrite(potaElectrovalvula4, LOW);
        }
      }
    }
  }
}
// --------------------------------------------------------

