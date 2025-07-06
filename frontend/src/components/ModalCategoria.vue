<template>
  <v-dialog v-model="modalAberto" max-width="500px">
    <v-card>
      <v-card-title>
        <span class="text-h6">
          {{ categoria?.id ? 'Editar Categoria' : 'Nova Categoria' }}
        </span>
      </v-card-title>

      <v-card-text>
        <v-text-field
          v-model="form.nome"
          label="Nome"
          required
        />
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn color="blue darken-1" text @click="modalAberto = false">
          Cancelar
        </v-btn>
        <v-btn color="primary" @click="salvar">
          Salvar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'
import axios from '../services/api'

const props = defineProps({
  modelValue: Boolean,
  categoria: Object,
})
const emit = defineEmits(['update:modelValue', 'salvo'])

const modalAberto = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const form = reactive({
  nome: '',
})

watch(() => props.categoria, (val) => {
  form.nome = val?.nome || ''
})

const salvar = async () => {
  const payload = { nome: form.nome }
  if (props.categoria?.id) {
    await axios.put(`/api/core/categories/${props.categoria.id}/`, payload)
  } else {
    await axios.post('/api/core/categories/', payload)
  }
  emit('salvo')
  modalAberto.value = false
}
</script>
