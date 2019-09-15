/**
  @Generated Pin Manager Header File

  @Company:
    Microchip Technology Inc.

  @File Name:
    pin_manager.h

  @Summary:
    This is the Pin Manager file generated using PIC10 / PIC12 / PIC16 / PIC18 MCUs

  @Description
    This header file provides APIs for driver for .
    Generation Information :
        Product Revision  :  PIC10 / PIC12 / PIC16 / PIC18 MCUs - 1.77
        Device            :  PIC16F18877
        Driver Version    :  2.11
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

#ifndef PIN_MANAGER_H
#define PIN_MANAGER_H

/**
  Section: Included Files
*/

#include <xc.h>

#define INPUT   1
#define OUTPUT  0

#define HIGH    1
#define LOW     0

#define ANALOG      1
#define DIGITAL     0

#define PULL_UP_ENABLED      1
#define PULL_UP_DISABLED     0

// get/set FR_SENSE2 aliases
#define FR_SENSE2_TRIS                 TRISAbits.TRISA1
#define FR_SENSE2_LAT                  LATAbits.LATA1
#define FR_SENSE2_PORT                 PORTAbits.RA1
#define FR_SENSE2_WPU                  WPUAbits.WPUA1
#define FR_SENSE2_OD                   ODCONAbits.ODCA1
#define FR_SENSE2_ANS                  ANSELAbits.ANSA1
#define FR_SENSE2_SetHigh()            do { LATAbits.LATA1 = 1; } while(0)
#define FR_SENSE2_SetLow()             do { LATAbits.LATA1 = 0; } while(0)
#define FR_SENSE2_Toggle()             do { LATAbits.LATA1 = ~LATAbits.LATA1; } while(0)
#define FR_SENSE2_GetValue()           PORTAbits.RA1
#define FR_SENSE2_SetDigitalInput()    do { TRISAbits.TRISA1 = 1; } while(0)
#define FR_SENSE2_SetDigitalOutput()   do { TRISAbits.TRISA1 = 0; } while(0)
#define FR_SENSE2_SetPullup()          do { WPUAbits.WPUA1 = 1; } while(0)
#define FR_SENSE2_ResetPullup()        do { WPUAbits.WPUA1 = 0; } while(0)
#define FR_SENSE2_SetPushPull()        do { ODCONAbits.ODCA1 = 0; } while(0)
#define FR_SENSE2_SetOpenDrain()       do { ODCONAbits.ODCA1 = 1; } while(0)
#define FR_SENSE2_SetAnalogMode()      do { ANSELAbits.ANSA1 = 1; } while(0)
#define FR_SENSE2_SetDigitalMode()     do { ANSELAbits.ANSA1 = 0; } while(0)

// get/set FR_SENSE1 aliases
#define FR_SENSE1_TRIS                 TRISAbits.TRISA2
#define FR_SENSE1_LAT                  LATAbits.LATA2
#define FR_SENSE1_PORT                 PORTAbits.RA2
#define FR_SENSE1_WPU                  WPUAbits.WPUA2
#define FR_SENSE1_OD                   ODCONAbits.ODCA2
#define FR_SENSE1_ANS                  ANSELAbits.ANSA2
#define FR_SENSE1_SetHigh()            do { LATAbits.LATA2 = 1; } while(0)
#define FR_SENSE1_SetLow()             do { LATAbits.LATA2 = 0; } while(0)
#define FR_SENSE1_Toggle()             do { LATAbits.LATA2 = ~LATAbits.LATA2; } while(0)
#define FR_SENSE1_GetValue()           PORTAbits.RA2
#define FR_SENSE1_SetDigitalInput()    do { TRISAbits.TRISA2 = 1; } while(0)
#define FR_SENSE1_SetDigitalOutput()   do { TRISAbits.TRISA2 = 0; } while(0)
#define FR_SENSE1_SetPullup()          do { WPUAbits.WPUA2 = 1; } while(0)
#define FR_SENSE1_ResetPullup()        do { WPUAbits.WPUA2 = 0; } while(0)
#define FR_SENSE1_SetPushPull()        do { ODCONAbits.ODCA2 = 0; } while(0)
#define FR_SENSE1_SetOpenDrain()       do { ODCONAbits.ODCA2 = 1; } while(0)
#define FR_SENSE1_SetAnalogMode()      do { ANSELAbits.ANSA2 = 1; } while(0)
#define FR_SENSE1_SetDigitalMode()     do { ANSELAbits.ANSA2 = 0; } while(0)

// get/set FL_SENSE1 aliases
#define FL_SENSE1_TRIS                 TRISAbits.TRISA3
#define FL_SENSE1_LAT                  LATAbits.LATA3
#define FL_SENSE1_PORT                 PORTAbits.RA3
#define FL_SENSE1_WPU                  WPUAbits.WPUA3
#define FL_SENSE1_OD                   ODCONAbits.ODCA3
#define FL_SENSE1_ANS                  ANSELAbits.ANSA3
#define FL_SENSE1_SetHigh()            do { LATAbits.LATA3 = 1; } while(0)
#define FL_SENSE1_SetLow()             do { LATAbits.LATA3 = 0; } while(0)
#define FL_SENSE1_Toggle()             do { LATAbits.LATA3 = ~LATAbits.LATA3; } while(0)
#define FL_SENSE1_GetValue()           PORTAbits.RA3
#define FL_SENSE1_SetDigitalInput()    do { TRISAbits.TRISA3 = 1; } while(0)
#define FL_SENSE1_SetDigitalOutput()   do { TRISAbits.TRISA3 = 0; } while(0)
#define FL_SENSE1_SetPullup()          do { WPUAbits.WPUA3 = 1; } while(0)
#define FL_SENSE1_ResetPullup()        do { WPUAbits.WPUA3 = 0; } while(0)
#define FL_SENSE1_SetPushPull()        do { ODCONAbits.ODCA3 = 0; } while(0)
#define FL_SENSE1_SetOpenDrain()       do { ODCONAbits.ODCA3 = 1; } while(0)
#define FL_SENSE1_SetAnalogMode()      do { ANSELAbits.ANSA3 = 1; } while(0)
#define FL_SENSE1_SetDigitalMode()     do { ANSELAbits.ANSA3 = 0; } while(0)

// get/set FL_SENSE2 aliases
#define FL_SENSE2_TRIS                 TRISAbits.TRISA4
#define FL_SENSE2_LAT                  LATAbits.LATA4
#define FL_SENSE2_PORT                 PORTAbits.RA4
#define FL_SENSE2_WPU                  WPUAbits.WPUA4
#define FL_SENSE2_OD                   ODCONAbits.ODCA4
#define FL_SENSE2_ANS                  ANSELAbits.ANSA4
#define FL_SENSE2_SetHigh()            do { LATAbits.LATA4 = 1; } while(0)
#define FL_SENSE2_SetLow()             do { LATAbits.LATA4 = 0; } while(0)
#define FL_SENSE2_Toggle()             do { LATAbits.LATA4 = ~LATAbits.LATA4; } while(0)
#define FL_SENSE2_GetValue()           PORTAbits.RA4
#define FL_SENSE2_SetDigitalInput()    do { TRISAbits.TRISA4 = 1; } while(0)
#define FL_SENSE2_SetDigitalOutput()   do { TRISAbits.TRISA4 = 0; } while(0)
#define FL_SENSE2_SetPullup()          do { WPUAbits.WPUA4 = 1; } while(0)
#define FL_SENSE2_ResetPullup()        do { WPUAbits.WPUA4 = 0; } while(0)
#define FL_SENSE2_SetPushPull()        do { ODCONAbits.ODCA4 = 0; } while(0)
#define FL_SENSE2_SetOpenDrain()       do { ODCONAbits.ODCA4 = 1; } while(0)
#define FL_SENSE2_SetAnalogMode()      do { ANSELAbits.ANSA4 = 1; } while(0)
#define FL_SENSE2_SetDigitalMode()     do { ANSELAbits.ANSA4 = 0; } while(0)

