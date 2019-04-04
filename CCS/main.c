#include "main.h"

void gpio_init()
{
    P1OUT = 0;                                  // All P1.x reset
    P1DIR = 0xFF;                               // All P1.x outputs
    P2OUT = 0;                                  // All P2.x reset
    P2DIR = 0xFF;                               // All P2.x outputs
    P3OUT = 0;                                  // All P3.x reset
    P3DIR = 0xFF;                               // All P3.x outputs
    P4OUT = 0;                                  // All P4.x reset
    P4DIR = 0xFF;                               // All P4.x outputs
    PJOUT = 0;                                  // All PJ.x reset
    PJDIR = 0xFFFF;                             // All PJ.x outputs

}

void main_init() {
    WDTCTL = WDTPW | WDTHOLD;   // stop watchdog timer
    PM5CTL0 &= ~LOCKLPM5;       // deactivate high impedance mode for GPIO

    gpio_init();

    // wake on sound
    mic_wake_up_init();

#if defined(SIMULATION)
    start_power_simulation(36866); // 36866 = 294930 us = 9 frames
#endif

#if defined(LOGIC)
    // output pins for logic analyzer
    P3DIR |= BIT0|BIT1;
    P3OUT = 0;
    P3OUT |=BIT0;
#endif

#if defined(UART)
    uart_init();
#endif

#if defined(DESYNC)
    desync_init();
#endif
}


int main(void)
{
    main_init();

    while (1) {             // loop for: recording->detecting->analyzing->comparing->..
        switch(state) {

        case RECORD:

            #if defined(SIMULATION)
                switch_timer_to_long();
                adapt_energy_buffer();
//            TA0CTL = MC__STOP;
            #endif

//                mic_normal_mode();
            mic_wait_for_sound();

            #if defined(DESYNC)
                desync();  // add loop with P=50%
            #endif

            #if defined(SIMULATION)
//            TA0CTL = TASSEL__SMCLK | MC__UP | ID_3;
                revert_energy_buffer();
                switch_timer_to_short();
            #endif

            #if defined(LOGIC)
                P3OUT |= BIT1;
            #endif

            counter = 0;
            ADC_config();
            while(counter < SAMPLES);
            mic_power_off();

            // needed for get_fingerprints()
            fp_rec.start = 0;
            fp_rec.end = NUM_FRAME;
            i_nv = fp_rec.start;

            #if defined(LOGIC)
                P3OUT &= ~BIT1;
            #endif
            state = ANALYZE;

            break;

        case ANALYZE:
            get_fingerprint(sampled_input, &fp_rec);

            compare_init();
            state = COMPARE;
            break;

        case COMPARE:
            for( ; lib_index<NUM_WORDS ; lib_index++) {
                word_value[lib_index] = linear_compare(fp_rec.data, wordlist[lib_index], NUM_FRAME, NUM_FRAME);
                if (word_value[lib_index] <= word_value[word_index]) {
                    word_index = lib_index;
                    }
                }

            #if defined(UART)
                if (word_index != NUM_WORDS) {
                    uart_sendStr( (uint8_t const *) words[word_index]);
                    uart_sendHex16(word_value[word_index]);
                }
            #endif
            /* no break */

        default:
            state = RECORD;
            break;
        } // end switch
    }

	return 0;
}



void desync_init() {
    TA1CCTL0 = CCIE;                        // TACCR0 interrupt enabled
    TA1CCR0 = 0; // don't start timer yet
    TA1EX0 = TAIDEX_1; // pre-divider 2
//    TA1CTL = TACLR | TASSEL__SMCLK | MC__UP | ID_3;   // SMCLK, counting up, divider 8
    TA1CTL = TACLR | TASSEL__ACLK | MC__UP;   // ACLK, counting up
}


void desync() {
    /*
     * Delay recording for de-synchronization
     * To be used in a setup with multiple nodes, to prevent all of them reacting to the same event, and miss the next one because of that.
     * The random number is based on LSBs from ADC values. P=50% is used
     */
    while (sampled_input[__randSel++] & 0x01) {
        if(__randSel >= SAMPLES) __randSel=0;
        // sleep for the time of 1 word
        mic_power_off();
        TA1CCR0 = 13000;  // +-700 ms

        P3OUT &= ~BIT0;
        __bis_SR_register(LPM3_bits | GIE);
        P3OUT |= BIT0;

        mic_wait_for_sound(); // will go into normal mode when wakes up.
    }
}

