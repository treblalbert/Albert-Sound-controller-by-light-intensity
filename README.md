# Webcam Volume Widget

A minimal Windows widget that controls system volume based on webcam brightness.

## Run in Development

```bash
npm install
npm start
```

## Build Portable EXE

### Step 1: Create your icon

An SVG template is provided in `assets/icon.svg`. Convert it to `.ico`:

**Option A: Online converter (easiest)**
1. Go to https://convertio.co/svg-ico/ or https://cloudconvert.com/svg-to-ico
2. Upload `assets/icon.svg`
3. Download the `.ico` file
4. Save it as `assets/icon.ico`

**Option B: Use your own icon**
1. Create or find a 256x256 PNG image
2. Convert to `.ico` using https://icoconvert.com/
3. Save as `assets/icon.ico`

### Step 2: Build

```bash
npm install
npm run build
```

The portable `WebcamVolumeWidget.exe` will be in the `dist` folder with your custom icon.

## Usage

- Drag the widget anywhere on screen
- Lighter webcam image = Higher volume
- Darker webcam image = Lower volume
- Click ✕ to close
