<template>
    <v-container fluid class="pa-4 bg-light">
        <v-card rounded="xl" elevation="2">
            <!-- Cabeçalho -->
            <v-card-title class="d-flex justify-space-between align-center">
                <span class="text-h5 font-weight-bold">🏦 Corretoras</span>
                <v-btn color="primary" rounded @click="abrirModal()">
                    ➕ Nova Corretora
                </v-btn>
            </v-card-title>

            <!-- Tabela -->
            <v-card-text>
                <v-table class="rounded-xl elevation-1">
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
                                <v-btn
                                    icon
                                    size="small"
                                    @click="abrirModal(broker)"
                                >
                                    <v-icon color="primary">mdi-pencil</v-icon>
                                </v-btn>
                                <v-btn
                                    icon
                                    size="small"
                                    @click="deletar(broker.id)"
                                >
                                    <v-icon color="red">mdi-delete</v-icon>
                                </v-btn>
                            </td>
                        </tr>
                    </tbody>
                </v-table>
            </v-card-text>
        </v-card>

        <!-- Modal -->
        <ModalCorretora
            v-model="modalAberto"
            :corretora="corretoraSelecionada"
            @salvo="carregarCorretoras"
        />
    </v-container>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import axios from "../services/api";
    import ModalCorretora from "../components/ModalCorretora.vue";

    const brokers = ref([]);
    const modalAberto = ref(false);
    const corretoraSelecionada = ref(null);

    const carregarCorretoras = async () => {
        const res = await axios.get("/api/core/brokers/");
        brokers.value = res.data;
    };

    const abrirModal = (corretora = null) => {
        corretoraSelecionada.value = corretora;
        modalAberto.value = true;
    };

    const deletar = async (id) => {
        if (confirm("Deseja apagar esta corretora?")) {
            await axios.delete(`/api/core/brokers/${id}/`);
            carregarCorretoras();
        }
    };

    onMounted(carregarCorretoras);
</script>

<style scoped>
    .bg-light {
        background-color: #f9f9f9;
    }
</style>
