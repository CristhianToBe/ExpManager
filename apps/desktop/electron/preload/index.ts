import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('gestor', {
  selectWorkspace: () => ipcRenderer.invoke('gestor:select-workspace'),
  getBackendStatus: () => ipcRenderer.invoke('gestor:get-backend-status'),
  getAppVersion: () => ipcRenderer.invoke('gestor:get-app-version')
})
