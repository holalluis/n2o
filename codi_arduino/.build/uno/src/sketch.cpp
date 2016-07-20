#include <Arduino.h>
#include <SoftwareSerial.h>
#include <string.h>
void setup();
void loop();
double llegeixP(int pin);
double llegeixT(int pin);
#line 1 "src/sketch.ino"
/*
 * Sketch per controlar valvules i sensors del aparell "N2O" | ICRA | abril/maig 2015 | lbosch@icra.cat | imorell@icra.cat
 */
 
//#include <SoftwareSerial.h>
//#include <string.h>

SoftwareSerial serialRPI(10, 11); // RX, TX
int valvules[] = {46, 47, 48, 49}; //pins digitals per les valvules 1 a 4
int impulsos[] = {50, 51, 52, 53}; //pins digitals pels emissors impulsos 1 a 4
int sensor_p[] = {A0, A1, A2, A3}; //pins analogics pels sensors de pressio
int sensor_t[] = {A4, A5, A6, A7}; //pins analogics pels sensors de temperatura

//The millis() function returns the number of milliseconds since the Arduino board began running the current program. 
//This number will overflow (go back to zero), after approximately 50 days.
unsigned long tempsInicial, tempsActual; 

void setup()
{
  Serial.begin(9600);
  serialRPI.begin(9600);
  //inputs i outputs
  pinMode(valvules[0], OUTPUT); 
  pinMode(valvules[1], OUTPUT); 
  pinMode(valvules[2], OUTPUT); 
  pinMode(valvules[3], OUTPUT);
  pinMode(impulsos[0], INPUT);  
  pinMode(impulsos[1], INPUT);
  pinMode(impulsos[2], INPUT);
  pinMode(impulsos[3], INPUT);
}

void loop()
{
  //recorre les quatre valvules
  for (int i = 0; i < 4; i++)
  {
    //activa valvula i
    Serial.println(String("[+] Activant valvula ")+i);
    digitalWrite(valvules[i], LOW);

    //registra el nombre de milisegons actual
    tempsInicial = millis();

    //variable per comptar els litres que han passat
    int litres = 0;

	//temps en el qual s'esta comptant el volum (milisegons)
    int temps = 5*60*1000; //5 minuts

    Serial.println(String("Comptant litres durant 5 minuts... Litres: ")+litres);

    while(abs((millis()-tempsInicial)) < temps)
    { 
      //llegeix l'emissor d'impulsos i
      if(digitalRead(impulsos[i])==HIGH)
      {
        litres += 10;
        Serial.println(String(">>> S'ha rebut un pols de l'emissor. Litres: ")+litres);
        //El pols dura 0.25 segons. Espera 2 segons una vegada detectat
		delay(2000);
      }
    }

	//NECESSITEM Temperatura i Pressio per la campana actual
	double t = llegeixT(sensor_t[i]);
	double p = llegeixP(sensor_p[i]);
        char t_str[6], p_str[6]; //convertir floats a string
        dtostrf(t,6,3,t_str);
        dtostrf(p,6,3,p_str);
	String comanda = String("campana=")+String(i+1)+String("&t=")+String(t_str)+String("&p=")+String(p_str)+String("&v=")+String(litres);
	Serial.println(String(">>>>>>>>>>Comanda enviada al RPI: ")+comanda);
	serialRPI.println(comanda);
    
    //indica que se salta de vàlvula
    Serial.println(String("[+] Desactivant valvula ")+i+String(". (Litres: ")+litres+String(")"));
    digitalWrite(valvules[i],HIGH);
    
    Serial.println();  
  }
}

/*
 * Funcions per llegir temperatura i pressio
 */
double llegeixP(int pin)
//retorna la pressio en bar des de 4-20 mA, amb una resistencia de 240 ohms
//el paràmetre "pin" serà A0, A1, A2 ò A3
{
  double volts   = analogRead(pin) * 5 / 1024;
  double pressio = (volts - 1) / 4 * 0.16;
  return pressio;
}

double llegeixT(int pin)
//retorna la temperatura en ºC des de 4-20 mA, amb una resistencia de 240 ohms
//el paràmetre "pin" serà A4, A5, A6 ò A7
{
  double volts = analogRead(pin) * 5 / 1024;
  double temp  = (volts - 1) / 4 * 60;
  return temp;
}
