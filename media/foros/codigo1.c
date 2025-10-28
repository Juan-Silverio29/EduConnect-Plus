#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>

// Función para retraso aleatorio
void random_delay() {
    usleep(rand() % 50000);
}

int main() {
    srand(time(NULL));

    // Proceso principal (Nivel 0)
    printf("[NIVEL 0] Proceso: %d | Padre: %d\n", getpid(), getppid());

    // Creación del proceso Nivel 1
    pid_t pid_n1 = fork();

    if (pid_n1 == 0) {  
        // Código del proceso Nivel 1
        random_delay();
        printf("[NIVEL 1] Proceso: %d | Padre: %d\n", getpid(), getppid());

        // Creación del proceso Nivel 2
        pid_t pid_n2 = fork();

        if (pid_n2 == 0) {  
            // Código del proceso Nivel 2
            random_delay();
            printf("[NIVEL 2] Proceso: %d | Padre: %d\n", getpid(), getppid());

            // PID del proceso Nivel 3 que tendrá descendencia
            pid_t pid_n3_con_hijos = 0;

            // Creación de 3 procesos Nivel 3
            for (int i = 0; i < 3; i++) {
                pid_t pid_n3 = fork();

                if (pid_n3 == 0) {  
                    // Código del proceso Nivel 3
                    random_delay();
                    printf("[NIVEL 3] Proceso: %d | Padre: %d\n", getpid(), getppid());

                    // Solo el primer Nivel 3 (i == 0) tendrá descendencia
                    if (i == 0) {
                        // Creación del proceso Nivel 4
                        pid_t pid_n4 = fork();

                        if (pid_n4 == 0) {  
                            // Código del proceso Nivel 4
                            random_delay();
                            printf("[NIVEL 4] Proceso: %d | Padre: %d\n", getpid(), getppid());

                            // Creación de 2 procesos Nivel 5
                            for (int j = 0; j < 2; j++) {
                                pid_t pid_n5 = fork();

                                if (pid_n5 == 0) {  
                                    // Código del proceso Nivel 5
                                    random_delay();
                                    printf("[NIVEL 5] Proceso: %d | Padre: %d\n", getpid(), getppid());

                                    // Nivel 5 termina primero
                                    sleep(4);
                                    printf("Finalizando Nivel 5: %d\n", getpid());
                                    exit(0);
                                }
                                else if (pid_n5 < 0) {
                                    perror("Error al crear proceso Nivel 5");
                                    exit(1);
                                }
                            }

                            // Nivel 4 espera a que terminen sus hijos (Nivel 5)
                            sleep(2);
                            for (int j = 0; j < 2; j++) {
                                int status;
                                wait(&status);
                            }
                            printf("Finalizando Nivel 4: %d\n", getpid());
                            exit(0);
                        }
                        else if (pid_n4 < 0) {
                            perror("Error al crear proceso Nivel 4");
                            exit(1);
                        }

                        // Nivel 3 con hijos espera a Nivel 4
                        sleep(2);
                        int status;
                        wait(&status);
                    } else {
                        // Nivel 3 sin hijos solo espera
                        sleep(2);
                    }

                    // Todos los Nivel 3 esperan a que N4 y N5 terminen
                    sleep(4);
                    printf("Finalizando Nivel 3: %d\n", getpid());
                    exit(0);
                }
                else if (pid_n3 < 0) {
                    perror("Error al crear proceso Nivel 3");
                    exit(1);
                }
                else if (i == 0) {
                    pid_n3_con_hijos = pid_n3;
                }
            }

            // Nivel 2 espera a que terminen los tres procesos Nivel 3
            sleep(2);
            for (int i = 0; i < 3; i++) {
                int status;
                wait(&status);
            }
            printf("Finalizando Nivel 2: %d\n", getpid());
            exit(0);
        }
        else if (pid_n2 < 0) {
            perror("Error al crear proceso Nivel 2");
            exit(1);
        }

        // Nivel 1 espera a Nivel 2
        sleep(2);
        int status;
        wait(&status);
        printf("Finalizando Nivel 1: %d\n", getpid());
        exit(0);
    }
    else if (pid_n1 < 0) {
        perror("Error al crear proceso Nivel 1");
        exit(1);
    }

    // Proceso padre (Nivel 0) espera a todos
    sleep(1);
    printf("\n--- TODOS LOS PROCESOS CREADOS. INICIANDO FINALIZACIÓN ORDENADA ---\n");

    int status;
    wait(&status);
    printf("Finalizando Nivel 0 (PADRE): %d\n", getpid());

    return 0;
}

