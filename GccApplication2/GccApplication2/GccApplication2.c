/*
 * tm1638.c
 * demo program interfacing TM1638 from Arduino UNO (ATmga238P)
 * reusing :
 *   -http://blog.3d-logic.com/2015/01/10/using-a-tm1638-based-board-with-arduino/
 *   -https://android.googlesource.com/platform/external/arduino/+/jb-mr1-dev/hardware/arduino/cores/arduino
 *
 * to keep things simple, we'll ony use PORTB
 *
 * Vcc : +5V, GND : ground
 * DIO : data (board pin 8)     (PB0)
 * CLK : clock (board pin 9)    (PB1)
 * STB : strobe (board pin 10) (PB2)
 *
 */

#include <avr/io.h>
#include <stdint.h>
#define F_CPU 16E6
#include <util/delay.h>
#include "AVR_TTC_scheduler.c"

#define HIGH 0x1
#define LOW  0x0

const uint8_t data = 0;
const uint8_t clock = 1;
const uint8_t strobe = 2;

void counting(void); // need to put them in .h

// read value from pin
int read(uint8_t pin)
{
    if (PINB & _BV(pin)) { // if pin set in port
        return HIGH;
    } else {
        return LOW;
    }
}

// write value to pin
void write(uint8_t pin, uint8_t val)
{
    if (val == LOW) {
        PORTB &= ~(_BV(pin)); // clear bit
    } else {
        PORTB |= _BV(pin); // set bit
    }
}

// shift out value to data
void shiftOut (uint8_t val)
{
    uint8_t i;
    for (i = 0; i < 8; i++)  {
        write(clock, LOW);   // bit valid on rising edge
        write(data, val & 1 ? HIGH : LOW); // lsb first
        val = val >> 1;
        write(clock, HIGH);
    }
}

void sendCommand(uint8_t value)
{
    write(strobe, LOW);
    shiftOut(value);
    write(strobe, HIGH);
}

void reset()
{
    // clear memory - all 16 addresses
    sendCommand(0x40); // set auto increment mode
    write(strobe, LOW);
    shiftOut(0xc0);   // set starting address to 0
    for(uint8_t i = 0; i < 16; i++)
    {
        shiftOut(0x00);
    }
    write(strobe, HIGH);
}

void setup()
{
     DDRB=0xff; // set port B as output

    sendCommand(0x89);  // activate and set brightness to medium
//  reset();
}

void counting()
{
                                 /*0*/  /*1*/   /*2*/  /*3*/  /*4*/  /*5*/  /*6*/  /*7*/   /*8*/  /*9*/
    uint8_t digits[] = { 0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f };

    static long teller = 0;
	uint8_t x = log10(teller) + 1;
	long nummer = teller;
	uint8_t digit;
	int lijst[x+1];
	
	for(uint8_t y = 0; y <= x; y++)
	{
		lijst[y] = nummer % 10; // als number = 0 dan array{0,0}
		nummer = nummer / 10;
	}

    sendCommand(0x40); // auto-increment address
    write(strobe, LOW);
    shiftOut(0xc0); // set starting address = 0
    for(uint8_t position = 8; position > 0; position--)
    {
        if(position > x) // als x = 1 dan digit = array[0]
		{
			shiftOut(0x00);
			shiftOut(0x00);
		}
		else
		{
			digit = lijst[position - 1];
			shiftOut(digits[digit]);
			shiftOut(0x00);
		}
	}
		

    write(strobe, HIGH);

   teller++;
}


int main()
{

    setup();
	SCH_Init_T1(); // init de timer en verwijder alle taken
	SCH_Add_Task(counting,0,50);
	SCH_Start(); // start de scheduler
	

    while (1) {
    SCH_Dispatch_Tasks();
       
    }
    
    return(0);
}