void compare_init() {
    word_index = NUM_WORDS;
    lib_index = 0;
}

uint32_t squared(int16_t x) {
//    return x*x;

    *((volatile int *)&MPYS) = x;   // First operand
    *((volatile int *)&OP2) = x;   // Second operand

    __no_operation();

    uint32_t result = ( (uint32_t) RESHI<<16 ) | RESLO;

    return result;
}


int16_t uint32_log2(uint32_t n)
/*
 * Integer Log function
 *      (from https://stackoverflow.com/posts/24748637/revisions)
 *
 * returns -1  if n == 0
 */
{
  #define S(k) if (n >= (UINT32_C(1) << k)) { i += k; n >>= k; }

  int i = -(n == 0);  S(16); S(8); S(4); S(2); S(1); return i;

  #undef S
}

void get_fingerprint(uint16_t *buf, fingerprint *fp) {
    /*
     * Computes "fingerprint" of spoken word by performing FFT and sorting the outcome into "spectral bands" (like histogram).
     *      After that normalizes the fingerprint.
     * @param buf: sound file (16-bit unsigned assumed here)
     * @param fp: fingerprint struct, with the frame numbers where the spoken word starts and ends in the buffer stored in fp.start and fp.end .
     *              the fingerprint itself will be stored in fp.data
     * @var i_nv: non volatile index, needs to be initialized to zero before the first run of this function!
     */
    uint32_t hist[12];
    uint16_t j;
    uint16_t shift;

    uint32_t energy;

    // PERFORM FFT ON FRAMES, SORT OUTCOME INTO SPECTRAL BANDS

    for ( ; i_nv < fp->end; i_nv++) {

        for ( j = 0; j < BANDS; j++) {  // init to 0
            hist[j] = 0;
        }

        for( j = 0; j < FRAMESIZE; j++) {   // copy values to vector in LEA-RAM section for FFT
            vec[j] = buf[FRAMESIZE*i_nv+j];
        }

        // use fft to compute energy in each spectral band
        #if defined(UART)
            if (msp_fft_auto_q15(&fftParams, vec, &shift)) uart_sendStr( (uint8_t const *) "FFT_ERR");
        #else
            msp_fft_auto_q15(&fftParams, vec, &shift);
        #endif


        j=(100/(SAMPLERATE / FRAMESIZE))+1;

        TILL_X_INTO_BIN_A(250,0)
        TILL_X_INTO_BINS_A_B(300,0,1)
        TILL_X_INTO_BIN_A(400,1)
        TILL_X_INTO_BINS_A_B(450,1,2)
        TILL_X_INTO_BIN_A(550,2)
        TILL_X_INTO_BINS_A_B(600,2,3)
        TILL_X_INTO_BIN_A(700,3)
        TILL_X_INTO_BINS_A_B(750,3,4)
        TILL_X_INTO_BIN_A(900,4)
        TILL_X_INTO_BIN_A(1200,5)
        TILL_X_INTO_BIN_A(1500,6)
        TILL_X_INTO_BIN_A(1800,7)
        TILL_X_INTO_BIN_A(2300,8)
        TILL_X_INTO_BIN_A(2800,9)
        TILL_X_INTO_BIN_A(3400,10)
        TILL_X_INTO_BIN_A(4000,11)

        // NORMALISATION OF SPECTRAL BANDS
        // norm = log(energy_in_band) - sum(log(energies_in_bands)) / #bands

        uint16_t average = 0;

        for ( j = 0; j < BANDS; ++j) {
            average += uint32_log2(hist[j]);
        }
        average /= BANDS;

        // update fingerprint
        for ( j = 0; j < BANDS; ++j) {
            fp->data[(i_nv-fp->start)*BANDS + j] = uint32_log2(hist[j]) - average;
        }
    }
    return;
}


/**
 * Configure ADC for microphone sampling
 */
