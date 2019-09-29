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
#pragma warning disable 520
#include "mcc_generated_files/mcc.h"

/*
                         Main application
 */
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "comms.h"
#include "pid.h"
#include "wheels.h"

const uint8_t ADC_CHANNELS[] = {
    FRONT_GROUND, 
    FL_CURRENT, 
    FR_CURRENT,
    REAR_GROUND,
    RL_CURRENT,
    RR_CURRENT, 
    BATT_VOLTAGE,
    channel_DAC1
};

volatile bool tick = false;
volatile command_t cmd;

inline void ADCC_SetChannel(uint8_t channel) {
    ADPCH = channel;
}


void OneHundredHertz(void) {
    cmd = *command;
    tick = true;
}
void Update(void) {
    static uint8_t count = 0;
    wheel_t* whl;
    if (new_command) {
        FOR_ALL_WHEELS(whl) {
            whl->stopped=false;
        }
        switch (cmd.mode) {
            case CMD_STOP:
                FOR_ALL_WHEELS(whl) {
                    wheel_stop(whl);
                }
                break;
            case CMD_DRIVE:
                wheel_set_speed(&wheels[FRONT_LEFT], cmd.left_speed);
                wheel_set_speed(&wheels[REAR_LEFT], cmd.left_speed);
                wheel_set_speed(&wheels[FRONT_RIGHT], cmd.right_speed);
                wheel_set_speed(&wheels[REAR_RIGHT], cmd.right_speed);
                break;
            case CMD_INDIVIDUAL:
                for(uint8_t i = 0; i< 4; i++) {
                    if (cmd.motor_speed[i]>0) {
                        wheels[i].set_direction(WHEEL_FORWARD);
                    } else {
                        wheels[i].set_direction(WHEEL_REVERSE);
                    }
                    wheels[i].set_pwm((uint16_t)cmd.motor_speed[i]);
                }
                break;
               
        }
        new_command = false;
    }
    if (cmd.mode == CMD_DISTANCE) {
        /* left */
        wheel_move_to(&wheels[FRONT_LEFT], cmd.left_distance, cmd.max_speed);
        wheel_move_to(&wheels[REAR_LEFT], cmd.left_distance, cmd.max_speed);
        wheel_move_to(&wheels[FRONT_RIGHT], cmd.right_distance, cmd.max_speed);
        wheel_move_to(&wheels[REAR_RIGHT], cmd.right_distance, cmd.max_speed);
    }
    if (count++ >= SAMPLE_SKIP) {
        count = 0;
        FOR_ALL_WHEELS(whl) {
            wheel_update_velocity(whl);
            wheel_update_power(whl);
        }
        FOR_ALL_WHEELS(whl) {
            wheel_check_current(whl);
        }
    }
}

void ADCResultReady(void) {
    static uint8_t channel_index = 0;
    static uint16_t ground = 0;
    uint8_t channel = ADC_CHANNELS[channel_index];
    uint16_t result = ADCC_GetConversionResult();
    switch (channel) {
        case FRONT_GROUND:
        case REAR_GROUND:
            ground = result;
            break;            
        case FL_CURRENT:
            current[FRONT_LEFT] = (result - ground) * 50;
            break;
        case FR_CURRENT:
            current[FRONT_RIGHT] = (result - ground) * 50;
            break;
        case RL_CURRENT:
            current[REAR_LEFT] = (result - ground) * 50;
            break;           
        case RR_CURRENT:
            current[REAR_RIGHT] = (result - ground) * 50;
            break;
        case BATT_VOLTAGE:
            *batt_voltage = result * 11 * 2;
            break;
        case channel_DAC1:
            *peripheral_voltage = result * 4 * 2;
            break;
        default:
            break;
    }
    channel_index = (channel_index+1) % sizeof(ADC_CHANNELS);
    channel = ADC_CHANNELS[channel_index];
    ADCC_SetChannel(channel);
}


void main(void)
{
    wheel_t* whl;
    SYSTEM_Initialize();
    comms_init();
    wheels_init();
    FOR_ALL_WHEELS(whl) {
        wheel_stop(whl);
    }
    TMR0_SetInterruptHandler(OneHundredHertz);
    ADCC_SetADIInterruptHandler(ADCResultReady);
    ADCC_SetChannel(FRONT_GROUND);
    // Enable the Interrupts
    INTERRUPT_GlobalInterruptEnable();
    INTERRUPT_PeripheralInterruptEnable();
    while (1)
    {
        while (!tick) {
            NOP();
        }
        tick = false;
        Update();
    }
}
/**
 End of File
*/