import { hasCookie, removeCookie } from '@/utils/cookies';
// import { useUserStore } from '@/store';

const COOKIE_KEY = 'token';

const hasLoginCookie = () => {
  // const userStore = useUserStore();
  return !!hasCookie(COOKIE_KEY);
};

const clearCookie = () => {
  removeCookie(COOKIE_KEY);
};

export { clearCookie, hasLoginCookie };
