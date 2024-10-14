import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QSpinBox, QProgressBar, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from tiled_map_generator.generator import TiledMapGenerator

class GeneratorThread(QThread):
    """
    A separate thread for running the map generation process.
    This allows the GUI to remain responsive during the generation.
    """
    progress_updated = pyqtSignal(int)
    generation_complete = pyqtSignal()

    def __init__(self, generator, width, height, output_path):
        super().__init__()
        self.generator = generator
        self.width = width
        self.height = height
        self.output_path = output_path

    def run(self):
        """
        The main process of map generation, run in a separate thread.
        """
        layers = []
        for i in range(3):  # Generate 3 layers
            population = self.generator.generate_initial_population(self.width, self.height, 100)
            for j in range(50):  # 50 generations
                population = self.generator.evolve_population(population)
                self.progress_updated.emit(i * 50 + j)
            best_individual = max(population, key=lambda x: x[0].fitness)
            layers.append(self.generator.generate_layer_from_tiles(best_individual, self.width, self.height))
        
        self.generator.save_to_tmx(layers, self.output_path)
        self.generation_complete.emit()

class MainWindow(QMainWindow):
    """
    The main window of the application.
    Contains all GUI elements and handles user interactions.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de Carte Tiled")
        self.setGeometry(100, 100, 400, 300)

        self.generator = TiledMapGenerator()

        self.init_ui()

    def init_ui(self):
        """
        Initialize all UI elements.
        """
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Button to select assets
        self.select_assets_button = QPushButton("Sélectionner les assets")
        self.select_assets_button.clicked.connect(self.select_assets)
        self.layout.addWidget(self.select_assets_button)

        # Label to show number of selected assets
        self.assets_label = QLabel("Aucun asset sélectionné")
        self.layout.addWidget(self.assets_label)

        # Width input
        self.width_layout = QHBoxLayout()
        self.width_label = QLabel("Largeur:")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 1000)
        self.width_spinbox.setValue(32)
        self.width_layout.addWidget(self.width_label)
        self.width_layout.addWidget(self.width_spinbox)
        self.layout.addLayout(self.width_layout)

        # Height input
        self.height_layout = QHBoxLayout()
        self.height_label = QLabel("Hauteur:")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 1000)
        self.height_spinbox.setValue(32)
        self.height_layout.addWidget(self.height_label)
        self.height_layout.addWidget(self.height_spinbox)
        self.layout.addLayout(self.height_layout)

        # Button to generate map
        self.generate_button = QPushButton("Générer la carte")
        self.generate_button.clicked.connect(self.generate_map)
        self.layout.addWidget(self.generate_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 150)
        self.layout.addWidget(self.progress_bar)

    def select_assets(self):
        """
        Open a file dialog to select asset images.
        """
        asset_paths, _ = QFileDialog.getOpenFileNames(self, "Sélectionner les assets", "", "Images (*.png *.jpg *.bmp)")
        if asset_paths:
            self.generator.set_assets(asset_paths)
            self.assets_label.setText(f"{len(asset_paths)} assets sélectionnés")

    def generate_map(self):
        """
        Start the map generation process.
        """
        if not self.generator.assets:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner des assets avant de générer la carte.")
            return

        width = self.width_spinbox.value()
        height = self.height_spinbox.value()

        output_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer la carte", "", "Tiled Map XML (*.tmx)")
        if output_path:
            self.generate_button.setEnabled(False)
            self.progress_bar.setValue(0)
            
            self.generator_thread = GeneratorThread(self.generator, width, height, output_path)
            self.generator_thread.progress_updated.connect(self.update_progress)
            self.generator_thread.generation_complete.connect(self.generation_complete)
            self.generator_thread.start()

    def update_progress(self, value):
        """
        Update the progress bar.
        """
        self.progress_bar.setValue(value)

    def generation_complete(self):
        """
        Handle the completion of map generation.
        """
        self.generate_button.setEnabled(True)
        QMessageBox.information(self, "Succès", "La carte a été générée avec succès !")

def run_app():
    """
    Run the application.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()