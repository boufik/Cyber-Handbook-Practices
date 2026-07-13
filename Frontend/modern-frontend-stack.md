# Modern Frontend Stack

**Purpose:** From plain `HTML/CSS/JS` stack to `Vite` + `React` + `TypeScript` + `Tailwind CSS` + `shadcn/ui`

**Audience:** Developers who are comfortable with the plain `HTML/CSS/JS` stack and want to understand what the modern toolchain includes.

**Running example:** A project called `my-security-tool`, whose web frontend lives under the folder `my-security-tool/ui/`.

---

## Table of contents

0. [The one idea that unlocks all of this](#0-the-one-idea-that-unlocks-all-of-this)
1. [Node.js: JavaScript outside the browser](#1-nodejs--javascript-outside-the-browser)
2. [nvm: Managing Node versions](#2-nvm--managing-node-versions)
3. [npm: Packages and scripts](#3-npm--packages-and-scripts)
4. [Vite: The dev server and bundler](#4-vite--the-dev-server-and-bundler)
5. [TypeScript: JavaScript with a type checker](#5-typescript--javascript-with-a-type-checker)
6. [React: `state` → `view`](#6-react--state--view)
7. [Tailwind CSS: Utility classes instead of stylesheets](#7-tailwind-css--utility-classes-instead-of-stylesheets)
8. [shadcn/ui: Components you copy, not install](#8-shadcnui--components-you-copy-not-install)
9. [How it all fits together](#9-how-it-all-fits-together)
10. [The honest downsides](#10-the-honest-downsides)
11. [Quickstart: The whole thing from zero](#11-quickstart-the-whole-thing-from-zero)

---

## 0. The one idea that unlocks all of this

The browser still only understands **HTML, CSS, and JavaScript**. Nothing in this document replaces that stack.

Every tool here is a **build-time transformation**. Each one eventually emits plain HTML/CSS/JS, and *that* is what ships to the browser.

```
(1) Source code           (2) Build step (runs on Node)          (3) What browser gets
────────────────    ──►   ─────────────────────────────    ──►   ──────────────────────
.tsx  .ts  .css            Vite + TS + Tailwind CSS               index.html
                                                                  assets/index-a3f9.js
                                                                  assets/index-b7c2.css
```

When you run the production build (`npm run build`), the output in `my-security-tool/ui/dist/` is something you could open with a plain `file://` URL. It is just unreadable by humans. **The tools exist so that *you* write nice code and the *machine* writes the "ugly" optimized code.** Keep this diagram in your head for the rest of the document.

---

## 1. Node.js: JavaScript outside the browser

JavaScript was originally locked inside the browser. `Node.js` is a standalone runtime, using Google's V8 engine plus a standard library, that lets JS run as a normal OS process, with filesystem access, sockets, child processes and so on. **Think of it as `python3`, but for JavaScript.**

> *Why you need it even though your app is browser-only?*

None of the tools below run in a browser. **Vite + TypeScript compiler +  Tailwind compiler are all Node programs** that read files from disk and write new files to disk. **Node is the engine that runs your *tooling*.**

###  Example 0: Inline expression

An example JS script you can run locally:

```bash
node -v                          # v22.14.0
node script.js                   # Run a file
node -e "console.log(1 + 1)"     # Inline expression
```

### Example 1: A plain build/utility script

Create the script `my-security-tool/ui/scripts/count-files.mjs`:

```js
import fs from 'node:fs';
const files = fs.readdirSync('./src');
console.log(`${files.length} files in src/`);
```

Run the script:
```bash
node scripts/count-files.mjs
```

Nothing browser-related here at all. *This is Node acting exactly like a Python script.*

### Example 2: A backend server

This is where Node competes with FastAPI, Flask or Express. Create the script `my-security-tool/ui/scripts/tiny-server.mjs`:

```js
import http from 'node:http';
http.createServer((req, res) => res.end('hello')).listen(3000);
```

You will probably *not* use Node for your backend if you already have one. But it's useful to know this is what Node fundamentally is.

### Example 3: Running the tools

When you type:

```bash
npx vite
```

you are literally executing a JavaScript program under Node. *That program starts an HTTP dev server and compiles your source files on request*. Same for `tsc`, same for the Tailwind compiler.

> **Takeaway:** Node is the prerequisite for everything else. Install it first!

---

## 2. nvm: Managing Node versions

**What it is:** Node has fast-moving releases and different projects pin different versions. `nvm` (Node Version Manager) lets you install multiple Node versions side by side and switch between them per shell or per directory. **It is the equivalent of `pyenv`.**

**Platform note:**
- On **Linux/macOS**: use the original Bash script `nvm`.
- On **Windows**: the original `nvm` does NOT work. Use **nvm-windows**, a separate project with the same idea but slightly different flags. Many developers instead do their Node work inside WSL or a Linux VM, which sidesteps the difference entirely.

### Example 1: Install and select a version

```bash
nvm install 22        # Download Node 22.x
nvm use 22            # Activate it in this shell
node -v               # Prints v22.14.0
```

### Example 2: Pin the version per project

Create the file `my-security-tool/ui/.nvmrc` containing a single line:

```
22
```

Then, from that directory:

```bash
nvm use               # Reads .nvmrc automatically
```

Commit `.nvmrc` to git. Now every teammate and every CI runner gets the same Node version. This kills an entire class of "works on my machine, breaks in the container" bugs.

### Example 3: Set a global default

```bash
nvm alias default 22        # New shells start on Node 22
```

> **Takeaway:** nvm installs and switches Node. Do this once, then mostly forget about it.

---

## 3. npm: Packages and scripts

`npm` ships bundled with Node. Installing Node gives you `npm` automatically. It has two jobs.

### Job 1: Dependency management

This is like `pip` + `requirements.txt`, but with different names.

| Python | JavaScript |
|---|---|
| PyPI | The registry `npmjs.com` |
| `pip install` | `npm install` |
| `requirements.txt` / `pyproject.toml` | `package.json` |
| Pinned lockfile | `package-lock.json` |
| `venv/` | `node_modules/` |

**The important difference:** `node_modules/` is **local to the project by default.** There is no `venv` to activate. Dependencies live in a folder next to your code. This is why it is famously enormous: thousands of tiny transitive packages. **It is always gitignored!**

### Job 2: Script runner

`package.json` also holds named shell commands. This is where 90% of daily interaction happens.

Example `my-security-tool/ui/package.json`:

```json
{
  "name": "my-security-tool-ui",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "lint": "oxlint"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "tailwindcss": "^4.3.2",
    "tw-animate-css": "^1.4.0",
    "shadcn": "^4.13.0"
  },
  "devDependencies": {
    "vite": "^8.0.0",
    "typescript": "~5.7.0",
    "oxlint": "^1.71.0",
    "@vitejs/plugin-react": "^4.3.0"
  }
}
```

Three things to notice:

- **`dependencies`**: Shipped to the browser (React).
- **`devDependencies`**: Only needed on your machine to *produce* the build (Vite + TS compiler). Never reaches the user.
- **`^19.0.0`**: A semver range meaning `"Use any 19.x version. Don't jump to 20"`. The lockfile `my-security-tool/ui/package-lock.json` pins the *exact* resolved version of every package so a teammate gets a byte-identical dependency tree. It is much more lengthy than `package.json`.

### Example 1: Installing from a fresh clone

```bash
cd my-security-tool/ui

npm ci          # Clean install STRICTLY from package-lock.json  → Must use in CI and Docker
npm install     # Install and may update the lockfile            → Use locally
```

`npm ci` deletes `node_modules/` and rebuilds it exactly as the lockfile describes. It is reproducible and faster. **Always use `npm ci` in a Dockerfile or pipeline.**

### Example 2: Adding a package

```bash
npm install axios          # Goes into "dependencies"
npm install -D vitest      # Goes into "devDependencies"
```

### Example 3: Running scripts and `npx`

```bash
npm run dev                     # Starts the Vite dev server
npm run build                   # Type-check, then produce dist/
npx shadcn@latest add button    # Run a CLI without installing it globally
```

**`npx` is the one to remember.** It is like `pipx run`: it downloads a package's binary temporarily, runs it and discards it. You will use it for scaffolding and for `shadcn/ui`.

**Takeaway:**
* `package.json` is the manifest
* `package-lock.json` is the truth
* `node_modules/` is the artifact
* `npm run <script>` is your daily driver.

---

## 4. Vite: The dev server and bundler

This is the tool that most directly replaces what you were doing by hand.

**What you did before:**

```html
<!-- Order matters, globals everywhere -->
<script src="utils.js"></script>
<script src="app.js"></script>
```

Vite does two *very different* things depending on the mode.

### Dev mode: `npm run dev`

Starts a local HTTP server with **Hot Module Replacement (HMR)**. You save a file and only the changed module is swapped into the already-running page, **without a full reload**. Your form input, your open dropdown, your scroll position all survive. It achieves this by leaning on **native ES modules** in the browser: it only transforms the one file you touched, so startup and reload stay fast regardless of how large the project grows.

### Build mode: `npm run build`

Bundles everything with Rollup: resolves imports, tree-shakes dead code, minifies, hashes filenames for cache-busting, splits chunks. Output lands unde the folder `my-security-tool/ui/dist/`.

### The entry point

Although minimal, `my-security-tool/ui/index.html` is a **real and first-class entry point**, NOT an afterthought. Vite reads it and follows the module script tag:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>My Security Tool</title>
    <link rel="icon" type="image/png" href="./favicon.png" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### Example 1: Scaffolding the project

```bash
npm create vite@latest ui -- --template react-ts
cd ui
npm install
npm run dev             # http://localhost:5173
```

That single command generates the whole `my-security-tool/ui/` skeleton.

### Example 2: Proxying your backend API (avoids CORS in dev)

Supposing that we have a FastAPI server (Swagger UI) running locally on port 8000, reate `my-security-tool/ui/vite.config.ts`:

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',   // The API backend
        changeOrigin: true,
      },
    },
  },
});
```

Now `fetch('/api/scans')` from your frontend code transparently hits your backend on port 8000. The browser thinks it is a same-origin request, so no CORS headers are needed during development.

### Example 3: Environment variables

Create `my-security-tool/ui/.env`:

```
VITE_API_BASE=https://api.example.com
```

Create `my-security-tool/ui/src/lib/config.ts`:

```ts
export const API_BASE = import.meta.env.VITE_API_BASE;
```

Only variables prefixed with `VITE_` are exposed to client code. A deliberate guard so you don't accidentally bake a secret into the bundle.

> ⚠️ Even so, anything you *do* prefix with `VITE_` ends up **publicly readable** in the shipped JavaScript. Never put a real secret there.

> **Takeaway:** Vite is the dev server *and* the production bundler. It is the orchestrator that all the other tools plug into.

---

## 5. TypeScript: JavaScript with a type checker

**What it is:** TypeScript is JavaScript plus type annotations. The TS compiler checks your types and then **erases them completely**. The emitted JavaScript contains zero type information.

**Types exist only at build time. There is no runtime enforcement whatsoever.** A malformed API response will happily flow through a typed variable and blow up somewhere far away. Remember this. It matters in section 5's third example.

**File extensions:**
- `.ts`: Regular TypeScript
- `.tsx`: TypeScript containing JSX (React markup)

**A subtlety worth knowing:** In a Vite project, Vite strips types using `esbuild` for raw speed and **does not type-check** during `npm run dev`. That is exactly why the build script is:

```json
"build": "tsc -b && vite build"
```

The `tsc -b` step is the real gatekeeper. Your editor also runs the checker live, so you see errors as you type.

### Example 1: Catching a typo before it reaches runtime

Create `my-security-tool/ui/src/types/scan.ts`:

```ts
export type ScanStatus = 'pending' | 'running' | 'done' | 'failed';

export type Scan = {
  id: string;
  target: string;
  status: ScanStatus;
  anomalies: number;
};
```

Create `my-security-tool/ui/src/lib/summarize.ts`:

```ts
import type { Scan } from '@/types/scan';

export function summarize(scan: Scan): string {
  return `${scan.target}: ${scan.anomalies} anomalies found...s`;
}

summarize({ id: '1', target: '10.0.0.1', status: 'runing', anomalies: 3 });
//                                               ^^^^^^^^
// Error: Type '"runing"' is not assignable to type 'ScanStatus'.
```

That `status` union means the compiler knows the **only four legal values**. Rename a status in your API and every consuming line in the codebase lights up red immediately.

### Example 2: Typing an API boundary

`my-security-tool/ui/src/api/scans.ts`:

```ts
import type { Scan } from '@/types/scan';

export async function getScans(): Promise<Scan[]> {
  const res = await fetch('/api/scans');
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json() as Promise<Scan[]>;
}
```

Note the `as`. That is a **type assertion**. You are telling the compiler `"Trust me"`. It performs NO validation.

### The real payoff

Beyond error-catching: once `Scan` is typed, typing `scan.` in your editor lists every field with its type.
**On a large codebase this autocomplete-as-documentation is arguably worth more than the error messages.**

> **Takeaway:** TS is a build-time safety net that vanishes at runtime. You can pair it with `zod` at the boundaries where untrusted data enters.

---

## 6. React: `state` → `view`

This is the biggest conceptual jump. Start with the pain it solves.

### The problem with plain JS

You hold the truth **in the DOM** and mutate it imperatively:

```js
const list = document.getElementById('scans');

function addScan(scan) {
  const li = document.createElement('li');
  li.id = `scan-${scan.id}`;
  li.textContent = scan.target;
  li.className = scan.status === 'failed' ? 'error' : '';
  list.appendChild(li);
}

function removeScan(id) {
  document.getElementById(`scan-${id}`)?.remove();
}

function updateStatus(id, status) {
  const li = document.getElementById(`scan-${id}`);
  li.className = status === 'failed' ? 'error' : '';
  // ...and whatever else needs touching
}
```

Every state change needs a hand-written DOM instruction. With 3 pieces of state this is fine. With 30 interacting pieces, you get bugs where the DOM and your variables quietly disagree.

### The React model

You hold the truth **in JS variables** and write **one function that describes what the UI should look like for any given state**. React runs that function, diffs the result against the current DOM and applies the minimal patch. **You never touch the DOM.** You change state → React re-runs your function and reconciles the difference.

```
UI = f(state)
```

### JSX

`.tsx` files let you write HTML-looking syntax inside JavaScript. It is **not HTML**. In reality, it is syntax sugar that Vite compiles into function calls. Consequences:

- `class` → `className`
- `onclick` → `onClick`
- `{ }` drops you back into JavaScript

### Example 1: A component with state
Create `my-security-tool/ui/src/components/Counter.tsx`:

```tsx
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);   // state value + its setter

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

Calling `setCount` → Tells React `"This state changed"` → React re-runs `Counter()` → Gets fresh JSX → Diffs it → Updates only that one text node.

**You wrote zero DOM code.**

### Example 2: Rendering a list from data

This is the case that is genuinely painful in vanilla JS.

Create `my-security-tool/ui/src/features/scans/ScanTable.tsx`:

```tsx
import type { Scan } from '@/types/scan';

type Props = {
  scans: Scan[];
};

export function ScanTable({ scans }: Props) {
  return (
    <table>
      <tbody>
        {scans.map((scan) => (
          <tr key={scan.id}>
            <td>{scan.target}</td>
            <td className={scan.status === 'failed' ? 'text-red-500' : ''}>
              {scan.status}
            </td>
            <td>{scan.anomalies}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

`scans` is a **prop**, an argument passed in from the parent component, exactly like a function parameter. When the parent passes a different array, the table re-renders. Add a scan, remove one, reorder them. **You never write insert/delete/move logic.** The `key` prop lets React track each row's identity across renders so it patches rather than rebuilds.

### Example 3: Fetching from your backend and rendering

Create `my-security-tool/ui/src/features/scans/ScanDashboard.tsx`:

```tsx
import { useState, useEffect } from 'react';
import { getScans } from '@/api/scans';
import type { Scan } from '@/types/scan';
import { ScanTable } from './ScanTable';

export function ScanDashboard() {
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getScans()
      .then(setScans)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);       // [] = Run once, on mount

  if (loading) return <p>Loading…</p>;
  if (error) return <p>Error: {error}</p>;
  return <ScanTable scans={scans} />;
}
```

Notice the **three-branch return**. The same function describes the loading state, the error state, and the success state. **That is the whole appeal: every possible UI is visible in one place, instead of scattered across a dozen event handlers.**

### Composition

Components nest the way functions call functions. Create `my-security-tool/ui/src/App.tsx`:

```tsx
import { Layout } from '@/components/Layout';
import { Sidebar } from '@/components/Sidebar';
import { ScanDashboard } from '@/features/scans/ScanDashboard';

export default function App() {
  return (
    <Layout>
      <Sidebar />
      <ScanDashboard />
    </Layout>
  );
}
```

**This is the "reusable component" idea everyone talks about, and it is the real replacement for copy-pasting `<div class="card">…</div>` blocks around your HTML files.**

> **Takeaway:** You describe *what the UI should be* for a given state. React figures out *how to get there* from the current DOM.

---

## 7. Tailwind CSS — utility classes instead of stylesheets

### The traditional approach

You invent a class name in HTML, go to another file (CSS) and write CSS rules.

```html
<div class="scan-card">…</div>
```

```css
.scan-card {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}
```

Three problems appear at scale:
1. Naming things is hard and names drift from meaning.
2. The stylesheet only ever grows. Nobody dares to delete a rule in case something still uses it.
3. You cannot tell what a class does without jumping to another file.

### The Tailwind approach

Tiny single-purpose classes, composed inline.

```html
<div class="flex gap-4 p-4 rounded-lg border border-gray-200">…</div>
```

The build step **scans your source files for class names and generates only the CSS you actually used.** Unused utilities never reach the bundle, so the CSS file stays small and stops growing with the project.

It looks ugly at first. The reason it wins in a React codebase: **you are already composing components**, so the repetition gets absorbed into the component. And when you delete a component, its styles vanish with it — no orphaned CSS.

### Setup

Create `my-security-tool/ui/vite.config.ts`:

```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

Edit `my-security-tool/ui/src/index.css`:

```css
@import "tailwindcss";
```

### Example 1: A status badge

Create `my-security-tool/ui/src/components/SeverityBadge.tsx`:

```tsx
export function SeverityBadge() {
  return (
    <span className="inline-flex items-center rounded-full bg-red-100 px-2 py-1 text-xs font-medium text-red-700">
      Critical
    </span>
  );
}
```

Read it left to right: inline-flex, vertically centered, pill-shaped, light red background, small padding, tiny bold red text. No context switch, no name to invent.

### Example 2: Responsive and state variants

The prefixes are where the real power is.

`my-security-tool/ui/src/features/scans/RunScanButton.tsx`:

```tsx
export function RunScanButton({ disabled }: { disabled: boolean }) {
  return (
    <button
      disabled={disabled}
      className="w-full md:w-auto bg-blue-600 hover:bg-blue-700 disabled:opacity-50 focus:ring-2"
    >
      Run scan
    </button>
  );
}
```

- `md:w-auto` → at viewport ≥768px, width becomes auto.
- `hover:` / `disabled:` / `focus:` → generate the corresponding pseudo-selectors.

In plain CSS this is a media query block plus three separate selectors, in a different file.

### Example 3: Conditional classes driven by state

Combine Tailwind with the `cn` helper (`clsx` + `tailwind-merge`) that shadcn/ui gives you.

Create `my-security-tool/ui/src/lib/utils.ts`:

```ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Create `my-security-tool/ui/src/features/scans/StatusCell.tsx`:

```tsx
import { cn } from '@/lib/utils';
import type { Scan } from '@/types/scan';

export function StatusCell({ scan }: { scan: Scan }) {
  return (
    <td
      className={cn(
        'px-3 py-2',
        scan.status === 'failed' && 'text-red-600 font-semibold',
        scan.status === 'done' && 'text-green-600',
      )}
    >
      {scan.status}
    </td>
  );
}
```

**This is `UI = f(state)` applied to styling.** `cn` also resolves conflicts intelligently: if two utilities fight (say `p-2` and `p-4`), `tailwind-merge` keeps the later one instead of letting both land in the class list and leaving the winner to CSS-specificity roulette.

> **Takeaway:** Tailwind turns class names in your source into a generated CSS file. Styles live next to the markup they style, and dead styles delete themselves.

---

## 8. `shadcn`/`ui`

Use `shadcn`/`ui` for **components you copy, NOT install**.
This one confuses people because it **inverts the normal model.**

### The normal model

A traditional component library (Material UI, Bootstrap, Chakra) is an `npm` dependency:

```bash
npm install some-ui-library
```

```tsx
import { Button } from 'some-ui-library';
```

The code lives in `node_modules/` — a black box you can only influence through whatever props and theme API the authors chose to expose. Want a different border radius on exactly one variant? You fight the theming system.

### The shadcn/ui model

**shadcn/ui is not a dependency. It is a CLI that copies source files into your repository.**

```bash
npx shadcn@latest init
npx shadcn@latest add button dialog table
```

After running that, you have real files like:

```
my-security-tool/ui/src/components/ui/button.tsx
my-security-tool/ui/src/components/ui/dialog.tsx
my-security-tool/ui/src/components/ui/table.tsx
my-security-tool/ui/src/lib/utils.ts          ← the cn() helper
my-security-tool/ui/components.json           ← config: where to copy files
```

These are **your files**. Committed to `git`. Editable in a text editor. They are built on **Radix UI** primitives (unstyled, accessible behavior, focus traps, keyboard navigation, ARIA wiring) with Tailwind classes layered on top.

**The tradeoff:** you own the code, so you also own the maintenance. There is no `npm update` that silently improves your `button.tsx`. That is the deal. Total control in exchange for no free upgrades.

### Example 1: Using a component

Create `my-security-tool/ui/src/features/scans/DeleteScanButton.tsx`:

```tsx
import { Button } from '@/components/ui/button';

export function DeleteScanButton({ onDelete }: { onDelete: () => void }) {
  return (
    <Button variant="destructive" size="sm" onClick={onDelete}>
      Delete scan
    </Button>
  );
}
```

`variant` and `size` come from a `cva` (class-variance-authority) configuration **inside the file you own**. Open `my-security-tool/ui/src/components/ui/button.tsx` and you will see the literal Tailwind class strings for every variant.

### Example 2: Modifying a component (the entire point)

Add your own branded variant by editing your own file.

Create `my-security-tool/ui/src/components/ui/button.tsx`:

```tsx
const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-white hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent',
        // ↓ your own addition — just another line in a file you own
        brand: 'bg-cyan-600 text-white hover:bg-cyan-500 shadow-lg shadow-cyan-500/20',
      },
      size: {
        default: 'h-9 px-4 py-2',
        sm: 'h-8 px-3',
        lg: 'h-10 px-8',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  },
);
```

Create `my-security-tool/ui/src/features/scans/StartReconButton.tsx`:

```tsx
import { Button } from '@/components/ui/button';

export function StartReconButton() {
  return <Button variant="brand">Start recon</Button>;
}
```

Try doing that with a black-box library.

### Example 3: A composed component with accessibility handled for you

Create `my-security-tool/ui/src/features/cves/CveDetailsDialog.tsx`:

```tsx
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

export function CveDetailsDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">CVE details</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>CVE-2025-14847</DialogTitle>
        </DialogHeader>
        <p>CVSS 9.8 · Actively exploited · Affects the database layer</p>
      </DialogContent>
    </Dialog>
  );
}
```

What Radix gives you for free underneath: focus is trapped inside the modal, `Escape` closes it, focus returns to the trigger button on close, background content is inert, and screen readers announce it correctly.

**You wrote none of that.** Writing it correctly by hand is a genuinely hard, easy-to-get-subtly-wrong job.

> **Takeaway:** `shadcn/ui` is a starting point, not a dependency. The moment the files land in your repo, they are ordinary React + Tailwind code that you maintain.

---

## 9. How it all fits together

### Directory layout

```
my-security-tool/
└── ui/
    ├── .nvmrc                          # "22"                       ← nvm
    ├── package.json                    # deps + scripts             ← npm
    ├── package-lock.json               # exact pinned tree          ← npm
    ├── node_modules/                   # gitignored artifact        ← npm
    ├── vite.config.ts                  # dev server, proxy, plugins ← Vite
    ├── tsconfig.json                   # type-checker config        ← TypeScript
    ├── components.json                 # where shadcn copies files  ← shadcn/ui
    ├── .env                            # VITE_* variables           ← Vite
    ├── index.html                      # the single real HTML page  ← Vite entry
    ├── src/
    │   ├── main.tsx                    # mounts React into #root
    │   ├── App.tsx                     # root component
    │   ├── index.css                   # @import "tailwindcss"      ← Tailwind
    │   ├── lib/
    │   │   └── utils.ts                # the cn() helper            ← shadcn/ui
    │   ├── types/
    │   │   └── scan.ts                 # shared TS types
    │   ├── api/
    │   │   └── scans.ts                # fetch wrappers
    │   ├── components/
    │   │   └── ui/                     # button.tsx, dialog.tsx — YOU OWN THESE ← shadcn/ui
    │   └── features/
    │       └── scans/                  # your actual app components ← React
    │           ├── ScanDashboard.tsx
    │           └── ScanTable.tsx
    └── dist/                           # build output with plain HTML/CSS/JS
```

### The wiring, top to bottom

`my-security-tool/ui/index.html`:

```html
<div id="root"></div>
<script type="module" src="/src/main.tsx"></script>
```

`my-security-tool/ui/src/main.tsx`:

```tsx
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';

createRoot(document.getElementById('root')!).render(
  ...
      <App />
  ...
);
```

That is the whole bridge. **One `<div>` and React fills it.** Every other element on the page is generated by JavaScript at runtime.

### The responsibility chain

| Tool | Responsibility |
|---|---|
| **nvm** | Picks *which* Node runs. |
| **Node.js** | Runs everything else. |
| **npm** | Fetches the packages, runs the scripts. |
| **Vite** | Serves in dev, bundles for prod, orchestrates the plugins. |
| **TypeScript** | Checks your types, then evaporates. |
| **React** | Turns state into DOM. |
| **Tailwind** | Turns class names into a CSS file. |
| **shadcn/ui** | Gave you pre-written React + Tailwind files that are now just *your* code. |

---

## 10. The honest downsides

- **`node_modules/` is a supply-chain surface.** Hundreds of transitive packages from strangers, some with `postinstall` scripts that execute arbitrary code at install time. `npm audit` is noisy but not optional. Use `npm ci` (never bare `npm install`) in CI and Docker so the lockfile is authoritative.

- **Client-side rendering means an effectively empty `index.html`.** `curl` the deployed site and you get a blank `<div id="root">`. This is bad for SEO, and it is worth remembering when your own recon tooling crawls single-page applications — the interesting content is in the JS bundle, not the HTML.

- **The bundle is public.** Everything in your shipped JavaScript — API base URLs, `VITE_*` variables, internal endpoint names, comments you forgot to strip — is readable by anyone with DevTools. **Minification is not obfuscation.**

- **There is a real learning cliff.** You have traded "open a file and edit it" for a build pipeline with half a dozen configuration files. When it breaks, you now need to know *which* tool broke.

---

## 11. Quickstart: The whole thing from zero

```bash
# 1. Node via nvm
nvm install 22
nvm use 22
node -v

# 2. Scaffold with Vite (React + TypeScript template)
mkdir my-security-tool && cd my-security-tool
npm create vite@latest ui -- --template react-ts
cd ui

# 3. Install dependencies (creates node_modules/ and package-lock.json)
npm install

# 4. Add Tailwind
npm install tailwindcss @tailwindcss/vite
#    → then add the tailwindcss() plugin to vite.config.ts
#    → and put `@import "tailwindcss";` at the top of src/index.css

# 5. Add shadcn/ui (copies component source into src/components/ui/)
npx shadcn@latest init
npx shadcn@latest add button

# 6. Pin the Node version for your team
echo "22" > .nvmrc

# 7. Develop
npm run dev        # → http://localhost:5173, with hot reload

# 8. Build for production
npm run build      # → type-checks, then writes dist/
npm run preview    # → serve dist/ locally to sanity-check it
```

### The single most useful exercise

After step 8, open `my-security-tool/ui/dist/` and read the generated `index.html` and the files in `dist/assets/`.

You will find plain HTML, plain CSS and plain JavaScript, the stack you already know. **Seeing that with your own eyes is the fastest way to make everything above click into place.**
