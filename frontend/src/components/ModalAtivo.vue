<template>
    <v-dialog v-model="model" max-width="600px">
        <v-card rounded="xl" elevation="3">
            <v-card-title class="text-h6 font-weight-bold">
                {{ isEdit ? "✏️ Editar Ativo" : "➕ Novo Ativo" }}
            </v-card-title>

            <v-card-text>
                <v-form @submit.prevent="salvar">
                    <v-autocomplete
                        v-model="form.codigo"
                        :items="filteredSymbols"
                        :search="searchQuery"
                        @update:search="updateSearch"
                        item-title="displayText"
                        item-value="codigo"
                        label="Código do Ativo"
                        placeholder="Digite o código ou nome do ativo..."
                        required
                        no-filter
                        hide-no-data
                        :loading="buscando"
                        outlined
                        rounded
                        class="mb-3"
                        @update:model-value="onSymbolSelected"
                    >
                        <template #item="{ props, item }">
                            <v-list-item v-bind="props">
                                <v-list-item-title>
                                    <strong>{{ item.raw.codigo }}</strong> - {{ item.raw.nome }}
                                </v-list-item-title>
                                <v-list-item-subtitle>
                                    {{ item.raw.categoria }} • {{ traduzirTipo(item.raw.tipo) }}
                                </v-list-item-subtitle>
                            </v-list-item>
                        </template>
                    </v-autocomplete>

                    <v-text-field
                        v-model="form.nome"
                        label="Nome"
                        required
                        outlined
                        rounded
                        class="mb-3"
                    />

                    <v-text-field
                        v-model="form.moeda"
                        label="Moeda"
                        required
                        outlined
                        rounded
                        class="mb-3"
                    />

                    <v-text-field
                        v-model="form.frequencia_dividendos"
                        label="Frequência de dividendos"
                        required
                        outlined
                        rounded
                        class="mb-3"
                    />

                    <v-select
                        v-model="form.categoria"
                        :items="categorias"
                        item-title="nome"
                        item-value="id"
                        label="Categoria"
                        required
                        outlined
                        rounded
                    >
                        <template #append-inner>
                            <v-btn
                                icon
                                size="small"
                                @mousedown.stop
                                @click.stop="abrirModalCategoria"
                            >
                                <v-icon>mdi-plus</v-icon>
                            </v-btn>
                        </template>
                    </v-select>

                    <v-text-field
                        v-model="form.tipo"
                        label="Tipo"
                        readonly
                        disabled
                        outlined
                        rounded
                        class="mt-3"
                    />

                    <v-btn
                        type="submit"
                        color="primary"
                        class="mt-4"
                        size="large"
                        rounded
                    >
                        {{ isEdit ? "💾 Atualizar" : "✅ Salvar" }}
                    </v-btn>
                </v-form>
            </v-card-text>
        </v-card>

        <ModalCategoria
            v-model="mostrarModalCategoria"
            :categoria="null"
            @salvo="recarregarCategorias"
        />
    </v-dialog>
</template>

