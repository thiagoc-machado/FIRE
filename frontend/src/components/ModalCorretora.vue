<template>
  <v-dialog v-model="model" max-width="500px">
    <v-card rounded="xl" elevation="3">
      <v-card-title class="text-h6 font-weight-bold">
        {{ corretora?.id ? '✏️ Editar Corretora' : '➕ Nova Corretora' }}
      </v-card-title>

      <v-card-text>
        <v-text-field
          v-model="nome"
          label="Nome"
          required
          outlined
          rounded
        />
      </v-card-text>

      <v-card-actions class="pb-4 px-4">
        <v-spacer />
        <v-btn color="grey" variant="text" @click="model = false" rounded>
          Cancelar
        </v-btn>
        <v-btn color="primary" @click="salvar" rounded>
          💾 Salvar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import axios from '../services/api'

const props = defineProps({ modelValue: Boolean, corretora: Object })
const emit = defineEmits(['update:modelValue', 'salvo'])

const model = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const nome = ref('')

watch(
  () => props.corretora,
  (c) => {
    nome.value = c?.nome || ''
  },
  { immediate: true }
)

const salvar = async () => {
  const payload = { nome: nome.value }
  if (props.corretora?.id) {
    await axios.put(`/api/core/brokers/${props.corretora.id}/`, payload)
  } else {
    await axios.post('/api/core/brokers/', payload)
  }
  emit('salvo')
  model.value = false
}
</script>
