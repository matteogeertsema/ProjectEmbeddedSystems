/*
 * GccApplication8.c
 *
 * Created: 28-10-2018 20:39:32
 *  Author: karel
 */ 


#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
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

void transmit(uint8_t data)
{
// wait for an empty transmit buffer
// UDRE is set when transmit buffer is empty
loop_until_bit_is_set(UCSR0A, UDRE0);
// send the data
UDR0 = data;
}

char receive(void) {
loop_until_bit_is_set(UCSR0A, RXC0); /* Wait until data exists. */
return UDR0;
}

int main() {
	
	uart_init();
	_delay_ms(1000);
		while (1) {
				transmit(0x33); _delay_ms(1000);
				}
}				