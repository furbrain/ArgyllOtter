#include <string.h>
#include <math.h>
#include <stdbool.h>
#include "comms.h"
#include "mcc_generated_files/i2c1.h"
#include "mcc_generated_files/memory.h"
#include "mcc_generated_files/pin_manager.h"
volatile uint8_t EEPROM_Buffer[BUFFER_SIZE] = {0};
volatile uint8_t EEPROM_Shadow[BUFFER_SIZE] = {0};
volatile command_t* const command = (command_t*)&EEPROM_Shadow[0x0];
volatile int32_t* const position = (int32_t*)&EEPROM_Shadow[0x10];
volatile int16_t* const velocity = (int16_t*)&EEPROM_Shadow[0x20];
volatile constants_t* const constants = (constants_t*)&EEPROM_Shadow[0x30];
volatile int16_t* const current = (int16_t*)&EEPROM_Shadow[0x40];
volatile int16_t* const current_limit = (int16_t*)&EEPROM_Shadow[0x48];
volatile int16_t* const batt_voltage = (int16_t*)&EEPROM_Shadow[0x50];
volatile int16_t* const peripheral_voltage = (int16_t*)&EEPROM_Shadow[0x54];
volatile uint8_t* const alert_status = &EEPROM_Shadow[ALERT_ADDRESS];


const constants_t constants_default = {0.0015, 0.0005, 0.0005, (WHEEL_DIAMETER*2*M_PI/374.0)};

volatile bool new_command = false;

typedef enum
{
    SLAVE_NORMAL_DATA,
    SLAVE_DATA_ADDRESS,
} SLAVE_WRITE_DATA_TYPE;

void memcpyBuffer2Shadow(uint8_t offset, uint8_t count) {
    memcpy(&EEPROM_Shadow[offset], &EEPROM_Buffer[offset], count);    
}

void memcpyShadow2Buffer(uint8_t offset, uint8_t count) {
    memcpy(&EEPROM_Buffer[offset], &EEPROM_Shadow[offset], count);        
}

void memcpy2ee(uint16_t dest, const uint8_t * src, uint8_t count) {
    while(count--) {
        DATAEE_WriteByte(dest++, *(src++));
    }
}

void eecpy2mem(uint8_t *dest, uint16_t src, uint8_t count) {
    while (count--) {
        *(dest++) = DATAEE_ReadByte(src++);
    }
}


void comms_init(void) {
//    if (DATAEE_ReadByte(0)==0xFF) {
//        //first run
//        *constants = constants_default;
//        memcpy2ee(0, (const char*)constants, sizeof(constants_t));
//    } else {
//        eecpy2mem(constants, 0, sizeof(constants_t));
//    }
    *current_limit = 2000; 
}

void I2C1_StatusCallback(I2C1_SLAVE_DRIVER_STATUS i2c_bus_state)
{

    static uint8_t eepromAddress    = 0;
    static uint8_t writeStart    = 0;
    static uint8_t slaveWriteType   = SLAVE_NORMAL_DATA;
    static bool dataToSave = false;


    switch (i2c_bus_state)
    {
        case I2C1_SLAVE_WRITE_REQUEST:
            // the master will be sending the eeprom address next
            slaveWriteType  = SLAVE_DATA_ADDRESS;
            dataToSave = false;
            break;


        case I2C1_SLAVE_WRITE_COMPLETED:

            switch(slaveWriteType)
            {
                case SLAVE_DATA_ADDRESS:
                    eepromAddress   = I2C1_slaveWriteData;
                    writeStart = eepromAddress;
                    break;


                case SLAVE_NORMAL_DATA:
                default:
                    // the master has written data to store in the eeprom
                    EEPROM_Buffer[eepromAddress++]    = I2C1_slaveWriteData;
                    if(sizeof(EEPROM_Buffer) <= eepromAddress)
                    {
                        eepromAddress = 0;    // wrap to start of eeprom page
                    }
                    dataToSave = true;
                    break;

            } // end switch(slaveWriteType)

            slaveWriteType  = SLAVE_NORMAL_DATA;
            break;

        case I2C1_SLAVE_READ_REQUEST:
            if (eepromAddress % 0x10==0) { //copy row from Shadow into Main Buffer
                memcpyShadow2Buffer(eepromAddress, 0x10);
            }
            if (eepromAddress == ALERT_ADDRESS) {
                ALERT_SetLow();
            }
            SSP1BUF = EEPROM_Buffer[eepromAddress++];
            if(sizeof(EEPROM_Buffer) <= eepromAddress)
            {
                eepromAddress = 0;    // wrap to start of eeprom page
            }
            dataToSave = false;
            break;

        case I2C1_SLAVE_READ_COMPLETED:
            break;
        case I2C1_SLAVE_STOP:
            if (dataToSave) {
                if (writeStart < eepromAddress) {
                    if (writeStart==0) {
                        new_command=true;
                    }
                    memcpyBuffer2Shadow(writeStart, eepromAddress-writeStart);
                } else if (writeStart > eepromAddress) {
                    memcpyBuffer2Shadow(0, eepromAddress);
                    memcpyBuffer2Shadow(writeStart, BUFFER_SIZE-writeStart);
                }
                if (writeStart==0x30) {
                    //constants written so update NVRAM
                    memcpy2ee(0, (const char*)&EEPROM_Buffer[0x30], sizeof(constants_t));
                }
                dataToSave = false;
            }
            break;
        default:
            break;
    } // end switch(i2c_bus_state)
}

void raise_alert(ALERT_STATUS status) {
    if (status == ALERT_NOALERT) {
        *alert_status = 0;
        ALERT_SetLow();
    } else {
        *alert_status |= status;
        ALERT_SetHigh();
    }
}