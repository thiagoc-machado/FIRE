import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { aliases, mdi } from 'vuetify/iconsets/mdi';

const customTheme = {
  dark: false,
  colors: {
    primary: '#FF5722',      // 🔥 Laranja queimado
    secondary: '#4CAF50',    // ✅ Verde FIRE
    accent: '#FFC107',       // ✨ Amarelo vibrante
    background: '#F9F9F9',   // ⚪ Fundo neutro
    surface: '#FFFFFF',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
    error: '#F44336',
  },
};

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme,
    },
  },
});
