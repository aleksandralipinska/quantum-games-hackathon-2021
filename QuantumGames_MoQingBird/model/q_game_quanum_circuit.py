from qiskit import QuantumCircuit, QuantumRegister, measure
import numpy as np

qubits_number = 1
birdMovement1 = 0
birdMovement2 = 0



def quantum_computer(self):
    qr = QuantumRegister(qubits_number, 'Qubits')
    cr =  ClassicalRegister(qubits_number)
    qc = QuantumCircuit(qr)

    if event.type == pygame.KEYDOWN:
        if event.key == pyagme.H and game_active:
            qc.h(0)
            # split 1 bird
            birdMovement1 += gravity
            birdieRectangle.centery += birdMovement1
            screen.blit(birdieRectangle)

            #split 2 bird
            birdMovement2 += gravity
            birdieRectangle.centery += birdMovement2
            screen.blit(birdieRectangle)

            qc.measure(qr, cr)
            if qc.measure(qr[0], cr[0])== 0:
                screen.blit(rotatebird, (0, 0))


            #now we have to split the bird

            #for x gate
        if event.key == pygame.X and game_active:
            qc.x(0)
            qc.measure(qr[0], cr[0])
            if qc.measure(qr[0], cr[0]) == 0:
                gameOver == True
                scoreDisplay (gamestate == gameOver)

            else:
                gameActive == True
        if event.key == pygame.Z and game_active:
            qc.z(0)
            qc.measure(qr[0], cr[0])
            if qc.measure(qr[0], cr[0]) == 0:
                gameOver == True
                scoreDisplay (gamestate == gameOver)
            else
                gameActive == True

