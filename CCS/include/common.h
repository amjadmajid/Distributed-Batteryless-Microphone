#include <msp430.h>
#include <stdint.h>

#define UART
#define LOGIC
//#define SIMULATION
//#define DESYNC

#define SAMPLERATE  7812
#define FRAMESIZE   256
#define NUM_WORDS   10
#define VERY_BIG    65535
#define BANDS       12
#define NUM_FRAME   9
#define SAMPLES     (NUM_FRAME*FRAMESIZE)

// For endpoint detection:
#define RECORDING_OFFSET 980//2048
#define ZCR_THRESHOLD    70


typedef struct fingerprint {
    uint16_t    start; // first frame of the word
    uint16_t    end;   // the frame after the last frame
    int16_t     data[NUM_FRAME*BANDS];
} fingerprint;



// From https://stackoverflow.com/a/32107675
#define max(x,y) ( \
    { __auto_type __x = (x); __auto_type __y = (y); \
      __x > __y ? __x : __y; })

#define min(x,y) ( \
    { __auto_type __x = (x); __auto_type __y = (y); \
      __x < __y ? __x : __y; })



#if defined(__TI_COMPILER_VERSION__)
#error "Non-volatile variables not defined for TI compiler. Please use #pragma PERSISTENT(var_name) additionally to the declaration."
//    #pragma PERSISTENT(word_index)
//    int16_t  word_index;
#elif defined(__GNUC__)
    #ifndef __nv
//        #define __nv __attribute__((section(".upper.rodata.persistent")))
        #define __nv  __attribute__((section(".nv_vars")))
    #endif
#endif
