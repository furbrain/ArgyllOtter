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

#define BUFFER_SIZE 128    
    
enum WHEEL {
    FRONT_RIGHT = 0, 
    FRONT_LEFT = 1, 
    BACK_RIGHT = 2, 
    BACK_LEFT = 3
};
    
typedef struct {
    uint8_t mode;
    union {
        struct {
            int16_t left_speed;
            int16_t right_speed;
        };
        struct {
            int32_t left_distance;
            int32_t right_distance;
            int16_t max_speed;
        };
        struct {
            int16_t angle;
        };
    };
} command_t;

extern volatile uint8_t EEPROM_Buffer[BUFFER_SIZE];
extern volatile uint8_t EEPROM_Shadow[BUFFER_SIZE];
extern volatile int32_t* const position;
extern volatile int16_t* const velocity;

typedef enum
{
    I2C1_SLAVE_WRITE_REQUEST,
    I2C1_SLAVE_READ_REQUEST,
    I2C1_SLAVE_WRITE_COMPLETED,
    I2C1_SLAVE_READ_COMPLETED,
    I2C1_SLAVE_STOP
} I2C1_SLAVE_DRIVER_STATUS;


void I2C1_StatusCallback(I2C1_SLAVE_DRIVER_STATUS i2c_bus_state);



#ifdef	__cplusplus
}
#endif

#endif	/* COMMANDS_H */

