
//#include <stdio.h>
#include "../dsplib/include/DSPLib.h"
#include "../mspProfiler/include/mspProfiler.h"
#include "../mspPwrSim/include/mspPwrSim.h"
#include "common.h"
#include "wake_on_sound.h"


enum state_t {RECORD, DETECT, ANALYZE, COMPARE};

void        ADC_config              ();
void        ADC_stop                ();
void        desync_init             ();
void        desync                  ();
uint32_t    squared                 (int16_t x);
void        endpoints_power_init    ();
int         endpoints_power         (uint16_t *buf, fingerprint *fp, int step);
void        endpoints_ZCR_init      ();
int         endpoints_ZCR           (uint16_t *buf, fingerprint *fp);
void        get_fingerprint         (uint16_t *buf, fingerprint *fp);
void        compare_init            ();
uint16_t    dtw_full                (int16_t x[NUM_FRAME*BANDS], const int16_t y[], uint16_t xsize, uint16_t ysize);
uint16_t    dtw_window              (int16_t x[NUM_FRAME*BANDS], const int16_t y[], uint16_t xsize, uint16_t ysize);
uint16_t    linear_compare          (int16_t x[NUM_FRAME*BANDS], const int16_t y[], uint16_t xsize, uint16_t ysize);




// configure FFT and initialize some arrays in FRAM

#if defined(MSP_USE_LEA)
    msp_fft_q15_params fftParams = {FRAMESIZE, 1, 0};
#else
    msp_fft_q15_params fftParams = {FRAMESIZE, 1, msp_cmplx_twiddle_table_128_q15};
#endif

DSPLIB_DATA(vec,MSP_ALIGN_FFT_Q15(FRAMESIZE))
int16_t  vec[FRAMESIZE];


// main
__nv enum state_t state = RECORD;
__nv fingerprint fp_rec;
__nv uint16_t lib_index = 0;
__nv uint16_t word_value[NUM_WORDS+1] = { [NUM_WORDS] = 65535};
__nv int16_t  word_index;
__nv uint16_t i_nv      = 0;
__nv uint16_t j_nv      = 0;
__nv int      __randSel = 0;

// Recording
volatile int16_t counter;
__nv uint16_t sampled_input[SAMPLES] = {0};

// get_fingerprint
#define TILL_X_INTO_BIN_A(X, A)\
    while (j < ((X)/(SAMPLERATE / FRAMESIZE))) {\
        hist[(A)] += squared(vec[j]);\
        j++;\
}

#define TILL_X_INTO_BINS_A_B(X, A, B)\
    while (j < ((X)/(SAMPLERATE / FRAMESIZE))) {\
        energy = squared(vec[j]);\
        hist[(A)] += energy;\
        hist[(B)] += energy;\
        j++;\
}

// Endpoints -> endpoints.h
// DTW -> in dtw.h


 const int16_t word_clear[9*12] = {
    1, 1, 0, 0, 1, 3, 0, -1, 0, -1, 0, 1,
    0, -1, -1, 0, 0, 1, 0, 0, 2, 0, 2, 2,
    -1, -1, 2, 3, 2, 0, -1, -1, 1, 0, 0, 0,
    0, 0, 3, 2, 3, 2, -2, -1, -1, 0, 0, 0,
    1, 1, 3, 5, 6, 2, -1, -2, -3, -1, -1, 1,
    0, 1, 4, 4, 6, 1, -1, -2, -2, -2, -1, 0,
    1, 2, 4, 4, 6, 2, 0, -1, -2, -3, -2, 0,
    0, 0, 5, 3, 6, 4, 0, -2, -2, -2, -2, 0,
    0, 3, 4, 4, 6, 3, 0, -3, -2, -3, -1, 0
 };


 const int16_t word_edit[9*12] = {
   -1, 0, 3, 3, 4, 5, 0, -2, -2, -2, 0, 1,
   -2, -1, 3, 1, 3, 5, 0, -4, -2, -2, -1, 2,
   0, 2, 3, 4, 4, 4, 0, -1, -2, -2, 0, -1,
   0, 3, 2, 3, 3, 3, -1, -3, -2, -2, 0, -1,
   0, 1, 1, 3, 4, 1, -1, -2, -1, -3, -2, 0,
   0, 3, 3, 5, 5, 2, -2, -4, -3, -3, -2, 0,
   1, 1, 2, 5, 4, 1, -3, -4, -2, -2, -1, 1,
   1, 1, 2, 3, 3, 0, -1, -2, -1, -1, -1, 0,
   2, 0, 1, 2, 3, 0, -1, -2, 0, 0, 0, 1
 };

