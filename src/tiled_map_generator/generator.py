import random
import xml.etree.ElementTree as ET
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt

class TiledMapGenerator:
    """
    Main class for generating tiled maps using genetic algorithms.
    This class handles the map generation process, including population management,
    fitness calculation, and map export.
    """

    def __init__(self):
        self.assets = []  # List to store the tile assets (QImage objects)
        self.compatibility_matrix = []  # Matrix to store compatibility scores between tiles

    def set_assets(self, asset_paths):
        """
        Load assets from the given file paths and initialize the compatibility matrix.
        :param asset_paths: List of file paths to the tile images
        """
        self.assets = [QImage(path) for path in asset_paths]
        self.initialize_compatibility_matrix()

    def initialize_compatibility_matrix(self):
        """
        Initialize the compatibility matrix with default values.
        This matrix determines how well different tiles fit together.
        """
        asset_count = len(self.assets)
        self.compatibility_matrix = [[0.5 for _ in range(asset_count)] for _ in range(asset_count)]
        # TODO: Define specific compatibility rules here

    def generate_map(self, width, height, output_path):
        """
        Generate a complete map with multiple layers and save it to a file.
        :param width: Width of the map in tiles
        :param height: Height of the map in tiles
        :param output_path: Path to save the generated map
        """
        layers = []
        for _ in range(3):  # Generate 3 layers
            population = self.generate_initial_population(width, height, 100)
            for _ in range(50):  # Evolve for 50 generations
                population = self.evolve_population(population)
            best_individual = max(population, key=lambda x: x[0].fitness)
            layers.append(self.generate_layer_from_tiles(best_individual, width, height))
        
        self.save_to_tmx(layers, output_path)

    def generate_initial_population(self, width, height, population_size):
        """
        Generate the initial population of random map layouts.
        :param width: Width of the map in tiles
        :param height: Height of the map in tiles
        :param population_size: Number of individuals in the population
        :return: List of individuals (each individual is a list of Tile objects)
        """
        return [[Tile(random.randint(0, len(self.assets) - 1)) for _ in range(width * height)] 
                for _ in range(population_size)]

    def evolve_population(self, population):
        """
        Evolve the population through one generation.
        :param population: Current population of map layouts
        :return: New population after evolution
        """
        for individual in population:
            self.calculate_fitness(individual)
        
        population.sort(key=lambda x: x[0].fitness, reverse=True)
        
        new_population = population[:10]  # Elitism: keep the best 10 individuals
        while len(new_population) < len(population):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)
        
        return new_population

    def crossover(self, parent1, parent2):
        """
        Perform crossover between two parent individuals to create a child.
        :param parent1: First parent individual
        :param parent2: Second parent individual
        :return: Child individual
        """
        crossover_point = random.randint(0, len(parent1) - 1)
        return parent1[:crossover_point] + parent2[crossover_point:]

    def mutate(self, individual):
        """
        Mutate an individual by randomly changing some of its tiles.
        :param individual: Individual to mutate
        """
        for tile in individual:
            if random.random() < 0.01:  # 1% chance of mutation
                tile.asset_index = random.randint(0, len(self.assets) - 1)

    def calculate_fitness(self, individual):
        """
        Calculate the fitness of an individual based on tile compatibility and distribution.
        :param individual: Individual to evaluate
        """
        width = int(len(individual) ** 0.5)
        fitness = 0
        for i, tile in enumerate(individual):
            x, y = i % width, i // width
            # Check compatibility with adjacent tiles
            if x > 0:
                fitness += self.compatibility_matrix[tile.asset_index][individual[i-1].asset_index]
            if x < width - 1:
                fitness += self.compatibility_matrix[tile.asset_index][individual[i+1].asset_index]
            if y > 0:
                fitness += self.compatibility_matrix[tile.asset_index][individual[i-width].asset_index]
            if y < width - 1:
                fitness += self.compatibility_matrix[tile.asset_index][individual[i+width].asset_index]
        
        # Calculate distribution score
        tile_counts = [0] * len(self.assets)
        for tile in individual:
            tile_counts[tile.asset_index] += 1
        
        distribution_score = sum(1 - abs(count / len(individual) - 1 / len(self.assets)) for count in tile_counts)
        
        # Combine compatibility and distribution scores
        fitness = fitness * 0.7 + distribution_score * 0.3
        individual[0].fitness = fitness

    def generate_layer_from_tiles(self, tiles, width, height):
        """
        Generate a QImage layer from a list of tiles.
        :param tiles: List of Tile objects
        :param width: Width of the map in tiles
        :param height: Height of the map in tiles
        :return: QImage representing the layer
        """
        layer = QImage(width * 32, height * 32, QImage.Format_ARGB32)
        layer.fill(Qt.transparent)
        for i, tile in enumerate(tiles):
            x, y = (i % width) * 32, (i // width) * 32
            layer.copy(self.assets[tile.asset_index], x, y, 32, 32)
        return layer

    def save_to_tmx(self, layers, output_path):
        """
        Save the generated map layers to a TMX (Tiled Map XML) file.
        :param layers: List of QImage layers
        :param output_path: Path to save the TMX file
        """
        root = ET.Element("map")
        root.set("version", "1.0")
        root.set("orientation", "orthogonal")
        root.set("width", str(layers[0].width() // 32))
        root.set("height", str(layers[0].height() // 32))
        root.set("tilewidth", "32")
        root.set("tileheight", "32")

        for i, layer in enumerate(layers):
            layer_elem = ET.SubElement(root, "layer")
            layer_elem.set("name", f"Layer {i+1}")
            layer_elem.set("width", str(layer.width() // 32))
            layer_elem.set("height", str(layer.height() // 32))

            data_elem = ET.SubElement(layer_elem, "data")
            data_elem.set("encoding", "csv")
            data = []
            for y in range(0, layer.height(), 32):
                for x in range(0, layer.width(), 32):
                    tile_id = random.randint(1, len(self.assets))
                    data.append(str(tile_id))
            data_elem.text = ",".join(data)

        tree = ET.ElementTree(root)
        tree.write(output_path)

class Tile:
    """
    Represents a single tile in the map.
    """
    def __init__(self, asset_index):
        self.asset_index = asset_index  # Index of the asset in the assets list
        self.fitness = 0  # Fitness score of this tile in its current position
