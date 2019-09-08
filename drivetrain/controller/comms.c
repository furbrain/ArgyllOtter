#include "comms.h"
#include "mcc_generated_files/i2c1.h"
volatile uint8_t EEPROM_Buffer[BUFFER_SIZE] = {0};
volatile uint8_t EEPROM_Shadow[BUFFER_SIZE] = {0};

typedef enum
{
    SLAVE_NORMAL_DATA,
    SLAVE_DATA_ADDRESS,
} SLAVE_WRITE_DATA_TYPE;


void I2C1_StatusCallback(I2C1_SLAVE_DRIVER_STATUS i2c_bus_state)
{

    static uint8_t eepromAddress    = 0;
    static uint8_t writeStart    = 0;
    static uint8_t slaveWriteType   = SLAVE_NORMAL_DATA;


    switch (i2c_bus_state)
    {
        case I2C1_SLAVE_WRITE_REQUEST:
            // the master will be sending the eeprom address next
            slaveWriteType  = SLAVE_DATA_ADDRESS;
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
                    break;

            } // end switch(slaveWriteType)

            slaveWriteType  = SLAVE_NORMAL_DATA;
            break;

        case I2C1_SLAVE_READ_REQUEST:
            SSP1BUF = EEPROM_Buffer[eepromAddress++];
            if(sizeof(EEPROM_Buffer) <= eepromAddress)
            {
                eepromAddress = 0;    // wrap to start of eeprom page
            }
            break;

        case I2C1_SLAVE_READ_COMPLETED:
        default:;

    } // end switch(i2c_bus_state)

}

