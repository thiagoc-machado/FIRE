<template>
    <v-navigation-drawer
        v-model="drawer"
        :temporary="isMobile"
        :permanent="!isMobile"
        app
        class="elevation-3"
    >
        <v-list nav dense>
            <v-list-item v-if="isMobile" class="justify-end">
                <v-btn icon @click="store.commit('setDrawer', false)">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-list-item>
            <v-list-item class="text-h6 font-weight-bold py-4 px-4">
                🔥 F.I.R.E.
            </v-list-item>

            <v-list-group prepend-icon="mdi-view-dashboard-outline">
                <template #activator="{ props }">
                    <v-list-item v-bind="props">
                        <v-list-item-title>Dashboard</v-list-item-title>
                    </v-list-item>
                </template>
                <v-list-item link to="/" @click="$emit('close-drawer')">
                    <v-list-item-title>Resumo geral</v-list-item-title>
                </v-list-item>
                <v-list-item
                    link
                    to="/dashboard-fire"
                    @click="$emit('close-drawer')"
                >
                    <v-list-item-title>Plano FIRE</v-list-item-title>
                </v-list-item>
                <v-list-item
                    link
                    to="/calculadora-fire"
                    @click="$emit('close-drawer')"
                >
                    <v-list-item-title>Calculadora FIRE</v-list-item-title>
                </v-list-item>
            </v-list-group>

            <v-list-group prepend-icon="mdi-finance">
                <template #activator="{ props }">
                    <v-list-item v-bind="props">
                        <v-list-item-title>Investimentos</v-list-item-title>
                    </v-list-item>
                </template>
                <v-list-item
                    link
                    to="/nova-operacao"
                    @click="$emit('close-drawer')"
                >
                    <v-list-item-title>Nova operação</v-list-item-title>
                </v-list-item>
                <v-list-item
                    link
                    to="/operacoes"
                    @click="$emit('close-drawer')"
                >
                    <v-list-item-title>Operações</v-list-item-title>
                </v-list-item>
                <v-list-item link to="/ativos" @click="$emit('close-drawer')">
                    <v-list-item-title>Ativos</v-list-item-title>
                </v-list-item>
                <v-list-item
                    link
                    to="/corretoras"
                    @click="$emit('close-drawer')"
                >
                    <v-list-item-title>Corretoras</v-list-item-title>
                </v-list-item>
                <v-list-item
                    link
                    to="/categorias"
                    @click="$emit('close-drawer')"
                >
                    <v-list-item-title>Categorias</v-list-item-title>
                </v-list-item>
            </v-list-group>

            <v-list-group prepend-icon="mdi-database-import">
                <template #activator="{ props }">
                    <v-list-item v-bind="props">
                        <v-list-item-title>Dados</v-list-item-title>
                    </v-list-item>
                </template>
                <v-list-item
                    link
                    to="/importar-exportar"
                    @click="$emit('close-drawer')"
                >
                    <v-list-item-title>Importar / Exportar</v-list-item-title>
                </v-list-item>
            </v-list-group>

            <v-list-group prepend-icon="mdi-cog-outline">
                <template #activator="{ props }">
                    <v-list-item v-bind="props">
                        <v-list-item-title>Sistema</v-list-item-title>
                    </v-list-item>
                </template>
                <v-list-item
                    link
                    to="/configuracoes"
                    @click="$emit('close-drawer')"
                >
                    <v-list-item-title>Configurações</v-list-item-title>
                </v-list-item>
            </v-list-group>

            <v-divider class="my-2" />

            <v-list-item @click="logout" class="text-red">
                <v-icon start color="red">mdi-logout</v-icon>
                <v-list-item-title>Cerrar sesión</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script setup>
    import { computed, ref, onMounted } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";
    import { useDisplay } from "vuetify";
    const { mdAndDown } = useDisplay();

    const store = useStore();
    const router = useRouter();

    const drawer = computed(() => store.state.drawer);
    const logout = () => {
        store.dispatch("auth/logout");
        router.push("/login");
    };

    const isMobile = computed(() => mdAndDown.value);

    // onMounted(() => {
    //     const updateIsMobile = () => {
    //         isMobile.value = window.innerWidth <= 768;
    //     };
    //     updateIsMobile();
    //     window.addEventListener("resize", updateIsMobile);
    // });

    const dashOpen = ref(true);
    const investOpen = ref(false);
    const dadosOpen = ref(false);
    const sistemaOpen = ref(false);
</script>

<style>
    .v-list-item {
        cursor: pointer;
    }
</style>
