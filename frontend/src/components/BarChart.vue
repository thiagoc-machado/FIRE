<template>
  <Bar :data="chartData" :options="options" />
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

defineProps({
  chartData: Object
})

const options = {
  responsive: true,
  scales: {
    y: {
      beginAtZero: true
    }
  }
}
</script>

<style scoped>
canvas {
  max-height: 300px;
}
</style>
