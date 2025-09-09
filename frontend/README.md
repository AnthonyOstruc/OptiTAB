# OptiTAB Frontend

This is the frontend application for OptiTAB, built with Vue.js and Vite.

## Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment

### Option 1: Render (Recommended)

1. **Build Command**: `npm run build`
2. **Publish Directory**: `dist`

The `npm run build` script now uses `npx vite build` which resolves permission issues in deployment environments.

### Option 2: Using Docker

```bash
# Build Docker image
docker build -t optitab-frontend .

# Run container
docker run -p 80:80 optitab-frontend
```

### Option 3: Manual Build Script

```bash
# Use the provided render-build.sh script
./render-build.sh
```

## Build Issues Resolution

If you encounter "vite: Permission denied" errors:

1. **For Render**: Make sure your build command is `npm run build` (not `vite build`)
2. **For local development**: The build script now uses `npx` to avoid permission issues
3. **For Docker**: Use the provided Dockerfile which handles permissions correctly

## Environment Variables

Create a `.env` file for local development:

```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── api/          # API service functions
├── components/   # Vue components
├── composables/  # Vue composables
├── stores/       # Pinia stores
├── views/        # Page components
├── router/       # Vue router configuration
└── styles/       # Global styles
```