// get/set FRONT_GROUND aliases
#define FRONT_GROUND_TRIS                 TRISAbits.TRISA6
#define FRONT_GROUND_LAT                  LATAbits.LATA6
#define FRONT_GROUND_PORT                 PORTAbits.RA6
#define FRONT_GROUND_WPU                  WPUAbits.WPUA6
#define FRONT_GROUND_OD                   ODCONAbits.ODCA6
#define FRONT_GROUND_ANS                  ANSELAbits.ANSA6
#define FRONT_GROUND_SetHigh()            do { LATAbits.LATA6 = 1; } while(0)
#define FRONT_GROUND_SetLow()             do { LATAbits.LATA6 = 0; } while(0)
#define FRONT_GROUND_Toggle()             do { LATAbits.LATA6 = ~LATAbits.LATA6; } while(0)
#define FRONT_GROUND_GetValue()           PORTAbits.RA6
#define FRONT_GROUND_SetDigitalInput()    do { TRISAbits.TRISA6 = 1; } while(0)
#define FRONT_GROUND_SetDigitalOutput()   do { TRISAbits.TRISA6 = 0; } while(0)
#define FRONT_GROUND_SetPullup()          do { WPUAbits.WPUA6 = 1; } while(0)
#define FRONT_GROUND_ResetPullup()        do { WPUAbits.WPUA6 = 0; } while(0)
#define FRONT_GROUND_SetPushPull()        do { ODCONAbits.ODCA6 = 0; } while(0)
#define FRONT_GROUND_SetOpenDrain()       do { ODCONAbits.ODCA6 = 1; } while(0)
#define FRONT_GROUND_SetAnalogMode()      do { ANSELAbits.ANSA6 = 1; } while(0)
#define FRONT_GROUND_SetDigitalMode()     do { ANSELAbits.ANSA6 = 0; } while(0)

// get/set FR_DIRECTION aliases
#define FR_DIRECTION_TRIS                 TRISAbits.TRISA7
#define FR_DIRECTION_LAT                  LATAbits.LATA7
#define FR_DIRECTION_PORT                 PORTAbits.RA7
#define FR_DIRECTION_WPU                  WPUAbits.WPUA7
#define FR_DIRECTION_OD                   ODCONAbits.ODCA7
#define FR_DIRECTION_ANS                  ANSELAbits.ANSA7
#define FR_DIRECTION_SetHigh()            do { LATAbits.LATA7 = 1; } while(0)
#define FR_DIRECTION_SetLow()             do { LATAbits.LATA7 = 0; } while(0)
#define FR_DIRECTION_Toggle()             do { LATAbits.LATA7 = ~LATAbits.LATA7; } while(0)
#define FR_DIRECTION_GetValue()           PORTAbits.RA7
#define FR_DIRECTION_SetDigitalInput()    do { TRISAbits.TRISA7 = 1; } while(0)
#define FR_DIRECTION_SetDigitalOutput()   do { TRISAbits.TRISA7 = 0; } while(0)
#define FR_DIRECTION_SetPullup()          do { WPUAbits.WPUA7 = 1; } while(0)
#define FR_DIRECTION_ResetPullup()        do { WPUAbits.WPUA7 = 0; } while(0)
#define FR_DIRECTION_SetPushPull()        do { ODCONAbits.ODCA7 = 0; } while(0)
#define FR_DIRECTION_SetOpenDrain()       do { ODCONAbits.ODCA7 = 1; } while(0)
#define FR_DIRECTION_SetAnalogMode()      do { ANSELAbits.ANSA7 = 1; } while(0)
#define FR_DIRECTION_SetDigitalMode()     do { ANSELAbits.ANSA7 = 0; } while(0)

// get/set RR_DIRECTION aliases
#define RR_DIRECTION_TRIS                 TRISBbits.TRISB0
#define RR_DIRECTION_LAT                  LATBbits.LATB0
#define RR_DIRECTION_PORT                 PORTBbits.RB0
#define RR_DIRECTION_WPU                  WPUBbits.WPUB0
#define RR_DIRECTION_OD                   ODCONBbits.ODCB0
#define RR_DIRECTION_ANS                  ANSELBbits.ANSB0
#define RR_DIRECTION_SetHigh()            do { LATBbits.LATB0 = 1; } while(0)
#define RR_DIRECTION_SetLow()             do { LATBbits.LATB0 = 0; } while(0)
#define RR_DIRECTION_Toggle()             do { LATBbits.LATB0 = ~LATBbits.LATB0; } while(0)
#define RR_DIRECTION_GetValue()           PORTBbits.RB0
#define RR_DIRECTION_SetDigitalInput()    do { TRISBbits.TRISB0 = 1; } while(0)
#define RR_DIRECTION_SetDigitalOutput()   do { TRISBbits.TRISB0 = 0; } while(0)
#define RR_DIRECTION_SetPullup()          do { WPUBbits.WPUB0 = 1; } while(0)
#define RR_DIRECTION_ResetPullup()        do { WPUBbits.WPUB0 = 0; } while(0)
#define RR_DIRECTION_SetPushPull()        do { ODCONBbits.ODCB0 = 0; } while(0)
#define RR_DIRECTION_SetOpenDrain()       do { ODCONBbits.ODCB0 = 1; } while(0)
#define RR_DIRECTION_SetAnalogMode()      do { ANSELBbits.ANSB0 = 1; } while(0)
#define RR_DIRECTION_SetDigitalMode()     do { ANSELBbits.ANSB0 = 0; } while(0)

// get/set RB1 procedures
#define RB1_SetHigh()            do { LATBbits.LATB1 = 1; } while(0)
#define RB1_SetLow()             do { LATBbits.LATB1 = 0; } while(0)
#define RB1_Toggle()             do { LATBbits.LATB1 = ~LATBbits.LATB1; } while(0)
#define RB1_GetValue()              PORTBbits.RB1
#define RB1_SetDigitalInput()    do { TRISBbits.TRISB1 = 1; } while(0)
#define RB1_SetDigitalOutput()   do { TRISBbits.TRISB1 = 0; } while(0)
#define RB1_SetPullup()             do { WPUBbits.WPUB1 = 1; } while(0)
#define RB1_ResetPullup()           do { WPUBbits.WPUB1 = 0; } while(0)
#define RB1_SetAnalogMode()         do { ANSELBbits.ANSB1 = 1; } while(0)
#define RB1_SetDigitalMode()        do { ANSELBbits.ANSB1 = 0; } while(0)

