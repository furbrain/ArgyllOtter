/* 
 * File:   commands.h
 * Author: phil
 *
 * Created on 07 September 2019, 18:07
 */

#ifndef COMMANDS_H
#define	COMMANDS_H

#ifdef	__cplusplus
extern "C" {
#endif
#include <stdint.h>
#include <stdbool.h>

#define BUFFER_SIZE 0x60
#define WHEEL_DIAMETER 70
#define ALERT_ADDRESS 0x5F

typedef enum {
    CMD_STOP = 0,
    CMD_DRIVE = 1,
    CMD_DISTANCE = 2,
    CMD_ROTATE = 3,
    CMD_INDIVIDUAL = 4,
    CMD_CALIBRATE = 0xFF
} cmd_enums;    
    
typedef struct {
    uint8_t mode;
    union {
        struct {
            int16_t left_speed;
            int16_t right_speed;
            uint8_t soft_start;
        };
        struct {
            int32_t left_distance;
            int32_t right_distance;
            int16_t max_speed;
        };
        struct {
            int16_t angle;
        };
        struct {
            int16_t motor_speed[4];
        };
    };
} command_t;

typedef struct {
    float kP;
    float kI;
    float kD;
    float mm_per_click;
} constants_t;


extern volatile uint8_t EEPROM_Buffer[BUFFER_SIZE];
extern volatile uint8_t EEPROM_Shadow[BUFFER_SIZE];
extern volatile int32_t* const position; // position for each wheel in encoder count
extern volatile int16_t* const velocity; // velocity for each wheel in counts/0.05s
extern volatile int16_t* const power; // velocity for each wheel in counts/0.05s
extern volatile command_t* const command; //current command
extern volatile constants_t* const constants; //kP, kI, kD, mm per click
extern volatile int16_t* const current; // current for each motor in mA
extern volatile int16_t* const current_limit; //current limit for each motor in mA
extern volatile int16_t* const batt_voltage; //voltage in mV
extern volatile int16_t* const peripheral_voltage; //5V level in mV
extern volatile uint8_t* const alert_status;
extern volatile bool new_command;


typedef enum
{
    I2C1_SLAVE_WRITE_REQUEST,
    I2C1_SLAVE_READ_REQUEST,
    I2C1_SLAVE_WRITE_COMPLETED,
    I2C1_SLAVE_READ_COMPLETED,
    I2C1_SLAVE_STOP
} I2C1_SLAVE_DRIVER_STATUS;

typedef enum 
{
    ALERT_NOALERT = 0,
    ALERT_DESTINATION = 1,
    ALERT_OVERCURRENT = 2, //go up in powers of two...
    ALERT_UNSPECIFIED = 0xFF
    
} ALERT_STATUS;

void I2C1_StatusCallback(I2C1_SLAVE_DRIVER_STATUS i2c_bus_state);

void comms_init(void);

void raise_alert(ALERT_STATUS status);

#ifdef	__cplusplus
}
#endif

#endif	/* COMMANDS_H */

