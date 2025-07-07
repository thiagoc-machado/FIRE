<template>
    <v-container fluid class="pa-4 bg-light">
        <!-- 🔥 Alerta motivacional -->
        <v-alert
            type="info"
            variant="outlined"
            color="deep-orange lighten-4"
            border="start"
            icon="mdi-fire"
            class="mb-4 font-weight-medium"
        >
            Seu progresso FIRE é de
            <strong
                >{{
                    progresso?.percentual_atingido?.toFixed(1) || "0.0"
                }}%</strong
            >!
            {{
                progresso?.percentual_atingido > 75
                    ? "Você está quase lá! 🎯"
                    : "Continue firme e invista com consistência 💪"
            }}
        </v-alert>

        <!-- 🔥 Resumo do plano -->
        <v-card class="mb-6" rounded="xl" elevation="1">
            <v-card-title class="text-h6 d-flex justify-space-between">
                🔥 Meu Plano F.I.R.E.
                <v-btn icon @click="abrirEdicao">
                    <v-icon>mdi-pencil</v-icon>
                </v-btn>
            </v-card-title>

            <v-card-text>
                <v-row dense>
                    <v-col cols="12" md="6" lg="4">
                        <v-card
                            class="pa-4 gradient-green text-center"
                            rounded="xl"
                            elevation="2"
                        >
                            <h3 class="text-white">Meta FIRE</h3>
                            <p class="text-h6 text-white font-weight-bold">
                                {{ formatCurrency(meta.meta_fire_total) }}
                            </p>
                        </v-card>
                    </v-col>

                    <v-col cols="12" md="6" lg="4">
                        <v-card
                            class="pa-4 gradient-blue text-center"
                            rounded="xl"
                            elevation="2"
                        >
                            <h3 class="text-white">Patrimônio Atual</h3>
                            <p class="text-h6 text-white font-weight-bold">
                                {{ formatCurrency(progresso.patrimonio_atual) }}
                            </p>
                        </v-card>
                    </v-col>

                    <v-col cols="12" md="6" lg="4">
                        <v-card
                            class="pa-4 gradient-purple text-center"
                            rounded="xl"
                            elevation="2"
                        >
                            <h3 class="text-white mb-2">Atingido</h3>
                            <v-progress-linear
                                :model-value="progresso.percentual_atingido"
                                height="24"
                                color="deep-purple"
                                rounded
                                class="mt-2"
                            >
                                <strong class="text-white">
                                    {{
                                        progresso.percentual_atingido.toFixed(
                                            1
                                        )
                                    }}%
                                </strong>
                            </v-progress-linear>
                        </v-card>
                    </v-col>
                </v-row>

                <v-row class="mt-4" dense>
                    <v-col cols="12" md="6">
                        <v-sheet
                            class="pa-4"
                            color="amber lighten-5"
                            rounded="xl"
                        >
                            <h4 class="mb-1">Renda desejada FIRE</h4>
                            <p class="text-h6 font-weight-bold">
                                {{ formatCurrency(meta.renda_fire_desejada) }} /
                                mês
                            </p>

                            <h4 class="mt-4 mb-1">Renda passiva estimada</h4>
                            <p class="text-h6 font-weight-bold">
                                {{
                                    formatCurrency(
                                        progresso.renda_atual_estimada
                                    )
                                }}
                                / mês
                            </p>
                        </v-sheet>
                    </v-col>

                    <v-col cols="12" md="6">
                        <v-sheet
                            class="pa-4"
                            color="indigo lighten-5"
                            rounded="xl"
                        >
                            <h4 class="mb-1">Gap Mensal</h4>
                            <p class="text-h6 font-weight-bold">
                                {{ formatCurrency(progresso.gap_mensal) }}
                            </p>

                            <h4 class="mt-4 mb-1">Aporte médio mensal</h4>
                            <p class="text-h6 font-weight-bold">
                                {{
                                    formatCurrency(
                                        progresso.aporte_mensal_medio
                                    )
                                }}
                            </p>

                            <h4 class="mt-4 mb-1">Meses estimados até FIRE</h4>
                            <p class="text-h5 font-weight-bold">
                                {{ progresso.meses_estimados }} meses
                            </p>
                        </v-sheet>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>

        <!-- 📈 Evolução -->
        <v-card class="mb-6" rounded="xl" elevation="1">
            <v-card-title class="text-h6">📈 Evolução Patrimonial</v-card-title>
            <v-card-text>
                <LineChart
                    v-if="evolucaoData?.labels?.length"
                    :chart-data="evolucaoData"
                />
                <div v-else class="text-center">
                    Sem dados de evolução ainda.
                </div>
            </v-card-text>
        </v-card>

        <!-- 📊 Planejamento -->
        <v-card class="mb-6" rounded="xl" elevation="1">
            <v-card-title class="text-h6">📊 Planejamento Mensal</v-card-title>
            <v-card-text>
                <GroupedBarChart
                    v-if="planejamentoData?.labels?.length"
                    :chart-data="planejamentoData"
                />
                <div v-else class="text-center">
                    Sem dados de planejamento ainda.
                </div>
            </v-card-text>
        </v-card>

        <!-- Modal de edição -->
        <v-dialog v-model="modal" max-width="500px">
            <v-card>
                <v-card-title class="text-h6">Editar metas FIRE</v-card-title>
                <v-card-text>
                    <v-form @submit.prevent="salvarEdicao">
                        <v-text-field
                            v-model="metaEdit.meta_fire_total"
                            label="Meta FIRE Total (€)"
                            type="number"
                            required
                        />
                        <v-text-field
                            v-model="metaEdit.renda_fire_desejada"
                            label="Renda FIRE desejada (€ por mês)"
                            type="number"
                            required
                        />
                        <v-btn type="submit" color="primary" class="mt-3"
                            >Salvar</v-btn
                        >
                    </v-form>
                </v-card-text>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import axios from "../services/api";
    import LineChart from "../components/LineChart.vue";
    import GroupedBarChart from "../components/GroupedBarChart.vue";

    const modal = ref(false);
    const metaEdit = ref({ meta_fire_total: 0, renda_fire_desejada: 0 });
    const progresso = ref({
        patrimonio_atual: 0,
        percentual_atingido: 0,
        renda_atual_estimada: 0,
        gap_mensal: 0,
        meses_estimados: 0,
        aporte_mensal_medio: 0,
    });

    const meta = ref({
        meta_fire_total: 0,
        renda_fire_desejada: 0,
    });
    const evolucaoData = ref({
        labels: [],
        datasets: [],
    });

    const planejamentoData = ref({
        labels: [],
        datasets: [],
    });

    const abrirEdicao = () => {
        metaEdit.value = { ...meta.value };
        modal.value = true;
    };

    const salvarEdicao = async () => {
        await axios.put("/api/users/settings/", {
            meta_fire_total: metaEdit.value.meta_fire_total,
            renda_fire_desejada: metaEdit.value.renda_fire_desejada,
        });
        modal.value = false;
        await fetchDados();
    };

    const formatCurrency = (valor) =>
        new Intl.NumberFormat("pt-BR", {
            style: "currency",
            currency: "EUR",
        }).format(valor);

    const fetchDados = async () => {
        const [progRes, metaRes, evolucaoRes, planejamentoRes] =
            await Promise.all([
                axios.get("/api/core/dashboard/progresso-fire/"),
                axios.get("/api/users/settings/"),
                axios.get("/api/core/dashboard/evolucao/"),
                axios.get("/api/core/dashboard/planejamento/"),
            ]);

        progresso.value = progRes.data;
        meta.value = metaRes.data;

        evolucaoData.value = {
            labels: evolucaoRes.data.map((i) => i.mes),
            datasets: [
                {
                    label: "Investido",
                    backgroundColor: "rgba(33, 150, 243, 0.2)",
                    borderColor: "#2196f3",
                    tension: 0.3,
                    fill: true,
                    data: evolucaoRes.data.map((i) => i.investido),
                },
                {
                    label: "Valorizado",
                    backgroundColor: "rgba(76, 175, 80, 0.2)",
                    borderColor: "#4caf50",
                    tension: 0.3,
                    fill: true,
                    data: evolucaoRes.data.map((i) => i.valorizado),
                },
            ],
        };

        planejamentoData.value = {
            labels: planejamentoRes.data.map((i) => i.mes),
            datasets: [
                {
                    label: "Aporte Planejado",
                    backgroundColor: "#ff9800",
                    data: planejamentoRes.data.map((i) => i.aporte_planejado),
                },
                {
                    label: "Aporte Real",
                    backgroundColor: "#2196f3",
                    data: planejamentoRes.data.map((i) => i.aporte_real),
                },
            ],
        };
    };

    onMounted(fetchDados);
</script>
<style scoped>
    .bg-light {
        background-color: #f5f5f5;
    }
    .gradient-blue {
        background: linear-gradient(135deg, #2196f3, #42a5f5);
    }
    .gradient-green {
        background: linear-gradient(135deg, #43a047, #66bb6a);
    }
    .gradient-purple {
        background: linear-gradient(135deg, #7e57c2, #ab47bc);
    }
</style>
