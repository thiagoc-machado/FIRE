<template>
  <v-container class="fill-height bg-light" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-6" rounded="xl" elevation="3">
          <v-card-title class="text-h5 font-weight-bold text-center">
            📝 Crear cuenta
          </v-card-title>

          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="email"
                label="Correo electrónico"
                type="email"
                outlined
                rounded
                required
                class="mb-3"
              />
              <v-text-field
                v-model="password"
                label="Contraseña"
                type="password"
                outlined
                rounded
                required
                class="mb-3"
              />
              <v-text-field
                v-model="re_password"
                label="Repetir contraseña"
                type="password"
                outlined
                rounded
                required
              />
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-4"
                size="large"
                rounded
              >
                🧾 Registrar
              </v-btn>
            </v-form>

            <div class="mt-4 text-center text-caption">
              <RouterLink to="/login" class="text-decoration-none">
                ¿Ya tienes cuenta? <strong>Inicia sesión</strong>
              </RouterLink>
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

<style scoped>
.bg-light {
  background-color: #f5f5f5;
}
.text-decoration-none {
  text-decoration: none;
}
</style>