// get/set RR_CURRENT aliases
#define RR_CURRENT_TRIS                 TRISBbits.TRISB2
#define RR_CURRENT_LAT                  LATBbits.LATB2
#define RR_CURRENT_PORT                 PORTBbits.RB2
#define RR_CURRENT_WPU                  WPUBbits.WPUB2
#define RR_CURRENT_OD                   ODCONBbits.ODCB2
#define RR_CURRENT_ANS                  ANSELBbits.ANSB2
#define RR_CURRENT_SetHigh()            do { LATBbits.LATB2 = 1; } while(0)
#define RR_CURRENT_SetLow()             do { LATBbits.LATB2 = 0; } while(0)
#define RR_CURRENT_Toggle()             do { LATBbits.LATB2 = ~LATBbits.LATB2; } while(0)
#define RR_CURRENT_GetValue()           PORTBbits.RB2
#define RR_CURRENT_SetDigitalInput()    do { TRISBbits.TRISB2 = 1; } while(0)
#define RR_CURRENT_SetDigitalOutput()   do { TRISBbits.TRISB2 = 0; } while(0)
#define RR_CURRENT_SetPullup()          do { WPUBbits.WPUB2 = 1; } while(0)
#define RR_CURRENT_ResetPullup()        do { WPUBbits.WPUB2 = 0; } while(0)
#define RR_CURRENT_SetPushPull()        do { ODCONBbits.ODCB2 = 0; } while(0)
#define RR_CURRENT_SetOpenDrain()       do { ODCONBbits.ODCB2 = 1; } while(0)
#define RR_CURRENT_SetAnalogMode()      do { ANSELBbits.ANSB2 = 1; } while(0)
#define RR_CURRENT_SetDigitalMode()     do { ANSELBbits.ANSB2 = 0; } while(0)

// get/set RR_ERROR aliases
#define RR_ERROR_TRIS                 TRISBbits.TRISB3
#define RR_ERROR_LAT                  LATBbits.LATB3
#define RR_ERROR_PORT                 PORTBbits.RB3
#define RR_ERROR_WPU                  WPUBbits.WPUB3
#define RR_ERROR_OD                   ODCONBbits.ODCB3
#define RR_ERROR_ANS                  ANSELBbits.ANSB3
#define RR_ERROR_SetHigh()            do { LATBbits.LATB3 = 1; } while(0)
#define RR_ERROR_SetLow()             do { LATBbits.LATB3 = 0; } while(0)
#define RR_ERROR_Toggle()             do { LATBbits.LATB3 = ~LATBbits.LATB3; } while(0)
#define RR_ERROR_GetValue()           PORTBbits.RB3
#define RR_ERROR_SetDigitalInput()    do { TRISBbits.TRISB3 = 1; } while(0)
#define RR_ERROR_SetDigitalOutput()   do { TRISBbits.TRISB3 = 0; } while(0)
#define RR_ERROR_SetPullup()          do { WPUBbits.WPUB3 = 1; } while(0)
#define RR_ERROR_ResetPullup()        do { WPUBbits.WPUB3 = 0; } while(0)
#define RR_ERROR_SetPushPull()        do { ODCONBbits.ODCB3 = 0; } while(0)
#define RR_ERROR_SetOpenDrain()       do { ODCONBbits.ODCB3 = 1; } while(0)
#define RR_ERROR_SetAnalogMode()      do { ANSELBbits.ANSB3 = 1; } while(0)
#define RR_ERROR_SetDigitalMode()     do { ANSELBbits.ANSB3 = 0; } while(0)

// get/set RR_SENSE2 aliases
#define RR_SENSE2_TRIS                 TRISBbits.TRISB4
#define RR_SENSE2_LAT                  LATBbits.LATB4
#define RR_SENSE2_PORT                 PORTBbits.RB4
#define RR_SENSE2_WPU                  WPUBbits.WPUB4
#define RR_SENSE2_OD                   ODCONBbits.ODCB4
#define RR_SENSE2_ANS                  ANSELBbits.ANSB4
#define RR_SENSE2_SetHigh()            do { LATBbits.LATB4 = 1; } while(0)
#define RR_SENSE2_SetLow()             do { LATBbits.LATB4 = 0; } while(0)
#define RR_SENSE2_Toggle()             do { LATBbits.LATB4 = ~LATBbits.LATB4; } while(0)
#define RR_SENSE2_GetValue()           PORTBbits.RB4
#define RR_SENSE2_SetDigitalInput()    do { TRISBbits.TRISB4 = 1; } while(0)
#define RR_SENSE2_SetDigitalOutput()   do { TRISBbits.TRISB4 = 0; } while(0)
#define RR_SENSE2_SetPullup()          do { WPUBbits.WPUB4 = 1; } while(0)
#define RR_SENSE2_ResetPullup()        do { WPUBbits.WPUB4 = 0; } while(0)
#define RR_SENSE2_SetPushPull()        do { ODCONBbits.ODCB4 = 0; } while(0)
#define RR_SENSE2_SetOpenDrain()       do { ODCONBbits.ODCB4 = 1; } while(0)
#define RR_SENSE2_SetAnalogMode()      do { ANSELBbits.ANSB4 = 1; } while(0)
#define RR_SENSE2_SetDigitalMode()     do { ANSELBbits.ANSB4 = 0; } while(0)

// get/set RR_SENSE1 aliases
#define RR_SENSE1_TRIS                 TRISBbits.TRISB5
#define RR_SENSE1_LAT                  LATBbits.LATB5
#define RR_SENSE1_PORT                 PORTBbits.RB5
#define RR_SENSE1_WPU                  WPUBbits.WPUB5
#define RR_SENSE1_OD                   ODCONBbits.ODCB5
#define RR_SENSE1_ANS                  ANSELBbits.ANSB5
#define RR_SENSE1_SetHigh()            do { LATBbits.LATB5 = 1; } while(0)
#define RR_SENSE1_SetLow()             do { LATBbits.LATB5 = 0; } while(0)
#define RR_SENSE1_Toggle()             do { LATBbits.LATB5 = ~LATBbits.LATB5; } while(0)
#define RR_SENSE1_GetValue()           PORTBbits.RB5
#define RR_SENSE1_SetDigitalInput()    do { TRISBbits.TRISB5 = 1; } while(0)
#define RR_SENSE1_SetDigitalOutput()   do { TRISBbits.TRISB5 = 0; } while(0)
#define RR_SENSE1_SetPullup()          do { WPUBbits.WPUB5 = 1; } while(0)
#define RR_SENSE1_ResetPullup()        do { WPUBbits.WPUB5 = 0; } while(0)
#define RR_SENSE1_SetPushPull()        do { ODCONBbits.ODCB5 = 0; } while(0)
#define RR_SENSE1_SetOpenDrain()       do { ODCONBbits.ODCB5 = 1; } while(0)
#define RR_SENSE1_SetAnalogMode()      do { ANSELBbits.ANSB5 = 1; } while(0)
#define RR_SENSE1_SetDigitalMode()     do { ANSELBbits.ANSB5 = 0; } while(0)

// get/set RB6 procedures
#define RB6_SetHigh()            do { LATBbits.LATB6 = 1; } while(0)
#define RB6_SetLow()             do { LATBbits.LATB6 = 0; } while(0)
#define RB6_Toggle()             do { LATBbits.LATB6 = ~LATBbits.LATB6; } while(0)
#define RB6_GetValue()              PORTBbits.RB6
#define RB6_SetDigitalInput()    do { TRISBbits.TRISB6 = 1; } while(0)
#define RB6_SetDigitalOutput()   do { TRISBbits.TRISB6 = 0; } while(0)
#define RB6_SetPullup()             do { WPUBbits.WPUB6 = 1; } while(0)
#define RB6_ResetPullup()           do { WPUBbits.WPUB6 = 0; } while(0)
#define RB6_SetAnalogMode()         do { ANSELBbits.ANSB6 = 1; } while(0)
#define RB6_SetDigitalMode()        do { ANSELBbits.ANSB6 = 0; } while(0)