const int16_t word_go[9*12] = {
    0, 0, 3, 2, 3, 0, -2, -4, -1, 0, 0, -1,
    -1, -1, 3, 2, 6, 0, -3, -2, -1, 1, -2, -2,
    -3, 0, 3, 3, 6, 3, -1, -2, 1, 1, -2, -3,
    -1, -1, 3, 3, 6, 2, 1, -1, 3, 0, -2, -2,
    -4, -1, 3, 3, 6, 3, 0, -1, 2, 0, -3, -3,
    -1, -1, 2, 4, 6, 3, -1, -1, 2, -1, -4, -4,
    -4, 2, 4, 5, 4, 3, -2, 0, 1, -4, -4, -5,
    -1, 2, 3, 3, 6, 3, -1, -1, 1, -4, -5, -4,
    -1, 2, 4, 4, 4, 0, -1, -1, 0, -3, -4, -4
};

const int16_t word_load[9*12] = {
     2, 2, 4, 6, 3, 5, -3, -3, -2, -1, -2, -2,
     0, -1, 3, 1, 3, 5, 0, -3, -1, 1, -2, -6,
     -1, -1, 3, -1, 4, 6, 2, -2, 1, 2, -2, -5,
     -1, 0, 3, 3, 5, 6, 1, -1, 1, 1, -3, -4,
     -1, -1, 3, 4, 4, 8, 0, -2, 2, 0, -3, -4,
     0, 2, 2, 4, 7, 5, 0, -1, 1, -1, -4, -4,
     1, 2, 3, 3, 6, 4, 0, -1, 1, -2, -3, -3,
     2, 1, 4, 3, 5, 1, -3, -2, 1, -1, -1, -2,
     1, 2, 3, 1, 3, 4, -1, -1, -1, 0, 0, -1
};

 const int16_t word_off[9*12] = {
      1, 2, 4, 4, 5, 6, 2, 1, -3, -5, -5, -5,
      -1, -1, 4, 3, 5, 6, 3, 0, -2, -4, -4, -5,
      -1, 1, 3, 3, 6, 5, 3, 1, -2, -3, -3, -4,
      -1, 2, 1, 0, 6, 6, 3, 0, -3, -4, -5, -5,
      -1, 0, 1, 2, 3, 4, 1, 0, -2, -2, -3, -3,
      1, 0, 2, 1, 1, 2, -1, -1, -1, -1, 1, 1,
      1, 0, 0, -1, 0, 1, -1, -1, 0, 1, 3, 3,
      1, 1, 2, 1, 1, 1, 0, -1, 0, 0, 3, 2,
      0, 0, 1, 2, 2, -1, 1, 0, 0, 1, 1, 3
 };


 const int16_t word_on[9*12] = {
     1, 2, 1, 2, 1, 2, 0, 0, 2, 1, -3, -3,
     0, 1, 1, 3, 2, 2, 1, 1, 3, -1, -4, -4,
     1, 2, 2, 3, 3, 2, 0, 1, 2, 0, -4, -3,
     -1, 2, 2, 1, 2, 1, 1, 0, 3, 0, -2, -4,
     -2, 0, 2, 1, 2, 0, 3, 1, 3, 2, -2, -3,
     -1, 1, 2, 0, 0, 1, 1, 0, 1, 2, -3, -3,
     -2, 2, 2, 2, 1, 2, 2, -1, 1, 1, -2, -3,
     0, 1, 3, 3, 3, 0, 0, 1, 0, 1, -1, -2,
     1, 1, 3, 0, 1, 0, 0, 0, 0, -1, -1, 0
 };

 const int16_t word_pause[9*12] = {
    0, 0, 3, 3, 2, 4, 4, 2, 3, -2, -4, -4,
    -1, 0, 3, 3, 2, 4, 5, 2, 2, -3, -3, -5,
    0, 1, 2, 3, 1, 5, 5, 3, 4, -3, -5, -5,
    -1, 1, 1, 1, 3, 3, 3, 3, 1, -3, -5, -5,
    -1, 1, 1, 1, 3, 4, 3, 3, 1, -3, -4, -5,
    0, 0, 2, 3, 3, 4, 3, 2, 1, -2, -3, -3,
    -1, 0, 3, 3, 4, 4, 2, 1, 0, -2, -2, -1,
    1, 1, 3, 3, 3, 3, 1, -1, 0, -1, -2, -3,
    0, 0, 1, -1, 1, 0, 1, 0, 0, -1, 2, 2
 };


 const int16_t word_cancel[9*12] = {
    1, 0, -1, 1, 1, 0, 0, -1, 0, -1, 0, 2,
    -2, -1, 2, 3, 4, 5, 1, -1, 0, -1, 0, -1,
    -1, 1, 2, 3, 2, 4, 0, -2, -2, -2, 0, -1,
    1, 1, 2, 3, 1, 4, 1, -2, 0, 0, 0, 0,
    1, 2, 1, 2, 2, 2, 0, -2, -3, -2, 0, -1,
    2, 2, 3, 2, 2, 1, -1, 0, -1, -1, 2, 0,
    1, 2, 2, 1, 2, 1, 0, -1, -3, -1, -1, -1,
    1, 2, 2, 3, 2, 1, 0, -1, -2, -1, -1, 0,
    -1, 0, 2, 1, -1, 1, -1, -1, -1, 0, 2, 4
 };


 const int16_t word_resume[9*12] = {
 1, 2, 4, 5, 5, 1, -4, -5, -2, -2, -1, 0,
 1, 1, 4, 5, 5, -1, -2, -3, -2, -2, -2, -1,
 0, 0, 2, 0, 1, -1, 0, -2, -1, -1, 1, 1,
 -3, -1, -1, 0, 0, 0, -1, 0, 2, 2, 1, 2,
 -2, -2, -1, -1, -2, 1, 1, 2, 3, 2, 1, 1,
 -1, 0, 1, 1, 0, -1, -1, 2, 1, 2, 1, 0,
 0, 2, 3, 4, 4, 1, -2, -2, -1, -2, -1, 0,
 0, 1, 3, 3, 4, 1, -2, -3, -2, -1, -2, 0,
 1, 3, 4, 4, 5, 2, 0, -2, -2, -2, -2, 0
 };

