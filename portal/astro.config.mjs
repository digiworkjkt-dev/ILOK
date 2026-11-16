import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

const siteUrl = process.env.SITE_URL || "https://lombakurasi.id";

export default defineConfig({
  site: siteUrl,
  trailingSlash: "always",
  integrations: [
    sitemap({
      filter: (page) => !page.endsWith("/tersimpan/"),
    }),
  ],
  build: {
    format: "directory",
  },
});
