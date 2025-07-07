<template>
    <v-container fluid class="pa-4 bg-light">
        <v-card rounded="xl" elevation="2">
            <!-- Cabeçalho -->
            <v-card-title class="d-flex justify-space-between align-center">
                <span class="text-h5 font-weight-bold">🗂️ Categorias</span>
                <v-btn color="primary" rounded @click="abrirModal()">
                    ➕ Nova Categoria
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
                        <tr v-for="categoria in categories" :key="categoria.id">
                            <td>{{ categoria.nome }}</td>
                            <td class="text-right">
                                <v-btn
                                    icon
                                    size="small"
                                    @click="abrirModal(categoria)"
                                >
                                    <v-icon color="primary">mdi-pencil</v-icon>
                                </v-btn>
                                <v-btn
                                    icon
                                    size="small"
                                    @click="deletar(categoria.id)"
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
        <ModalCategoria
            v-model="modalAberto"
            :categoria="categoriaSelecionada"
            @salvo="carregarCategorias"
        />
    </v-container>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import axios from "../services/api";
    import ModalCategoria from "../components/ModalCategoria.vue";

    const categories = ref([]);
    const modalAberto = ref(false);
    const categoriaSelecionada = ref(null);

    const carregarCategorias = async () => {
        const res = await axios.get("/api/core/categories/");
        categories.value = res.data;
    };

    const abrirModal = (categoria = null) => {
        categoriaSelecionada.value = categoria;
        modalAberto.value = true;
    };

    const deletar = async (id) => {
        if (confirm("Deseja apagar esta categoria?")) {
            await axios.delete(`/api/core/categories/${id}/`);
            carregarCategorias();
        }
    };

    onMounted(carregarCategorias);
</script>

<style scoped>
    .bg-light {
        background-color: #f9f9f9;
    }
</style>
