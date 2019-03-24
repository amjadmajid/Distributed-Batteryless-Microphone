/*
 * This library is to be used with the PMM-3738-VM1010-R MEMS microphone.
 * It enables the MSP430 to sleep until sound is detected.
 *
 * Pin 5.0 is used to set  mode (output)
 * Pin 5.1 is used to read d_out (input)
 *
 * Optionally pin 5.2 can be used to power the microphone, so it will be powered off when not needed.
 */

#include "include/common.h"


void mic_wake_up_init() {

    // Pin for powering microphone
    P5DIR |= BIT2;     // use 5.2 as output
    P5OUT &= ~BIT2;     // power off

    // make mode pin low (normal mode)
//    P5SELC &= ~BIT0;     // set 5.0 to GPIO
    P5DIR |= BIT0;      // use 5.0 as output
    P5OUT &= ~BIT0;     // low output

    // read d_out from microhpone
//    P5SELC &= ~BIT1;     // set 5.1 to GPIO
    P5DIR &= ~BIT1;     // use 5.1 as input
    P5REN |= BIT1;      // Enable pull-up / pull-down
    P5OUT &= ~BIT1;     // Select pull down resistor
    P5IES &= ~BIT1;     // Rising edge
    P5IFG = 0;          // Clear all P5 interrupt flags
    P5IE |= BIT1;       // P5.1 interrupt enabled
}


void mic_wait_for_sound() {
    //set microhpone to wake_on_sound mode
    P5OUT |= BIT0 | BIT2;

#if defined(SIMULATION)
    __bis_SR_register(LPM0_bits | GIE);
    __no_operation();                   // For debugger
#else
    //sleep
    __bis_SR_register(LPM3_bits | GIE); // Enter LPM3 w/interrupt
    __no_operation();                   // For debugger
#endif
}


void mic_normal_mode() {
    P5OUT |= BIT2;
    P5OUT &= ~BIT0;
}

void mic_power_off() {
    P5OUT &= ~ (BIT2 | BIT0);
}


// ADD THIS TO ISR:
//__bic_SR_register_on_exit(LPM3_bits); // Exit LPM3
//mic_normal_mode();
