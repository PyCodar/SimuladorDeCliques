# Importando os módulos necessários do PyQt5
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QLabel, QPushButton, QVBoxLayout, 
                             QGridLayout)
from PyQt5.QtCore import QTimer, Qt
import ctypes  # Importando ctypes para interagir com a API do Windows
import sys  # Importando o módulo sys para interagir com o interpretador Python

# Definindo constantes para os eventos do mouse
MOUSE_LEFTDOWN = 0x0002
MOUSE_LEFTUP = 0x0004

# Definindo a classe da janela principal
class Window(QMainWindow): 

    # Inicialização da classe Window
    def __init__(self): 
        super().__init__() 
        self.setWindowTitle("")  # Define o título da janela como vazio
        self.setGeometry(1000, 150, 240, 300)  # Define a geometria da janela
        self.setFixedSize(220, 180)  # Define o tamanho fixo da janela
        self.initUI()  # Chama o método para inicializar a interface
        self.show()  # Exibe a janela

    # Método para inicializar a interface
    def initUI(self): 
        central_widget = QWidget()  # Cria um widget central
        self.setCentralWidget(central_widget)  # Define o widget central na janela

        layout = QVBoxLayout(central_widget)  # Cria um layout vertical
        grid_layout = QGridLayout()  # Cria um layout de grade

        # Cria um rótulo para exibir o número de cliques
        self.label = QLabel("0 cliques", alignment=Qt.AlignCenter)
        self.label.setStyleSheet("border: 3px solid black; font: 15pt Times;")
        grid_layout.addWidget(self.label, 0, 0, 1, 2)  # Adiciona o rótulo ao layout de grade

        # Cria um segundo rótulo para exibir a taxa de cliques
        self.label2 = QLabel("20 cliques por segundo", alignment=Qt.AlignCenter)
        self.label2.setStyleSheet("font: 10pt Times;")
        grid_layout.addWidget(self.label2, 1, 0, 1, 2)  # Adiciona o segundo rótulo ao layout de grade

        # Cria um botão para iniciar os cliques
        start_button = QPushButton("Iniciar", clicked=self.start_action)
        grid_layout.addWidget(start_button, 2, 0)  # Adiciona o botão ao layout de grade

        # Cria um botão para pausar os cliques
        pause_button = QPushButton("Pausar", clicked=self.pause_action)
        grid_layout.addWidget(pause_button, 2, 1)  # Adiciona o botão ao layout de grade

        # Cria um botão para zerar os cliques
        reset_button = QPushButton("Zerar", clicked=self.reset_action)
        grid_layout.addWidget(reset_button, 3, 0, 1, 2)  # Adiciona o botão ao layout de grade

        layout.addLayout(grid_layout)  # Adiciona o layout de grade ao layout vertical

        self.count = 0  # Inicializa a contagem de cliques como zero
        self.start = False  # Define a variável de controle de início como False
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Mantém a janela no topo

        timer = QTimer(self)  # Cria um temporizador
        timer.timeout.connect(self.showTime)  # Conecta o temporizador ao método showTime
        timer.start(50)  # Inicia o temporizador com um intervalo de 50 milissegundos

    # Método para atualizar o número de cliques e simular o evento de clique do mouse
    def showTime(self): 
        if self.start:  # Verifica se o início está ativado
            self.count += 1  # Incrementa a contagem de cliques
            ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN)  # Simula o evento de clique do mouse (botão pressionado)
            ctypes.windll.user32.mouse_event(MOUSE_LEFTUP)  # Simula o evento de clique do mouse (botão solto)
            
        if self.count == 100000000000:  # Se a contagem atingir um limite alto
            self.start = False  # Desativa o início
            self.label.setText("Concluído!!!")  # Define o texto do rótulo como "Concluído!!!"

        if self.start:  # Se o início estiver ativado
            text = f"{self.count} cliques"  # Formata o texto com o número de cliques
            self.label.setText(text)  # Atualiza o texto do rótulo com a nova contagem

    # Método para iniciar a contagem de cliques
    def start_action(self): 
        self.start = True  # Ativa o início
        if self.count < 0:  # Se a contagem for menor que zero
            self.start = False  # Desativa o início
  
    # Método para pausar a contagem de cliques
    def pause_action(self): 
        self.start = False  # Desativa o início
  
    # Método para zerar a contagem de cliques
    def reset_action(self): 
        self.start = False  # Desativa o início
        self.count = 0  # Reseta a contagem de cliques
        self.label.setText("0 cliques")  # Atualiza o texto do rótulo para "0 cliques"

# Verifica se o código está sendo executado diretamente
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Cria uma instância da aplicação
    window = Window()  # Cria uma instância da janela principal
    sys.exit(app.exec())  # Executa o loop principal do aplicativo e aguarda o encerramento

