#include <Servo.h>
#include<SoftwareSerial.h>
Servo myservo;  

void setup() {
  //SoftwareSerial Bluetooth(10,11);//RX=,TX=
  Serial.begin(9600); //监听软串口
  myservo.attach(9); //舵机控制
  myservo.write(10);
//  delay(10000); 
}

void loop() {
  while(Serial.available())
  {
    char c;
    c = Serial.read();  //读取串口数据
    Serial.println(c);
    switch(c)
    {
      case '1':servo_init();
      break;
      case '2':open_the_door();
      break;
      case '3':close_the_door();
    }
  }

}


void open_the_door()  //舵机开门
{
  myservo.write(170);
}
void close_the_door()  //舵机关门
{
  myservo.write(0);
}
void servo_init()  //舵机初始化
{
  myservo.write(10);
}
