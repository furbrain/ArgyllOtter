/**
  PWM4 Generated Driver File

  @Company
    Microchip Technology Inc.

  @File Name
    pwm4.c

  @Summary
    This is the generated driver implementation file for the PWM4 driver using PIC10 / PIC12 / PIC16 / PIC18 MCUs

  @Description
    This source file provides implementations for driver APIs for PWM4.
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

/**
  Section: Included Files
*/

#include <xc.h>
#include "pwm4.h"

/**
  Section: Macro Declarations
*/

#define PWM4_INITIALIZE_DUTY_VALUE    0

/**
  Section: PWM Module APIs
*/

void PWM4_Initialize(void)
{
    // Set the PWM4 to the options selected in the User Interface
	
	// MODE PWM; EN enabled; CCP4FMT right_aligned; 
	CCP4CON = 0x8F;    
	
	// RH 0; 
	CCPR4H = 0x00;    
	
	// RL 0; 
	CCPR4L = 0x00;    

	// Selecting Timer 2
	CCPTMRS0bits.C4TSEL = 0x1;
    
}

void PWM4_LoadDutyValue(uint16_t dutyValue)
{
    dutyValue &= 0x03FF;
    
    // Load duty cycle value
    if(CCP4CONbits.CCP4FMT)
    {
        dutyValue <<= 6;
        CCPR4H = dutyValue >> 8;
        CCPR4L = dutyValue;
    }
    else
    {
        CCPR4H = dutyValue >> 8;
        CCPR4L = dutyValue;
    }
}

bool PWM4_OutputStatusGet(void)
{
    // Returns the output status
    return(CCP4CONbits.OUT);
}
/**
 End of File
*/

