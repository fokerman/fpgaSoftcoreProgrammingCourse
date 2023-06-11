; MIT License
; Copyright (c) 2023 David Alejandro Gonzalez Marquez
; ----------------------------------------------------------------------------
; -- OrgaSmallSystem ---------------------------------------------------------
; ----------------------------------------------------------------------------

; EXAMPLE OrgaSmall
; test_serial.asm: Interruption rutine, serial value generator

; Memory
; 0x00 = entry point
; ...
; 0xFB = stack base
; 0xFC = port Output
; 0xFD = port Input
; 0xFE = port Interrupt
; 0xFF = Interrupt rutine pointer

; ---------------------------------------------------------
; set STACK
SET R7, 0xFB

; Set Interrupt Rutine
SET R0, interrupt_handler
STR  [0xFF], R0

; Set Interrupt Flag
SET R0, 0x10
LOADF R0

; main
SET R0, 0x0
SET R1, 0x1

; loop
whileTrue:
    STR [0xFC], R1        ; out <- 0001
    CALL |R7|, sleep
    STR [0xFC], R0        ; out <- 0000
    SET R3, 0x7
    whileSerie:
        CALL |R7|, sleep
        LOAD R2, [current]
        AND R2, R1
        SHL R2, 1
        STR [0xFC], R2    ; out <- 00X0
        LOAD R2, [current]
        SHR R2, 1
        STR [current], R2    ; [data]  <- [data] >> 1
        SUB R3, R1
        JZ continuar
        JMP whileSerie
    continuar:
    LOAD R2, [data]
    STR [current], R2
JMP whileTrue

sleep:
    PUSH |R7|, R0
    PUSH |R7|, R1
    PUSH |R7|, R2
    PUSH |R7|, R3
    PUSH |R7|, R4
    SET R2, 10
    ciclo:
        CMP R2, R0
        JZ end_sleep
        SUB R2, R1
        JMP ciclo
    end_sleep:
    POP  |R7|, R4
    POP  |R7|, R3
    POP  |R7|, R2
    POP  |R7|, R1
    POP  |R7|, R0
    RET  |R7|

; ---------------------------------------------------------
current:
    DB 0x00
data:
    DB 0x00

; ---------------------------------------------------------
interrupt_handler:
    ; save registers
    PUSH |R7|, R0
    PUSH |R7|, R1
    PUSH |R7|, R2
    PUSH |R7|, R3
    PUSH |R7|, R4
    SET R0, 0x1
    SET R1, 0x2
    LOAD R3, [0xFE]
    CMP R3, R0
    JZ inc
    CMP R3, R1
    JZ dec
    end_interrupt:
    POP  |R7|, R4
    POP  |R7|, R3
    POP  |R7|, R2
    POP  |R7|, R1
    POP  |R7|, R0
    RETI |R7|
    
    inc:
        LOAD R3, [data]
        ADD R3, R0
        STR [data], R3
        JMP end_interrupt
    
    dec:
        LOAD R3, [data]
        SUB R3, R0
        STR [data], R3
        JMP end_interrupt