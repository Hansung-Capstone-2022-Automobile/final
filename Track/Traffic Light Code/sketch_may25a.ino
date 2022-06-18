void setup()
{
 pinMode(2, OUTPUT);
 pinMode(3, OUTPUT);
 pinMode(4, OUTPUT);
}
void loop(){
  digitalWrite(4, HIGH); //적색 
  delay(30000);
  digitalWrite(4, LOW);
  
  digitalWrite(3, HIGH); //오렌지색 
  delay(5000);
  digitalWrite(3, LOW);
  
  digitalWrite(2, HIGH); //초록색 
  delay(30000);
  digitalWrite(2, LOW);
  
}
