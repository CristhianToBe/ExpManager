import { app, BrowserWindow, dialog, ipcMain } from 'electron'
import path from 'node:path'
import { spawn, ChildProcessWithoutNullStreams } from 'node:child_process'

const API_BASE_URL = process.env.GESTOR_API_URL ?? 'http://127.0.0.1:8000/api/v1'
let backendProcess: ChildProcessWithoutNullStreams | null = null

function createWindow(): void {
  const win = new BrowserWindow({ width: 1200, height: 800, webPreferences: { nodeIntegration: false, contextIsolation: true, preload: path.join(__dirname, '../preload/index.js') } })
  const devServerUrl = process.env.VITE_DEV_SERVER_URL
  if (devServerUrl) win.loadURL(devServerUrl)
  else win.loadFile(path.join(__dirname, '../renderer/index.html'))
}

function startBackend(): void {
  if (process.env.GESTOR_SKIP_BACKEND_START === '1') return
  backendProcess = spawn('python', ['-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'], { cwd: path.resolve(__dirname, '../../../../api'), env: { ...process.env }, shell: process.platform === 'win32' })
  backendProcess.stdout.on('data', data => console.log(`[api] ${data}`))
  backendProcess.stderr.on('data', data => console.error(`[api] ${data}`))
}

ipcMain.handle('gestor:select-workspace', async () => {
  const result = await dialog.showOpenDialog({ properties: ['openDirectory', 'createDirectory'] })
  return result.canceled || result.filePaths.length === 0 ? null : result.filePaths[0]
})
ipcMain.handle('gestor:get-backend-status', async () => {
  try { const response = await fetch(`${API_BASE_URL}/health`); return await response.json() }
  catch (error) { return { status: 'unavailable', error: error instanceof Error ? error.message : 'unknown' } }
})
ipcMain.handle('gestor:get-app-version', () => app.getVersion())

app.whenReady().then(() => { startBackend(); createWindow() })
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })
app.on('before-quit', () => { backendProcess?.kill() })