// get/set RB7 procedures
#define RB7_SetHigh()            do { LATBbits.LATB7 = 1; } while(0)
#define RB7_SetLow()             do { LATBbits.LATB7 = 0; } while(0)
#define RB7_Toggle()             do { LATBbits.LATB7 = ~LATBbits.LATB7; } while(0)
#define RB7_GetValue()              PORTBbits.RB7
#define RB7_SetDigitalInput()    do { TRISBbits.TRISB7 = 1; } while(0)
#define RB7_SetDigitalOutput()   do { TRISBbits.TRISB7 = 0; } while(0)
#define RB7_SetPullup()             do { WPUBbits.WPUB7 = 1; } while(0)
#define RB7_ResetPullup()           do { WPUBbits.WPUB7 = 0; } while(0)
#define RB7_SetAnalogMode()         do { ANSELBbits.ANSB7 = 1; } while(0)
#define RB7_SetDigitalMode()        do { ANSELBbits.ANSB7 = 0; } while(0)

// get/set RC0 procedures
#define RC0_SetHigh()            do { LATCbits.LATC0 = 1; } while(0)
#define RC0_SetLow()             do { LATCbits.LATC0 = 0; } while(0)
#define RC0_Toggle()             do { LATCbits.LATC0 = ~LATCbits.LATC0; } while(0)
#define RC0_GetValue()              PORTCbits.RC0
#define RC0_SetDigitalInput()    do { TRISCbits.TRISC0 = 1; } while(0)
#define RC0_SetDigitalOutput()   do { TRISCbits.TRISC0 = 0; } while(0)
#define RC0_SetPullup()             do { WPUCbits.WPUC0 = 1; } while(0)
#define RC0_ResetPullup()           do { WPUCbits.WPUC0 = 0; } while(0)
#define RC0_SetAnalogMode()         do { ANSELCbits.ANSC0 = 1; } while(0)
#define RC0_SetDigitalMode()        do { ANSELCbits.ANSC0 = 0; } while(0)

// get/set FL_DIRECTION aliases
#define FL_DIRECTION_TRIS                 TRISCbits.TRISC1
#define FL_DIRECTION_LAT                  LATCbits.LATC1
#define FL_DIRECTION_PORT                 PORTCbits.RC1
#define FL_DIRECTION_WPU                  WPUCbits.WPUC1
#define FL_DIRECTION_OD                   ODCONCbits.ODCC1
#define FL_DIRECTION_ANS                  ANSELCbits.ANSC1
#define FL_DIRECTION_SetHigh()            do { LATCbits.LATC1 = 1; } while(0)
#define FL_DIRECTION_SetLow()             do { LATCbits.LATC1 = 0; } while(0)
#define FL_DIRECTION_Toggle()             do { LATCbits.LATC1 = ~LATCbits.LATC1; } while(0)
#define FL_DIRECTION_GetValue()           PORTCbits.RC1
#define FL_DIRECTION_SetDigitalInput()    do { TRISCbits.TRISC1 = 1; } while(0)
#define FL_DIRECTION_SetDigitalOutput()   do { TRISCbits.TRISC1 = 0; } while(0)
#define FL_DIRECTION_SetPullup()          do { WPUCbits.WPUC1 = 1; } while(0)
#define FL_DIRECTION_ResetPullup()        do { WPUCbits.WPUC1 = 0; } while(0)
#define FL_DIRECTION_SetPushPull()        do { ODCONCbits.ODCC1 = 0; } while(0)
#define FL_DIRECTION_SetOpenDrain()       do { ODCONCbits.ODCC1 = 1; } while(0)
#define FL_DIRECTION_SetAnalogMode()      do { ANSELCbits.ANSC1 = 1; } while(0)
#define FL_DIRECTION_SetDigitalMode()     do { ANSELCbits.ANSC1 = 0; } while(0)

// get/set FL_CURRENT aliases
#define FL_CURRENT_TRIS                 TRISCbits.TRISC2
#define FL_CURRENT_LAT                  LATCbits.LATC2
#define FL_CURRENT_PORT                 PORTCbits.RC2
#define FL_CURRENT_WPU                  WPUCbits.WPUC2
#define FL_CURRENT_OD                   ODCONCbits.ODCC2
#define FL_CURRENT_ANS                  ANSELCbits.ANSC2
#define FL_CURRENT_SetHigh()            do { LATCbits.LATC2 = 1; } while(0)
#define FL_CURRENT_SetLow()             do { LATCbits.LATC2 = 0; } while(0)
#define FL_CURRENT_Toggle()             do { LATCbits.LATC2 = ~LATCbits.LATC2; } while(0)
#define FL_CURRENT_GetValue()           PORTCbits.RC2
#define FL_CURRENT_SetDigitalInput()    do { TRISCbits.TRISC2 = 1; } while(0)
#define FL_CURRENT_SetDigitalOutput()   do { TRISCbits.TRISC2 = 0; } while(0)
#define FL_CURRENT_SetPullup()          do { WPUCbits.WPUC2 = 1; } while(0)
#define FL_CURRENT_ResetPullup()        do { WPUCbits.WPUC2 = 0; } while(0)
#define FL_CURRENT_SetPushPull()        do { ODCONCbits.ODCC2 = 0; } while(0)
#define FL_CURRENT_SetOpenDrain()       do { ODCONCbits.ODCC2 = 1; } while(0)
#define FL_CURRENT_SetAnalogMode()      do { ANSELCbits.ANSC2 = 1; } while(0)
#define FL_CURRENT_SetDigitalMode()     do { ANSELCbits.ANSC2 = 0; } while(0)

// get/set SCL1 aliases
#define SCL1_TRIS                 TRISCbits.TRISC3
#define SCL1_LAT                  LATCbits.LATC3
#define SCL1_PORT                 PORTCbits.RC3
#define SCL1_WPU                  WPUCbits.WPUC3
#define SCL1_OD                   ODCONCbits.ODCC3
#define SCL1_ANS                  ANSELCbits.ANSC3
#define SCL1_SetHigh()            do { LATCbits.LATC3 = 1; } while(0)
#define SCL1_SetLow()             do { LATCbits.LATC3 = 0; } while(0)
#define SCL1_Toggle()             do { LATCbits.LATC3 = ~LATCbits.LATC3; } while(0)
#define SCL1_GetValue()           PORTCbits.RC3
#define SCL1_SetDigitalInput()    do { TRISCbits.TRISC3 = 1; } while(0)
#define SCL1_SetDigitalOutput()   do { TRISCbits.TRISC3 = 0; } while(0)
#define SCL1_SetPullup()          do { WPUCbits.WPUC3 = 1; } while(0)
#define SCL1_ResetPullup()        do { WPUCbits.WPUC3 = 0; } while(0)
#define SCL1_SetPushPull()        do { ODCONCbits.ODCC3 = 0; } while(0)
#define SCL1_SetOpenDrain()       do { ODCONCbits.ODCC3 = 1; } while(0)
#define SCL1_SetAnalogMode()      do { ANSELCbits.ANSC3 = 1; } while(0)
#define SCL1_SetDigitalMode()     do { ANSELCbits.ANSC3 = 0; } while(0)

