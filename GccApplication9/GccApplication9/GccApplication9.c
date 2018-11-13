#define F_CPU 16E6
#include <avr/io.h>
#include <util/delay.h>
#include <stdlib.h>
#include "AVR_TTC_scheduler.c"

#define UBBRVAL 51

char tot_string[6];
uint8_t tijdelijk;
float tijdelijk_float;
char input;
int temp1;
int temp2;

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
	loop_until_bit_is_set(UCSR0A, RXC0); /* Wait until data exists. */
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
		
		DDRD |= 1<<5; // Setup HC-SR04 Trigger as an output
		DDRD &= ~(1<<4); // Setup HC-SR04 Echo a an input
		
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
	
	dtostrf(tijdelijk_float, 2, 2, tot_string);// tijdelijk_float naar string
	
	transmit('\r'); transmit('\n');
	UART_Putstring(tot_string);
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
	_delay_ms(1000);
	PORTB = 0b00000100;
	_delay_ms(1000);
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
	temp1 = hcsr04();
	_delay_ms(100);
	temp2 = hcsr04();
	
	if (tijdelijk_float >= 160)
	{
		led_rood();
	}
	else if(tijdelijk_float < 5)
	{
		led_groen();
	}
	else if (tijdelijk_float > 5 && tijdelijk_float < 160 && temp1 < temp2)
	{
		uitrollen();
	}
	else if (tijdelijk_float > 5 && tijdelijk_float < 160 && temp1 > temp2)
	{
		inrollen();
	}
	
}

int main(void)
{
	SCH_Init_T1();
	SCH_Add_Task(berekening_verzend, 0 , 10);
	SCH_Add_Task(simulatie_motor, 0, 10);
	SCH_Start();
	while(1)
	{		
		SCH_Dispatch_Tasks();	
	}
}




