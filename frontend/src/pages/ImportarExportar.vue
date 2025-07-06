// ✅ ImportarExportar.vue
<template>
    <v-container>
        <v-card class="mb-4">
            <v-card-title class="text-h5"
                >Importar Operações (CSV)</v-card-title
            >
            <v-card-text>
                <v-file-input
                    v-model="arquivo"
                    label="Selecionar arquivo CSV"
                    accept=".csv"
                    prepend-icon="mdi-file-upload"
                    @change="carregarPreview"
                />

                <v-table v-if="preview.length" class="mt-4">
                    <thead>
                        <tr>
                            <th
                                v-for="(valor, chave) in preview[0]"
                                :key="chave"
                            >
                                {{ chave }}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(linha, i) in preview.slice(0, 5)" :key="i">
                            <td v-for="(valor, chave) in linha" :key="chave">
                                {{ valor }}
                            </td>
                        </tr>
                    </tbody>
                </v-table>

                <v-btn
                    :disabled="!arquivo"
                    color="primary"
                    class="mt-4"
                    @click="importarCSV"
                >
                    Importar Arquivo
                </v-btn>

                <v-alert
                    v-if="mensagem"
                    :type="erro ? 'error' : 'success'"
                    class="mt-4"
                >
                    {{ mensagem }}
                </v-alert>
            </v-card-text>
        </v-card>

        <v-card>
            <v-card-title class="text-h5"
                >Exportar Operações (JSON)</v-card-title
            >
            <v-card-text>
                <v-btn color="success" @click="exportarJSON">
                    Exportar Json
                </v-btn>
                <v-btn color="info" class="ml-2" @click="exportarExcel">
                    Exportar Excel
                </v-btn>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
    import { ref } from "vue";
    import axios from "../services/api";
    const exportarExcel = async () => {
        const res = await axios.get("/api/core/operations/exportar-excel/", {
            responseType: "blob",
        });
        const blob = new Blob([res.data], {
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "operacoes.xlsx";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    const arquivo = ref(null);
    const preview = ref([]);
    const mensagem = ref("");
    const erro = ref(false);

    const carregarPreview = async () => {
        mensagem.value = "";
        erro.value = false;
        preview.value = [];

        if (!arquivo.value) return;

        const file = arquivo.value;
        const text = await file.text();
        const linhas = text.split("\n").filter(Boolean);
        const colunas = linhas[0].split(",");
        preview.value = linhas.slice(1).map((linha) => {
            const valores = linha.split(",");
            return colunas.reduce((obj, col, i) => {
                obj[col.trim()] = valores[i]?.trim();
                return obj;
            }, {});
        });
    };

    const importarCSV = async () => {
        const form = new FormData();
        form.append("file", arquivo.value);

        try {
            const res = await axios.post(
                "/api/core/operations/importar/",
                form
            );
            mensagem.value = res.data.mensagem || "Importação concluída";
            erro.value = false;
            preview.value = [];
            arquivo.value = null;
        } catch (e) {
            erro.value = true;
            mensagem.value = "Erro ao importar arquivo";
        }
    };

    const exportarJSON = async () => {
        const res = await axios.get("/api/core/operations/exportar/");
        const blob = new Blob([JSON.stringify(res.data, null, 2)], {
            type: "application/json",
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "operacoes.json";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };
</script>
