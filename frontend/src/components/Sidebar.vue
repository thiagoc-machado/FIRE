<template>
    <v-navigation-drawer v-model="drawer" app>
        <v-list nav dense>
            <v-list-item title="F.I.R.E." class="text-h6 font-weight-bold" />

            <!-- 📊 DASHBOARD -->
            <v-list-subheader class="text-grey">Dashboard</v-list-subheader>
            <v-list-item link to="/">
                <v-list-item-title>Dashboard</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/dashboard-fire">
                <v-list-item-icon
                    ><v-icon color="deep-orange"
                        >mdi-fire</v-icon
                    ></v-list-item-icon
                >
                <v-list-item-title>Plano FIRE</v-list-item-title>
            </v-list-item>

            <!-- 💼 OPERAÇÕES -->
            <v-subheader class="text-grey">Investimentos</v-subheader>
            <v-list-item link to="/nova-operacao">
                <v-list-item-title>Nova operação</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/operacoes">
                <v-list-item-title>Operações</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/ativos">
                <v-list-item-title>Ativos</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/corretoras">
                <v-list-item-title>Corretoras</v-list-item-title>
            </v-list-item>
            <v-list-item link to="/categorias">
                <v-list-item-title>Categorias</v-list-item-title>
            </v-list-item>

            <!-- 🔁 IMPORTAÇÃO -->
            <v-subheader class="text-grey">Dados</v-subheader>
            <v-list-item link to="/importar-exportar">
                <v-list-item-title>Importar/Exportar</v-list-item-title>
            </v-list-item>

            <!-- ⚙️ CONFIGURAÇÕES -->
            <v-subheader class="text-grey">Sistema</v-subheader>
            <v-list-item link to="/configuracoes">
                <v-list-item-icon><v-icon>mdi-cog</v-icon></v-list-item-icon>
                <v-list-item-title>Configurações</v-list-item-title>
            </v-list-item>

            <!-- 🔒 SAIR -->
            <v-divider class="my-2" />
            <v-list-item @click="logout" class="text-red">
                <v-list-item>
                    <v-icon start color="red">mdi-logout</v-icon>
                    <v-list-item-title>Cerrar sesión</v-list-item-title>
                </v-list-item>
                <v-list-item-title>Cerrar sesión</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script setup>
    import { computed } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";

    const store = useStore();
    const router = useRouter();

    const drawer = computed(() => store.state.drawer);
    const toggleDrawer = () => store.commit("toggleDrawer");

    const logout = () => {
        store.dispatch("auth/logout");
        router.push("/login");
    };
</script>
