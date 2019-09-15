/**
  MSSP1 Generated Driver File

  @Company
    Microchip Technology Inc.

  @File Name
    i2c1.c

  @Summary
    This is the generated header file for the MSSP1 driver using 
    PIC10 / PIC12 / PIC16 / PIC18 MCUs

  @Description
    This header file provides APIs for driver for I2C1.
    Generation Information :
        Product Revision  :  PIC10 / PIC12 / PIC16 / PIC18 MCUs - 1.77
        Device            :  PIC16F18877
        Driver Version    :  2.01
    The generated drivers are tested against the following:
        Compiler          :  XC8 2.05 and above
        MPLAB 	          :  MPLAB X 5.20	
*/

/*
    (c) 2018 Microchip Technology Inc. and its subsidiaries. 
    
    Subject to your compliance with these terms, you may use Microchip software and any 
    derivatives exclusively with Microchip products. It is your responsibility to comply with third party 
    license terms applicable to your use of third party software (including open source software) that 
    may accompany Microchip software.
    
    THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER 
    EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY 
    IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS 
    FOR A PARTICULAR PURPOSE.
    
    IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE, 
    INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND 
    WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP 
    HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO 
    THE FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL 
    CLAIMS IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT 
    OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS 
    SOFTWARE.
*/

#include "i2c1.h"
#include "../comms.h"

#define I2C1_SLAVE_ADDRESS 0x33 
#define I2C1_SLAVE_MASK    0x7F


/**
 Section: Global Variables
*/

volatile uint8_t    I2C1_slaveWriteData      = 0x55;



/**
  Prototype:        void I2C1_Initialize(void)
  Input:            none
  Output:           none
  Description:      I2C1_Initialize is an
                    initialization routine that takes inputs from the GUI.
  Comment:          
  Usage:            I2C1_Initialize();

*/
void I2C1_Initialize(void)
{
    // initialize the hardware
    // SMP Standard Speed; CKE enabled; 
    SSP1STAT = 0xC0;
    // SSPEN enabled; CKP disabled; SSPM 7 Bit Polling; 
    SSP1CON1 = 0x26;
    // ACKEN disabled; GCEN disabled; PEN disabled; ACKDT acknowledge; RSEN disabled; RCEN disabled; SEN disabled; 
    SSP1CON2 = 0x00;
    // SBCDE disabled; BOEN disabled; SCIE disabled; PCIE enabled; DHEN disabled; SDAHT 300ns; AHEN disabled; 
    SSP1CON3 = 0x48;
    // SSPMSK 127; 
    SSP1MSK = (I2C1_SLAVE_MASK << 1);  // adjust UI mask for R/nW bit            
    // SSPADD 51; 
    SSP1ADD = (I2C1_SLAVE_ADDRESS << 1);  // adjust UI address for R/nW bit
	
    // clear the slave interrupt flag
    PIR3bits.SSP1IF = 0;
    // enable the master interrupt
    PIE3bits.SSP1IE = 1;

}

void I2C1_ISR ( void )
{
    uint8_t     i2c_data                = 0x55;


    // NOTE: The slave driver will always acknowledge
    //       any address match.

    PIR3bits.SSP1IF = 0;        // clear the slave interrupt flag
    i2c_data        = SSP1BUF;  // read SSPBUF to clear BF
    if(1 == SSP1STATbits.P)
    {
        // this is a stop condition
        I2C1_StatusCallback(I2C1_SLAVE_STOP);
        return;
    }
    else if(1 == SSP1STATbits.R_nW)
    {
        if((1 == SSP1STATbits.D_nA) && (1 == SSP1CON2bits.ACKSTAT))
        {
            // callback routine can perform any post-read processing
            I2C1_StatusCallback(I2C1_SLAVE_READ_COMPLETED);
        }
        else
        {
            // callback routine should write data into SSPBUF
            I2C1_StatusCallback(I2C1_SLAVE_READ_REQUEST);
        }
    }
    else if(0 == SSP1STATbits.D_nA)
    {
        // this is an I2C address

        // callback routine should prepare to receive data from the master
        I2C1_StatusCallback(I2C1_SLAVE_WRITE_REQUEST);
    }
    else
    {
        I2C1_slaveWriteData   = i2c_data;

        // callback routine should process I2C1_slaveWriteData from the master
        I2C1_StatusCallback(I2C1_SLAVE_WRITE_COMPLETED);
    }

    SSP1CON1bits.CKP    = 1;    // release SCL

} // end I2C1_ISR()
