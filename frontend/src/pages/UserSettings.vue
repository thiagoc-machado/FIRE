<template>
  <v-container>
    <v-card class="mb-4">
      <v-card-title class="text-h5">🔐 Dados do Usuário</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field v-model="user.username" label="Nome de usuário" readonly />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field v-model="user.email" label="Email" readonly />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title class="text-h5">⚙️ Configurações e Metas FIRE</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="salvar">
          <v-row>
            <v-col cols="12" sm="4">
              <v-select
                v-model="settings.moeda_padrao"
                :items="['EUR', 'USD', 'BRL']"
                label="Moeda Padrão"
              />
            </v-col>

            <v-col cols="12" sm="4">
              <v-select
                v-model="settings.idioma"
                :items="['pt', 'en', 'es']"
                label="Idioma"
              />
            </v-col>

            <v-col cols="12" sm="4">
              <v-text-field
                v-model="settings.frequencia_atualizacao"
                label="Atualização (em horas)"
                type="number"
              />
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                v-model="settings.meta_fire_total"
                label="Meta FIRE Total (€)"
                type="number"
              />
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                v-model="settings.renda_fire_desejada"
                label="Renda FIRE desejada (€/mês)"
                type="number"
              />
            </v-col>

            <v-col cols="12">
              <v-btn type="submit" color="primary">Salvar alterações</v-btn>
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

const user = ref({ username: '', email: '' })
const settings = ref({
  moeda_padrao: 'EUR',
  idioma: 'pt',
  frequencia_atualizacao: 24,
  meta_fire_total: 600000,
  renda_fire_desejada: 2000
})

const fetchDados = async () => {
  const [userRes, settingsRes] = await Promise.all([
    axios.get('/api/auth/users/me/'),
    axios.get('/api/users/settings/')
  ])
  user.value = userRes.data
  settings.value = settingsRes.data
}

const salvar = async () => {
  await axios.put('/api/users/settings/', settings.value)
  alert('Configurações salvas com sucesso!')
}

onMounted(fetchDados)
</script>
