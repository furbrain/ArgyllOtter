#include <stdio.h>
#include "pid.h"
#define MANUAL 0
#define AUTOMATIC 1
 
float pid_compute(pid_t* ctx, float input)
{
    /*Compute all the working error variables*/
    float output, dP, dI, dD;
    float error = ctx->setPoint - input;
    ctx->ITerm+= (ctx->kI * error);
    if(ctx->ITerm > PID_MAX) ctx->ITerm = PID_MAX;
    else if(ctx->ITerm < PID_MIN) ctx->ITerm= PID_MIN;
    double dInput = (input - ctx->lastInput);
    
    /*Compute P-Term*/
    if(ctx->pOnE) dP = ctx->kP * error;
    else dP = -ctx->kP * (input-ctx->startInput); 
    dD = -ctx->kD *dInput;
    dI = ctx->ITerm;
    /*Compute Rest of PID Output*/
      output = dP+dD+dI;    
    if(output > PID_MAX) output = PID_MAX;
    else if(output < PID_MIN) output = PID_MIN;
    /* limit chang in output*/
    if(output < ctx->lastOutput-RATE_LIMIT) output = ctx->lastOutput-RATE_LIMIT;
    if(output > ctx->lastOutput+RATE_LIMIT) output = ctx->lastOutput+RATE_LIMIT;

    /*Remember some variables for next time*/
    ctx->lastInput = input;
    ctx->lastOutput = output;
    //printf("in: %5f dP: %5f dI: %5f dD: %5f out: %5f\n", input, dP, dI, dD, output);
    return output;
}
 
void pid_tune(pid_t *ctx, float Kp, float Ki, float Kd)
{
   ctx->kP = Kp;
   ctx->kI = Ki;
   ctx->kD = Kd;
}
 
void pid_setPoint(pid_t *ctx, float point) {
    ctx->setPoint = point;
}

 
void pid_init(pid_t *ctx, float input, float current_output)
{
   ctx->lastInput = input;
   ctx->lastOutput = current_output;
   ctx->startInput = input;
   ctx->ITerm = current_output;
   if(ctx->ITerm > PID_MAX) ctx->ITerm= PID_MAX;
   else if(ctx->ITerm< PID_MIN) ctx->ITerm= PID_MIN;
}