// ✅ Dashboard.vue (controle das abas)
<template>
  <v-container>
    <v-tabs v-model="aba" background-color="grey lighten-4" grow>
      <v-tab>Resumo Financeiro</v-tab>
      <v-tab>Plano FIRE</v-tab>
    </v-tabs>

    <v-window v-model="aba">
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

<!-- styles opcionais -->
<style scoped>
.v-container {
  padding-top: 20px;
}
</style>
