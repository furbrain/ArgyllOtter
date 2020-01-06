#include "wheels.h"
#include "comms.h"
#include "mcc_generated_files/pin_manager.h"
#include "mcc_generated_files/adcc.h"
#include "mcc_generated_files/pwm1.h"
#include "mcc_generated_files/pwm2.h"
#include "mcc_generated_files/pwm4.h"
#include "mcc_generated_files/pwm5.h"
#include "mcc_generated_files/interrupt_manager.h"
#include "mcc_generated_files/tmr1.h"

#define update_times(wheel)\
    last_times[wheel] = times[wheel];\
    times[wheel] = TMR1_ReadTimer();    

uint16_t times[4] = {0};
uint16_t last_times[4] = {0};


int16_t power2duty(float power) {
    return (int16_t)(power*0x3ff);
}

float duty2power(int16_t duty) {
    return (float)(duty / 1023.0);
}

void FR_set_direction(uint8_t dir) {
    FR_DIRECTION_LAT = dir;
}

void FL_set_direction(uint8_t dir) {
    FL_DIRECTION_LAT = dir;
}

void RR_set_direction(uint8_t dir) {
    RR_DIRECTION_LAT = dir;
}

void RL_set_direction(uint8_t dir) {
    RL_DIRECTION_LAT = dir;
}

void FR_sensor(void) {
    if (!FR_SENSE2_GetValue()) {
        position[FRONT_RIGHT]++;
    } else {
        position[FRONT_RIGHT]--;
    }
    update_times(FRONT_RIGHT);
}

void FL_sensor(void) {
    if (!FL_SENSE2_GetValue()) {
        position[FRONT_LEFT]++;
    } else {
        position[FRONT_LEFT]--;
    }
    update_times(FRONT_LEFT);
}

void RR_sensor(void) {
    if (!RR_SENSE2_GetValue()) {
        position[REAR_RIGHT]++;
    } else {
        position[REAR_RIGHT]--;
    }
    update_times(REAR_RIGHT);
}

void RL_sensor(void) {
    if (!RL_SENSE2_GetValue()) {
        position[REAR_LEFT]++;
    } else {
        position[REAR_LEFT]--;
    }
    update_times(REAR_LEFT);
}


pid_t pids[4] = {0};

#define WHEEL_DATA(initials, name) \
    {\
        initials##_CURRENT,\
        false,\
        0,\
        &position[name],\
        0,\
        &current[name],\
        0,\
        1 << 4 + name,\
        name\
    }

wheel_t wheels[4] = {
    WHEEL_DATA(FR, FRONT_RIGHT),
    WHEEL_DATA(FL, FRONT_LEFT),
    WHEEL_DATA(RR, REAR_RIGHT),
    WHEEL_DATA(RL, REAR_LEFT),
};



void (*set_direction[4])(uint8_t) = {
    FR_set_direction,
    FL_set_direction,
    RR_set_direction,
    RL_set_direction
};

void (*set_pwm[4])(uint16_t) = {
    PWM5_LoadDutyValue,
    PWM1_LoadDutyValue,
    PWM2_LoadDutyValue,
    PWM4_LoadDutyValue
};


void wheels_init(void) {
    wheel_t* whl;
    uint8_t idx;
    IOCAF3_SetInterruptHandler(FL_sensor);
    IOCAF2_SetInterruptHandler(FR_sensor);
    IOCCF5_SetInterruptHandler(RL_sensor);
    IOCBF5_SetInterruptHandler(RR_sensor);
    FOR_ALL_WHEELS(whl) {
        idx = whl->index;
        pid_init(&pids[idx], 0, 0);
        pids[idx].pOnE=true;
        pid_setPoint(&pids[idx], 0);
    }
}

void wheels_reset_position(void) {
    wheel_t *whl;
    FOR_ALL_WHEELS(whl) {
        *whl->pos = 0;
        whl->last_pos = 0;
    }  
}

void wheel_set_power(wheel_t *whl, int16_t duty) {
    uint8_t idx = whl->index;
    if (duty < 0) {
        set_direction[idx](WHEEL_REVERSE);
    } else {
        set_direction[idx](WHEEL_FORWARD);
    }    
    set_pwm[idx]((uint16_t)duty);
    power[idx] = duty;
}

void wheel_set_speed(wheel_t *whl, float speed) {
    pid_setPoint(&pids[whl->index], speed);
}    

void wheel_set_target_pos(wheel_t *whl, int32_t target) {
    whl->target_pos = target;
}    

void wheel_soft_start(wheel_t *whl) {
    uint8_t idx = whl->index;
    pid_init(&pids[idx], (float)velocity[idx], duty2power(power[idx]));
}

void wheel_update_power(wheel_t *whl) {
    float output;
    int16_t duty;
    uint8_t idx = whl->index;
    if (whl->stopped) return;
    output = pid_compute(&pids[idx], (float)velocity[idx]);
    duty = power2duty(output);
    wheel_set_power(whl, duty);
}

void wheel_update_velocity(wheel_t *whl) {
    int32_t diff = *whl->pos - whl->last_pos;
    int32_t speed;
    uint8_t idx = whl->index;
    if (diff==0) {
        velocity[idx] = 0;
    } else if ((-30 < diff) && (diff < 30)) {
        uint16_t dt = times[idx] - last_times[idx];        
        if (dt==0) {
            velocity[idx] = diff * SAMPLE_FREQUENCY/SAMPLE_SKIP;
        } else {
            speed = 1000000/dt;
            if (diff<0) {
                velocity[idx] = -speed;
            } else {
                velocity[idx] = speed;
            }
        }
    } else {
        velocity[idx] = diff * SAMPLE_FREQUENCY/SAMPLE_SKIP;
    }
    whl->last_pos = *whl->pos;
}

void wheel_stop(wheel_t *whl) {
    uint8_t idx = whl->index;
    set_direction[idx](0);
    set_pwm[idx](0);
    whl->stopped = true;
    pid_init(&pids[idx], 0, 0);
}

void wheel_move_to(wheel_t *whl, int16_t max_speed) {
    if (*whl->pos < whl->target_pos) {
        wheel_set_speed(whl, max_speed);
    } else {
        wheel_set_speed(whl, -max_speed);
    }
}
void wheel_check_current(wheel_t *whl) {
    wheel_t *whl2;
    volatile int16_t local_current;
    volatile int16_t local_current_limit;
    
    INTERRUPT_GlobalInterruptDisable();
    local_current = *whl->current;
    local_current_limit = *current_limit;
    INTERRUPT_GlobalInterruptEnable();
    
    if (local_current > local_current_limit) {
        whl->over_current_count++;
        if (whl->over_current_count > 10) {
            FOR_ALL_WHEELS(whl2) {
                wheel_stop(whl2);
            }
            raise_alert(ALERT_OVERCURRENT | whl->bitmask);
        }
    } else {
        whl->over_current_count = 0;
    }
}
