#include "main.h"
#include <string.h> // For strcmp

void Handler(int signo) {
    // System Exit
    printf("\r\nHandler: Motor Stop\r\n");
    Motor_Stop(MOTORA);
    Motor_Stop(MOTORB);
    DEV_ModuleExit();

    exit(0);
}
/*
void forward() {
    printf("Moving Forward\n");
    Motor_Run(MOTORA, FORWARD, 50);
    Motor_Run(MOTORB, FORWARD, 50);
}
*/

void right() {
   //Motor_Run(MOTORA, BACKWARD, 50);
   Motor_Run(MOTORB, FORWARD, 50);
}
void left() {
    Motor_Run(MOTORA, FORWARD, 50);
    //Motor_Run(MOTORB, FORWARD, 50);
}
void forward() {
    Motor_Run(MOTORA, BACKWARD, 50);
    Motor_Run(MOTORB, FORWARD, 50);
}

void backward() {
    Motor_Run(MOTORA, FORWARD, 50);
    Motor_Run(MOTORB, BACKWARD, 50);
}

void stop() {
    printf("Stopping\n");
    Motor_Stop(MOTORA);
    Motor_Stop(MOTORB);
}

int main(int argc, char *argv[]) {
    // 1. System Initialization
    if (DEV_ModuleInit())
        exit(0);

    // 2. Motor Initialization
    Motor_Init();

    // Exception handling: ctrl + c
    signal(SIGINT, Handler);

    // Check for command-line arguments
    if (argc < 2) {
        printf("Usage: %s <command>\n", argv[0]);
        printf("Commands: forward, backward, left, right, stop\n");
        DEV_ModuleExit();
        return 1;
    }

    // Parse the command
    if (strcmp(argv[1], "forward") == 0) {
        forward();
    } else if (strcmp(argv[1], "backward") == 0) {
        backward();
    } else if (strcmp(argv[1], "left") == 0) {
        left();
    } else if (strcmp(argv[1], "right") == 0) {
        right();
    } else if (strcmp(argv[1], "stop") == 0) {
        stop();
    } else {
        printf("Invalid command: %s\n", argv[1]);
        printf("Commands: forward, backward, left, right, stop\n");
    }

    // 3. System Exit
    DEV_ModuleExit();
    return 0;
}
