#define F_CPU 16E6
#include <avr/io.h>
#include <util/delay.h>
#include <avr/sfr_defs.h>
#include <string.h>

#define UBBRVAL 51

char string[10];
long duration;
long cm;

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

int read_ultrasonic()
{	
	int count = 0;
	
	PORTD &= ~_BV(PIND2);		// beginnen met naar low setten
		_delay_us(5);				
		PORTD |= _BV(PIND2);		// set de trigpin 10us naar high
		_delay_us(10);
		PORTD &= ~_BV(PIND2);

	_delay_ms(1);		     // delay to wait for transmitter to die off
	for (int i=0;i < 10000;i++){ // Checking port in loop 10,000 times

		if (PIND3&0x10){	     // read PORTD pin 3 for echo pulse
			count++;	// count if still high count			
		}
	}

return count;
}

int main(void)
{
	DDRD |= _BV(DDD2);

	while(1)
	{
		uart_init();
		_delay_ms(1000);
		
		duration = read_ultrasonic();
		cm = (double)duration / 466.47;
		dtostrf(cm, 2, 2, string);/* distance to string */
		strcat(string, " cm   ");	/* Concat unit i.e.cm */
		
		UART_Putstring(string);
		transmit('\r');
		transmit('\n');
		_delay_ms(100);
	}
}