// get/set SDA1 aliases
#define SDA1_TRIS                 TRISCbits.TRISC4
#define SDA1_LAT                  LATCbits.LATC4
#define SDA1_PORT                 PORTCbits.RC4
#define SDA1_WPU                  WPUCbits.WPUC4
#define SDA1_OD                   ODCONCbits.ODCC4
#define SDA1_ANS                  ANSELCbits.ANSC4
#define SDA1_SetHigh()            do { LATCbits.LATC4 = 1; } while(0)
#define SDA1_SetLow()             do { LATCbits.LATC4 = 0; } while(0)
#define SDA1_Toggle()             do { LATCbits.LATC4 = ~LATCbits.LATC4; } while(0)
#define SDA1_GetValue()           PORTCbits.RC4
#define SDA1_SetDigitalInput()    do { TRISCbits.TRISC4 = 1; } while(0)
#define SDA1_SetDigitalOutput()   do { TRISCbits.TRISC4 = 0; } while(0)
#define SDA1_SetPullup()          do { WPUCbits.WPUC4 = 1; } while(0)
#define SDA1_ResetPullup()        do { WPUCbits.WPUC4 = 0; } while(0)
#define SDA1_SetPushPull()        do { ODCONCbits.ODCC4 = 0; } while(0)
#define SDA1_SetOpenDrain()       do { ODCONCbits.ODCC4 = 1; } while(0)
#define SDA1_SetAnalogMode()      do { ANSELCbits.ANSC4 = 1; } while(0)
#define SDA1_SetDigitalMode()     do { ANSELCbits.ANSC4 = 0; } while(0)

// get/set RL_SENSE1 aliases
#define RL_SENSE1_TRIS                 TRISCbits.TRISC5
#define RL_SENSE1_LAT                  LATCbits.LATC5
#define RL_SENSE1_PORT                 PORTCbits.RC5
#define RL_SENSE1_WPU                  WPUCbits.WPUC5
#define RL_SENSE1_OD                   ODCONCbits.ODCC5
#define RL_SENSE1_ANS                  ANSELCbits.ANSC5
#define RL_SENSE1_SetHigh()            do { LATCbits.LATC5 = 1; } while(0)
#define RL_SENSE1_SetLow()             do { LATCbits.LATC5 = 0; } while(0)
#define RL_SENSE1_Toggle()             do { LATCbits.LATC5 = ~LATCbits.LATC5; } while(0)
#define RL_SENSE1_GetValue()           PORTCbits.RC5
#define RL_SENSE1_SetDigitalInput()    do { TRISCbits.TRISC5 = 1; } while(0)
#define RL_SENSE1_SetDigitalOutput()   do { TRISCbits.TRISC5 = 0; } while(0)
#define RL_SENSE1_SetPullup()          do { WPUCbits.WPUC5 = 1; } while(0)
#define RL_SENSE1_ResetPullup()        do { WPUCbits.WPUC5 = 0; } while(0)
#define RL_SENSE1_SetPushPull()        do { ODCONCbits.ODCC5 = 0; } while(0)
#define RL_SENSE1_SetOpenDrain()       do { ODCONCbits.ODCC5 = 1; } while(0)
#define RL_SENSE1_SetAnalogMode()      do { ANSELCbits.ANSC5 = 1; } while(0)
#define RL_SENSE1_SetDigitalMode()     do { ANSELCbits.ANSC5 = 0; } while(0)

// get/set RL_SENSE2 aliases
#define RL_SENSE2_TRIS                 TRISCbits.TRISC6
#define RL_SENSE2_LAT                  LATCbits.LATC6
#define RL_SENSE2_PORT                 PORTCbits.RC6
#define RL_SENSE2_WPU                  WPUCbits.WPUC6
#define RL_SENSE2_OD                   ODCONCbits.ODCC6
#define RL_SENSE2_ANS                  ANSELCbits.ANSC6
#define RL_SENSE2_SetHigh()            do { LATCbits.LATC6 = 1; } while(0)
#define RL_SENSE2_SetLow()             do { LATCbits.LATC6 = 0; } while(0)
#define RL_SENSE2_Toggle()             do { LATCbits.LATC6 = ~LATCbits.LATC6; } while(0)
#define RL_SENSE2_GetValue()           PORTCbits.RC6
#define RL_SENSE2_SetDigitalInput()    do { TRISCbits.TRISC6 = 1; } while(0)
#define RL_SENSE2_SetDigitalOutput()   do { TRISCbits.TRISC6 = 0; } while(0)
#define RL_SENSE2_SetPullup()          do { WPUCbits.WPUC6 = 1; } while(0)
#define RL_SENSE2_ResetPullup()        do { WPUCbits.WPUC6 = 0; } while(0)
#define RL_SENSE2_SetPushPull()        do { ODCONCbits.ODCC6 = 0; } while(0)
#define RL_SENSE2_SetOpenDrain()       do { ODCONCbits.ODCC6 = 1; } while(0)
#define RL_SENSE2_SetAnalogMode()      do { ANSELCbits.ANSC6 = 1; } while(0)
#define RL_SENSE2_SetDigitalMode()     do { ANSELCbits.ANSC6 = 0; } while(0)

// get/set RL_ERROR aliases
#define RL_ERROR_TRIS                 TRISCbits.TRISC7
#define RL_ERROR_LAT                  LATCbits.LATC7
#define RL_ERROR_PORT                 PORTCbits.RC7
#define RL_ERROR_WPU                  WPUCbits.WPUC7
#define RL_ERROR_OD                   ODCONCbits.ODCC7
#define RL_ERROR_ANS                  ANSELCbits.ANSC7
#define RL_ERROR_SetHigh()            do { LATCbits.LATC7 = 1; } while(0)
#define RL_ERROR_SetLow()             do { LATCbits.LATC7 = 0; } while(0)
#define RL_ERROR_Toggle()             do { LATCbits.LATC7 = ~LATCbits.LATC7; } while(0)
#define RL_ERROR_GetValue()           PORTCbits.RC7
#define RL_ERROR_SetDigitalInput()    do { TRISCbits.TRISC7 = 1; } while(0)
#define RL_ERROR_SetDigitalOutput()   do { TRISCbits.TRISC7 = 0; } while(0)
#define RL_ERROR_SetPullup()          do { WPUCbits.WPUC7 = 1; } while(0)
#define RL_ERROR_ResetPullup()        do { WPUCbits.WPUC7 = 0; } while(0)
#define RL_ERROR_SetPushPull()        do { ODCONCbits.ODCC7 = 0; } while(0)
#define RL_ERROR_SetOpenDrain()       do { ODCONCbits.ODCC7 = 1; } while(0)
#define RL_ERROR_SetAnalogMode()      do { ANSELCbits.ANSC7 = 1; } while(0)
#define RL_ERROR_SetDigitalMode()     do { ANSELCbits.ANSC7 = 0; } while(0)

