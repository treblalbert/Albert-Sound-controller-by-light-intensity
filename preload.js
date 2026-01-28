const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('volumeAPI', {
    setVolume: (volume) => ipcRenderer.invoke('set-volume', volume),
    getVolume: () => ipcRenderer.invoke('get-volume'),
    closeApp: () => ipcRenderer.send('close-app')
});
