import { createRouter, createWebHistory } from "vue-router";
import store from "../store";

const routes = [
    {
        path: "/",
        name: "Home",
        component: () => import("../pages/Dashboard.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/login",
        name: "Login",
        component: () => import("../pages/Login.vue"),
    },
    {
        path: "/register",
        name: "Register",
        component: () => import("../pages/Register.vue"),
    },
    {
        path: "/nova-operacao",
        name: "NovaOperacao",
        component: () => import("../pages/NovaOperacao.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/operacoes",
        name: "Operacoes",
        component: () => import("../pages/Operacoes.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/operacoes/:id/editar",
        name: "EditarOperacao",
        component: () => import("../pages/EditarOperacao.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/dashboard",
        name: "Dashboard",
        component: () => import("../pages/Dashboard.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/ativos",
        name: "Ativos",
        component: () => import("../pages/Ativos.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/corretoras",
        name: "Corretoras",
        component: () => import("../pages/Corretoras.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/categorias",
        name: "Categorias",
        component: () => import("../pages/Categorias.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/dashboard-fire",
        name: "DashboardFIRE",
        component: () => import("../pages/DashboardFIRE.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/importar-exportar",
        name: "ImportarExportar",
        component: () => import("../pages/ImportarExportar.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/configuracoes",
        name: "Configuracoes",
        component: () => import("../pages/UserSettings.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/calculadora-fire",
        name: "CalculadoraFIRE",
        component: () => import("../pages/CalculadoraFIRE.vue"),
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
  const isAuth = store.getters['auth/isAuthenticated']

  if (to.meta.requiresAuth) {
    if (!isAuth) {
      return next('/login')
    }

    // Garante que o usuário está carregado
    if (!store.getters['auth/getUser']) {
      try {
        await store.dispatch('auth/fetchUser')
      } catch {
        return next('/login')
      }
    }
  }

  next()
})

export default router;
