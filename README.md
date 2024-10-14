# 🗺️ Tiled Map Generator

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A powerful GUI application for generating tiled maps using AI-driven algorithms. Create coherent and visually appealing tile-based maps for games or other applications with ease.

## 👨‍💻 Author

**Haritiana Randria** (Nogoezen)

## ✨ Features

- 🖥️ User-friendly graphical interface
- 🧠 AI-driven map generation using genetic algorithms
- 🎨 Support for multiple layers
- 📐 Customizable map dimensions
- 📊 Real-time progress tracking during map generation
- 💾 Export to Tiled Map Editor (TMX) format

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Nogoezen/tiled-map-generator.git
   ```

2. Navigate to the project directory:
   ```bash
   cd tiled-map-generator
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

1. Run the application:
   ```bash
   python -m tiled_map_generator
   ```

2. Use the interface to:
   - 🖼️ Select tile assets (PNG, JPG, or BMP images)
   - 🔢 Set the desired map width and height
   - 🔄 Generate the map
   - 💾 Save the generated map as a TMX file

## 🧠 How it works

The Tiled Map Generator uses a genetic algorithm approach to create coherent maps:

1. 🌱 It starts with a random population of map layouts.
2. 📊 Each generation, it evaluates the fitness of each layout based on tile compatibility and distribution.
3. 🏆 The best layouts are selected and combined to create the next generation.
4. 🔁 This process repeats for a set number of generations.
5. 🎉 The final result is the best map layout found by the algorithm.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Nogoezen/tiled-map-generator/issues) if you want to contribute.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by Haritiana Randria
</p>
