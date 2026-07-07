import { defineStore } from 'pinia'

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
export interface Workspace { id: number; name: string; root_path: string; technical_dir_relative_path: string; db_relative_path: string; config_relative_path: string; app_version: string; is_active: boolean }

export const useWorkspaceStore = defineStore('workspace', {
  state: () => ({ backendStatus: null as Record<string, unknown> | null, appVersion: '', currentWorkspace: null as Workspace | null, error: '' }),
  actions: {
    async refreshBackendStatus() { this.backendStatus = await window.gestor.getBackendStatus() },
    async loadVersion() { this.appVersion = await window.gestor.getAppVersion() },
    async loadCurrentWorkspace() { const response = await fetch(`${API_BASE_URL}/workspace/current`); this.currentWorkspace = await response.json() },
    async selectAndInitWorkspace() {
      this.error = ''
      const rootPath = await window.gestor.selectWorkspace()
      if (!rootPath) return
      const response = await fetch(`${API_BASE_URL}/workspace/init`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ root_path: rootPath, profile_display_name: 'Usuario Local' }) })
      if (!response.ok) { this.error = await response.text(); return }
      const data = await response.json()
      this.currentWorkspace = data.workspace
      await this.refreshBackendStatus()
    }
  }
})
