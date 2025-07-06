<template>
  <v-container class="fill-height" fluid>
    <h1>Register template</h1>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title class="text-h5">Crear cuenta</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field v-model="email" label="Correo electrónico" type="email" required />
              <v-text-field v-model="password" label="Contraseña" type="password" required />
              <v-text-field v-model="re_password" label="Repetir contraseña" type="password" required />
              <v-btn type="submit" color="primary" block>Registrar</v-btn>
            </v-form>
            <div class="mt-3 text-center">
              <RouterLink to="/login">¿Ya tienes cuenta? Inicia sesión</RouterLink>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from '../services/api'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const re_password = ref('')
const router = useRouter()

const handleRegister = async () => {
  try {
    await axios.post('/api/users/register/', {
      email: email.value,
      username: email.value,
      password: password.value,
      re_password: re_password.value
    })
    router.push('/login')
  } catch (error) {
    alert('Error al registrar usuario')
  }
}
</script>
