import express from "express";
import { createServer } from "vite";
import fs from 'fs/promises'

// Create Server
const base = '/';
const app = express();

// Vite middleware
let vite = await createServer({
  server: { middlewareMode: true },
  appType: 'custom',
  base: base,
})

app.use(vite.middlewares)

app.listen(3000, () => {
    console.log("Server is running on port 3000");
});

// Serve HTML
app.use('*all', async (req, res) => {
  try {
    const url = req.originalUrl.replace(base, '')

    let template = await fs.readFile('./index.html', 'utf-8')
    template = await vite.transformIndexHtml(url, template)

    let render = (await vite.ssrLoadModule('/src/entry-server.tsx')).render
    const rendered = await render(url)

    const html = template
      .replace(`<!--app-head-->`, rendered.head ?? '')
      .replace(`<!--app-html-->`, rendered.html ?? '')

    res.status(200).set({ 'Content-Type': 'text/html' }).send(html)
  } catch (e) {
    vite?.ssrFixStacktrace(e)
    console.log(e.stack)
    res.status(500).end(e.stack)
  }
})

// Start http server
app.listen(3000, () => {
  console.log(`Server started at http://localhost:3000`)
})