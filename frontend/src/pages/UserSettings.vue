<template>
    <v-container fluid class="pa-4 bg-light">
        <!-- 👤 Dados do Usuário -->
        <v-card class="mb-6" rounded="xl" elevation="2">
            <v-card-title class="text-h5 font-weight-bold"
                >🔐 Dados do Usuário</v-card-title
            >
            <v-card-text>
                <v-row dense>
                    <v-col cols="12" sm="6">
                        <v-text-field
                            v-model="user.username"
                            label="Nome de usuário"
                            readonly
                            outlined
                            rounded
                        />
                    </v-col>
                    <v-col cols="12" sm="6">
                        <v-text-field
                            v-model="user.email"
                            label="Email"
                            readonly
                            outlined
                            rounded
                        />
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>

        <!-- ⚙️ Configurações e Metas FIRE -->
        <v-card rounded="xl" elevation="2">
            <v-card-title class="text-h5 font-weight-bold">
                ⚙️ Configurações e Metas FIRE
            </v-card-title>
            <v-card-text>
                <v-form @submit.prevent="salvar">
                    <v-row dense>
                        <v-col cols="12" sm="4">
                            <v-select
                                v-model="settings.moeda_padrao"
                                :items="['EUR', 'USD', 'BRL']"
                                label="Moeda Padrão"
                                outlined
                                rounded
                            />
                        </v-col>

                        <v-col cols="12" sm="4">
                            <v-select
                                v-model="settings.idioma"
                                :items="['pt', 'en', 'es']"
                                label="Idioma"
                                outlined
                                rounded
                            />
                        </v-col>

                        <v-col cols="12" sm="4">
                            <v-text-field
                                v-model="settings.frequencia_atualizacao"
                                label="Atualização (em horas)"
                                type="number"
                                outlined
                                rounded
                            />
                        </v-col>

                        <v-col cols="12" sm="6">
                            <v-text-field
                                v-model="settings.meta_fire_total"
                                label="Meta FIRE Total (€)"
                                type="number"
                                outlined
                                rounded
                            />
                        </v-col>

                        <v-col cols="12" sm="6">
                            <v-text-field
                                v-model="settings.renda_fire_desejada"
                                label="Renda FIRE desejada (€/mês)"
                                type="number"
                                outlined
                                rounded
                            />
                        </v-col>

                        <v-col cols="12" class="text-end">
                            <v-btn
                                type="submit"
                                color="primary"
                                size="large"
                                rounded
                            >
                                💾 Salvar alterações
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import axios from "../services/api";

    const user = ref({ username: "", email: "" });
    const settings = ref({
        moeda_padrao: "EUR",
        idioma: "pt",
        frequencia_atualizacao: 24,
        meta_fire_total: 600000,
        renda_fire_desejada: 2000,
    });

    const fetchDados = async () => {
        const [userRes, settingsRes] = await Promise.all([
            axios.get("/api/auth/users/me/"),
            axios.get("/api/users/settings/"),
        ]);
        user.value = userRes.data;
        settings.value = settingsRes.data;
    };

    const salvar = async () => {
        await axios.put("/api/users/settings/", settings.value);
        alert("Configurações salvas com sucesso!");
    };

    onMounted(fetchDados);
</script>

<style scoped>
    .bg-light {
        background-color: #f5f5f5;
    }
</style>
