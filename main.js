const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const loudness = require('loudness');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 280,
        height: 160,
        resizable: false,
        frame: false,
        transparent: true,
        alwaysOnTop: true,
        skipTaskbar: false,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        }
    });

    mainWindow.loadFile('index.html');
    
    // Allow dragging the window
    mainWindow.setMovable(true);
}

// IPC handlers for volume control
ipcMain.handle('set-volume', async (event, volume) => {
    try {
        await loudness.setVolume(Math.round(volume));
        return true;
    } catch (err) {
        console.error('Error setting volume:', err);
        return false;
    }
});

ipcMain.handle('get-volume', async () => {
    try {
        return await loudness.getVolume();
    } catch (err) {
        console.error('Error getting volume:', err);
        return 50;
    }
});

ipcMain.on('close-app', () => {
    app.quit();
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    app.quit();
});
