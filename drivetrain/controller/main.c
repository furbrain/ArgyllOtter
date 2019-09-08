/**
  Generated Main Source File

  Company:
    Microchip Technology Inc.

  File Name:
    main.c

  Summary:
    This is the main file generated using PIC10 / PIC12 / PIC16 / PIC18 MCUs

  Description:
    This header file provides implementations for driver APIs for all modules selected in the GUI.
    Generation Information :
        Product Revision  :  PIC10 / PIC12 / PIC16 / PIC18 MCUs - 1.77
        Device            :  PIC16F18877
        Driver Version    :  2.00
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

#include "mcc_generated_files/mcc.h"

/*
                         Main application
 */
#include <stdint.h>
#include <string.h>
#include "comms.h"
#include "pid.h"
int16_t *counts = (int16_t*)EEPROM_Buffer;
volatile int32_t current_count = 0, last_count = 0, target=0;
int8_t count_index = 0, print_count = -1;
pid_t pid;

void RR_sensor(void) {
    if (RR_SENSE2_GetValue()) {
        current_count++;
    } else {
        current_count--;
    }
}

bool within(int32_t desired, int32_t actual, int32_t range) {
    return (((desired + range) > actual) && ((desired - range) < actual));
}

void OneHundredHertz(void) {
    float power;
    
    int32_t input;
    int16_t duty;
    if (print_count > 0) {
        printf("Pos: %ld\n\r", current_count);
        print_count--;
    }
    if (within(target, current_count, 10)) {
        // turn off motors
        if (print_count==-1) {
            print_count=5;
            printf("On target!\n\r");
        }
        RR_DIRECTION_SetLow();
        PWM2_LoadDutyValue(0);
    } else if (within(target, current_count, 300)){
        if (current_count < target) {
            pid_setPoint(&pid, 15);
        } else {
            pid_setPoint(&pid, -15);
        }
    } else {
        if (current_count < target) {
            pid_setPoint(&pid, 50);
        } else {
            pid_setPoint(&pid, -50);
        }
        
    }
    if (!(within(target, current_count, 10)) && (count_index >=5)) {
        input = current_count-last_count;
        last_count = current_count;
        power = pid_compute(&pid, input);
        duty = (int16_t)(power*0x3ff);
        if (power < 0.0) {
            RR_DIRECTION_SetHigh();
            PWM2_LoadDutyValue(0x3ff - (uint16_t)(-duty));
        } else {
            RR_DIRECTION_SetLow();
            PWM2_LoadDutyValue((uint16_t)duty);            
        }
        count_index=0;
    }
    count_index++;
}

void ADCResultReady(void) {
    uint16_t result = ADCC_GetConversionResult();
    printf("ADCC: %d\n\r", result);
}


void main(void)
{
    // initialize the device
    SYSTEM_Initialize();
    pid_tune(&pid, 0.03, 0.01, 0.01); //tuned for movement
    //pid_tune(&pid, 0.05, 0.001, 0.6); //tuned for postion, pOnE
    //pid_tune(&pid, 0.01, 0.001, 0.3); //tuned for postion, pOnM
    pid.pOnE=true;
    pid_init(&pid,0,0);
    pid_setPoint(&pid, 0);
    current_count = 0;
    count_index = 5;
    IOCBF5_SetInterruptHandler(RR_sensor);
    TMR0_SetInterruptHandler(OneHundredHertz);
    ADCC_SetADIInterruptHandler(ADCResultReady);
    ADCC_StartConversion(RR_CURRENT);
    // Enable the Global Interrupts
    memset(counts, 0, 256);
    INTERRUPT_GlobalInterruptEnable();
    INTERRUPT_PeripheralInterruptEnable();
    while (1)
    {
        target = 1600;
        print_count = -1;
        __delay_ms(5000);
        target = 0;
        print_count = -1;
        __delay_ms(5000);
        target = -60;
        print_count = -1;
        __delay_ms(5000);
        target = -600;
        print_count = -1;
        __delay_ms(5000);
    }
}
/**
 End of File
*/