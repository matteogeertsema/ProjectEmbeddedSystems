#define F_CPU 16E6
#include <avr/io.h>
#include <util/delay.h>
#include <avr/sfr_defs.h>
#include <stdlib.h>
#include "AVR_TTC_scheduler.c"

#define UBBRVAL 51

char tot_string[6];
uint8_t tijdelijk;
float tijdelijk_float;
char input;
char ADCOut[10];
double ADCRes;
int overgang_temp;
double avg_temp;
double licht1;
char licht2[10];
int lichtintensiteit;

void uart_init()
{
	// set the baud rate
	UBRR0H = 19200;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable transmitter and receiver
	UCSR0B = _BV(TXEN0)|_BV(RXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}

void UART_Putstring(char* eenstring)
{
	while(*eenstring != 0X00)
	{
		transmit(*eenstring);
		eenstring++;
	}
}

char receive(void)
{
	        while(!(UCSR0A) & (1<<RXC0));                     // wait while data is being received
	        return UDR0;
}

void transmit(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

uint8_t hcsr04()
{
	uint8_t count = 0;
	
	DDRD |= 1<<5; //HC-SR04 Trigger als output
	DDRD &= ~(1<<4); //HC-SR04 Echo als input
	
	PORTD |= (1<<5);
	_delay_us(15); //		15 uS pulse naar trigger pin
	PORTD &= ~(1<<5);
	
	// deze code is overgenomen van "http://eecs.oregonstate.edu/tekbots/modules/hcsr04"
	
	while ((PIND & (1<<4)) != (1<<4)); // Loop doorlopen wanneer echo pin HIGH is
	while (1){
		if (count == 238) // max waarde van 160 bereikt
		return(count); // return maximum distance.
		if ((PIND & (1<<4)) != (1<<4)) // Echo pulse on PORTD, Pin 4 is high (detected)
		return(count); // Return current count
		_delay_us(39); // delay 40 usec
		count ++; // Increment Count
	}
}

void berekening_verzend()
{
	uart_init();
	tijdelijk = hcsr04();
	tijdelijk_float = (float)(tijdelijk) * 39; //een float maken en omrekenen naar uS
	tijdelijk_float = tijdelijk_float/58; //afstand in cm bereken
}

void initADC(){
	
	ADMUX |=(1<<REFS0)|(1<<REFS1)|(1<<ADLAR);

	// enable ADC
	// set prescaler to 128
	ADCSRA |=(1<<ADEN)|(1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2);
}

uint16_t ADC_switch(uint8_t pin)
{
	ADMUX &= 0xf0;
	ADMUX |=pin;
	
	ADCSRA |= _BV(ADSC);
	while((ADCSRA & _BV(ADSC)));
	return ADCH;
}

double temp_gem(){
	
	int duur;
	double total = 0;
	uint16_t voltage1;
	voltage1 = ADC_switch(1);
	
	for(duur = 0; duur < 40; duur++){
		ADCRes = (voltage1*(1100.0/256)-500)/10; //Bereken temperatuur in Celsius van de ADC output
		total += ADCRes; //Geef temperatuur aan total
	}	
	double avg = total / 40; //bereken gemiddelde
	
	return avg;
}

void temp_show(){
	double avg_temp = temp_gem();//gemiddelde temperatuur aan avg_temp geven
	
	dtostrf(avg_temp, 2, 2, ADCOut);// float naar string
		UART_Putstring(ADCOut);
		_delay_ms(1800);
}

void lichtsensor(){
	uint16_t voltage2;
	voltage2 = ADC_switch(0);
	
	licht1 = voltage2 * 4.98 / 1023; //berekening om lichtintesiteit te berekenen
	
	 dtostrf(licht1, 2, 2, licht2);// licht 1 naar string (licht2)
	 
	 UART_Putstring(licht2);
}

void led_groen()
{
	DDRB = 0xff;
	PORTB = 0b00000001;
}

void uitrollen()
{
	DDRB = 0xff;
	PORTB = 0b00000110;
	_delay_ms(500);
	PORTB = 0b00000100;
	_delay_ms(500);
}

void inrollen()
{
	DDRB = 0xff;
	PORTB = 0b00000011;
	_delay_ms(1000);
	PORTB = 0b00000001;
	_delay_ms(1000);
}

void led_rood()
{
	DDRB = 0xff;
	PORTB = 0b00000100;
}

void simulatie_motor()
{
	avg_temp = temp_gem();
	overgang_temp = 18;
	lichtintensiteit = licht1;
	
	if(avg_temp > overgang_temp && lichtintensiteit < 0.90)
	{
		if (tijdelijk_float < 50)
		{
			uitrollen();
		}
		else
		{
			led_rood();
		}			
	}
	if(avg_temp < overgang_temp || lichtintensiteit > 0.90)
	{
		if(tijdelijk_float > 5)
		{
			inrollen();
		}
		else
		{
			led_groen();
		}			
	}
}

int main(void)
{
 	uart_init();
	initADC();
	
	SCH_Init_T1();
	SCH_Add_Task(berekening_verzend, 0, 10);	//10 ticks = 0.1 seconde
	SCH_Add_Task(simulatie_motor, 0, 10);		//10 ticks = 0.1 seconde
	SCH_Add_Task(temp_show, 0, 6000);			//6000 ticks = 1 minuut
	SCH_Add_Task(lichtsensor, 0, 6000);			//6000 ticks = 1 minuut
	SCH_Start();
	while(1)
	{
		SCH_Dispatch_Tasks();
	}
	return(0);
}