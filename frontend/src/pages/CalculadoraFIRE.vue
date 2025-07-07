<template>
  <v-container fluid class="pa-4 bg-light">
    <!-- 🔢 Formulário da calculadora -->
    <v-card class="mb-6" rounded="xl" elevation="2">
      <v-card-title class="text-h5 font-weight-bold">
        🧮 Calculadora FIRE
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="calcular">
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="form.meta_fire_total"
                label="Meta FIRE Total (€)"
                type="number"
                outlined
                rounded
                required
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="form.aporte_mensal"
                label="Aporte Mensal (€)"
                type="number"
                outlined
                rounded
                required
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="form.patrimonio_atual"
                label="Patrimônio Atual (€)"
                type="number"
                outlined
                rounded
                required
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="form.rentabilidade_anual"
                label="Rentabilidade Anual (%)"
                type="number"
                outlined
                rounded
                required
              />
            </v-col>
          </v-row>
          <v-btn color="primary" class="mt-4" type="submit" size="large" rounded>
            🔍 Calcular
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- 📊 Resultado -->
    <v-card v-if="resultado" rounded="xl" elevation="2">
      <v-card-title class="text-h6 font-weight-bold">📊 Resultado</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6">
            <p><strong>Meses estimados:</strong> {{ resultado.meses_estimados }}</p>
          </v-col>
          <v-col cols="12" sm="6">
            <p><strong>Data prevista:</strong> {{ resultado.data_prevista }}</p>
          </v-col>
        </v-row>

        <LineChart :chart-data="grafico" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from '../services/api'
import LineChart from '../components/LineChart.vue'

const form = ref({
  meta_fire_total: 750000,
  aporte_mensal: 1000,
  patrimonio_atual: 50000,
  rentabilidade_anual: 6
})

const resultado = ref(null)
const grafico = ref({ labels: [], datasets: [] })

const calcular = async () => {
  const res = await axios.post('/api/core/dashboard/calculadora-fire/', form.value)
  resultado.value = res.data

  grafico.value = {
    labels: res.data.grafico.labels,
    datasets: [
      {
        label: 'Projeção Patrimonial',
        data: res.data.grafico.valores,
        borderColor: '#4caf50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        fill: true,
        tension: 0.3
      }
    ]
  }
}
</script>

<style scoped>
.bg-light {
  background-color: #f9f9f9;
}
</style>
