#include <msp430.h> 
#include "mspDebugger.h"

#ifndef __nv
#define __nv  __attribute__((section(".nv_vars")))
#endif

// off-time and sleep-time expressed in on-time
#define OFF_FACTOR 18 // 9 times really, but on-time is doubled manually
#define SLEEP_FACTOR 38


__nv int __noise[] = {
#include "../mspPwrSim/pattern_on.txt"
};

__nv unsigned int __noiseSel = 0;
unsigned int rstInterval = 0;
unsigned int timecounter = 0;
unsigned int power = 1;
unsigned int low_power_mode = 0;


void start_power_simulation(unsigned int interval)
{
    power = 1;
    timecounter=1; // so t_on = (1+1) * interval; set to 0 if no factor is needed
    rstInterval = interval;

    if(__noiseSel >= 200) {
       __noiseSel=0;
    }

    TA0CCTL0 = CCIE;                          // TACCR0 interrupt enabled
    TA0CCR0 =rstInterval+__noise[__noiseSel]; // comment: noise is amplified as well by divider
    TA0CTL = TASSEL__SMCLK | MC__UP | ID_3;   // SMCLK, counting up, divider 8

    __noiseSel++;
    __bis_SR_register(GIE);       // enable general interrupt
}

void switch_timer_to_short(){
    int newcounter;
    //stop timer
    TA0CTL = MC__STOP;
    TA0R = 0;
    //read timecounter and set new timer
    newcounter = timecounter / SLEEP_FACTOR;
    TA0CCR0 = (timecounter % SLEEP_FACTOR) * ((rstInterval/SLEEP_FACTOR) ); // How short timer depends on time left in long timer
    timecounter = newcounter;
    //start timer
    TA0CTL = TASSEL__SMCLK | MC__UP | ID_3;
}

void switch_timer_to_long(){
    //stop timer
    TA0CTL = MC__STOP;
    //read timer and set new counter
    timecounter *= SLEEP_FACTOR;
    timecounter += (rstInterval-TA0R) / (rstInterval/SLEEP_FACTOR); // How long timer depends on time left in short timer
    TA0R = 0;
    TA0CCR0 = rstInterval;
    //start timer
    TA0CTL = TASSEL__SMCLK | MC__UP | ID_3;
}

void adapt_energy_buffer() {
    if (timecounter >= SLEEP_FACTOR) {
        timecounter -= SLEEP_FACTOR;
        low_power_mode = 1;
    }
    else {
        // recharge
        P5IE &= ~BIT1;       // disable mic interrupt
        ADC12IER0 &= ~ADC12IE0;  // disable ADC interrupt
        TA1CCR0 = 0; // stop other timer

        power=0;  // turn node "off"
        timecounter = (OFF_FACTOR-1) - ((timecounter * OFF_FACTOR/2)/SLEEP_FACTOR);
        P3OUT &= ~(BIT0|BIT1); // for logic analyzer

        if(__noiseSel >= 200)  __noiseSel=0;

        TA0CCR0 = rstInterval+__noise[__noiseSel];
        __noiseSel++;

        // sleep LPM0 -> SMCLOCK remains active if SMCLKOFF = 0 (if SMCLK in use)
        __bis_SR_register(LPM0_bits | GIE);
        __no_operation();
    }
}

void revert_energy_buffer() {
    timecounter += SLEEP_FACTOR;
    low_power_mode = 0;
}

// Timer0_A0 interrupt service routine
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector = TIMER0_A0_VECTOR
__interrupt void Timer0_A0_ISR (void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(TIMER0_A0_VECTOR))) Timer0_A0_ISR (void)
#else
#error Compiler not supported!
#endif
{
    if (power==1){
        if (timecounter==0) {
            P5IE &= ~BIT1;       // disable mic interrupt
            ADC12IER0 &= ~ADC12IE0;  // disable ADC interrupt
            TA1CCR0 = 0; // stop other timer

            power=0;  // turn node "off" in next if statement (same run of ISR)
            P3OUT &= ~(BIT0|BIT1); // for logic analyzer
            if (low_power_mode) {
                timecounter = OFF_FACTOR/2;
            }
            else {
                timecounter = OFF_FACTOR;
            }
        }
        else {
            timecounter--;
            if(__noiseSel >= 200)  __noiseSel=0;

            TA0CCR0 = rstInterval+__noise[__noiseSel];
            __noiseSel++;
        }
    }

    if (power==0) {     // simulating the time that the node is off-line and harvesting energy

        if (timecounter != 0){
            timecounter--;

            if(__noiseSel >= 200)  __noiseSel=0;

            TA0CCR0 = rstInterval+__noise[__noiseSel];
            __noiseSel++;

            // sleep LPM0 -> SMCLOCK remains active if SMCLKOFF = 0 (if SMCLK in use)
            __bis_SR_register(LPM0_bits | GIE);
            __no_operation();
        }

        else    // reset
            {
            __no_operation();
            PMMCTL0 = PMMPW|PMMSWBOR;
            }
    }


}
