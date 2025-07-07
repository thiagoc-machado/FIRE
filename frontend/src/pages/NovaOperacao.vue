<template>
    <v-container fluid class="pa-4 bg-light">
        <v-card rounded="xl" elevation="2" class="pa-4">
            <v-card-title class="text-h5 font-weight-bold">
                📝 Nova Operação
            </v-card-title>
            <v-card-text>
                <v-form @submit.prevent="submit">
                    <v-row dense>
                        <v-col cols="12" sm="6">
                            <v-select
                                v-model="tipo"
                                :items="['compra', 'venda']"
                                label="Tipo de operação"
                                outlined
                                rounded
                                required
                            />
                        </v-col>

                        <v-col cols="12" sm="6">
                            <v-select
                                v-model="asset"
                                :items="assets"
                                item-title="codigo"
                                item-value="id"
                                label="Ativo"
                                outlined
                                rounded
                                required
                            >
                                <template #append-inner>
                                    <v-btn
                                        icon
                                        size="small"
                                        @mousedown.stop
                                        @click.stop="abrirModalAtivo"
                                    >
                                        <v-icon>mdi-plus</v-icon>
                                    </v-btn>
                                </template>
                            </v-select>
                            <ModalAtivo
                                v-model="mostrarModalAtivo"
                                :categorias="categories"
                                :ativo="null"
                                @salvo="recarregarAtivos"
                            />
                        </v-col>

                        <v-col cols="12" sm="6">
                            <v-select
                                v-model="broker"
                                :items="brokers"
                                item-title="nome"
                                item-value="id"
                                label="Corretora"
                                outlined
                                rounded
                                required
                            >
                                <template #append-inner>
                                    <v-btn
                                        icon
                                        size="small"
                                        @mousedown.stop
                                        @click.stop="
                                            mostrarModalCorretora = true
                                        "
                                    >
                                        <v-icon>mdi-plus</v-icon>
                                    </v-btn>
                                </template>
                            </v-select>
                            <ModalCorretora
                                v-model="mostrarModalCorretora"
                                :corretora="null"
                                @salvo="carregarCorretoras"
                            />
                        </v-col>

                        <v-col cols="12" sm="6">
                            <v-select
                                v-model="category"
                                :items="categories"
                                item-title="nome"
                                item-value="id"
                                label="Categoria"
                                outlined
                                rounded
                                required
                            >
                                <template #append-inner>
                                    <v-btn
                                        icon
                                        size="small"
                                        @mousedown.stop
                                        @click.stop="
                                            mostrarModalCategoria = true
                                        "
                                    >
                                        <v-icon>mdi-plus</v-icon>
                                    </v-btn>
                                </template>
                            </v-select>
                            <ModalCategoria
                                v-model="mostrarModalCategoria"
                                :categoria="null"
                                @salvo="carregarCategorias"
                            />
                        </v-col>

                        <v-col cols="12" sm="6">
                            <v-text-field
                                v-model="quantidade"
                                label="Quantidade"
                                type="number"
                                outlined
                                rounded
                                required
                            />
                        </v-col>

                        <v-col cols="12" sm="6">
                            <v-text-field
                                v-model="valor"
                                label="Valor de compra"
                                type="number"
                                outlined
                                rounded
                                required
                            />
                        </v-col>

                        <v-col cols="12" sm="6">
                            <v-text-field
                                v-model="data"
                                label="Data"
                                type="date"
                                outlined
                                rounded
                                required
                            />
                        </v-col>

                        <v-col cols="12" class="text-end">
                            <v-btn
                                type="submit"
                                color="primary"
                                size="large"
                                rounded
                            >
                                💾 Salvar
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
    import { useRouter } from "vue-router";

    const router = useRouter();

    const tipo = ref("");
    const asset = ref("");
    const broker = ref("");
    const category = ref("");
    const data = ref("");
    const quantidade = ref("");
    const valor = ref("");

    const assets = ref([]);
    const brokers = ref([]);
    const categories = ref([]);
    const loading = ref({
        assets: false,
        brokers: false,
        categories: false,
    });

    import ModalAtivo from "../components/ModalAtivo.vue";

    const mostrarModalAtivo = ref(false);
    const abrirModalAtivo = () => {
        mostrarModalAtivo.value = true;
    };

    const recarregarAtivos = async () => {
        const res = await axios.get("/api/core/assets/");
        assets.value = res.data;
    };
    import ModalCategoria from "../components/ModalCategoria.vue";
    import ModalCorretora from "../components/ModalCorretora.vue";

    const mostrarModalCategoria = ref(false);
    const mostrarModalCorretora = ref(false);

    const carregarCategorias = async () => {
        const res = await axios.get("/api/core/categories/");
        categories.value = res.data;
    };

    const carregarCorretoras = async () => {
        const res = await axios.get("/api/core/brokers/");
        brokers.value = res.data;
    };

    const fetchData = async () => {
        loading.value.assets = true;
        loading.value.brokers = true;
        loading.value.categories = true;

        const [a, b, c] = await Promise.all([
            axios.get("/api/core/assets/"),
            axios.get("/api/core/brokers/"),
            axios.get("/api/core/categories/"),
        ]);

        assets.value = a.data;
        brokers.value = b.data;
        categories.value = c.data;

        loading.value.assets = false;
        loading.value.brokers = false;
        loading.value.categories = false;
    };

    onMounted(fetchData);

    const submit = async () => {
        try {
            await axios.post("/api/core/operations/", {
                tipo: tipo.value.toUpperCase(),
                ativo: asset.value,
                corretora: broker.value,
                categoria: category.value,
                valor_compra: valor.value,
                data: data.value,
                quantidade: quantidade.value,
            });
            //     await axios.post('/api/core/operations/', {
            //   tipo: tipo.value,
            //   ativo: asset.value,
            //   corretora: broker.value,
            //   categoria: category.value,
            //   quantidade: quantidade.value,
            //   valor_compra: valor.value,
            //   data: data.value
            // })
            router.push("/");
        } catch (err) {
            alert("Erro ao salvar operação.");
        }
    };
</script>

<style scoped>
    .bg-light {
        background-color: #f5f5f5;
    }
</style>
