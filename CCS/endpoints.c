#include "include/endpoints.h"

void endpoints_power_init() {
    /*
     * This function has to be run every time after successfully returning from endpoints_power
     */
    i_nv = 0;
    start = 0;
    end = (SAMPLES/FRAMESIZE);
    lower = 0;
    upper = 0;
}

int endpoints_power(uint16_t *buf, fingerprint *fp, int step) {
    /*
     * Detects the beginning and end of a spoken word in a sound file.
     *
     * @param buf: sound file (16-bit unsigned assumed here)
     * @param fp: start frame will be stored in fp.start and the end frame in fp.end
     * @param step: every x samples are taken into account. Use step=1 to sum all samples.
     * @var i_nv: non volatile index, needs to be initialized to zero before the first run of this function
     * @var j_nv: non volatile index, needs to be initialized to zero before the first run of this function
     */
    uint16_t j;
    uint32_t sum = 0;
    const uint32_t treshold = 1500/step;//1735;         // average in Patrick's apartment
    const uint32_t upper_treshold = 6900/step;


    for ( ; i_nv<(SAMPLES/FRAMESIZE); i_nv++) {

      sum = 0;
      for (j=0 ; j<FRAMESIZE; j+=step) {
        sum += squared((buf[FRAMESIZE*i_nv + j] - RECORDING_OFFSET)/16);           // energy = sum(magnitude^2)
      }

      if (!lower && (sum > treshold)) {

        if (i_nv == 0) { // If there is no silence before the word begins
            return 0;
        }
        start = i_nv;
        lower = 1;
      }

      if (sum > upper_treshold) {
        upper = 1;
      }

      if (lower && (sum < treshold)) {
        if (upper) {
          end = i_nv;
          break;
        }
        else lower = 0;
      }

    }

    if (end-start < 2) {  // If detected region is only 1 frame
        return 0;
    }

    if (end == ((SAMPLES/FRAMESIZE)) ) { // If there is no silence after the word has ended
        return 0;
    }

    fp->start = start;
    fp->end = end;

    return 1;
}

// =========================================================================================================

// =========================================================================================================

void endpoints_ZCR_init() {
    /*
     * This function has to be run every time after successfully returning from endpoints_ZCR
     */
    i_nv = 0;
    backwards = 0;
}

int endpoints_ZCR(uint16_t *buf, fingerprint *fp) {
    /*
     * Detects the beginning and end of a spoken word in a sound file.
     *
     * @param buf: sound file (16-bit unsigned assumed here)
     * @param fp: start frame will be stored in fp.start and the end frame in fp.end
     * @var i_nv: non volatile index, needs to be initialized to zero before the first run of this function
     * @var j_nv: non volatile index, needs to be initialized to zero before the first run of this function
     */
    uint16_t j;
    uint32_t sum = 0;
    uint16_t above = 0;

    if (!backwards) {
        for ( ; i_nv<( (SAMPLES/FRAMESIZE)-1); i_nv++) {

          sum = 0;
          above = 0;
          for (j=0 ; j<FRAMESIZE; j++) {

            if (above && (buf[FRAMESIZE*i_nv + j] < RECORDING_OFFSET) ) {
                sum ++;
                above = 0;
            }
            else if (!above && (buf[FRAMESIZE*i_nv + j] > RECORDING_OFFSET) ) {
                sum ++;
                above = 1;
            }
          }

          // decision process here
          if (sum < ZCR_THRESHOLD) {

              if (i_nv == 0) { // If there is no silence before the word begins
                  return 0;
              }
              start = i_nv;
              i_nv = (SAMPLES/FRAMESIZE)-1;  // start searching from the end
              break;
          }

          if (i_nv == (SAMPLES/FRAMESIZE) -2) { // If there is no word detected at all
              return 0;
          }
        }
    }

    backwards = 1;

    for ( ; i_nv > start; i_nv--) {

      sum = 0;
      above = 0;
      for (j=0 ; j<FRAMESIZE; j++) {
        if (above && (buf[FRAMESIZE*i_nv + j] < RECORDING_OFFSET) ) {
            sum ++;
            above = 0;
        }
        else if (!above && (buf[FRAMESIZE*i_nv + j] > RECORDING_OFFSET) ) {
            sum ++;
            above = 1;
        }
      }

      // decision process here
      if (sum < ZCR_THRESHOLD) {

          if (i_nv == ((SAMPLES/FRAMESIZE)-1) ) { // If there is no silence after the word has ended
              return 0;
          }
          end = i_nv + 1;
          break;
      }
    }

    if (end-start < 2) {  // If detected region is only 1 frame
        return 0;
    }

    fp->start = start;
    fp->end = end;

    return 1;
}
