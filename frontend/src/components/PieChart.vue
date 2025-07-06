<template>
  <div>
    <Doughnut :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

defineProps({
  chartData: Object
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}
</script>

<style scoped>
div {
  height: 300px;
}
</style>
