Toast UI Image Editor vendored assets
====================================

Place the following files in this directory to use local assets instead of the CDN:

Required files (matching latest release or desired version):
- tui-image-editor.css
- tui-image-editor.js
- tui-color-picker.js
- tui-code-snippet.js

You can obtain them via:
- npm (recommended):
  npm install @toast-ui/image-editor tui-color-picker @toast-ui/editor --save
  Then copy the built browser files from node_modules into this folder.

- CDN download:
  https://uicdn.toast.com/tui-image-editor/latest/tui-image-editor.css
  https://uicdn.toast.com/tui-image-editor/latest/tui-image-editor.js
  https://uicdn.toast.com/tui-color-picker/latest/tui-color-picker.js
  https://uicdn.toast.com/tui.code-snippet/latest/tui-code-snippet.js

After copying, the admin editor will prefer these local files and only fall back to CDN if they are missing.

