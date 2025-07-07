<template>
  <v-container fluid class="bg-light pa-4">
    <!-- 🔷 Resumo financeiro -->
    <v-row dense>
      <v-col cols="12" sm="4">
        <v-card class="pa-4 gradient-blue text-center" rounded="xl" elevation="2">
          <v-icon size="30" color="white">mdi-cash-multiple</v-icon>
          <h4 class="text-white mt-2">Total Investido</h4>
          <p class="text-h6 text-white font-weight-bold">
            {{ formatCurrency(total.investido) }}
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="pa-4 gradient-green text-center" rounded="xl" elevation="2">
          <v-icon size="30" color="white">mdi-trending-up</v-icon>
          <h4 class="text-white mt-2">Valorização</h4>
          <p class="text-h6 text-white font-weight-bold">
            {{ formatCurrency(total.valorizacao) }}
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="pa-4 gradient-purple text-center" rounded="xl" elevation="2">
          <v-icon size="30" color="white">mdi-cash-refund</v-icon>
          <h4 class="text-white mt-2">Dividendos</h4>
          <p class="text-h6 text-white font-weight-bold">
            {{ formatCurrency(total.dividendos) }}
          </p>
        </v-card>
      </v-col>
    </v-row>

    <!-- 🟠 Gráficos -->
    <v-card class="mt-6" rounded="xl" elevation="1">
      <v-card-title class="text-subtitle-1 font-weight-bold">Distribuição por Categoria</v-card-title>
      <v-card-text>
        <PieChart :chart-data="chartData" />
      </v-card-text>
    </v-card>

    <v-card class="mt-4" rounded="xl" elevation="1">
      <v-card-title class="text-subtitle-1 font-weight-bold">Distribuição por Corretora</v-card-title>
      <v-card-text>
        <PieChart v-if="corretoraData" :chart-data="corretoraData" />
      </v-card-text>
    </v-card>

    <v-card class="mt-4" rounded="xl" elevation="1">
      <v-card-title class="text-subtitle-1 font-weight-bold">Distribuição por Ativo</v-card-title>
      <v-card-text>
        <PieChart v-if="ativoData" :chart-data="ativoData" />
      </v-card-text>
    </v-card>

    <v-card class="mt-4 mb-8" rounded="xl" elevation="1">
      <v-card-title class="text-subtitle-1 font-weight-bold">Dividendos Mensais</v-card-title>
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

<style scoped>
.bg-light {
  background-color: #f5f5f5;
}

.gradient-blue {
  background: linear-gradient(135deg, #2196f3, #42a5f5);
}
.gradient-green {
  background: linear-gradient(135deg, #43a047, #66bb6a);
}
.gradient-purple {
  background: linear-gradient(135deg, #7e57c2, #ab47bc);
}
</style>
