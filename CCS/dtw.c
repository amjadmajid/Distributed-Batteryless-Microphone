
#include "dtw.h"

/*
 * The follwing functions do not work intermittently --> the function has to run in one go
 */


uint16_t dtw_full(int16_t x[NUM_FRAME*BANDS], const int16_t y[],
                uint16_t xsize, uint16_t ysize) {

    /*
    * Dynamic Time Warping
    * Steps from: https://en.wikipedia.org/wiki/Dynamic_time_warping
    *
    * returns distance between two "fingerprints"
    */

    uint16_t total;
    uint16_t i, j, k;
    int16_t tb_sq;
    uint16_t mindist;


    // xsize and ysize should not be larger than the array size (Dist & globdist))
    if (xsize > NUM_FRAME || ysize > NUM_FRAME)     return VERY_BIG;


    /*Compute distance matrix*/

    for(i=0;i<xsize;i++) {
      for(j=0;j<ysize;j++) {
        total = 0;
        for (k=0;k<BANDS;k++) {
//            total += squared(x[i*BANDS + k] - y[j*BANDS + k]);

            tb_sq = x[i*BANDS + k] - y[j*BANDS + k];
            *((volatile int *)&MPYS) = tb_sq;   // First operand
            *((volatile int *)&OP2) = tb_sq;   // Second operand

            total += RESLO;                   // result
        }

        Dist[i][j] = total;

      }
    }


    for (i=0; i <xsize; i++)
        globdist[i][0] = VERY_BIG;

    for (i=0; i <ysize; i++)
        globdist[0][i] = VERY_BIG;

    globdist[0][0] = Dist[0][0];


    for (i=1; i<xsize; i++) {
      for (j=1; j<ysize; j++) {

        if ( (globdist[i-1][j] < globdist[i][j-1]) && (globdist[i-1][j] < globdist[i-1][j-1]) )
          mindist = globdist[i-1][j];
        else if (globdist[i][j-1] < globdist[i-1][j-1])
          mindist = globdist[i][j-1];
        else
          mindist = globdist[i-1][j-1];

        globdist[i][j] = Dist[i][j] + mindist;
      }
    }



    return globdist[xsize-1][ysize-1];
}


uint16_t dtw_window(int16_t x[NUM_FRAME*BANDS], const int16_t y[],
                uint16_t xsize, uint16_t ysize) {

    /*
    * Dynamic Time Warping
    * Steps from: https://en.wikipedia.org/wiki/Dynamic_time_warping
    *
    * returns distance between two "fingerprints"
    */

    uint16_t total;
    uint16_t i, j, k;
    int16_t tb_sq;
    uint16_t mindist;
    int16_t window;


    // xsize and ysize should not be larger than the array size (Dist & globdist))
    if (xsize > NUM_FRAME || ysize > NUM_FRAME)     return VERY_BIG;


    /*Compute distance matrix*/

    for(i=0;i<xsize;i++) {
      for(j=0;j<ysize;j++) {
        total = 0;
        for (k=0;k<BANDS;k++) {
//            total += squared(x[i*BANDS + k] - y[j*BANDS + k]);

            tb_sq = x[i*BANDS + k] - y[j*BANDS + k];
            *((volatile int *)&MPYS) = tb_sq;   // First operand
            *((volatile int *)&OP2) = tb_sq;   // Second operand

            total += RESLO;                   // result
        }

        Dist[i][j] = total;

      }
    }


    // w := max(w, abs(n-m))
    window = xsize > ysize ? max(2, xsize-ysize) : max(2, ysize-xsize);


    for(i=0;i<xsize;i++) {
        for(j=0;j<ysize;j++) {
            globdist[i][j] = VERY_BIG;
        }
    }

    globdist[0][0] = Dist[0][0];


    for (i=1; i<xsize; i++) {
//      for (j=1; j<ysize; j++) {
        for (j=max(1, i-window); j < min(ysize, i+window); j++)  {

        if ( (globdist[i-1][j] < globdist[i][j-1]) && (globdist[i-1][j] < globdist[i-1][j-1]) )
          mindist = globdist[i-1][j];
        else if (globdist[i][j-1] < globdist[i-1][j-1])
          mindist = globdist[i][j-1];
        else
          mindist = globdist[i-1][j-1];

        globdist[i][j] = Dist[i][j] + mindist;
      }
    }


    return globdist[xsize-1][ysize-1];
}





uint16_t linear_compare(int16_t x[NUM_FRAME*BANDS], const int16_t y[],
                uint16_t xsize, uint16_t ysize) {

    /*
    * returns distance between two "fingerprints"
    */

    uint16_t total;
    uint16_t i, k;
    int16_t tb_sq;

//    uint16_t Dist[xsize][ysize];          // declared in dtw.h and placed in FRAM


    // xsize and ysize should not be larger than the array size (Dist) )
    if (xsize > NUM_FRAME || ysize > NUM_FRAME)     return VERY_BIG;


    /*Compute distance*/

    total = 0;

    for(i=0;i< min(xsize,ysize);i++) {
        
        for (k=0;k<BANDS;k++) {
//            total += squared(x[i*BANDS + k] - y[j*BANDS + k]);

            tb_sq = x[i*BANDS + k] - y[i*BANDS + k];
            *((volatile int *)&MPYS) = tb_sq;   // First operand
            *((volatile int *)&OP2) = tb_sq;   // Second operand

            total += RESLO;                   // result
        }
      
    }


    // Penalty for difference in size

    if (xsize > ysize)   total += (xsize-ysize)*50;
    else                 total += (ysize-xsize)*50;

    return total;

}
