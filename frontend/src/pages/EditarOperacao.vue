<template>
  <v-container>
    <v-card>
      <v-card-title class="text-h5">Editar operação</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="atualizarOperacao">
          <v-row>
            <v-col cols="12" sm="6">
              <v-select v-model="tipo" :items="['COMPRA', 'VENDA']" label="Tipo" required />
            </v-col>

            <v-col cols="12" sm="6">
              <v-select
                v-model="asset"
                :items="assets"
                item-title="codigo"
                item-value="id"
                label="Ativo"
                :loading="loading.assets"
                required
              />
            </v-col>

            <v-col cols="12" sm="6">
              <v-select
                v-model="broker"
                :items="brokers"
                item-title="nome"
                item-value="id"
                label="Corretora"
                :loading="loading.brokers"
                required
              />
            </v-col>

            <v-col cols="12" sm="6">
              <v-select
                v-model="category"
                :items="categories"
                item-title="nome"
                item-value="id"
                label="Categoria"
                :loading="loading.categories"
                required
              />
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field v-model="quantidade" label="Quantidade" type="number" required />
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field v-model="valor" label="Valor de compra" type="number" required />
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field v-model="data" label="Data" type="date" required />
            </v-col>

            <v-col cols="12">
              <v-btn type="submit" color="primary">Atualizar</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../services/api'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const tipo = ref('')
const asset = ref('')
const broker = ref('')
const category = ref('')
const quantidade = ref('')
const valor = ref('')
const data = ref('')

const assets = ref([])
const brokers = ref([])
const categories = ref([])
const loading = ref({ assets: false, brokers: false, categories: false })

const fetchOperacao = async () => {
  const { data: op } = await axios.get(`/api/core/operations/${route.params.id}/`)
  tipo.value = op.tipo
  asset.value = op.ativo
  broker.value = op.corretora
  category.value = op.categoria
  quantidade.value = op.quantidade
  valor.value = op.valor_compra
  data.value = op.data
}

const fetchDropdowns = async () => {
  loading.value.assets = loading.value.brokers = loading.value.categories = true
  const [a, b, c] = await Promise.all([
    axios.get('/api/core/assets/'),
    axios.get('/api/core/brokers/'),
    axios.get('/api/core/categories/')
  ])
  assets.value = a.data
  brokers.value = b.data
  categories.value = c.data
  loading.value.assets = loading.value.brokers = loading.value.categories = false
}

const atualizarOperacao = async () => {
  await axios.put(`/api/core/operations/${route.params.id}/`, {
    tipo: tipo.value.toUpperCase(),
    ativo: asset.value,
    corretora: broker.value,
    categoria: category.value,
    quantidade: quantidade.value,
    valor_compra: valor.value,
    data: data.value
  })
  router.push('/operacoes')
}

onMounted(() => {
  fetchOperacao()
  fetchDropdowns()
})
</script>
