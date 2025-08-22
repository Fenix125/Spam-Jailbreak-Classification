import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import * as dotenv from "dotenv";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.resolve(__dirname, "../../.env") });

export default defineConfig({
    plugins: [react()],
    envDir: path.resolve(__dirname, "../../"),
    envPrefix: ["APP"],
    server: {
        host: process.env.APP_FRONTEND_HOST,
        port: Number(process.env.APP_FRONTEND_PORT),
    },
});
