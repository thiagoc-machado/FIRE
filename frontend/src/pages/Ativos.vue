<template>
    <v-container>
        <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
                <span class="text-h5">Ativos</span>
                <div>
                    <v-btn icon @click="abrirNovoAtivo">
                        <v-icon>mdi-plus</v-icon>
                    </v-btn>
                    <v-btn
                        color="primary"
                        @click="atualizarCotacoes"
                        :loading="loadingAtualizacao"
                    >
                        Atualizar cotações
                    </v-btn>
                </div>
            </v-card-title>

            <v-card-text>
                <v-data-table
                    :items="ativos"
                    :headers="headers"
                    :loading="loading"
                    class="mt-2"
                >
                    <!-- Campo categoria -->
                    <template #item.categoria_nome="{ item }">
                        {{ item.categoria?.nome || "—" }}
                    </template>

                    <!-- Campo cotação -->
                    <template #item.cotacao="{ item }">
                        {{
                            item.preco_atual != null
                                ? "€ " + Number(item.preco_atual).toFixed(2)
                                : "—"
                        }}
                    </template>

                    <!-- Ações -->
                    <template #item.actions="{ item }">
                        <v-btn icon @click="editar(item)">
                            <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                        <v-btn icon @click="deletar(item.id)">
                            <v-icon color="red">mdi-delete</v-icon>
                        </v-btn>
                    </template>
                </v-data-table>
            </v-card-text>
        </v-card>

        <ModalAtivo
            v-model="mostrarModal"
            :ativo="ativoSelecionado"
            :categorias="categorias"
            @salvo="fetchAtivos"
        />
    </v-container>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import axios from "../services/api";
    import ModalAtivo from "../components/ModalAtivo.vue";

    const ativos = ref([]);
    const categorias = ref([]);
    const loading = ref(false);
    const loadingAtualizacao = ref(false);

    const mostrarModal = ref(false);
    const ativoSelecionado = ref(null);

    const headers = [
        { title: "Código", key: "codigo" },
        { title: "Nome", key: "nome" },
        { title: "Moeda", key: "moeda" },
        { title: "Frequência", key: "frequencia_dividendos" },
        { title: "Categoria", key: "categoria_nome" },
        { title: "Cotação", key: "cotacao" },
        { title: "Ações", key: "actions", sortable: false },
    ];

    const fetchAtivos = async () => {
        loading.value = true;
        const [a, c] = await Promise.all([
            axios.get("/api/core/assets/"),
            axios.get("/api/core/categories/"),
        ]);
        ativos.value = a.data.map((item) => ({
            ...item,
            categoria_nome: item.categoria?.nome || "",
            cotacao: item.preco_atual,
        }));
        categorias.value = c.data;
        loading.value = false;
    };

    const atualizarCotacoes = async () => {
        loadingAtualizacao.value = true;
        await axios.get("/api/core/assets/atualizar/");
        await fetchAtivos();
        loadingAtualizacao.value = false;
    };

    const abrirNovoAtivo = () => {
        ativoSelecionado.value = null;
        mostrarModal.value = true;
    };

    const editar = (item) => {
        ativoSelecionado.value = { ...item };
        mostrarModal.value = true;
    };

    const deletar = async (id) => {
        if (confirm("Deseja realmente excluir este ativo?")) {
            await axios.delete(`/api/core/assets/${id}/`);
            await fetchAtivos();
        }
    };

    onMounted(fetchAtivos);
</script>
