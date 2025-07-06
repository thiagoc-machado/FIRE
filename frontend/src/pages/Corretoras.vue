<template>
  <v-container>
    <v-row>
      <v-col cols="12" class="d-flex justify-end">
        <v-btn color="primary" @click="abrirModal()">Nova Corretora</v-btn>
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
            <tr v-for="broker in brokers" :key="broker.id">
              <td>{{ broker.nome }}</td>
              <td class="text-right">
                <v-btn icon @click="abrirModal(broker)">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon @click="deletar(broker.id)">
                  <v-icon color="red">mdi-delete</v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-col>
    </v-row>

    <ModalCorretora
      v-model="modalAberto"
      :corretora="corretoraSelecionada"
      @salvo="carregarCorretoras"
    />
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../services/api'
import ModalCorretora from '../components/ModalCorretora.vue'

const brokers = ref([])
const modalAberto = ref(false)
const corretoraSelecionada = ref(null)

const carregarCorretoras = async () => {
  const res = await axios.get('/api/core/brokers/')
  brokers.value = res.data
}

const abrirModal = (corretora = null) => {
  corretoraSelecionada.value = corretora
  modalAberto.value = true
}

const deletar = async (id) => {
  if (confirm('Deseja apagar esta corretora?')) {
    await axios.delete(`/api/core/brokers/${id}/`)
    carregarCorretoras()
  }
}

onMounted(carregarCorretoras)
</script>
