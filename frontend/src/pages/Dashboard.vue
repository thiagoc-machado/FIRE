<template>
  <v-container fluid class="dashboard-container">
    <!-- Abas -->
    <v-tabs
      v-model="aba"
      grow
      class="fire-tabs"
      color="primary"
      bg-color="white"
      slider-color="accent"
      height="50"
    >
      <v-tab>
        <v-icon start>mdi-currency-usd</v-icon>
        Resumo Financeiro
      </v-tab>
      <v-tab>
        <v-icon start>mdi-fire</v-icon>
        Plano FIRE
      </v-tab>
    </v-tabs>

    <!-- Conteúdo das abas -->
    <v-window v-model="aba" class="pa-4">
      <v-window-item>
        <DashboardFinanceiro />
      </v-window-item>
      <v-window-item>
        <DashboardFIRE />
      </v-window-item>
    </v-window>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import DashboardFinanceiro from './DashboardFinanceiro.vue'
import DashboardFIRE from './DashboardFIRE.vue'

const aba = ref(0)
</script>

<style scoped>
.dashboard-container {
  background-color: #f5f5f5;
  min-height: 100vh;
  padding-top: 16px;
}

/* Estilo suave para as abas */
.fire-tabs {
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
</style>