const int16_t word_stop[9*12] = {
  0, -2, -1, -1, -1, -1, 0, 1, 2, 1, 1, 2,
  -1, -3, -3, -1, 1, 0, 0, 2, 3, 3, 2, 4,
  1, 1, -1, 0, 1, 0, -1, -1, -2, 1, 1, 2,
  1, 0, 0, -1, 0, 2, -1, 0, 1, 2, 1, 3,
  -2, 0, 0, 2, 3, 3, 2, -1, 1, 2, -1, 0,
  -1, -1, 2, 1, 3, 2, 2, -1, 2, 1, -2, -3,
  -3, -1, 2, 1, 1, 2, 3, -1, 3, 0, -2, -1,
  -2, -2, 0, 0, 1, 1, 3, 1, 4, 1, -2, -2,
  -2, -1, 1, -1, 1, 2, 3, 1, 4, 0, -3, -5
};

const int16_t *wordlist[NUM_WORDS] = {word_clear, word_edit, word_go, word_load, word_off, word_on, word_pause, word_cancel, word_resume, word_stop};
const int wordlength[NUM_WORDS] = {9, 9, 9, 9, 9, 9, 9, 9, 9, 9};
const char words[NUM_WORDS][10] = {" clear", " edit", " go", " load", " off", " on", " pause", " cancel", " resume", " stop"};