<script setup>
    import { ref, watch, reactive, computed, onMounted } from "vue";
    import axios from "../services/api";
    import ModalCategoria from "./ModalCategoria.vue";
    import symbolsDatabase from "../assets/symbols_database.json";

    const mostrarModalCategoria = ref(false);
    const searchQuery = ref("");
    const symbolsData = ref(symbolsDatabase);
    const filteredSymbols = ref([]);

    const abrirModalCategoria = () => {
        mostrarModalCategoria.value = true;
    };

    const recarregarCategorias = async () => {
        const res = await axios.get("/api/core/categories/");
        props.categorias.splice(0, props.categorias.length, ...res.data);
    };

    // Função para atualizar a busca no autocomplete
    const updateSearch = (query) => {
        searchQuery.value = query;
        if (!query || query.length < 2) {
            filteredSymbols.value = [];
            return;
        }

        const searchTerm = query.toLowerCase();
        const filtered = symbolsData.value
            .filter(symbol => 
                symbol.codigo.toLowerCase().includes(searchTerm) ||
                symbol.nome.toLowerCase().includes(searchTerm)
            )
            .slice(0, 20) // Limitar a 20 resultados para performance
            .map(symbol => ({
                ...symbol,
                displayText: `${symbol.codigo} - ${symbol.nome}`
            }));
        
        filteredSymbols.value = filtered;
    };

    // Função chamada quando um símbolo é selecionado
    const onSymbolSelected = async (codigo) => {
        if (!codigo) return;
        
        const selectedSymbol = symbolsData.value.find(s => s.codigo === codigo);
        if (selectedSymbol) {
            // Preencher automaticamente os campos com os dados do símbolo
            form.nome = selectedSymbol.nome;
            form.tipo = traduzirTipo(selectedSymbol.tipo);
            
            // Mapear categoria automaticamente
            const categoriaCorrespondente = props.categorias.find(
                (c) => c.nome.toLowerCase() === selectedSymbol.categoria.toLowerCase()
            );
            if (categoriaCorrespondente) {
                form.categoria = categoriaCorrespondente.id;
            }
            
            // Buscar dados adicionais da API se necessário
            await buscarDados();
        }
    };

    const props = defineProps({
        modelValue: Boolean,
        ativo: Object,
        categorias: Array,
    });

    const emit = defineEmits(["update:modelValue", "salvo"]);

    const model = ref(false);

    const buscando = ref(false);

    const buscarDados = async () => {
        if (!form.codigo) return;

        buscando.value = true;
        try {
            const response = await axios.get(`/api/core/assets/buscar/`, {
                params: { codigo: form.codigo },
            });

            const data = response.data;
            form.nome = data.nome || "";
            form.moeda = data.moeda || "";
            form.frequencia_dividendos = data.frequencia_dividendos || "";
            form.tipo = traduzirTipo(data.tipo);
            form.categoria_nome = data.categoria || "";

            // Mapear automaticamente a categoria pelo nome
            const categoriaCorrespondente = props.categorias.find(
                (c) =>
                    c.nome.toLowerCase() === form.categoria_nome.toLowerCase()
            );
            if (categoriaCorrespondente) {
                form.categoria = categoriaCorrespondente.id;
            }
        } catch (error) {
            alert("Ação não encontrada ou erro ao buscar.");
        } finally {
            buscando.value = false;
        }
    };
    const traduzirTipo = (tipo) => {
        const mapa = {
            ETF: "Fundo de Índice",
            EQUITY: "Ação",
            MUTUALFUND: "Fundo Mútuo",
            INDEX: "Índice",
            CRYPTOCURRENCY: "Criptomoeda",
        };
        return mapa[tipo?.toUpperCase()] || tipo;
    };

    watch(
        () => props.modelValue,
        (val) => (model.value = val)
    );
    watch(model, (val) => emit("update:modelValue", val));

    const isEdit = computed(() => !!props.ativo?.id);

    const form = reactive({
        codigo: "",
        nome: "",
        moeda: "",
        frequencia_dividendos: "",
        categoria: null,
        tipo: "",
        categoria_nome: "",
    });

    watch(
        () => props.ativo,
        (val) => {
            if (val) Object.assign(form, val);
            else
                Object.assign(form, {
                    codigo: "",
                    nome: "",
                    moeda: "",
                    frequencia_dividendos: "",
                    categoria: null,
                });
        },
        { immediate: true }
    );

    const salvar = async () => {
        const payload = { ...form };

        if (isEdit.value) {
            await axios.put(`/api/core/assets/${props.ativo.id}/`, payload);
        } else {
            await axios.post("/api/core/assets/", payload);
        }

        emit("salvo");
        model.value = false;
    };

    // Inicializar o componente
    onMounted(() => {
        // Preparar dados dos símbolos para o autocomplete
        filteredSymbols.value = [];
    });
</script>

<style scoped>
    .mb-3 {
        margin-bottom: 1rem;
    }
</style>
