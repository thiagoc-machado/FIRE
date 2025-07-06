<template>
  <div>
    <Line :data="chartData" :options="options" />
  </div>
</template>

<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

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
