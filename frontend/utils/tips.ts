import { type ConfigProviderProps, createDiscreteApi, darkTheme, lightTheme } from 'naive-ui';
import { computed } from 'vue';
import { useChatStore } from '~/stores/chat';
const store = useChatStore();

const configProviderPropsRef = computed<ConfigProviderProps>(() => ({
    theme: store.getColorMode() === 'light' ? lightTheme : darkTheme,
}));

const { message, notification, dialog, loadingBar } = createDiscreteApi(
    ['message', 'dialog', 'notification', 'loadingBar'],
    {
        configProviderProps: configProviderPropsRef,
    }
);

export { dialog as Dialog, loadingBar as LoadingBar, message as Message, notification as Notification};