// get/set FL_ERROR aliases
#define FL_ERROR_TRIS                 TRISDbits.TRISD0
#define FL_ERROR_LAT                  LATDbits.LATD0
#define FL_ERROR_PORT                 PORTDbits.RD0
#define FL_ERROR_WPU                  WPUDbits.WPUD0
#define FL_ERROR_OD                   ODCONDbits.ODCD0
#define FL_ERROR_ANS                  ANSELDbits.ANSD0
#define FL_ERROR_SetHigh()            do { LATDbits.LATD0 = 1; } while(0)
#define FL_ERROR_SetLow()             do { LATDbits.LATD0 = 0; } while(0)
#define FL_ERROR_Toggle()             do { LATDbits.LATD0 = ~LATDbits.LATD0; } while(0)
#define FL_ERROR_GetValue()           PORTDbits.RD0
#define FL_ERROR_SetDigitalInput()    do { TRISDbits.TRISD0 = 1; } while(0)
#define FL_ERROR_SetDigitalOutput()   do { TRISDbits.TRISD0 = 0; } while(0)
#define FL_ERROR_SetPullup()          do { WPUDbits.WPUD0 = 1; } while(0)
#define FL_ERROR_ResetPullup()        do { WPUDbits.WPUD0 = 0; } while(0)
#define FL_ERROR_SetPushPull()        do { ODCONDbits.ODCD0 = 0; } while(0)
#define FL_ERROR_SetOpenDrain()       do { ODCONDbits.ODCD0 = 1; } while(0)
#define FL_ERROR_SetAnalogMode()      do { ANSELDbits.ANSD0 = 1; } while(0)
#define FL_ERROR_SetDigitalMode()     do { ANSELDbits.ANSD0 = 0; } while(0)

// get/set BATT_VOLTAGE aliases
#define BATT_VOLTAGE_TRIS                 TRISDbits.TRISD1
#define BATT_VOLTAGE_LAT                  LATDbits.LATD1
#define BATT_VOLTAGE_PORT                 PORTDbits.RD1
#define BATT_VOLTAGE_WPU                  WPUDbits.WPUD1
#define BATT_VOLTAGE_OD                   ODCONDbits.ODCD1
#define BATT_VOLTAGE_ANS                  ANSELDbits.ANSD1
#define BATT_VOLTAGE_SetHigh()            do { LATDbits.LATD1 = 1; } while(0)
#define BATT_VOLTAGE_SetLow()             do { LATDbits.LATD1 = 0; } while(0)
#define BATT_VOLTAGE_Toggle()             do { LATDbits.LATD1 = ~LATDbits.LATD1; } while(0)
#define BATT_VOLTAGE_GetValue()           PORTDbits.RD1
#define BATT_VOLTAGE_SetDigitalInput()    do { TRISDbits.TRISD1 = 1; } while(0)
#define BATT_VOLTAGE_SetDigitalOutput()   do { TRISDbits.TRISD1 = 0; } while(0)
#define BATT_VOLTAGE_SetPullup()          do { WPUDbits.WPUD1 = 1; } while(0)
#define BATT_VOLTAGE_ResetPullup()        do { WPUDbits.WPUD1 = 0; } while(0)
#define BATT_VOLTAGE_SetPushPull()        do { ODCONDbits.ODCD1 = 0; } while(0)
#define BATT_VOLTAGE_SetOpenDrain()       do { ODCONDbits.ODCD1 = 1; } while(0)
#define BATT_VOLTAGE_SetAnalogMode()      do { ANSELDbits.ANSD1 = 1; } while(0)
#define BATT_VOLTAGE_SetDigitalMode()     do { ANSELDbits.ANSD1 = 0; } while(0)

// get/set ALERT aliases
#define ALERT_TRIS                 TRISDbits.TRISD2
#define ALERT_LAT                  LATDbits.LATD2
#define ALERT_PORT                 PORTDbits.RD2
#define ALERT_WPU                  WPUDbits.WPUD2
#define ALERT_OD                   ODCONDbits.ODCD2
#define ALERT_ANS                  ANSELDbits.ANSD2
#define ALERT_SetHigh()            do { LATDbits.LATD2 = 1; } while(0)
#define ALERT_SetLow()             do { LATDbits.LATD2 = 0; } while(0)
#define ALERT_Toggle()             do { LATDbits.LATD2 = ~LATDbits.LATD2; } while(0)
#define ALERT_GetValue()           PORTDbits.RD2
#define ALERT_SetDigitalInput()    do { TRISDbits.TRISD2 = 1; } while(0)
#define ALERT_SetDigitalOutput()   do { TRISDbits.TRISD2 = 0; } while(0)
#define ALERT_SetPullup()          do { WPUDbits.WPUD2 = 1; } while(0)
#define ALERT_ResetPullup()        do { WPUDbits.WPUD2 = 0; } while(0)
#define ALERT_SetPushPull()        do { ODCONDbits.ODCD2 = 0; } while(0)
#define ALERT_SetOpenDrain()       do { ODCONDbits.ODCD2 = 1; } while(0)
#define ALERT_SetAnalogMode()      do { ANSELDbits.ANSD2 = 1; } while(0)
#define ALERT_SetDigitalMode()     do { ANSELDbits.ANSD2 = 0; } while(0)

// get/set RL_CURRENT aliases
#define RL_CURRENT_TRIS                 TRISDbits.TRISD4
#define RL_CURRENT_LAT                  LATDbits.LATD4
#define RL_CURRENT_PORT                 PORTDbits.RD4
#define RL_CURRENT_WPU                  WPUDbits.WPUD4
#define RL_CURRENT_OD                   ODCONDbits.ODCD4
#define RL_CURRENT_ANS                  ANSELDbits.ANSD4
#define RL_CURRENT_SetHigh()            do { LATDbits.LATD4 = 1; } while(0)
#define RL_CURRENT_SetLow()             do { LATDbits.LATD4 = 0; } while(0)
#define RL_CURRENT_Toggle()             do { LATDbits.LATD4 = ~LATDbits.LATD4; } while(0)
#define RL_CURRENT_GetValue()           PORTDbits.RD4
#define RL_CURRENT_SetDigitalInput()    do { TRISDbits.TRISD4 = 1; } while(0)
#define RL_CURRENT_SetDigitalOutput()   do { TRISDbits.TRISD4 = 0; } while(0)
#define RL_CURRENT_SetPullup()          do { WPUDbits.WPUD4 = 1; } while(0)
#define RL_CURRENT_ResetPullup()        do { WPUDbits.WPUD4 = 0; } while(0)
#define RL_CURRENT_SetPushPull()        do { ODCONDbits.ODCD4 = 0; } while(0)
#define RL_CURRENT_SetOpenDrain()       do { ODCONDbits.ODCD4 = 1; } while(0)
#define RL_CURRENT_SetAnalogMode()      do { ANSELDbits.ANSD4 = 1; } while(0)
#define RL_CURRENT_SetDigitalMode()     do { ANSELDbits.ANSD4 = 0; } while(0)

// get/set RL_DIRECTION aliases
#define RL_DIRECTION_TRIS                 TRISDbits.TRISD5
#define RL_DIRECTION_LAT                  LATDbits.LATD5
#define RL_DIRECTION_PORT                 PORTDbits.RD5
#define RL_DIRECTION_WPU                  WPUDbits.WPUD5
#define RL_DIRECTION_OD                   ODCONDbits.ODCD5
#define RL_DIRECTION_ANS                  ANSELDbits.ANSD5
#define RL_DIRECTION_SetHigh()            do { LATDbits.LATD5 = 1; } while(0)
#define RL_DIRECTION_SetLow()             do { LATDbits.LATD5 = 0; } while(0)
#define RL_DIRECTION_Toggle()             do { LATDbits.LATD5 = ~LATDbits.LATD5; } while(0)
#define RL_DIRECTION_GetValue()           PORTDbits.RD5
#define RL_DIRECTION_SetDigitalInput()    do { TRISDbits.TRISD5 = 1; } while(0)
#define RL_DIRECTION_SetDigitalOutput()   do { TRISDbits.TRISD5 = 0; } while(0)
#define RL_DIRECTION_SetPullup()          do { WPUDbits.WPUD5 = 1; } while(0)
#define RL_DIRECTION_ResetPullup()        do { WPUDbits.WPUD5 = 0; } while(0)
#define RL_DIRECTION_SetPushPull()        do { ODCONDbits.ODCD5 = 0; } while(0)
#define RL_DIRECTION_SetOpenDrain()       do { ODCONDbits.ODCD5 = 1; } while(0)
#define RL_DIRECTION_SetAnalogMode()      do { ANSELDbits.ANSD5 = 1; } while(0)
#define RL_DIRECTION_SetDigitalMode()     do { ANSELDbits.ANSD5 = 0; } while(0)

