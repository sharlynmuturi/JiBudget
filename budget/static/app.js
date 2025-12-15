// Only try to import SplashScreen if running inside Capacitor
(async () => {
  if (window.Capacitor) {
    try {
      const { SplashScreen } = await import('@capacitor/splash-screen');

      window.addEventListener('load', () => {
        SplashScreen.hide();
      });
    } catch (e) {
      console.warn("SplashScreen plugin not available:", e);
    }
  }
})();
