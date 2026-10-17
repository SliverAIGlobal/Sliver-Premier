# Android Trusted Web Activity (TWA) Pathway

To package PRISM 9 as a native Android application using Trusted Web Activity (TWA):

## Step 1: Install Bubblewrap CLI
```bash
npm install -g @bubblewrap/cli
```

## Step 2: Initialize TWA Project
```bash
bubblewrap init --manifest=https://prism9.yourdomain.com/manifest.json
```

## Step 3: Build Android APK / AAB
```bash
bubblewrap build
```

The resulting `.apk` / `.aab` can be published directly to Google Play Store.