// get/set RD6 procedures
#define RD6_SetHigh()            do { LATDbits.LATD6 = 1; } while(0)
#define RD6_SetLow()             do { LATDbits.LATD6 = 0; } while(0)
#define RD6_Toggle()             do { LATDbits.LATD6 = ~LATDbits.LATD6; } while(0)
#define RD6_GetValue()              PORTDbits.RD6
#define RD6_SetDigitalInput()    do { TRISDbits.TRISD6 = 1; } while(0)
#define RD6_SetDigitalOutput()   do { TRISDbits.TRISD6 = 0; } while(0)
#define RD6_SetPullup()             do { WPUDbits.WPUD6 = 1; } while(0)
#define RD6_ResetPullup()           do { WPUDbits.WPUD6 = 0; } while(0)
#define RD6_SetAnalogMode()         do { ANSELDbits.ANSD6 = 1; } while(0)
#define RD6_SetDigitalMode()        do { ANSELDbits.ANSD6 = 0; } while(0)

// get/set REAR_GROUND aliases
#define REAR_GROUND_TRIS                 TRISDbits.TRISD7
#define REAR_GROUND_LAT                  LATDbits.LATD7
#define REAR_GROUND_PORT                 PORTDbits.RD7
#define REAR_GROUND_WPU                  WPUDbits.WPUD7
#define REAR_GROUND_OD                   ODCONDbits.ODCD7
#define REAR_GROUND_ANS                  ANSELDbits.ANSD7
#define REAR_GROUND_SetHigh()            do { LATDbits.LATD7 = 1; } while(0)
#define REAR_GROUND_SetLow()             do { LATDbits.LATD7 = 0; } while(0)
#define REAR_GROUND_Toggle()             do { LATDbits.LATD7 = ~LATDbits.LATD7; } while(0)
#define REAR_GROUND_GetValue()           PORTDbits.RD7
#define REAR_GROUND_SetDigitalInput()    do { TRISDbits.TRISD7 = 1; } while(0)
#define REAR_GROUND_SetDigitalOutput()   do { TRISDbits.TRISD7 = 0; } while(0)
#define REAR_GROUND_SetPullup()          do { WPUDbits.WPUD7 = 1; } while(0)
#define REAR_GROUND_ResetPullup()        do { WPUDbits.WPUD7 = 0; } while(0)
#define REAR_GROUND_SetPushPull()        do { ODCONDbits.ODCD7 = 0; } while(0)
#define REAR_GROUND_SetOpenDrain()       do { ODCONDbits.ODCD7 = 1; } while(0)
#define REAR_GROUND_SetAnalogMode()      do { ANSELDbits.ANSD7 = 1; } while(0)
#define REAR_GROUND_SetDigitalMode()     do { ANSELDbits.ANSD7 = 0; } while(0)

// get/set FR_ERROR aliases
#define FR_ERROR_TRIS                 TRISEbits.TRISE0
#define FR_ERROR_LAT                  LATEbits.LATE0
#define FR_ERROR_PORT                 PORTEbits.RE0
#define FR_ERROR_WPU                  WPUEbits.WPUE0
#define FR_ERROR_OD                   ODCONEbits.ODCE0
#define FR_ERROR_ANS                  ANSELEbits.ANSE0
#define FR_ERROR_SetHigh()            do { LATEbits.LATE0 = 1; } while(0)
#define FR_ERROR_SetLow()             do { LATEbits.LATE0 = 0; } while(0)
#define FR_ERROR_Toggle()             do { LATEbits.LATE0 = ~LATEbits.LATE0; } while(0)
#define FR_ERROR_GetValue()           PORTEbits.RE0
#define FR_ERROR_SetDigitalInput()    do { TRISEbits.TRISE0 = 1; } while(0)
#define FR_ERROR_SetDigitalOutput()   do { TRISEbits.TRISE0 = 0; } while(0)
#define FR_ERROR_SetPullup()          do { WPUEbits.WPUE0 = 1; } while(0)
#define FR_ERROR_ResetPullup()        do { WPUEbits.WPUE0 = 0; } while(0)
#define FR_ERROR_SetPushPull()        do { ODCONEbits.ODCE0 = 0; } while(0)
#define FR_ERROR_SetOpenDrain()       do { ODCONEbits.ODCE0 = 1; } while(0)
#define FR_ERROR_SetAnalogMode()      do { ANSELEbits.ANSE0 = 1; } while(0)
#define FR_ERROR_SetDigitalMode()     do { ANSELEbits.ANSE0 = 0; } while(0)

// get/set FR_CURRENT aliases
#define FR_CURRENT_TRIS                 TRISEbits.TRISE1
#define FR_CURRENT_LAT                  LATEbits.LATE1
#define FR_CURRENT_PORT                 PORTEbits.RE1
#define FR_CURRENT_WPU                  WPUEbits.WPUE1
#define FR_CURRENT_OD                   ODCONEbits.ODCE1
#define FR_CURRENT_ANS                  ANSELEbits.ANSE1
#define FR_CURRENT_SetHigh()            do { LATEbits.LATE1 = 1; } while(0)
#define FR_CURRENT_SetLow()             do { LATEbits.LATE1 = 0; } while(0)
#define FR_CURRENT_Toggle()             do { LATEbits.LATE1 = ~LATEbits.LATE1; } while(0)
#define FR_CURRENT_GetValue()           PORTEbits.RE1
#define FR_CURRENT_SetDigitalInput()    do { TRISEbits.TRISE1 = 1; } while(0)
#define FR_CURRENT_SetDigitalOutput()   do { TRISEbits.TRISE1 = 0; } while(0)
#define FR_CURRENT_SetPullup()          do { WPUEbits.WPUE1 = 1; } while(0)
#define FR_CURRENT_ResetPullup()        do { WPUEbits.WPUE1 = 0; } while(0)
#define FR_CURRENT_SetPushPull()        do { ODCONEbits.ODCE1 = 0; } while(0)
#define FR_CURRENT_SetOpenDrain()       do { ODCONEbits.ODCE1 = 1; } while(0)
#define FR_CURRENT_SetAnalogMode()      do { ANSELEbits.ANSE1 = 1; } while(0)
#define FR_CURRENT_SetDigitalMode()     do { ANSELEbits.ANSE1 = 0; } while(0)

// get/set RE2 procedures
#define RE2_SetHigh()            do { LATEbits.LATE2 = 1; } while(0)
#define RE2_SetLow()             do { LATEbits.LATE2 = 0; } while(0)
#define RE2_Toggle()             do { LATEbits.LATE2 = ~LATEbits.LATE2; } while(0)
#define RE2_GetValue()              PORTEbits.RE2
#define RE2_SetDigitalInput()    do { TRISEbits.TRISE2 = 1; } while(0)
#define RE2_SetDigitalOutput()   do { TRISEbits.TRISE2 = 0; } while(0)
#define RE2_SetPullup()             do { WPUEbits.WPUE2 = 1; } while(0)
#define RE2_ResetPullup()           do { WPUEbits.WPUE2 = 0; } while(0)
#define RE2_SetAnalogMode()         do { ANSELEbits.ANSE2 = 1; } while(0)
#define RE2_SetDigitalMode()        do { ANSELEbits.ANSE2 = 0; } while(0)

