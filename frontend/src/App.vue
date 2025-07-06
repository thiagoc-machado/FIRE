<template>
    <v-app>
        <Sidebar />

        <v-app-bar app color="primary" dark>
            <v-app-bar-nav-icon @click="toggleDrawer" />
            <v-toolbar-title>F.I.R.E.</v-toolbar-title>

            <v-spacer />

            <!-- Nome do usuário -->
            <span v-if="user.username" class="mr-2 text-caption">
                {{ user.username }}
            </span>
            <v-menu offset-y>
                <template #activator="{ props }">
                    <v-btn v-bind="props" icon>
                        <v-avatar size="32">
                            <v-icon>mdi-account-circle</v-icon>
                        </v-avatar>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item
                        title="Configurações"
                        @click="router.push('/configuracoes')"
                    />
                    <v-list-item
                        title="Sair"
                        @click="logout"
                        class="text-red"
                    />
                </v-list>
            </v-menu>
        </v-app-bar>

        <v-main>
            <router-view />
        </v-main>
    </v-app>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import Sidebar from "./components/Sidebar.vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";
    import axios from "./services/api";

    const store = useStore();
    const router = useRouter();

    const toggleDrawer = () => store.commit("toggleDrawer");
    const logout = () => {
        store.dispatch("auth/logout");
        router.push("/login");
    };

    // 🧑 Nome do usuário logado
    const user = ref({ email: "" });

    const fetchUser = async () => {
        try {
            const res = await axios.get("/api/auth/users/me/");
            user.value = res.data;
        } catch (e) {
            console.error("Erro ao buscar usuário logado", e);
        }
    };

    onMounted(fetchUser);
</script>
