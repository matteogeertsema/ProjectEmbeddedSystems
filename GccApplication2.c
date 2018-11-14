/*
 * GccApplication4.c
 *
 * Created: 5-11-2018 12:04:13
 *  Author: Matteo
 */ 

#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
#define UBBRVAL 51
#include "AVR_TTC_scheduler.c"

double ADCRes;
char ADCOut[6];

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

void initADC(){
	// Internal 2.56V voltage reference
	// set ADC0 as the ADC input channel
	ADMUX |=(1<<REFS0)|(1<<REFS1)|(1<<ADLAR);

	// enable ADC
	// set prescaler to 128
	ADCSRA |=(1<<ADEN)|(1<<ADATE)|(1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2);
	ADCSRA |=(1<<ADSC);
}

void temp(){
	ADCRes = ADCH* 4.98/ 1023.0; //Calculate temperature in degrees C from ADC output
	 snprintf(ADCOut, 5, "#f", ADCRes); //Transform ADCRes floating point to string called ADCOut
	 
	 dtostrf(ADCRes, 2, 2, ADCOut);// tijdelijk_float naar string 
	 
	 UART_Putstring(ADCOut);
	 transmit('\r'); transmit('\n');
	 
	 _delay_ms(1000);
}

int main(void)
{
	uart_init();
	initADC();
	
	SCH_Init_T1(); // init de timer en verwijder alle taken
	SCH_Add_Task(temp,0,50);
	SCH_Start(); // start de scheduler
	
    while(1)
    {
		SCH_Dispatch_Tasks();
	}
	return(0);
}