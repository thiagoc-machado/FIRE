<template>
  <div v-if="hasData">
    <Line :data="chartData" :options="options" />
  </div>
  <div v-else class="text-center py-4">Sem dados disponíveis.</div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
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

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  }
})

const hasData = computed(() =>
  props.chartData &&
  Array.isArray(props.chartData.labels) &&
  props.chartData.labels.length > 0 &&
  Array.isArray(props.chartData.datasets) &&
  props.chartData.datasets.length > 0 &&
  props.chartData.datasets.every(ds => Array.isArray(ds.data))
)

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
