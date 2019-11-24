/* 
 * File:   pid.h
 * Author: phil
 *
 * Created on September 8, 2019, 12:20 PM
 */

#ifndef PID_H
#define	PID_H

#ifdef	__cplusplus
extern "C" {
#endif
#include <stdint.h>
#include <stdbool.h>
#include <float.h>
    
#define PID_MIN -1.0
#define PID_MAX 1.0 
#define RATE_LIMIT 0.15 //1.0 = disabled
    
typedef struct {
    float kP, kI, kD;
    float setPoint, lastInput, ITerm;
    float startInput, lastOutput;
    bool pOnE;
} pid_t;

void pid_init(pid_t *ctx, float input, float current_output);
float pid_compute(pid_t *ctx, float input);
void pid_setPoint(pid_t *ctx, float point);
void pid_tune(pid_t *ctx, float Kp, float Ki, float Kd);

#ifdef	__cplusplus
}
#endif

#endif	/* PID_H */

