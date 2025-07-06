<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="d-flex justify-end">
        <v-btn color="primary" @click="abrirModal()">Nova Categoria</v-btn>
      </v-col>
      <v-col cols="12">
        <v-table>
          <thead>
            <tr>
              <th>Nome</th>
              <th class="text-right">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="categoria in categories" :key="categoria.id">
              <td>{{ categoria.nome }}</td>
              <td class="text-right">
                <v-btn icon @click="abrirModal(categoria)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deletar(categoria.id)">
                  <v-icon color="red">mdi-delete</v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>

    <ModalCategoria
      v-model="modalAberto"
      :categoria="categoriaSelecionada"
      @salvo="carregarCategorias"
    />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../services/api'
import ModalCategoria from '../components/ModalCategoria.vue'

const categories = ref([])
const modalAberto = ref(false)
const categoriaSelecionada = ref(null)

const carregarCategorias = async () => {
  const res = await axios.get('/api/core/categories/')
  categories.value = res.data
}

const abrirModal = (categoria = null) => {
  categoriaSelecionada.value = categoria
  modalAberto.value = true
}

const deletar = async (id) => {
  if (confirm('Deseja apagar esta categoria?')) {
    await axios.delete(`/api/core/categories/${id}/`)
    carregarCategorias()
  }
}

onMounted(carregarCategorias)
</script>
