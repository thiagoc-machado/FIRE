<template>
    <v-app>
        <!-- Menu lateral -->
        <Sidebar @close-drawer="fecharDrawer" />

        <!-- Barra superior -->
        <v-app-bar app elevation="3" class="gradient-background" dark>
            <v-app-bar-nav-icon @click="toggleDrawer" />

            <v-toolbar-title class="font-weight-bold" @click="router.push('/')">
                🔥 F.I.R.E.
            </v-toolbar-title>

            <v-spacer />

            <!-- Nome do usuário -->
            <div class="d-flex align-center">
                <span v-if="user.username" class="me-2 text-caption text-white">
                    {{ user.username }}
                </span>
                <v-btn icon @click="router.push('/nova-operacao')">
                    <v-icon>mdi-plus</v-icon>
                </v-btn>

                <v-menu offset-y>
                    <template #activator="{ props }">
                        <v-btn v-bind="props" icon>
                            <v-avatar size="32" class="elevation-2">
                                <v-icon>mdi-account-circle</v-icon>
                            </v-avatar>
                        </v-btn>
                    </template>

                    <v-list>
                        <v-list-item
                            title="Nova operaçao"
                            @click="router.push('/nova-operacao')"
                        />
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
            </div>
        </v-app-bar>

        <!-- Conteúdo principal -->
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
    const fecharDrawer = () => {
        if (window.innerWidth <= 1280) {
            store.commit("setDrawer", false);
        }
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

<style>
    .gradient-bar {
        background: linear-gradient(90deg, #ff5722, #ff9800) !important;
    }
    .bg-main {
        background-color: #f9f9f9;
        min-height: calc(100vh - 64px); /* Compensa a app-bar */
        padding: 16px;
    }
    .me-2 {
        margin-right: 8px;
    }
    .gradient-background {
        position: relative;
        overflow: hidden;
    }

    .gradient-background::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, #ff5722, #ff9800);
        z-index: 0;
    }

    .gradient-background * {
        position: relative;
        z-index: 1;
    }
</style>
