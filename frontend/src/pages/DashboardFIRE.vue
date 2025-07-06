<template>
    <v-container>
        <!-- Alerta com progresso -->
        <v-alert
            type="info"
            border="start"
            color="blue lighten-4"
            icon="mdi-fire"
            class="mb-4"
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

        <!-- Metas e progresso -->
        <v-card class="mb-6">
            <v-card-title class="text-h5 d-flex justify-space-between">
                🔥 Meu Plano F.I.R.E.
                <v-btn icon @click="abrirEdicao">
                    <v-icon>mdi-pencil</v-icon>
                </v-btn>
            </v-card-title>

            <v-card-text>
                <v-row>
                    <v-col cols="12" md="6" lg="4">
                        <v-sheet
                            class="pa-4 text-center"
                            color="green lighten-5"
                            rounded
                        >
                            <h3>Meta FIRE</h3>
                            <p class="text-h6">
                                {{ formatCurrency(meta.meta_fire_total) }}
                            </p>
                        </v-sheet>
                    </v-col>

                    <v-col cols="12" md="6" lg="4">
                        <v-sheet
                            class="pa-4 text-center"
                            color="blue lighten-5"
                            rounded
                        >
                            <h3>Patrimônio Atual</h3>
                            <p class="text-h6">
                                {{ formatCurrency(progresso.patrimonio_atual) }}
                            </p>
                        </v-sheet>
                    </v-col>

                    <v-col cols="12" md="6" lg="4">
                        <v-sheet
                            class="pa-4 text-center"
                            color="purple lighten-5"
                            rounded
                        >
                            <h3>Atingido</h3>
                            <v-progress-linear
                                :model-value="progresso.percentual_atingido"
                                height="25"
                                color="deep-purple"
                                rounded
                                class="mt-2"
                            >
                                <strong
                                    >{{
                                        progresso.percentual_atingido.toFixed(
                                            1
                                        )
                                    }}%</strong
                                >
                            </v-progress-linear>
                        </v-sheet>
                    </v-col>
                </v-row>

                <v-row class="mt-4">
                    <v-col cols="12" md="6">
                        <v-sheet class="pa-4" color="amber lighten-5" rounded>
                            <h3 class="mb-2">Renda desejada FIRE</h3>
                            <p class="text-h6">
                                {{ formatCurrency(meta.renda_fire_desejada) }} /
                                mês
                            </p>

                            <h3 class="mt-4 mb-2">Renda passiva estimada</h3>
                            <p class="text-h6">
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
                        <v-sheet class="pa-4" color="indigo lighten-5" rounded>
                            <h3 class="mb-2">Gap Mensal</h3>
                            <p class="text-h6">
                                {{ formatCurrency(progresso.gap_mensal) }}
                            </p>

                            <h3 class="mt-4 mb-2">Aporte médio mensal</h3>
                            <p class="text-h6">
                                {{
                                    formatCurrency(
                                        progresso.aporte_mensal_medio
                                    )
                                }}
                            </p>

                            <h3 class="mt-4 mb-2">Meses estimados até FIRE</h3>
                            <p class="text-h5 font-weight-bold">
                                {{ progresso.meses_estimados }} meses
                            </p>
                        </v-sheet>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>

        <!-- Gráfico de evolução -->
        <v-card class="mb-6">
            <v-card-title class="text-h6">📈 Evolução Patrimonial</v-card-title>
            <v-card-text>
                <LineChart
                    v-if="
                        evolucaoData?.labels?.length &&
                        evolucaoData?.datasets?.length
                    "
                    :chart-data="evolucaoData"
                />
                <div v-else class="text-center">
                    Sem dados de evolução ainda.
                </div>
            </v-card-text>
        </v-card>

        <!-- Gráfico de planejamento -->
        <v-card class="mb-6">
            <v-card-title class="text-h6">📊 Planejamento Mensal</v-card-title>
            <v-card-text>
                <GroupedBarChart
                    v-if="
                        planejamentoData?.labels?.length &&
                        planejamentoData?.datasets?.length
                    "
                    :chart-data="planejamentoData"
                />
                <div v-else class="text-center">
                    Sem dados de planejamento ainda.
                </div>
            </v-card-text>
        </v-card>

        <!-- Modal -->
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
