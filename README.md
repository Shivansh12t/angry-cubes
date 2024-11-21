# Angry Cubes

## **Updates**
### **v0.1**
- Added a `BirdCube` projectile with customizable properties like color and velocity reduction on collision.
- Fixed collision logic for brown blocks to reflect properly and prevent phasing.
- Improved the game loop to allow multiple shots and smoother slingshot functionality.

### **v0.0**
- Initial release with basic gameplay:
  - Map generation (`map_generator.py`) with ice-blue and brown blocks.
  - Map loading and playing functionality.
  - Basic slingshot mechanic with cubes.

---

## **How to Play**

### **Setup Instructions**
1. **Clone or download this repository**:
   ```bash
   git clone https://github.com/Shivansh12t/angry-cubes.git
   cd angry-cubes
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   Start the main menu by running:
   ```bash
   python main.py
   ```

---

### **Gameplay Instructions**

#### **Main Menu**:
1. **Load Map**: Select a pre-generated map from the `maps` folder to play.
2. **Create Map**: Design your own map using `map_generator.py` and save it for later use.

#### **Game Controls**:
- **Drag and Release**: Use the left mouse button to drag the `BirdCube` from the slingshot and release to launch it.
- **Objective**: Break all ice-blue blocks to win. Brown blocks act as indestructible obstacles.

---

## **Requirements**
The required Python packages are listed in the `requirements.txt` file. These include:
- **pygame**: For rendering and game mechanics.
- **json**: For saving and loading maps.

Install them using:
```bash
pip install -r requirements.txt
```

---

## **Folder Structure**
```
angry-cubes/
├── main.py                # Main game file
├── map_generator.py       # Map creation tool
├── game.py                # Game logic
├── maps/                  # Folder to store saved maps
├── requirements.txt       # List of dependencies
└── README.md              # This file
```

---

## **Future Updates**
- Add more block types with unique properties.
- Implement scoring and level progression.
- Introduce power-ups and special projectiles.
