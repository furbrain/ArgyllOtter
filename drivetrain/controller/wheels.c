#include "wheels.h"
#include "comms.h"
#include "mcc_generated_files/pin_manager.h"
#include "mcc_generated_files/adcc.h"
#include "mcc_generated_files/pwm1.h"
#include "mcc_generated_files/pwm2.h"
#include "mcc_generated_files/pwm4.h"
#include "mcc_generated_files/pwm5.h"

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
}

void FL_sensor(void) {
    if (!FL_SENSE2_GetValue()) {
        position[FRONT_LEFT]++;
    } else {
        position[FRONT_LEFT]--;
    }
}

void RR_sensor(void) {
    if (!RR_SENSE2_GetValue()) {
        position[REAR_RIGHT]++;
    } else {
        position[REAR_RIGHT]--;
    }
}

void RL_sensor(void) {
    if (!RL_SENSE2_GetValue()) {
        position[REAR_LEFT]++;
    } else {
        position[REAR_LEFT]--;
    }
}


pid_t pids[4] = {0};

wheel_t wheels[4] = {
    {
        FR_CURRENT,
        false,
        0,
        &position[FRONT_RIGHT],
        &velocity[FRONT_RIGHT],
        &pids[FRONT_RIGHT],
        FR_set_direction,
        PWM5_LoadDutyValue,
    },
    {
        FL_CURRENT,
        false,
        0,
        &position[FRONT_LEFT],
        &velocity[FRONT_LEFT],
        &pids[FRONT_LEFT],
        FL_set_direction,
        PWM1_LoadDutyValue,
    },
    {
        RR_CURRENT,
        false,
        0,
        &position[REAR_RIGHT],
        &velocity[REAR_RIGHT],
        &pids[REAR_RIGHT],
        RR_set_direction,
        PWM2_LoadDutyValue,
    },
    {
        RL_CURRENT,
        false,
        0,
        &position[REAR_LEFT],
        &velocity[REAR_LEFT],
        &pids[REAR_LEFT],
        RL_set_direction,
        PWM4_LoadDutyValue,
    }
};

bool within(int32_t desired, int32_t actual, int32_t range) {
    return (((desired + range) > actual) && ((desired - range) < actual));
}


void wheels_init(void) {
    wheel_t* whl;
    IOCAF3_SetInterruptHandler(FL_sensor);
    IOCAF2_SetInterruptHandler(FR_sensor);
    IOCCF5_SetInterruptHandler(RL_sensor);
    IOCBF5_SetInterruptHandler(RR_sensor);
    FOR_ALL_WHEELS(whl) {
        pid_init(whl->pid, 0, 0);
        pid_tune(whl->pid, 0.0015, 0.0005, 0.0005);
        whl->pid->pOnE=true;
        pid_setPoint(whl->pid, 0);
    }
}

void wheel_set_power(wheel_t *whl, float power) {
    int16_t duty = (int16_t)(power*0x3ff);
    if (power < 0.0) {
        whl->set_direction(WHEEL_REVERSE);
    } else {
        whl->set_direction(WHEEL_FORWARD);
    }    
    whl->set_pwm((uint16_t)duty);
}

void wheel_set_speed(wheel_t *whl, float speed) {
    pid_setPoint(whl->pid, speed);
}    

void wheel_update_power(wheel_t *whl) {
    float power;
    if (whl->stopped) return;
    power = pid_compute(whl->pid, (float)*(whl->velocity));
    wheel_set_power(whl, power);
}

void wheel_update_velocity(wheel_t *whl) {
    *whl->velocity = (*whl->pos - whl->last_pos) * SAMPLE_FREQUENCY/SAMPLE_SKIP;
    whl->last_pos = *whl->pos;
}

void wheel_stop(wheel_t *whl) {
    whl->set_direction(0);
    whl->set_pwm(0);
    whl->stopped = true;    
}

void wheel_move_to(wheel_t *whl, int32_t pos, int16_t max_speed) {
    if (whl->stopped) return;
    if (within(pos, *whl->pos, 10)) {
        // turn off motor
        wheel_stop(whl);
    } else if (within(pos, *whl->pos, 300)){
        if (*whl->pos < pos) {
            wheel_set_speed(whl, 200);
        } else {
            wheel_set_speed(whl, -200);
        }
    } else {
        if (*whl->pos < pos) {
            wheel_set_speed(whl, max_speed);
        } else {
            wheel_set_speed(whl, -max_speed);
        }        
    }
}