/**
   @Param
    none
   @Returns
    none
   @Description
    GPIO and peripheral I/O initialization
   @Example
    PIN_MANAGER_Initialize();
 */
void PIN_MANAGER_Initialize (void);

/**
 * @Param
    none
 * @Returns
    none
 * @Description
    Interrupt on Change Handling routine
 * @Example
    PIN_MANAGER_IOC();
 */
void PIN_MANAGER_IOC(void);


/**
 * @Param
    none
 * @Returns
    none
 * @Description
    Interrupt on Change Handler for the IOCAF2 pin functionality
 * @Example
    IOCAF2_ISR();
 */
void IOCAF2_ISR(void);

/**
  @Summary
    Interrupt Handler Setter for IOCAF2 pin interrupt-on-change functionality

  @Description
    Allows selecting an interrupt handler for IOCAF2 at application runtime
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    InterruptHandler function pointer.

  @Example
    PIN_MANAGER_Initialize();
    IOCAF2_SetInterruptHandler(MyInterruptHandler);

*/
void IOCAF2_SetInterruptHandler(void (* InterruptHandler)(void));

/**
  @Summary
    Dynamic Interrupt Handler for IOCAF2 pin

  @Description
    This is a dynamic interrupt handler to be used together with the IOCAF2_SetInterruptHandler() method.
    This handler is called every time the IOCAF2 ISR is executed and allows any function to be registered at runtime.
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    None.

  @Example
    PIN_MANAGER_Initialize();
    IOCAF2_SetInterruptHandler(IOCAF2_InterruptHandler);

*/
extern void (*IOCAF2_InterruptHandler)(void);

/**
  @Summary
    Default Interrupt Handler for IOCAF2 pin

  @Description
    This is a predefined interrupt handler to be used together with the IOCAF2_SetInterruptHandler() method.
    This handler is called every time the IOCAF2 ISR is executed. 
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    None.

  @Example
    PIN_MANAGER_Initialize();
    IOCAF2_SetInterruptHandler(IOCAF2_DefaultInterruptHandler);

*/
void IOCAF2_DefaultInterruptHandler(void);


/**
 * @Param
    none
 * @Returns
    none
 * @Description
    Interrupt on Change Handler for the IOCAF3 pin functionality
 * @Example
    IOCAF3_ISR();
 */
void IOCAF3_ISR(void);

/**
  @Summary
    Interrupt Handler Setter for IOCAF3 pin interrupt-on-change functionality

  @Description
    Allows selecting an interrupt handler for IOCAF3 at application runtime
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    InterruptHandler function pointer.

  @Example
    PIN_MANAGER_Initialize();
    IOCAF3_SetInterruptHandler(MyInterruptHandler);

*/
void IOCAF3_SetInterruptHandler(void (* InterruptHandler)(void));

/**
  @Summary
    Dynamic Interrupt Handler for IOCAF3 pin

  @Description
    This is a dynamic interrupt handler to be used together with the IOCAF3_SetInterruptHandler() method.
    This handler is called every time the IOCAF3 ISR is executed and allows any function to be registered at runtime.
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    None.

  @Example
    PIN_MANAGER_Initialize();
    IOCAF3_SetInterruptHandler(IOCAF3_InterruptHandler);

*/
extern void (*IOCAF3_InterruptHandler)(void);

/**
  @Summary
    Default Interrupt Handler for IOCAF3 pin

  @Description
    This is a predefined interrupt handler to be used together with the IOCAF3_SetInterruptHandler() method.
    This handler is called every time the IOCAF3 ISR is executed. 
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    None.

  @Example
    PIN_MANAGER_Initialize();
    IOCAF3_SetInterruptHandler(IOCAF3_DefaultInterruptHandler);

*/
void IOCAF3_DefaultInterruptHandler(void);


/**
 * @Param
    none
 * @Returns
    none
 * @Description
    Interrupt on Change Handler for the IOCBF5 pin functionality
 * @Example
    IOCBF5_ISR();
 */
void IOCBF5_ISR(void);

/**
  @Summary
    Interrupt Handler Setter for IOCBF5 pin interrupt-on-change functionality

  @Description
    Allows selecting an interrupt handler for IOCBF5 at application runtime
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    InterruptHandler function pointer.

  @Example
    PIN_MANAGER_Initialize();
    IOCBF5_SetInterruptHandler(MyInterruptHandler);

*/
void IOCBF5_SetInterruptHandler(void (* InterruptHandler)(void));

/**
  @Summary
    Dynamic Interrupt Handler for IOCBF5 pin

  @Description
    This is a dynamic interrupt handler to be used together with the IOCBF5_SetInterruptHandler() method.
    This handler is called every time the IOCBF5 ISR is executed and allows any function to be registered at runtime.
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    None.

  @Example
    PIN_MANAGER_Initialize();
    IOCBF5_SetInterruptHandler(IOCBF5_InterruptHandler);

*/
extern void (*IOCBF5_InterruptHandler)(void);

/**
  @Summary
    Default Interrupt Handler for IOCBF5 pin

  @Description
    This is a predefined interrupt handler to be used together with the IOCBF5_SetInterruptHandler() method.
    This handler is called every time the IOCBF5 ISR is executed. 
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    None.

  @Example
    PIN_MANAGER_Initialize();
    IOCBF5_SetInterruptHandler(IOCBF5_DefaultInterruptHandler);

*/
void IOCBF5_DefaultInterruptHandler(void);


/**
 * @Param
    none
 * @Returns
    none
 * @Description
    Interrupt on Change Handler for the IOCCF5 pin functionality
 * @Example
    IOCCF5_ISR();
 */
void IOCCF5_ISR(void);

/**
  @Summary
    Interrupt Handler Setter for IOCCF5 pin interrupt-on-change functionality

  @Description
    Allows selecting an interrupt handler for IOCCF5 at application runtime
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    InterruptHandler function pointer.

  @Example
    PIN_MANAGER_Initialize();
    IOCCF5_SetInterruptHandler(MyInterruptHandler);

*/
void IOCCF5_SetInterruptHandler(void (* InterruptHandler)(void));

/**
  @Summary
    Dynamic Interrupt Handler for IOCCF5 pin

  @Description
    This is a dynamic interrupt handler to be used together with the IOCCF5_SetInterruptHandler() method.
    This handler is called every time the IOCCF5 ISR is executed and allows any function to be registered at runtime.
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    None.

  @Example
    PIN_MANAGER_Initialize();
    IOCCF5_SetInterruptHandler(IOCCF5_InterruptHandler);

*/
extern void (*IOCCF5_InterruptHandler)(void);

/**
  @Summary
    Default Interrupt Handler for IOCCF5 pin

  @Description
    This is a predefined interrupt handler to be used together with the IOCCF5_SetInterruptHandler() method.
    This handler is called every time the IOCCF5 ISR is executed. 
    
  @Preconditions
    Pin Manager intializer called

  @Returns
    None.

  @Param
    None.

  @Example
    PIN_MANAGER_Initialize();
    IOCCF5_SetInterruptHandler(IOCCF5_DefaultInterruptHandler);

*/
void IOCCF5_DefaultInterruptHandler(void);



#endif // PIN_MANAGER_H
/**
 End of File
*/