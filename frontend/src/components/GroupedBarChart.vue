<template>
  <div>
    <Bar :data="chartData" :options="options" />
  </div>
</template>

<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  chartData: Object
})

const options = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: value => `€${value.toLocaleString('pt-BR')}`
      }
    }
  },
  plugins: {
    legend: { position: 'top' }
  }
}
</script>

<style scoped>
div {
  height: 300px;
}
</style>
