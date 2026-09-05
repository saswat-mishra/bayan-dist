import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// No CDN, no external font, no runtime fetch except the enclave-local API.
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/v1": { target: process.env.BAYAN_GATE || "http://127.0.0.1:8787", changeOrigin: false } } },
  build: { outDir: "dist", sourcemap: false, assetsInlineLimit: 0 },
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    include: ["tests/**/*.test.tsx", "tests/**/*.test.ts"],
    globals: true,
  },
});
