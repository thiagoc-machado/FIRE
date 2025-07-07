<template>
    <v-container class="fill-height bg-light" fluid>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="8" md="4">
                <v-card class="pa-6" rounded="xl" elevation="3">
                    <v-card-title class="text-h5 font-weight-bold text-center">
                        🔐 Iniciar sesión
                    </v-card-title>

                    <v-card-text>
                        <v-form @submit.prevent="handleLogin">
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
                            />
                            <v-btn
                                type="submit"
                                color="primary"
                                block
                                class="mt-4"
                                size="large"
                                rounded
                            >
                                🚀 Entrar
                            </v-btn>
                        </v-form>

                        <div class="mt-4 text-center text-caption">
                            <RouterLink
                                to="/register"
                                class="text-decoration-none"
                            >
                                ¿No tienes cuenta? <strong>Regístrate</strong>
                            </RouterLink>
                        </div>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
    import { ref } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";

    const email = ref("");
    const password = ref("");
    const store = useStore();
    const router = useRouter();

    const handleLogin = async () => {
        try {
            await store.dispatch("auth/login", {
                email: email.value,
                password: password.value,
            });
            await store.dispatch("auth/fetchUser");
            router.push("/");
        } catch (error) {
            alert("Credenciales inválidas");
        }
    };
</script>

<style scoped>
    .bg-light {
        background-color: #f5f5f5;
    }
    .text-decoration-none {
        text-decoration: none;
    }
</style>
