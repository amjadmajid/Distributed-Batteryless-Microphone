#include "main.h"

void main_init() {
    WDTCTL = WDTPW | WDTHOLD;   // stop watchdog timer
    PM5CTL0 &= ~LOCKLPM5;       // deactivate high impedance mode for GPIO

    // wake on sound
    mic_wake_up_init();

#if defined(SIMULATION)
    start_power_simulation(36866); // 36866 = 294930 us = 9 frames
#endif

#if defined(LOGIC)
    // output pins for logic analyzer
    P3DIR = BIT0|BIT1;
    P3OUT = BIT0;
#endif

#if defined(UART)
    uart_init();
#endif
}


int main(void)
{
    uint16_t temp;

    main_init();

    while (1) {             // loop for: recording->detecting->analyzing->comparing->..
        switch(state) {

        case RECORD:
            mic_wait_for_sound();

            #if defined(LOGIC)
                P3OUT |= BIT1;
            #endif

            counter = 0;
            ADC_init();
            ADC_start();
            while(counter < SAMPLES);

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
                temp = linear_compare(fp_rec.data, wordlist[lib_index], NUM_FRAME, NUM_FRAME);
                if (temp <= word_value) {
                    word_value = temp;
                    word_index = lib_index;
                    }
                }

            if (word_index != -1) {

                #if defined(UART)
                    uint8_t * c = words[word_index];
                    uart_sendStr(c);
                    uart_sendHex16(word_value);
                #endif
            }
            /* no break */

        default:
            state = RECORD;
            break;
        } // end switch
    }

	return 0;
}





void compare_init() {
    word_value = VERY_BIG;
    word_index = -1;
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
//    uint16_t freq;
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
            if (msp_fft_auto_q15(&fftParams, vec, &shift)) uart_sendText("FFT_ERR", 7);
        #else
            msp_fft_auto_q15(&fftParams, vec, &shift);
        #endif

        // To eliminate the IF statements in the following FOR loop,
        // the FOR loop is split in multiple WHILE loops. See below

//        for ( j=(100/(SAMPLERATE / FRAMESIZE))+1 ; j < (4000/(SAMPLERATE / FRAMESIZE)); j++) {     // range such that freq is from 100-4000 Hz
////        for ( j=0 ; j < FRAMESIZE; j++) {
//            freq = j * (SAMPLERATE / FRAMESIZE);
//            if (freq > 100 && freq < 300) hist[0] += squared(vec[j]); // mag^2 = energy
//            if (freq > 250 && freq < 450) hist[1] += squared(vec[j]);
//            if (freq > 400 && freq < 600) hist[2] += squared(vec[j]);
//            if (freq > 550 && freq < 750) hist[3] += squared(vec[j]);
//            if (freq > 700 && freq < 900) hist[4] += squared(vec[j]);
//            else if (freq > 900 && freq < 1200) hist[5] += squared(vec[j]);
//            else if (freq > 1200 && freq < 1500) hist[6] += squared(vec[j]);
//            else if (freq > 1500 && freq < 1800) hist[7] += squared(vec[j]);
//            else if (freq > 1800 && freq < 2300) hist[8] += squared(vec[j]);
//            else if (freq > 2300 && freq < 2800) hist[9] += squared(vec[j]);
//            else if (freq > 2800 && freq < 3400) hist[10] += squared(vec[j]);
//            else if (freq > 3400 && freq < 4000) hist[11] += squared(vec[j]
//        }

//            ||
//           \||/
//            \/

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
void ADC_init()
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

}

void ADC_start()
{
    // Enable interrupt for (only) MEM0
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
#else
#error Compiler not supported!
#endif
{
    switch(__even_in_range(P5IV, P5IV__P5IFG7))
        {
            case P5IV__NONE:    break;          // Vector  0:  No interrupt
            case P5IV__P5IFG0:  break;          // Vector  2:  P5.0 interrupt flag
            case P5IV__P5IFG1:                  // Vector  4:  P5.1 interrupt flag

                #if defined(SIMULATION)
                    switch_timer_to_short();
                    __bic_SR_register_on_exit(LPM0_bits); // Exit LPM0
                #else
                    __bic_SR_register_on_exit(LPM4_bits); // Exit LPM4
                #endif
                mic_normal_mode();
                break;
            case P5IV__P5IFG2:  break;          // Vector  6:  P5.2 interrupt flag
            case P5IV__P5IFG3:  break;          // Vector  8:  P5.3 interrupt flag
            case P5IV__P5IFG4:  break;          // Vector  10:  P5.4 interrupt flag
            case P5IV__P5IFG5:  break;          // Vector  12:  P5.5 interrupt flag
            case P5IV__P5IFG6:  break;          // Vector  14:  P5.6 interrupt flag
            case P5IV__P5IFG7:  break;          // Vector  16:  P5.7 interrupt flag
            default: break;
        }
}
