#define F_CPU 16E6
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>

#define UBBRVAL 51

void uart_init() {
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

void transmit(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

uint8_t hcsr04(){
		uint8_t count = 0; 
		
		PORTD |= (1<<5); 
		_delay_us(15); //		15 uS pulse naar trigger pin 
		PORTD &= ~(1<<5); 
		
		// deze code is overgenomen van "http://eecs.oregonstate.edu/tekbots/modules/hcsr04"
		
		while ((PIND & (1<<4)) != (1<<4)); // Loop doorlopen wanneer echo pin HIGH is 
		while (1){ 
			if ((PIND & (1<<4)) != (1<<4)) // Echo pulse on PORTD, Pin 4 is high (detected)
				return(count); // Return current count
			_delay_us(39); // delay van 39 sec
			count ++; // Increment Count
		}
}		


int main(void)
{	
	char tot_string[6];
	uint8_t tijdelijk;
	float tijdelijk_float;
	
	DDRD |= 1<<5; // Setup HC-SR04 Trigger as an output
	DDRD &= ~(1<<4); // Setup HC-SR04 Echo a an input
	_delay_ms(50);
	
	while(1)
	{
		tijdelijk = hcsr04();
		tijdelijk_float = (float)(tijdelijk) * 40; //een float maken en omrekenen naar uS
		tijdelijk_float = tijdelijk_float/58; //afstand in cm bereken
		
		dtostrf(tijdelijk_float, 2, 2, tot_string);// tijdelijk_float naar string 
		
		uart_init();
		UART_Putstring(tot_string); UART_Putstring(" cm");
		transmit('\r'); transmit('\n');
		_delay_ms(1000);
		
	}
}




