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

static volatile int pulse = 0;
static volatile int i = 0;

int main(void)

{
	int16_t count_a = 0;
	char show_a[16];
	
	DDRD = 0b11111011;
	_delay_ms(50);

	EIMSK |= 1<<INT0;
	EICRA |= 1<<ISC00;
	
	TCCR1A = 0;

	sei();
	
	while(1)
	{
		PORTD |= (1<<PIND0);
		_delay_us(15);
		PORTD &= ~(1<<PIND0);
		
		count_a = (double)pulse / 466.47;
		count_a = count_a/2;
		 
		dtostrf(count_a, 2, 2, show_a);/* count_a to string */
		strcat(show_a, " cm   ");	/* Concat unit i.e.cm */

		uart_init();
		UART_Putstring(show_a);
		transmit('\r');
		transmit('\n');
		_delay_ms(1000);
		
	}
}

ISR(INT0_vect)
{
  if(i == 1)
  {
    TCCR1B = 0;
    pulse = TCNT1;
    TCNT1 = 0;
    i = 0;
  }

  if(i==0)
  {
    TCCR1B |= (1<<CS10);
    i = 1;
  }
}