export {}

declare global {
  interface Window {
    gestor: {
      selectWorkspace: () => Promise<string | null>
      getBackendStatus: () => Promise<Record<string, unknown>>
      getAppVersion: () => Promise<string>
    }
  }
}
