/* 
 * File:   wheels.h
 * Author: phil
 *
 * Created on September 8, 2019, 10:11 PM
 */

#ifndef WHEELS_H
#define	WHEELS_H

#ifdef	__cplusplus
extern "C" {
#endif

#include "pid.h"
#include "stdint.h"
    
enum WHEEL {
    FRONT_RIGHT = 0, 
    FRONT_LEFT = 1, 
    REAR_RIGHT = 2, 
    REAR_LEFT = 3
};

#define WHEEL_FORWARD 0
#define WHEEL_REVERSE 1

#define SAMPLE_FREQUENCY 100
#define SAMPLE_SKIP 5

#define FOR_ALL_WHEELS(x) for(x = &wheels[FRONT_RIGHT]; x<= &wheels[REAR_LEFT]; x++)

    
typedef struct {
    uint8_t adc_channel;
    bool stopped;
    volatile int32_t last_pos;
    volatile int32_t *pos;
    volatile int16_t *velocity;
    pid_t   *pid;
    void (*set_direction)(uint8_t);
    void (*set_pwm)(uint16_t);
            
} wheel_t;

extern wheel_t wheels[4];
void wheels_init(void);
void wheel_set_power(wheel_t *whl, float power);
void wheel_set_speed(wheel_t *whl, float speed);
void wheel_update_power(wheel_t *whl);
void wheel_update_velocity(wheel_t* whl);
void wheel_stop(wheel_t *whl);
void wheel_move_to(wheel_t *whl, int32_t pos, int16_t max_speed);

#ifdef	__cplusplus
}
#endif

#endif	/* WHEELS_H */

