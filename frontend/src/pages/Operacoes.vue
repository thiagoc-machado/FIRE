<template>
    <v-container fluid class="pa-4 bg-light">
        <v-card rounded="xl" elevation="2">
            <v-card-title class="text-h5 font-weight-bold">
                📋 Operações
            </v-card-title>

            <v-card-text>
                <!-- 🔎 Filtros -->
                <v-row dense>
                    <v-col cols="12" sm="3">
                        <v-select
                            v-model="filtros.tipo"
                            :items="['COMPRA', 'VENDA']"
                            label="Tipo"
                            outlined
                            rounded
                            clearable
                        />
                    </v-col>

                    <v-col cols="12" sm="3">
                        <v-select
                            v-model="filtros.corretora"
                            :items="brokers"
                            item-title="nome"
                            item-value="id"
                            label="Corretora"
                            outlined
                            rounded
                            clearable
                            :loading="loading.brokers"
                        />
                    </v-col>

                    <v-col cols="12" sm="3">
                        <v-select
                            v-model="filtros.categoria"
                            :items="categories"
                            item-title="nome"
                            item-value="id"
                            label="Categoria"
                            outlined
                            rounded
                            clearable
                            :loading="loading.categories"
                        />
                    </v-col>

                    <v-col cols="12" sm="3">
                        <v-text-field
                            v-model="filtros.data_inicial"
                            label="Data inicial"
                            type="date"
                            outlined
                            rounded
                            clearable
                        />
                    </v-col>

                    <v-col cols="12" sm="3">
                        <v-text-field
                            v-model="filtros.data_final"
                            label="Data final"
                            type="date"
                            outlined
                            rounded
                            clearable
                        />
                    </v-col>

                    <v-col cols="12" sm="3" class="d-flex align-end">
                        <v-btn color="primary" @click="fetchOperacoes" rounded>
                            🔍 Filtrar
                        </v-btn>
                    </v-col>
                </v-row>

                <!-- 📊 Tabela -->
                <v-data-table
                    :items="operacoes"
                    :headers="headers"
                    :loading="loading.operacoes"
                    class="mt-6 rounded-xl elevation-1"
                    density="comfortable"
                >
                    <template #item.actions="{ item }">
                        <v-btn icon size="small" @click="editar(item)">
                            <v-icon color="primary">mdi-pencil</v-icon>
                        </v-btn>
                        <v-btn icon size="small" @click="excluir(item.id)">
                            <v-icon color="red">mdi-delete</v-icon>
                        </v-btn>
                    </template>
                </v-data-table>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import axios from "../services/api";
    import { useRouter } from "vue-router";

    const router = useRouter();
    const operacoes = ref([]);
    const brokers = ref([]);
    const categories = ref([]);
    const loading = ref({
        operacoes: false,
        brokers: false,
        categories: false,
    });

    const filtros = ref({
        tipo: null,
        corretora: null,
        categoria: null,
        data_inicial: null,
        data_final: null,
    });

    const headers = [
        { title: "Tipo", key: "tipo" },
        { title: "Ativo", key: "ativo_nome" },
        { title: "Corretora", key: "corretora_nome" },
        { title: "Categoria", key: "categoria_nome" },
        { title: "Quantidade", key: "quantidade" },
        { title: "Valor", key: "valor_compra" },
        { title: "Data", key: "data" },
        { title: "Ações", key: "actions", sortable: false },
    ];

    const fetchOperacoes = async () => {
        loading.value.operacoes = true;
        try {
            const params = {
                tipo: filtros.value.tipo,
                corretora: filtros.value.corretora,
                categoria: filtros.value.categoria,
                data_inicial: filtros.value.data_inicial,
                data_final: filtros.value.data_final,
            };
            const { data } = await axios.get("/api/core/operations/", {
                params,
            });
            // Adapta nomes relacionados se não vierem prontos
            operacoes.value = data.map((op) => ({
                ...op,
                ativo_nome: op.ativo_nome || op.ativo?.nome || "",
                corretora_nome: op.corretora_nome || op.corretora?.nome || "",
                categoria_nome: op.categoria_nome || op.categoria?.nome || "",
            }));
        } finally {
            loading.value.operacoes = false;
        }
    };

    const fetchBrokersAndCategories = async () => {
        loading.value.brokers = true;
        loading.value.categories = true;
        const [b, c] = await Promise.all([
            axios.get("/api/core/brokers/"),
            axios.get("/api/core/categories/"),
        ]);
        brokers.value = b.data;
        categories.value = c.data;
        loading.value.brokers = false;
        loading.value.categories = false;
    };

    const editar = (item) => {
        router.push(`/operacoes/${item.id}/editar`);
    };

    const excluir = async (id) => {
        if (confirm("Deseja realmente excluir esta operação?")) {
            await axios.delete(`/api/core/operations/${id}/`);
            fetchOperacoes();
        }
    };

    onMounted(() => {
        fetchOperacoes();
        fetchBrokersAndCategories();
    });
</script>

<style scoped>
    .bg-light {
        background-color: #f9f9f9;
    }
</style>
