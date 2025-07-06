// ✅ DashboardFinanceiro.vue
<template>
  <v-container>
    <v-card class="mb-4">
      <v-card-title class="text-h5">Resumo Financeiro</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="4">
            <v-sheet class="pa-4 text-center" color="blue lighten-5" rounded>
              <h3>Total Investido</h3>
              <p class="text-h6">{{ formatCurrency(total.investido) }}</p>
            </v-sheet>
          </v-col>
          <v-col cols="12" sm="4">
            <v-sheet class="pa-4 text-center" color="green lighten-5" rounded>
              <h3>Valorização</h3>
              <p class="text-h6">{{ formatCurrency(total.valorizacao) }}</p>
            </v-sheet>
          </v-col>
          <v-col cols="12" sm="4">
            <v-sheet class="pa-4 text-center" color="purple lighten-5" rounded>
              <h3>Dividendos</h3>
              <p class="text-h6">{{ formatCurrency(total.dividendos) }}</p>
            </v-sheet>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title class="text-h5">Distribuição por Categoria</v-card-title>
      <v-card-text>
        <PieChart :chart-data="chartData" />
      </v-card-text>
    </v-card>

    <v-card class="mt-4">
      <v-card-title class="text-h6">Distribuição por Corretora</v-card-title>
      <v-card-text>
        <PieChart v-if="corretoraData" :chart-data="corretoraData" />
      </v-card-text>
    </v-card>

    <v-card class="mt-4">
      <v-card-title class="text-h6">Distribuição por Ativo</v-card-title>
      <v-card-text>
        <PieChart v-if="ativoData" :chart-data="ativoData" />
      </v-card-text>
    </v-card>

    <v-card class="mt-4">
      <v-card-title class="text-h6">Dividendos Mensais</v-card-title>
      <v-card-text>
        <BarChart :chart-data="dividendosData" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../services/api'
import PieChart from '../components/PieChart.vue'
import BarChart from '../components/BarChart.vue'

const total = ref({ investido: 0, valorizacao: 0, dividendos: 0 })
const chartData = ref({ labels: [], datasets: [] })
const corretoraData = ref(null)
const ativoData = ref(null)
const dividendosData = ref({ labels: [], datasets: [] })

const formatCurrency = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'EUR'
  }).format(valor)
}

const fetchDashboard = async () => {
  const totalRes = await axios.get('/api/core/dashboard/total/')
  total.value = totalRes.data

  const categoriaRes = await axios.get('/api/core/dashboard/por-categoria/')
  chartData.value = {
    labels: categoriaRes.data.map(item => item.nome),
    datasets: [
      {
        label: 'Investido',
        backgroundColor: ['#3f51b5', '#e91e63', '#4caf50', '#ff9800'],
        data: categoriaRes.data.map(item => item.valor)
      }
    ]
  }
}

const fetchCorretora = async () => {
  const res = await axios.get('/api/core/dashboard/por-corretora/')
  corretoraData.value = {
    labels: res.data.map(i => i.nome),
    datasets: [
      {
        label: 'Investido',
        backgroundColor: ['#ff7043', '#26c6da', '#ab47bc'],
        data: res.data.map(i => i.valor)
      }
    ]
  }
}

const fetchAtivo = async () => {
  const res = await axios.get('/api/core/dashboard/por-ativo/')
  ativoData.value = {
    labels: res.data.map(i => i.codigo),
    datasets: [
      {
        label: 'Investido',
        backgroundColor: ['#4db6ac', '#ba68c8', '#ffd54f'],
        data: res.data.map(i => i.valor)
      }
    ]
  }
}

const fetchDividendos = async () => {
  const res = await axios.get('/api/core/dashboard/dividendos-mensais/')
  dividendosData.value = {
    labels: res.data.map(i => i.mes),
    datasets: [
      {
        label: 'Dividendos',
        backgroundColor: '#42a5f5',
        data: res.data.map(i => i.total)
      }
    ]
  }
}

onMounted(() => {
  fetchDashboard()
  fetchCorretora()
  fetchAtivo()
  fetchDividendos()
})
</script>
