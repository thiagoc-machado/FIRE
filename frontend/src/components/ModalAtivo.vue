<template>
    <v-dialog v-model="model" max-width="600px">
        <v-card rounded="xl" elevation="3">
            <v-card-title class="text-h6 font-weight-bold">
                {{ isEdit ? "✏️ Editar Ativo" : "➕ Novo Ativo" }}
            </v-card-title>

            <v-card-text>
                <v-form @submit.prevent="salvar">
                    <v-text-field
                        v-model="form.codigo"
                        label="Código"
                        required
                        append-inner-icon="mdi-magnify"
                        @click:append-inner="buscarDados"
                        :loading="buscando"
                        hint="Clique na lupa para buscar os dados automaticamente"
                        outlined
                        rounded
                        class="mb-3"
                    />

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
    import { ref, watch, reactive, computed } from "vue";
    import axios from "../services/api";
    import ModalCategoria from "./ModalCategoria.vue";

    const mostrarModalCategoria = ref(false);

    const abrirModalCategoria = () => {
        mostrarModalCategoria.value = true;
    };

    const recarregarCategorias = async () => {
        const res = await axios.get("/api/core/categories/");
        props.categorias.splice(0, props.categorias.length, ...res.data);
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
</script>

<style scoped>
    .mb-3 {
        margin-bottom: 1rem;
    }
</style>
