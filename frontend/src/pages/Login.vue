<template>
  <v-container class="fill-height" fluid>
    <h1>Login template</h1>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title class="text-h5">Iniciar sesión</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field v-model="email" label="Correo electrónico" type="email" required />
              <v-text-field v-model="password" label="Contraseña" type="password" required />
              <v-btn type="submit" color="primary" block>Entrar</v-btn>
            </v-form>
            <div class="mt-3 text-center">
              <RouterLink to="/register">¿No tienes cuenta? Regístrate</RouterLink>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const store = useStore()
const router = useRouter()

const handleLogin = async () => {
  try {
    await store.dispatch('auth/login', {
      email: email.value,
      password: password.value
    })
    await store.dispatch('auth/fetchUser')
    router.push('/')
  } catch (error) {
    alert('Credenciales inválidas')
  }
}
</script>
