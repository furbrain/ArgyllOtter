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
#include <stdlib.h>
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
    tick = true;
}

#define within(a, b, delta) (abs(a-b) < delta)

void set_wheel_differentials(int32_t left, int32_t right, int16_t speed) {
    int32_t left_speed, right_speed;
    if (left == right) {
        left_speed = right_speed = speed;
    } else {
        int32_t max_distance = max(abs(left), abs(right));
        left_speed = abs((left * speed) / max_distance);
        right_speed = abs((right * speed) / max_distance);
    }
    wheel_move_to(&wheels[FRONT_LEFT], left_speed);
    wheel_move_to(&wheels[REAR_LEFT], left_speed);
    wheel_move_to(&wheels[FRONT_RIGHT], right_speed);
    wheel_move_to(&wheels[REAR_RIGHT], right_speed);    
}

void Update(void) {
    static uint8_t count = 0;
    wheel_t* whl;
    if (new_command) {
        cmd = *command;
        raise_alert(ALERT_NOALERT);
        FOR_ALL_WHEELS(whl) {
            whl->stopped=false;
        }
        if (cmd.flags & FLAG_RESET_POS) {
                wheels_reset_position();            
        }
        if (cmd.flags & FLAG_SOFT_START) {
            FOR_ALL_WHEELS(whl) {
                wheel_soft_start(whl);
            }
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
                    wheel_set_power(&wheels[i], cmd.motor_speed[i]);
                }
                break;
            case CMD_FAST_DISTANCE:
            case CMD_DISTANCE:
                wheel_set_target_pos(&wheels[FRONT_LEFT], cmd.left_distance);
                wheel_set_target_pos(&wheels[REAR_LEFT], cmd.left_distance);
                wheel_set_target_pos(&wheels[FRONT_RIGHT], cmd.right_distance);
                wheel_set_target_pos(&wheels[REAR_RIGHT], cmd.right_distance);
                set_wheel_differentials(cmd.left_distance, cmd.right_distance, cmd.max_speed);
                break;
        }
        new_command = false;
    }
    if (cmd.mode == CMD_DISTANCE) {
        /* left */
        bool nearby = false;
        bool stopped = false;
        
        FOR_ALL_WHEELS(whl) {
            if (whl->stopped) {
                stopped = true;
                break;
            }
            if (within(whl->target_pos, *whl->pos, 10)) {
                raise_alert(ALERT_DESTINATION);
                stopped = true;
                break;
            } else if (within(whl->target_pos, *whl->pos, 300)){
                nearby = true;
            }
        }
        if (stopped) {
            FOR_ALL_WHEELS(whl) {
                wheel_stop(whl);
                cmd.mode = CMD_STOP;
            }
        } else if (nearby) {
            set_wheel_differentials(cmd.left_distance, cmd.right_distance, cmd.max_speed/4);
        } else {
            set_wheel_differentials(cmd.left_distance, cmd.right_distance, cmd.max_speed);
        }
    } else if (cmd.mode == CMD_FAST_DISTANCE) {
        FOR_ALL_WHEELS(whl) {
            if (!*alert_status) {
                if (abs(*whl->pos) > abs(whl->target_pos)) {
                    raise_alert(ALERT_DESTINATION);
                    break;
                } 
            }
        }
    }
    if (count++ >= SAMPLE_SKIP) {
        count = 0;
        FOR_ALL_WHEELS(whl) {
            wheel_update_velocity(whl);
            if (cmd.mode != CMD_INDIVIDUAL) {
                wheel_update_power(whl);
            }
        }
        FOR_ALL_WHEELS(whl) {
            //wheel_check_current(whl);
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
    TMR6_SetInterruptHandler(OneHundredHertz);
    TMR1_StartTimer();
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
