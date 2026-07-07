<script setup lang="ts">
import { onMounted } from 'vue'
import { useWorkspaceStore } from './stores/workspace'
const workspace = useWorkspaceStore()
onMounted(async () => { await Promise.all([workspace.refreshBackendStatus(), workspace.loadVersion()]); await workspace.loadCurrentWorkspace() })
</script>

<template>
  <main class="min-h-screen bg-slate-950 text-slate-100">
    <section class="mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-8 py-12">
      <p class="mb-3 text-sm font-semibold uppercase tracking-[0.3em] text-cyan-300">Fase 1</p>
      <h1 class="text-4xl font-bold">Gestor de Expedientes</h1>
      <p class="mt-4 max-w-2xl text-lg text-slate-300">Base desktop local-first con Electron, Vue 3, FastAPI y workspace SQLite local.</p>
      <div class="mt-8 grid gap-4 md:grid-cols-3">
        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5"><h2 class="font-semibold text-slate-200">Backend</h2><pre class="mt-3 overflow-auto rounded bg-slate-950 p-3 text-xs text-cyan-100">{{ workspace.backendStatus }}</pre></article>
        <article class="rounded-2xl border border-slate-800 bg-slate-900 p-5 md:col-span-2">
          <h2 class="font-semibold text-slate-200">Workspace actual</h2>
          <div v-if="workspace.currentWorkspace" class="mt-3 text-sm text-slate-300"><p><strong>Nombre:</strong> {{ workspace.currentWorkspace.name }}</p><p><strong>Ruta:</strong> {{ workspace.currentWorkspace.root_path }}</p><p><strong>DB:</strong> {{ workspace.currentWorkspace.db_relative_path }}</p></div>
          <p v-else class="mt-3 text-sm text-slate-400">No hay workspace activo.</p>
        </article>
      </div>
      <div class="mt-8 flex items-center gap-4"><button class="rounded-xl bg-cyan-400 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-300" @click="workspace.selectAndInitWorkspace">Seleccionar workspace</button><span class="text-sm text-slate-400">App {{ workspace.appVersion || 'dev' }}</span></div>
      <p v-if="workspace.error" class="mt-4 rounded-lg border border-red-800 bg-red-950 p-3 text-red-200">{{ workspace.error }}</p>
    </section>
  </main>
</template>