void ADC_config()
{
    // Pin P1.3 set for Ternary Module Function (which includes A3)
    P1SEL0 |= BIT3;
    P1SEL1 |= BIT3;

    // Clear ENC bit to allow register settings
    ADC12CTL0 &= ~ADC12ENC;

    // Clock source select
    //
    // source: MCLK (DCO, 1 MHz)
    // pre-divider: 4
    // divider: 1
    ADC12CTL1 |= ADC12SSEL_2 | ADC12PDIV_1 | ADC12DIV_0;

    // sampling period select for MEM0: 16 clock cycles (*)
    // multiple sample and conversion: enabled
    ADC12CTL0 |= ADC12SHT0_2 | ADC12MSC;
    // (*) freq = MCLK / (ADC12PDIV_1 * ADC12SHT0_2)
    //          = 1000000 / (4 * 16)
    //          = 15625 Hz (should be)
    //          != 7812.5 Hz (getting this)

    // conversion sequence mode: repeat-single-channel
    // pulse-mode select: SAMPCON signal is sourced from the sampling timer
    ADC12CTL1 |= ADC12CONSEQ_2 | ADC12SHP;

    // resolution: 12 bit
    // data format: right-aligned, unsigned
    ADC12CTL2 |= ADC12RES__12BIT ;
    ADC12CTL2 &= ~ADC12DF;
    // conversion start address: MEM0
    ADC12CTL3 |= ADC12CSTARTADD_0;

    // MEM0 control register
    // reference select: VR+ = AVCC (3V), VR- = AVSS (0V)
    // input channel select: A3
    ADC12MCTL0 |= ADC12VRSEL_0 | ADC12INCH_3;

    // Clear interrupt for MEM0
    ADC12IFGR0 &= ~ADC12IFG0;

    // Enable general interrupt
    __enable_interrupt();

    // Enable interrupt for MEM0
    ADC12IER0 = ADC12IE0;

    // Trigger first conversion (Enable conversion and Start conversion)
    // ADC module ON
    ADC12CTL0 |= ADC12ENC | ADC12SC | ADC12ON;
}

void ADC_stop()
{
    // disable ADC conversion and disable interrupt request for MEM0
    ADC12CTL0 &= ~ADC12ENC;
    ADC12IER0 &= ~ADC12IE0;

    // turn off the ADC to save energy
    ADC12CTL0 &= ~ADC12ON;
}

#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=ADC12_VECTOR
__interrupt
#elif defined(__GNUC__)
__attribute__((interrupt(ADC12_VECTOR)))
#endif
void ADC12_ISR(void)
{
    switch(__even_in_range(ADC12IV,12))
    {
    case 12:                                // Vector 12:  ADC12BMEM0 Interrupt
        if (counter < SAMPLES)
            // Read ADC12MEM0 value
            sampled_input[counter++] = ADC12MEM0;
        else {
            ADC_stop();
        }
        break;

    default: break;
    }
}

// Port 5 interrupt service routine
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector=PORT5_VECTOR
__interrupt void port5_isr_handler(void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(PORT5_VECTOR))) port5_isr_handler (void)
#endif
{
    switch(__even_in_range(P5IV, P5IV__P5IFG7))
        {
            case P5IV__P5IFG1:                  // Vector  4:  P5.1 interrupt flag
                #if defined(SIMULATION)
//                    switch_timer_to_short();
                    __bic_SR_register_on_exit(LPM0_bits); // Exit LPM0
                #else
                    __bic_SR_register_on_exit(LPM3_bits); // Exit LPM3
                #endif
                mic_normal_mode();
                break;
            default: break;
        }
}


// Timer A1 interrupt service routine
#if defined(__TI_COMPILER_VERSION__) || defined(__IAR_SYSTEMS_ICC__)
#pragma vector = TIMER1_A0_VECTOR
__interrupt void Timer1_A0_ISR(void)
#elif defined(__GNUC__)
void __attribute__ ((interrupt(TIMER1_A0_VECTOR))) Timer1_A0_ISR (void)
#endif
{
    TA1CCR0 = 0; //stop timer
    __bic_SR_register_on_exit(LPM3_bits); // Exit LPM3

}

