# trayBat

![trayBat in system tray](/src/example.png)

**trayBat** is a small Windows application written in Python using the wxPython library. The program adds an icon to the system tray, allowing you to quickly and conveniently launch your `.bat` files directly from the tray.

## Key Features

- **Easy Access**: All your `.bat` files are always at hand via the system tray menu.
- **Flexible Configuration**: You can create and group your own `.bat` file list using a simple `JSON` format.
- **Easy Integration**: To add new scripts, simply place them in the `include` folder and update the corresponding `JSON` file.

## Installation and Usage

1. **Clone the repository**:
```
git clone https://github.com/free-gen/trayBat.git
cd trayBat
```

2. **Install dependencies**:
Make sure you have Python installed. <br/>Install the required dependencies with pip:
```
pip install wxPython
```

3. **Configure**:

Put your `.bat` files in the `include` folder.
Edit `config.json` to specify the paths to your `.bat` files and their grouping.
Example of `config.json` structure:

```
{
    "Group1": [
        {"name": "Script 1", "path": "include/script1.bat"},
        {"name": "Script 2", "path": "include/script2.bat"}
    ],
    "Group2": [
        {"name": "Script 3", "path": "include/script3.bat"}
    ]
}
```

4. **Running the application**:

Run **trayBat**:

```
python trayBat.py
```

The application will add an icon to the system tray, where you can select and run the desired `.bat` file.

## Requirements

Windows 7 or higher<br/>
Python 3.7 or higher<br/>
wxPython<br/>
Support and Contributions<br/><br/>

## License
This project is licensed under the MIT License.
